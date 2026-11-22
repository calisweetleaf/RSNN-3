// examples/load_reconstruct.cpp — load an LQT file and reconstruct its tensors.
//
// Usage: load_reconstruct [in_path]   (default /tmp/example.lqt)
#include <cstdio>
#include <string>

#include "lqt/model.h"

using namespace lqt;

int main(int argc, char** argv) {
    const std::string path = (argc > 1) ? argv[1] : "/tmp/example.lqt";

    LqtModel m = LqtModel::load(path); // verifies whole-file CRC32

    std::printf("Loaded %s  format v%u.%u  tensors=%zu\n",
                path.c_str(),
                m.header().version_major(), m.header().version_minor(),
                m.tensors().size());

    for (const auto& [key, value] : m.hyperparams()) {
        std::printf("  hyperparam %s = %.3f\n", key.c_str(), value);
    }

    for (const auto& t : m.tensors()) {
        const std::vector<float> w = m.reconstruct(t.desc.name);
        std::printf("  tensor '%s' [%zu elems]:", t.desc.name.c_str(), w.size());
        for (size_t i = 0; i < w.size() && i < 16; ++i) std::printf(" %.3f", w[i]);
        std::printf("\n");
    }
    return 0;
}
