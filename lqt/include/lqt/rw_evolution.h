// lqt/rw_evolution.h — EvolutionEngine + PatternLibrary for Recursive Weights.
// Ports PatternLibrary and EvolutionEngine from recursive_weights_core.py.
// Council: Heimdall (Patch 4).
#pragma once
#include <cstdint>
#include <functional>
#include <map>
#include <random>
#include <string>
#include <vector>
#include "lqt/error.h"
#include "lqt/recursive_weight.h"

namespace lqt {

// ── PatternLibrary ──────────────────────────────────────────────────────────
// Stores named pattern vectors. Patterns are registered and looked up by ID.
// Ports: PatternLibrary.register_pattern(), get_pattern_value().
class PatternLibrary {
public:
    PatternLibrary() = default;

    // Register a named pattern with given data vector.
    // pattern_id must be >= 0 and < 65536.
    void register_pattern(uint32_t pattern_id, std::vector<float> data,
                          const std::string& name = "");

    // Look up pattern and compute context-dependent value.
    // Returns element-wise: pattern[i] * context[i % pattern.size()] if context non-empty,
    // else returns the raw pattern data.
    std::vector<float> get_pattern_value(uint32_t pattern_id,
                                         const std::vector<float>& context) const;

    // Returns true if pattern_id is registered.
    bool has_pattern(uint32_t pattern_id) const;

    // Number of registered patterns.
    size_t size() const;

private:
    struct PatternEntry { uint32_t id; std::vector<float> data; std::string name; };
    std::map<uint32_t, PatternEntry> patterns_;
};

// ── Fitness function type ───────────────────────────────────────────────────
// Given a RecursiveWeight, return a scalar fitness score (higher = better).
using FitnessFunc = std::function<float(const RecursiveWeight&)>;

// ── EvolutionEngine ─────────────────────────────────────────────────────────
// Ports EvolutionEngine from recursive_weights_core.py.
// Implements tournament selection, crossover, mutation for RecursiveWeight populations.
class EvolutionEngine {
public:
    explicit EvolutionEngine(uint64_t seed = 42);

    // Evolve a population for one generation.
    // population: input weight vector (modified in place).
    // fitness_fn: function to score each weight.
    // mutation_rate: probability of mutating self_reference_coeff per weight.
    // crossover_rate: probability of crossover per pair.
    // Returns average fitness after evolution.
    float evolve_generation(std::vector<RecursiveWeight>& population,
                            FitnessFunc fitness_fn,
                            float mutation_rate  = 0.01f,
                            float crossover_rate = 0.1f);

    // Run `generations` rounds of evolution.
    // Returns history of average fitness per generation.
    std::vector<float> evolve(std::vector<RecursiveWeight>& population,
                              FitnessFunc fitness_fn,
                              uint32_t generations   = 10,
                              float mutation_rate    = 0.01f,
                              float crossover_rate   = 0.1f);

    // Single mutation: perturbs self_reference_coeff by Gaussian noise.
    // Clips result to (-0.99, 0.99).
    void mutate(RecursiveWeight& w, float mutation_rate);

    // Single crossover: blends two weights' self_reference_coeff.
    // Returns a new RecursiveWeight inheriting base_index from parent1,
    // self_reference_coeff = mean(p1.coeff, p2.coeff).
    RecursiveWeight crossover(const RecursiveWeight& p1, const RecursiveWeight& p2);

    // Tournament selection: picks the best of `tournament_size` randomly chosen weights.
    const RecursiveWeight& tournament_select(const std::vector<RecursiveWeight>& population,
                                              FitnessFunc fitness_fn,
                                              uint32_t tournament_size = 3);

private:
    std::mt19937 rng_;
};

} // namespace lqt
