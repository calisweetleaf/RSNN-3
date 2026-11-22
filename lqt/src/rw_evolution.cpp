// lqt/rw_evolution.cpp — Implementation of PatternLibrary + EvolutionEngine.
// Ports PatternLibrary and EvolutionEngine from recursive_weights_core.py.
// Council: Heimdall (Patch 4). Single-threaded; no torch/numpy.
#include "lqt/rw_evolution.h"

#include <algorithm>
#include <numeric>
#include <random>
#include <stdexcept>

namespace lqt {

// ── PatternLibrary ──────────────────────────────────────────────────────────

void PatternLibrary::register_pattern(uint32_t pattern_id,
                                      std::vector<float> data,
                                      const std::string& name) {
    if (pattern_id >= 65536) {
        throw ValidationError("PatternLibrary: pattern_id must be < 65536");
    }
    if (patterns_.find(pattern_id) != patterns_.end()) {
        throw ValidationError("PatternLibrary: duplicate pattern_id");
    }
    PatternEntry entry{pattern_id, std::move(data), name};
    patterns_.emplace(pattern_id, std::move(entry));
}

std::vector<float> PatternLibrary::get_pattern_value(
    uint32_t pattern_id, const std::vector<float>& context) const {
    auto it = patterns_.find(pattern_id);
    if (it == patterns_.end()) {
        return {};
    }
    const std::vector<float>& data = it->second.data;
    if (context.empty()) {
        return data;
    }
    if (data.empty()) {
        return {};
    }
    const size_t n = std::max(data.size(), context.size());
    std::vector<float> result(n);
    for (size_t i = 0; i < n; ++i) {
        result[i] = data[i % data.size()] * context[i % context.size()];
    }
    return result;
}

bool PatternLibrary::has_pattern(uint32_t pattern_id) const {
    return patterns_.find(pattern_id) != patterns_.end();
}

size_t PatternLibrary::size() const {
    return patterns_.size();
}

// ── EvolutionEngine ─────────────────────────────────────────────────────────

EvolutionEngine::EvolutionEngine(uint64_t seed)
    : rng_(static_cast<std::mt19937::result_type>(seed)) {}

void EvolutionEngine::mutate(RecursiveWeight& w, float mutation_rate) {
    std::uniform_real_distribution<float> uniform(0.0f, 1.0f);
    if (uniform(rng_) < mutation_rate) {
        std::normal_distribution<float> gauss(0.0f, 0.1f);
        float noise = gauss(rng_);
        float updated = w.self_reference_coeff + noise;
        if (updated < -0.99f) updated = -0.99f;
        if (updated >  0.99f) updated =  0.99f;
        w.self_reference_coeff = updated;
    }
}

RecursiveWeight EvolutionEngine::crossover(const RecursiveWeight& p1,
                                           const RecursiveWeight& p2) {
    RecursiveWeight child = p1;
    child.base_index = p1.base_index;
    child.self_reference_coeff =
        (p1.self_reference_coeff + p2.self_reference_coeff) / 2.0f;
    return child;
}

const RecursiveWeight& EvolutionEngine::tournament_select(
    const std::vector<RecursiveWeight>& population,
    FitnessFunc fitness_fn,
    uint32_t tournament_size) {
    if (population.empty()) {
        throw ValidationError("EvolutionEngine::tournament_select: empty population");
    }
    const size_t pop_size = population.size();
    const size_t k = std::min(static_cast<size_t>(tournament_size), pop_size);

    // Pick k distinct indices when possible (sample without replacement).
    std::vector<size_t> picks;
    picks.reserve(k);
    if (k >= pop_size) {
        for (size_t i = 0; i < pop_size; ++i) picks.push_back(i);
    } else {
        std::uniform_int_distribution<size_t> dist(0, pop_size - 1);
        while (picks.size() < k) {
            size_t idx = dist(rng_);
            if (std::find(picks.begin(), picks.end(), idx) == picks.end()) {
                picks.push_back(idx);
            }
        }
    }

    size_t best_idx = picks[0];
    float best_fit = fitness_fn(population[best_idx]);
    for (size_t i = 1; i < picks.size(); ++i) {
        float f = fitness_fn(population[picks[i]]);
        if (f > best_fit) {
            best_fit = f;
            best_idx = picks[i];
        }
    }
    return population[best_idx];
}

float EvolutionEngine::evolve_generation(std::vector<RecursiveWeight>& population,
                                         FitnessFunc fitness_fn,
                                         float mutation_rate,
                                         float crossover_rate) {
    if (population.empty()) {
        return 0.0f;
    }

    // 1. Score all weights.
    std::vector<float> scores(population.size());
    for (size_t i = 0; i < population.size(); ++i) {
        scores[i] = fitness_fn(population[i]);
    }

    // 2. Crossover pass: for each weight, with crossover_rate probability,
    // tournament-select two parents and replace this weight with their child.
    std::uniform_real_distribution<float> uniform(0.0f, 1.0f);
    if (population.size() >= 2) {
        std::vector<RecursiveWeight> next = population;
        for (size_t i = 0; i < population.size(); ++i) {
            if (uniform(rng_) < crossover_rate) {
                const RecursiveWeight& parent1 =
                    tournament_select(population, fitness_fn, 3);
                const RecursiveWeight& parent2 =
                    tournament_select(population, fitness_fn, 3);
                next[i] = crossover(parent1, parent2);
            }
        }
        population = std::move(next);
    }

    // 3. Mutation pass.
    for (auto& w : population) {
        mutate(w, mutation_rate);
    }

    // 4. Re-score for mean fitness reporting.
    float sum = 0.0f;
    for (const auto& w : population) {
        sum += fitness_fn(w);
    }
    return sum / static_cast<float>(population.size());
}

std::vector<float> EvolutionEngine::evolve(std::vector<RecursiveWeight>& population,
                                           FitnessFunc fitness_fn,
                                           uint32_t generations,
                                           float mutation_rate,
                                           float crossover_rate) {
    std::vector<float> history;
    history.reserve(generations);
    for (uint32_t g = 0; g < generations; ++g) {
        float avg = evolve_generation(population, fitness_fn,
                                      mutation_rate, crossover_rate);
        history.push_back(avg);
    }
    return history;
}

} // namespace lqt
