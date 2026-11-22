// examples/mutate_lqt.cpp — edit a codebook entry with validation + edit log.
//
// Demonstrates the editable-post-quantization core of LQT: load a model, edit a
// codebook primitive, validate the change against the mutation framework, record
// it in a tamper-evident append-only edit log, and re-save.
//
// Usage: mutate_lqt [in_path] [out_path]
//        defaults: /tmp/example.lqt -> /tmp/example_mutated.lqt
#include <cstdio>
#include <string>
#include <vector>

#include "lqt/edit_log.h"
#include "lqt/model.h"
#include "lqt/mutation.h"

using namespace lqt;

static void print_tensor(const LqtModel& m, const char* name) {
    const std::vector<float> w = m.reconstruct(name);
    std::printf("  %s:", name);
    for (size_t i = 0; i < w.size() && i < 16; ++i) std::printf(" %.3f", w[i]);
    std::printf("\n");
}

int main(int argc, char** argv) {
    const std::string in_path  = (argc > 1) ? argv[1] : "/tmp/example.lqt";
    const std::string out_path = (argc > 2) ? argv[2] : "/tmp/example_mutated.lqt";

    try {
        LqtModel m = LqtModel::load(in_path);
        std::printf("Before mutation:\n");
        print_tensor(m, "ffn0.weight");

        // --- Propose a codebook edit: codebook[0] entry 0 -> -4.0 -------------
        const uint16_t cb_id = 0;
        const uint32_t entry = 0;
        const float new_value = -4.0f;

        Codebook* cb = m.codebook_mut(cb_id);
        if (!cb) { std::printf("codebook %u not found\n", cb_id); return 1; }

        // --- Validate the change (constraint 2 value bounds + constraint 4) ---
        MutationValidator validator(-8.0f, 8.0f);
        const ValidationResult vb = validator.check_value_bounds(&new_value, 1);
        if (!vb.ok) { std::printf("rejected: %s\n", vb.reason.c_str()); return 1; }

        const TensorBlob* tb = m.find_tensor("ffn0.weight");
        if (tb) {
            const ValidationResult ac = validator.check_access(tb->desc, /*authorized=*/true);
            if (!ac.ok) { std::printf("rejected: %s\n", ac.reason.c_str()); return 1; }
        }

        // --- Apply + record in a tamper-evident edit log ----------------------
        cb->set_scalar(entry, new_value);

        EditLog log;
        EditLogEntry e = make_entry(MutationType::CodebookEdit, "codebook[0][0]",
                                    &new_value, sizeof(new_value), log.tail_hash());
        log.append(e);
        std::printf("Edit log: %zu entry, chain valid = %s\n",
                    log.size(), log.verify_chain() ? "true" : "false");

        m.save(out_path);
        LqtModel reloaded = LqtModel::load(out_path);
        std::printf("After mutation (reloaded %s):\n", out_path.c_str());
        print_tensor(reloaded, "ffn0.weight");
        return 0;
    } catch (const LqtError& ex) {
        std::printf("LQT error: %s\n", ex.what());
        return 1;
    }
}
