"""Gate: isolated candidate copies, URSMIF-style invariants, evaluator subprocess.

Invariants the loop cannot edit (URSMIF v1.5 sec. 3.4 "formal verification of
intervention correctness"; Eigenrecursion 4.2.1 "safety invariant preservation"):

I1  only files under ``cognition/mutable/`` named in config.MUTABLE_MODULES may differ
    from the frozen snapshot; every other file (this gate, evaluator, objective,
    runner, loop detector, config, the IALA ethics filter, the engine) must be
    byte-identical (sha256 manifest of the snapshot), and no file may be added/removed.
I2  each mutable module is ASCII, parses, compiles, imports only config.ALLOWED_IMPORTS
    and references none of FORBIDDEN_NAMES or any dunder attribute.
I3  the evaluator runs in a subprocess (timeout config.EVAL_TIMEOUT_S) with the
    candidate root as the only repo on PYTHONPATH, its own cwd and BIOC storage, and
    must report every mutable module as imported from that candidate root.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from runtime.selfmod import config as C

FORBIDDEN_NAMES = {"open", "exec", "eval", "compile", "__import__", "globals", "locals", "getattr",
                   "setattr", "delattr", "vars", "input", "breakpoint", "exit", "quit", "help",
                   "memoryview", "os", "sys", "subprocess", "importlib", "builtins", "pathlib", "shutil"}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def mutable_paths() -> List[str]:
    return [f"{C.ALLOWED_EDIT_PREFIX}{m}.py" for m in C.MUTABLE_MODULES]


def extract_snapshot(repo: Path, commit: str, dest: Path) -> Dict[str, str]:
    """git archive <commit> into dest; returns the sha256 manifest of every file."""
    dest.mkdir(parents=True, exist_ok=False)
    arch = subprocess.run(["git", "-C", str(repo), "archive", "--format=tar", commit],
                          check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=arch, check=True)
    return manifest(dest)


def manifest(root: Path) -> Dict[str, str]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            out[str(p.relative_to(root))] = sha256(p)
    return out


def scan_module(src: str, name: str) -> List[str]:
    """Static invariant I2 for one mutable module. Returns violations (empty = ok)."""
    errs = []
    try:
        src.encode("ascii")
    except UnicodeEncodeError:
        errs.append(f"{name}: non-ASCII source")
    try:
        tree = ast.parse(src)
        compile(src, name, "exec")
    except SyntaxError as e:
        return errs + [f"{name}: syntax error {e}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in C.ALLOWED_IMPORTS:
                    errs.append(f"{name}: import {a.name} not allowed")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in C.ALLOWED_IMPORTS or node.level:
                errs.append(f"{name}: from {node.module} import not allowed")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            errs.append(f"{name}: forbidden name {node.id}")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            errs.append(f"{name}: dunder attribute {node.attr}")
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            errs.append(f"{name}: global/nonlocal statement")
    return errs


def build_candidate(snapshot: Path, current: Dict[str, str], edits: Dict[str, str], base_tmp: Path) -> Path:
    """Copy the snapshot, overlay the incumbent mutable sources, then the edits."""
    cand = Path(tempfile.mkdtemp(prefix="cand_", dir=base_tmp))
    shutil.rmtree(cand)
    shutil.copytree(snapshot, cand, symlinks=False)
    for rel, src in {**current, **edits}.items():
        (cand / rel).write_text(src)
    return cand


def check_invariants(cand: Path, snap_manifest: Dict[str, str]) -> List[str]:
    errs = []
    allowed = set(mutable_paths())
    cm = manifest(cand)
    added = sorted(set(cm) - set(snap_manifest))
    removed = sorted(set(snap_manifest) - set(cm))
    if added:
        errs.append(f"I1 files added: {added[:5]}")
    if removed:
        errs.append(f"I1 files removed: {removed[:5]}")
    changed = [k for k in cm if k in snap_manifest and cm[k] != snap_manifest[k]]
    illegal = [k for k in changed if k not in allowed]
    if illegal:
        errs.append(f"I1 protected files changed: {illegal[:5]}")
    for rel in allowed:
        p = cand / rel
        if not p.exists():
            errs.append(f"I1 mutable module missing: {rel}")
            continue
        errs += [f"I2 {e}" for e in scan_module(p.read_text(), rel)]
    return errs


def run_evaluator(root: Path, out_json: Path, split: str = "select", seeds: Optional[str] = None,
                  keep_records: bool = False, timeout: int = C.EVAL_TIMEOUT_S) -> Dict:
    work = Path(tempfile.mkdtemp(prefix="evalwd_", dir=out_json.parent))
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH",)}
    env.update({"PYTHONPATH": str(root), "BIOC_STORAGE_PATH": str(work / "bioc"),
                "PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    cmd = [sys.executable, "-m", "runtime.selfmod.evaluate", "--split", split, "--out", str(out_json)]
    if seeds:
        cmd += ["--seeds", seeds]
    if keep_records:
        cmd.append("--keep-records")
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=timeout)
        rc = proc.returncode
        tail = (proc.stderr or "")[-1500:]
    except subprocess.TimeoutExpired:
        shutil.rmtree(work, ignore_errors=True)
        return {"error": f"evaluator timeout after {timeout}s", "rc": None, "wall": time.time() - t0}
    shutil.rmtree(work, ignore_errors=True)
    if rc != 0 or not out_json.exists():
        return {"error": f"evaluator exit {rc}", "stderr_tail": tail, "rc": rc, "wall": time.time() - t0}
    res = json.loads(out_json.read_text())
    res["rc"] = rc
    res["wall"] = time.time() - t0
    if not res.get("error"):
        for name, info in res.get("mutable_modules", {}).items():
            if not info["path"].startswith(str(root)):
                res["error"] = f"I3 {name} imported from {info['path']}, outside candidate {root}"
    return res
