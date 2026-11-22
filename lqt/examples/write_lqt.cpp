// examples/write_lqt.cpp — build a small LQT model and write it to disk.
//
// Usage: write_lqt [out_path]   (default /tmp/example.lqt)
#include <cstdio>
#include <string>
#include <vector>

#include "lqt/model.h"

using namespace lqt;

int main(int argc, char** argv) {
    const std::string path = (argc > 1) ? argv[1] : "/tmp/example.lqt";

    LqtModel m;
    m.set_hyperparam("num_layers", 4.0f);
    m.set_hyperparam("hidden_dim", 8.0f);
    m.set_module_graph_json(
        "{\"modules\":[{\"id\":\"ffn0\",\"type\":\"FFN\"}],"
        "\"inputs\":[\"x\"],\"outputs\":[\"y\"]}");

    // A 4-entry scalar codebook (id 0).
    Codebook cb(0, 4, 1);
    cb.set_scalar(0, -1.0f);
    cb.set_scalar(1, 0.0f);
    cb.set_scalar(2, 1.0f);
    cb.set_scalar(3, 2.0f);
    m.add_codebook(cb);

    // One INT4 tensor of 8 elements, indices {0,1,2,3,3,2,1,0}.
    // Packed low-nibble-first: (0,1)=0x10 (2,3)=0x32 (3,2)=0x23 (1,0)=0x01.
    TensorDescriptor d;
    d.name = "ffn0.weight";
    d.tensor_type = TensorType::Standard;
    d.dtype = DType::INT4;
    d.shape = {8};
    d.codebook_id = 0;
    d.delta_id = 0;
    d.scale = 0.5f;
    d.set_flag(TensorFlag::Trainable, true);
    m.add_tensor(d, std::vector<uint8_t>{0x10, 0x32, 0x23, 0x01});

    // A zero delta buffer (FP16) the user can later fine-tune.
    DeltaBuffer dl;
    dl.delta_id = 0;
    dl.dtype = DType::FP16;
    dl.sparse = false;
    dl.values = std::vector<float>(8, 0.0f);
    m.add_delta(dl);

    m.save(path);
    const std::vector<uint8_t> image = m.serialize_to_bytes();
    std::printf("Wrote %s (%zu bytes); tensors=%zu, codebooks present.\n",
                path.c_str(), image.size(), m.tensors().size());
    return 0;
}
