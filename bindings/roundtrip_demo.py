"""End-to-end round trip through lqt_native (C++), run from the repo root:

    python bindings/roundtrip_demo.py [out_dir]

create weights in C++ -> save .lqt -> reload -> reconstruct -> mutate (edit log)
-> save -> reload -> reconstruct -> rollback -> hand values to RecursiveTensor compute.
Every expected number is recomputed independently in numpy and asserted.
"""
import os
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import lqt_py as L  # noqa: E402

out_dir = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="lqt_rt_")
os.makedirs(out_dir, exist_ok=True)
p1 = os.path.join(out_dir, "model_v1.lqt")
p2 = os.path.join(out_dir, "model_v2_mutated.lqt")
np.set_printoptions(precision=4, suppress=True)

# ---------------------------------------------------------------- storage: build in C++
cb_vals = np.linspace(-1.0, 1.0, 16, dtype=np.float32)          # 16-entry scalar codebook
cb = L.Codebook.from_numpy(0, cb_vals)
model = L.LqtModel()
model.set_hyperparam("hidden_dim", 8.0)
model.module_graph_json = '{"modules":[{"id":"lattice","type":"RTA"}]}'
model.add_codebook(cb)

# Standard INT4 tensor
std_idx = np.array([0, 3, 7, 15, 8, 1, 12, 5], dtype=np.uint32)
std_desc = L.TensorDescriptor("ffn.weight", [2, 4], dtype=L.DType.INT4, codebook_id=0, scale=0.5)
model.add_tensor_indices(std_desc, std_idx)

# RecursiveTensor-typed tensor: RTA block selects positions on a 2x2x2x1x1 lattice;
# RecursiveWeight buckets own their B / T / Phi / epsilon.
rt_idx = np.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=np.uint32)
rt_desc = L.TensorDescriptor("lattice", [2, 2, 2, 1, 1], dtype=L.DType.INT4,
                             tensor_type=L.TensorType.RecursiveTensor, codebook_id=0, scale=2.0)
model.add_tensor_indices(rt_desc, rt_idx)
dims = L.RtaDimensionBlock([2, 2, 2, 1, 1], L.RtaDistribution.Normal)
model.add_rta_block("lattice", L.RtaBlock(dims, L.SparseEncoding.Uniform, L.sparse_build_uniform(8)))

w_a = L.RecursiveWeight(base_index=15, phase=np.array([0.2, -0.1, 0.05], np.float32),
                        reference=np.full((2, 3, 3), 0.01, np.float32),
                        tensor_position=np.array([0, 1, 0, 0, 0], np.float32),
                        error=np.array([0.01, 0.03], np.float32), self_reference_coeff=0.4)
w_b = L.RecursiveWeight(base_index=0, phase=np.zeros(4, np.float32),
                        tensor_position=np.array([1, 1, 1, 0, 0], np.float32),
                        error=np.array([-0.5], np.float32), self_reference_coeff=0.3)
model.add_recursive_weight("lattice", w_a)
model.add_recursive_weight("lattice", w_b)

print("RecursiveWeight A:", w_a)
print("  phase_at(0.125) =", round(w_a.phase_at(0.125), 6))
print("  effective value (depth 8, t=0) =", round(w_a.compute_effective_value(cb_vals, 2.0), 6))
print("  converge:", w_a.converge(cb_vals, 2.0))
v = L.validate_weight(w_a)
print("  validate_weight: valid=%s score=%.3f passes=%s" % (v["valid"], v["overall_score"], [p["name"] for p in v["passes"]]))
assert L.RecursiveWeight.from_bytes(w_a.to_bytes()).base_index == 15

model.save(p1)
print("saved", p1, os.path.getsize(p1), "bytes")

# ---------------------------------------------------------------- reload + reconstruct
m1 = L.LqtModel.load(p1)
assert m1.tensor_names() == ["ffn.weight", "lattice"], m1.tensor_names()
assert np.array_equal(m1.indices("ffn.weight"), std_idx)
cb_fp16 = m1.codebook(0).values()[:, 0]   # codebooks are stored FP16 on disk
std = m1.reconstruct("ffn.weight")
exp_std = (cb_fp16[std_idx] * 0.5).reshape(2, 4)
print("ffn.weight reconstructed:\n", std)
assert np.allclose(std, exp_std, atol=0), (std, exp_std)

lat = m1.reconstruct("lattice")
exp_lat = (cb_fp16[rt_idx] * 2.0).reshape(2, 2, 2, 1, 1).copy()
exp_lat[0, 1, 0, 0, 0] = cb_fp16[15] * 2.0 + 0.0 + np.mean([0.01, 0.03])   # bucket A (phase_at(0)=0)
exp_lat[1, 1, 1, 0, 0] = cb_fp16[0] * 2.0 + 0.0 + (-0.5)                    # bucket B
print("lattice reconstructed (buckets at [0,1,0] and [1,1,1]):\n", lat)
assert np.allclose(lat, exp_lat, atol=1e-6), (lat, exp_lat)
rw_loaded = m1.recursive_weights("lattice")
assert len(rw_loaded) == 2 and rw_loaded[0].base_index == 15
assert np.allclose(rw_loaded[0].reference, 0.01)

# ---------------------------------------------------------------- mutate with edit log
m1.edit_codebook_scalar(0, 15, 3.0)      # B=15 feeds bucket A and std index 15
m1.edit_codebook_scalar(0, 3, -2.0)
m1.set_hyperparam("hidden_dim", 16.0)
log = m1.edit_log()
print("edit log after mutation:", [(e["type"].name, e["target"], hex(e["data_hash"])) for e in log])
assert len(log) == 2 and m1.verify_edit_log() and m1.undo_depth == 2
m1.save(p2)

m2 = L.LqtModel.load(p2)
assert m2.verify_edit_log(), "edit-log hash chain must survive save/load"
assert len(m2.edit_log()) == 2 and m2.edit_log_tail_hash == m1.edit_log_tail_hash
cb2 = m2.codebook(0).values()[:, 0]
lat2 = m2.reconstruct("lattice")
std2 = m2.reconstruct("ffn.weight")
print("after mutate+reload ffn.weight:\n", std2)
print("after mutate+reload lattice:\n", lat2)
assert cb2[15] == 3.0 and cb2[3] == -2.0
assert np.isclose(lat2[0, 1, 0, 0, 0], 3.0 * 2.0 + 0.02, atol=1e-6)
assert std2[0, 1] == -2.0 * 0.5 and std2[0, 3] == 3.0 * 0.5
print("hyperparams:", m2.hyperparams)

# rollback in-memory (undo stack is per-session, edit log truncates with it)
m1.rollback(2)
assert m1.undo_depth == 0 and len(m1.edit_log()) == 0
assert np.allclose(m1.reconstruct("lattice"), exp_lat, atol=1e-6)
print("rollback(2) restored original lattice values")

# ---------------------------------------------------------------- compute: RecursiveTensor
T = L.RecursiveTensor.from_numpy(lat2.astype(np.float64))
G = T.contract(T, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4])            # full contraction = squared Frobenius norm
fro2 = float(np.sum(lat2.astype(np.float64) ** 2))
print("RecursiveTensor contract(all axes) =", G.to_numpy(), " numpy sum(x^2) =", fro2)
assert np.isclose(G.to_numpy().reshape(-1)[0], fro2)
M = T.contract(T, [2], [2])                          # (2,2,1,1,2,2,1,1)
assert np.allclose(M.to_numpy(), np.tensordot(lat2, lat2, axes=([2], [2])), atol=1e-5)
R = L.RecursiveTensor([4, 4, 3], L.Distribution.Normal, 0.0, seed=7)
print("RecursiveTensor(4,4,3) seed=7: norm=%.6f entropy=%.6f" % (R.norm(), R.compute_entropy()))
rta_path = os.path.join(out_dir, "lattice.rta")
T.save(rta_path)
assert np.array_equal(L.RecursiveTensor.load(rta_path).to_numpy(), T.to_numpy())

a5 = lat2
c5 = L.rta_contract(a5, a5, [1, 2, 3, 4], [1, 2, 3, 4])    # Gram over axis 0 (free 1+1)
ref = np.tensordot(a5, a5, axes=([1, 2, 3, 4], [1, 2, 3, 4]))
print("lqt rta_contract 5-D shape:", c5.shape, "gram:\n", c5.reshape(2, 2))
assert np.allclose(c5.reshape(2, 2), ref, atol=1e-5)
print("ROUNDTRIP OK")
