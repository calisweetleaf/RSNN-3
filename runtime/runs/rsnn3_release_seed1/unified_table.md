| tensor | shape | group | repr | base | bits | scale | base-only max err | reload max err |
|---|---|---|---|---|---|---|---|---|
| `W_R` | (16, 16) | psi | buckets | codebook 0 | 8 | 0.7268 | 0.00281 | 0 |
| `W_E` | (16, 5) | psi | buckets | codebook 0 | 8 | 1.09 | 0.00417 | 0 |
| `W_M` | (16, 8) | psi | buckets | codebook 0 | 8 | 1.284 | 0.00491 | 0 |
| `engine.consciousness_integrator.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.consciousness_integrator.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_cognitive_weight.tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_cognitive_weight.error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1.318 | 0.00516 | 0 |
| `engine.meta_cognitive_weight.base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 4.011 | 0.0156 | 0 |
| `engine.meta_cognitive_weight.harmonic_amplitudes` | (4, 64) | rw_registry | buckets | codebook 0 | 8 | 3.71 | 0.0149 | 0 |
| `engine.meta_cognitive_weight.frequencies` | (4,) | rw_registry | buckets | codebook 0 | 8 | 7.861 | 0.0282 | 0 |
| `engine.meta_cognitive_weight.phase_offsets` | (4,) | rw_registry | buckets | codebook 0 | 8 | 2.356 | 0.00873 | 0 |
| `engine.meta_cognitive_weight.base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_cognitive_weight.delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.thought_encoder.0.weight` | (128, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.thought_encoder.0.bias` | (128,) | engine | buckets | codebook 0 | 8 | 0.1238 | 0.000509 | 0 |
| `engine.thought_encoder.2.weight` | (128,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.thought_encoder.2.bias` | (128,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.thought_encoder.3.weight` | (64, 128) | engine | base_eps | codebook 0 | 8 | 0.08837 | 0.000365 | 0 |
| `engine.thought_encoder.3.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.08772 | 0.000334 | 0 |
| `engine.consciousness_integrator.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000511 | 0 |
| `engine.consciousness_integrator.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.ethical_aligner.0.weight` | (64, 70) | ethical | base_eps | codebook 0 | 8 | 0.1195 | 0.000491 | 0 |
| `engine.ethical_aligner.0.bias` | (64,) | ethical | buckets | codebook 0 | 8 | 0.1188 | 0.000463 | 0 |
| `engine.ethical_aligner.2.weight` | (64, 64) | ethical | buckets | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.ethical_aligner.2.bias` | (64,) | ethical | buckets | codebook 0 | 8 | 0.1245 | 0.000476 | 0 |
| `engine.metacognitive_analyzer.0.weight` | (64, 192) | metacognitive | base_eps | codebook 0 | 8 | 0.07217 | 0.000299 | 0 |
| `engine.metacognitive_analyzer.0.bias` | (64,) | metacognitive | buckets | codebook 0 | 8 | 0.06774 | 0.000259 | 0 |
| `engine.metacognitive_analyzer.2.weight` | (32, 64) | metacognitive | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.metacognitive_analyzer.2.bias` | (32,) | metacognitive | buckets | codebook 0 | 8 | 0.1233 | 0.000481 | 0 |
| `engine.metacognitive_analyzer.4.weight` | (4, 32) | metacognitive | buckets | codebook 0 | 8 | 0.1765 | 0.000687 | 0 |
| `engine.metacognitive_analyzer.4.bias` | (4,) | metacognitive | buckets | codebook 0 | 8 | 0.08454 | 0.000328 | 0 |
| `engine.code_generator.thought_processor.weight_ih_l0` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.code_generator.thought_processor.weight_hh_l0` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.code_generator.thought_processor.bias_ih_l0` | (256,) | engine | buckets | codebook 0 | 8 | 0.1238 | 0.000482 | 0 |
| `engine.code_generator.thought_processor.bias_hh_l0` | (256,) | engine | buckets | codebook 0 | 8 | 0.1245 | 0.000507 | 0 |
| `engine.code_generator.thought_processor.weight_ih_l1` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.code_generator.thought_processor.weight_hh_l1` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.code_generator.thought_processor.bias_ih_l1` | (256,) | engine | buckets | codebook 0 | 8 | 0.1238 | 0.000482 | 0 |
| `engine.code_generator.thought_processor.bias_hh_l1` | (256,) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000509 | 0 |
| `engine.code_generator.thought_processor.weight_ih_l2` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.code_generator.thought_processor.weight_hh_l2` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.code_generator.thought_processor.bias_ih_l2` | (256,) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000488 | 0 |
| `engine.code_generator.thought_processor.bias_hh_l2` | (256,) | engine | buckets | codebook 0 | 8 | 0.1245 | 0.000487 | 0 |
| `engine.code_generator.code_projector.weight` | (50257, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.code_generator.code_projector.bias` | (50257,) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.language_generator.reasoning_generator.weight_ih_l0` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.language_generator.reasoning_generator.weight_hh_l0` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000515 | 0 |
| `engine.language_generator.reasoning_generator.bias_ih_l0` | (256,) | engine | buckets | codebook 0 | 8 | 0.1232 | 0.000484 | 0 |
| `engine.language_generator.reasoning_generator.bias_hh_l0` | (256,) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000487 | 0 |
| `engine.language_generator.reasoning_generator.weight_ih_l1` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.language_generator.reasoning_generator.weight_hh_l1` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.language_generator.reasoning_generator.bias_ih_l1` | (256,) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000487 | 0 |
| `engine.language_generator.reasoning_generator.bias_hh_l1` | (256,) | engine | buckets | codebook 0 | 8 | 0.1242 | 0.00048 | 0 |
| `engine.meta_reflective_head.reflection_core.memory_bank` | (5, 64) | meta_reflective | buckets | codebook 0 | 8 | 3.176 | 0.0126 | 0 |
| `engine.code_generator.quality_assessor.0.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.code_generator.quality_assessor.0.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1241 | 0.000481 | 0 |
| `engine.code_generator.quality_assessor.2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.code_generator.quality_assessor.2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.06084 | 0.000232 | 0 |
| `engine.code_generator.quality_assessor.4.weight` | (1, 64) | engine | buckets | codebook 0 | 8 | 0.1235 | 0.000481 | 0 |
| `engine.code_generator.quality_assessor.4.bias` | (1,) | engine | buckets | codebook 0 | 8 | 0.04309 | 0 | 0 |
| `engine.data_generator.data_processor.0.weight` | (128, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.data_generator.data_processor.0.bias` | (128,) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000487 | 0 |
| `engine.data_generator.data_processor.2.weight` | (128,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.data_generator.data_processor.2.bias` | (128,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.data_generator.data_processor.3.weight` | (64, 128) | engine | base_eps | codebook 0 | 8 | 0.08838 | 0.000367 | 0 |
| `engine.data_generator.data_processor.3.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.0878 | 0.000343 | 0 |
| `engine.data_generator.schema_generator.0.weight` | (512, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.data_generator.schema_generator.0.bias` | (512,) | engine | buckets | codebook 0 | 8 | 0.1242 | 0.000487 | 0 |
| `engine.data_generator.schema_generator.2.weight` | (256, 512) | engine | base_eps | codebook 0 | 8 | 0.04419 | 0.000183 | 0 |
| `engine.data_generator.schema_generator.2.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.04419 | 0.000177 | 0 |
| `engine.data_generator.schema_generator.4.weight` | (128, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.data_generator.schema_generator.4.bias` | (128,) | engine | buckets | codebook 0 | 8 | 0.05975 | 0.000234 | 0 |
| `engine.data_generator.quality_assessor.0.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.data_generator.quality_assessor.0.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.1242 | 0.000488 | 0 |
| `engine.data_generator.quality_assessor.2.weight` | (1, 64) | engine | buckets | codebook 0 | 8 | 0.117 | 0.000448 | 0 |
| `engine.data_generator.quality_assessor.2.bias` | (1,) | engine | buckets | codebook 0 | 8 | 0.09446 | 0 | 0 |
| `engine.language_generator.quality_assessor.0.weight` | (128, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000514 | 0 |
| `engine.language_generator.quality_assessor.0.bias` | (128,) | engine | buckets | codebook 0 | 8 | 0.1246 | 0.000486 | 0 |
| `engine.language_generator.quality_assessor.2.weight` | (1, 128) | engine | buckets | codebook 0 | 8 | 0.08742 | 0.000336 | 0 |
| `engine.language_generator.quality_assessor.2.bias` | (1,) | engine | buckets | codebook 0 | 8 | 0.0761 | 0 | 0 |
| `engine.meta_cognitive_weight.recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_cognitive_weight.recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.044 | 0.00414 | 0 |
| `engine.meta_reflective_head.output_processor.0.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000514 | 0 |
| `engine.meta_reflective_head.output_processor.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1206 | 0.00046 | 0 |
| `engine.meta_reflective_head.output_processor.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.output_processor.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_attention.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_attention.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.pattern_detector.weight` | (64, 8, 3) | meta_reflective | buckets | codebook 0 | 8 | 0.2041 | 0.000815 | 0 |
| `engine.meta_reflective_head.abstraction_layer.pattern_detector.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.2028 | 0.00079 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.weight_ih_l0` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.weight_hh_l0` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.bias_ih_l0` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.00049 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.bias_hh_l0` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 0.1243 | 0.000485 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.weight_ih_l1` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.weight_hh_l1` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.bias_ih_l1` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000482 | 0 |
| `engine.meta_reflective_head.reflection_core.state_tracker.bias_hh_l1` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 0.1231 | 0.00048 | 0 |
| `engine.meta_reflective_head.reflection_core.memory_attention.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.meta_reflective_head.reflection_core.memory_attention.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.cross_thought_attention.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.00063 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.cross_thought_attention.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_ih_l0` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_hh_l0` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_ih_l0` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1247 | 0.000485 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_hh_l0` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.00049 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_ih_l0_reverse` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_hh_l0_reverse` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_ih_l0_reverse` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000512 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_hh_l0_reverse` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.124 | 0.000496 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_ih_l1` | (256, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_hh_l1` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_ih_l1` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1247 | 0.000482 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_hh_l1` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000502 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_ih_l1_reverse` | (256, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.weight_hh_l1_reverse` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000514 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_ih_l1_reverse` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1244 | 0.00049 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_detector.bias_hh_l1_reverse` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000487 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_projector.weight` | (64, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.08838 | 0.000365 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.emergence_projector.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.08745 | 0.000333 | 0 |
| `engine.meta_reflective_head.internal_thought_generator.0.weight` | (128, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000511 | 0 |
| `engine.meta_reflective_head.internal_thought_generator.0.bias` | (128,) | meta_reflective | buckets | codebook 0 | 8 | 0.1244 | 0.000482 | 0 |
| `engine.meta_reflective_head.internal_thought_generator.1.weight` | (128,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.internal_thought_generator.1.bias` | (128,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.internal_thought_generator.3.weight` | (64, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.08839 | 0.000366 | 0 |
| `engine.meta_reflective_head.internal_thought_generator.3.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.08819 | 0.000338 | 0 |
| `engine.meta_reflective_head.reflection_synthesizer.0.weight` | (64, 192) | meta_reflective | base_eps | codebook 0 | 8 | 0.07216 | 0.000299 | 0 |
| `engine.meta_reflective_head.reflection_synthesizer.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.07175 | 0.000273 | 0 |
| `engine.meta_reflective_head.reflection_synthesizer.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_synthesizer.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_synthesizer.3.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000515 | 0 |
| `engine.meta_reflective_head.reflection_synthesizer.3.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1229 | 0.000484 | 0 |
| `engine.meta_reflective_head.self_modifier.0.weight` | (16, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000513 | 0 |
| `engine.meta_reflective_head.self_modifier.0.bias` | (16,) | meta_reflective | buckets | codebook 0 | 8 | 0.124 | 0.000483 | 0 |
| `engine.meta_reflective_head.self_modifier.2.weight` | (64, 16) | meta_reflective | buckets | codebook 0 | 8 | 0.25 | 0.00102 | 0 |
| `engine.meta_reflective_head.self_modifier.2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.2498 | 0.000974 | 0 |
| `engine.meta_reflective_head.depth_controller.0.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000511 | 0 |
| `engine.meta_reflective_head.depth_controller.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1207 | 0.000468 | 0 |
| `engine.meta_reflective_head.depth_controller.2.weight` | (5, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000501 | 0 |
| `engine.meta_reflective_head.depth_controller.2.bias` | (5,) | meta_reflective | buckets | codebook 0 | 8 | 0.0898 | 0.000327 | 0 |
| `engine.autodidactic_learner.ethical_filter.ethical_manifold` | (5, 64) | ethical | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['thought_processor'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['thought_processor'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['thought_processor'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.2589 | 0.00101 | 0 |
| `engine.weight_registry._weights['thought_processor'].harmonic_amplitudes` | (3, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1727 | 0.000679 | 0 |
| `engine.weight_registry._weights['thought_processor'].frequencies` | (3,) | rw_registry | buckets | codebook 0 | 8 | 0.7726 | 0.00289 | 0 |
| `engine.weight_registry._weights['thought_processor'].phase_offsets` | (3,) | rw_registry | buckets | codebook 0 | 8 | 2.094 | 0.00821 | 0 |
| `engine.weight_registry._weights['thought_processor'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['thought_processor'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].tensor_position` | (5,) | ethical | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].error_preservation` | (64,) | ethical | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].base_phase` | (64,) | ethical | buckets | codebook 0 | 8 | 0.2234 | 0.000801 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].harmonic_amplitudes` | (2, 64) | ethical | buckets | codebook 0 | 8 | 0.1159 | 0.00045 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].frequencies` | (2,) | ethical | buckets | codebook 0 | 8 | 5.236 | 0.0102 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].phase_offsets` | (2,) | ethical | buckets | codebook 0 | 8 | 1.571 | 0.00616 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].base_delta` | (64,) | ethical | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['ethical_aligner'].delta_adaptive_factor` | (64,) | ethical | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.0.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.self_reflection_processor.layers.0.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.0.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.self_reflection_processor.layers.0.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1243 | 0.00049 | 0 |
| `engine.self_reflection_processor.layers.0.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.self_reflection_processor.layers.0.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05961 | 0.000244 | 0 |
| `engine.self_reflection_processor.layers.0.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.0.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.0.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.0.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.1.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.self_reflection_processor.layers.1.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.1.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.self_reflection_processor.layers.1.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1243 | 0.00049 | 0 |
| `engine.self_reflection_processor.layers.1.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.self_reflection_processor.layers.1.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05961 | 0.000244 | 0 |
| `engine.self_reflection_processor.layers.1.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.1.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.1.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.1.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.2.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.self_reflection_processor.layers.2.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.2.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.self_reflection_processor.layers.2.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1243 | 0.00049 | 0 |
| `engine.self_reflection_processor.layers.2.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.self_reflection_processor.layers.2.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05961 | 0.000244 | 0 |
| `engine.self_reflection_processor.layers.2.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.2.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.2.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.2.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.3.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.self_reflection_processor.layers.3.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.3.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.self_reflection_processor.layers.3.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1243 | 0.00049 | 0 |
| `engine.self_reflection_processor.layers.3.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.self_reflection_processor.layers.3.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05961 | 0.000244 | 0 |
| `engine.self_reflection_processor.layers.3.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.3.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.3.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.3.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.4.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.self_reflection_processor.layers.4.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.4.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.self_reflection_processor.layers.4.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1243 | 0.00049 | 0 |
| `engine.self_reflection_processor.layers.4.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.self_reflection_processor.layers.4.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05961 | 0.000244 | 0 |
| `engine.self_reflection_processor.layers.4.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.4.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.4.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.4.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.5.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.self_reflection_processor.layers.5.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.5.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.self_reflection_processor.layers.5.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1243 | 0.00049 | 0 |
| `engine.self_reflection_processor.layers.5.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.self_reflection_processor.layers.5.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05961 | 0.000244 | 0 |
| `engine.self_reflection_processor.layers.5.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.5.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.5.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.self_reflection_processor.layers.5.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_attention.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_attention.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_combiner.0.weight` | (64, 480) | meta_reflective | base_eps | codebook 0 | 8 | 0.04564 | 0.000189 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_combiner.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.04528 | 0.000171 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_combiner.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_combiner.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_combiner.3.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_combiner.3.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1239 | 0.000484 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_controller.0.weight` | (64, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.08839 | 0.000366 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_controller.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.08768 | 0.000335 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_controller.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_controller.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_controller.3.weight` | (3, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.1243 | 0.000487 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_controller.3.bias` | (3,) | meta_reflective | buckets | codebook 0 | 8 | 0.1122 | 0.000318 | 0 |
| `engine.meta_reflective_head.reflection_core.self_assessor.0.weight` | (32, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.reflection_core.self_assessor.0.bias` | (32,) | meta_reflective | buckets | codebook 0 | 8 | 0.1236 | 0.000476 | 0 |
| `engine.meta_reflective_head.reflection_core.self_assessor.1.weight` | (32,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.self_assessor.1.bias` | (32,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.self_assessor.3.weight` | (4, 32) | meta_reflective | buckets | codebook 0 | 8 | 0.1768 | 0.000687 | 0 |
| `engine.meta_reflective_head.reflection_core.self_assessor.3.bias` | (4,) | meta_reflective | buckets | codebook 0 | 8 | 0.1764 | 0.000613 | 0 |
| `engine.meta_reflective_head.reflection_core.memory_attention.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000514 | 0 |
| `engine.meta_reflective_head.reflection_core.memory_attention.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.thought_encoder.0.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.thought_encoder.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1232 | 0.000477 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.thought_encoder.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.thought_encoder.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.process_encoder.0.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000514 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.process_encoder.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1244 | 0.000485 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.process_encoder.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.process_encoder.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.cross_thought_attention.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.cross_thought_attention.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.0.weight` | (64, 64, 5) | meta_reflective | base_eps | codebook 0 | 8 | 0.0559 | 0.000231 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.05441 | 0.000212 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.3.weight` | (64, 64, 3) | meta_reflective | base_eps | codebook 0 | 8 | 0.07216 | 0.000299 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.3.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.07094 | 0.000274 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.4.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.meta_pattern_net.4.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.uncertainty_net.0.weight` | (64, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.08838 | 0.000366 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.uncertainty_net.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.08779 | 0.000347 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.uncertainty_net.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.uncertainty_net.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.uncertainty_net.3.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000515 | 0 |
| `engine.meta_reflective_head.metacognitive_processor.uncertainty_net.3.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1236 | 0.000463 | 0 |
| `engine.backbone.field.recursive_tensor.data` | (16, 16) | rta | buckets | codebook 0 | 8 | 0.009998 | 4e-05 | 0 |
| `engine.backbone.field.ethical_state.field_potential` | (16, 16) | ethical | buckets | codebook 0 | 8 | 31.65 | 0.124 | 0 |
| `engine.backbone.field.ethical_state.ethical_manifold_data` | (5, 16, 16) | ethical | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.ethical_state.symbol_resonance` | (16, 16) | ethical | buckets | codebook 0 | 8 | 158.3 | 0.62 | 0 |
| `engine.backbone.field.ethical_state.narrative_momentum` | (2, 16, 16) | ethical | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.ethical_state.meaning_potential` | (16, 16) | ethical | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.metacog_tensor.integration_layer.weight` | (64, 128) | metacognitive | base_eps | codebook 0 | 8 | 0.08837 | 0.000366 | 0 |
| `engine.backbone.field.metacog_tensor.integration_layer.bias` | (64,) | metacognitive | buckets | codebook 0 | 8 | 0.0857 | 0.000335 | 0 |
| `engine.backbone.field.metacog_tensor.consciousness_gate.weight` | (1, 5) | metacognitive | buckets | codebook 0 | 8 | 0.2054 | 0.000756 | 0 |
| `engine.backbone.field.metacog_tensor.consciousness_gate.bias` | (1,) | metacognitive | buckets | codebook 0 | 8 | 0.3604 | 0 | 0 |
| `engine.backbone.field.metacog_tensor.metacognitive_projector.weight` | (64, 64) | metacognitive | buckets | codebook 0 | 8 | 0.125 | 0.000498 | 0 |
| `engine.backbone.field.metacog_tensor.metacognitive_projector.bias` | (64,) | metacognitive | buckets | codebook 0 | 8 | 0.1238 | 0.000479 | 0 |
| `engine.autodidactic_learner.metacognitive_monitor.identity_tracker.core_identity` | (256,) | metacognitive | buckets | codebook 0 | 8 | 3.331 | 0.013 | 0 |
| `engine.self_reflection_processor.layers.0.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.self_reflection_processor.layers.0.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.1.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.self_reflection_processor.layers.1.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.2.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.self_reflection_processor.layers.2.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.3.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.self_reflection_processor.layers.3.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.4.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.self_reflection_processor.layers.4.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.self_reflection_processor.layers.5.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.self_reflection_processor.layers.5.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000632 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.multihead_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000633 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.multihead_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000485 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05656 | 0.000234 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.norm3.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.norm3.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000632 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.multihead_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000633 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.multihead_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000485 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05656 | 0.000234 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.norm3.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.norm3.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000632 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.multihead_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000633 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.multihead_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000485 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05656 | 0.000234 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.norm3.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.norm3.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000632 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.multihead_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000633 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.multihead_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000485 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.05656 | 0.000234 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.norm3.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.norm3.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.0.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.language_generator.language_processor.layers.0.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.0.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.0.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000481 | 0 |
| `engine.language_generator.language_processor.layers.0.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.language_generator.language_processor.layers.0.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.06238 | 0.000243 | 0 |
| `engine.language_generator.language_processor.layers.0.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.0.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.0.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.0.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.1.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.language_generator.language_processor.layers.1.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.1.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.1.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000481 | 0 |
| `engine.language_generator.language_processor.layers.1.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.language_generator.language_processor.layers.1.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.06238 | 0.000243 | 0 |
| `engine.language_generator.language_processor.layers.1.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.1.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.1.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.1.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.2.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.language_generator.language_processor.layers.2.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.2.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.2.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000481 | 0 |
| `engine.language_generator.language_processor.layers.2.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.language_generator.language_processor.layers.2.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.06238 | 0.000243 | 0 |
| `engine.language_generator.language_processor.layers.2.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.2.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.2.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.2.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.3.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.language_generator.language_processor.layers.3.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.3.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.3.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000481 | 0 |
| `engine.language_generator.language_processor.layers.3.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.language_generator.language_processor.layers.3.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.06238 | 0.000243 | 0 |
| `engine.language_generator.language_processor.layers.3.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.3.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.3.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.3.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.4.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.language_generator.language_processor.layers.4.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.4.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.4.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000481 | 0 |
| `engine.language_generator.language_processor.layers.4.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.language_generator.language_processor.layers.4.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.06238 | 0.000243 | 0 |
| `engine.language_generator.language_processor.layers.4.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.4.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.4.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.4.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.5.self_attn.in_proj_weight` | (192, 64) | engine | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.language_generator.language_processor.layers.5.self_attn.in_proj_bias` | (192,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.5.linear1.weight` | (256, 64) | engine | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.5.linear1.bias` | (256,) | engine | buckets | codebook 0 | 8 | 0.1244 | 0.000481 | 0 |
| `engine.language_generator.language_processor.layers.5.linear2.weight` | (64, 256) | engine | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.language_generator.language_processor.layers.5.linear2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 0.06238 | 0.000243 | 0 |
| `engine.language_generator.language_processor.layers.5.norm1.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.5.norm1.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.5.norm2.weight` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.language_generator.language_processor.layers.5.norm2.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.0.0.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.0.0.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000479 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.0.1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.0.1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.0.3.weight` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.0.3.bias` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1247 | 0.000495 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.1.0.weight` | (32, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000505 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.1.0.bias` | (32,) | meta_reflective | buckets | codebook 0 | 8 | 0.1193 | 0.000436 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.1.1.weight` | (32,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.1.1.bias` | (32,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.1.3.weight` | (128, 32) | meta_reflective | buckets | codebook 0 | 8 | 0.1767 | 0.000733 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.1.3.bias` | (128,) | meta_reflective | buckets | codebook 0 | 8 | 0.176 | 0.000677 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.2.0.weight` | (16, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000503 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.2.0.bias` | (16,) | meta_reflective | buckets | codebook 0 | 8 | 0.1228 | 0.000443 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.2.1.weight` | (16,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.2.1.bias` | (16,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.2.3.weight` | (64, 16) | meta_reflective | buckets | codebook 0 | 8 | 0.2497 | 0.00101 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.2.3.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.2464 | 0.000965 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.3.0.weight` | (8, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.3.0.bias` | (8,) | meta_reflective | buckets | codebook 0 | 8 | 0.1169 | 0.000449 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.3.1.weight` | (8,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.3.1.bias` | (8,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.3.3.weight` | (32, 8) | meta_reflective | buckets | codebook 0 | 8 | 0.353 | 0.00138 | 0 |
| `engine.meta_reflective_head.abstraction_layer.concept_hierarchies.3.3.bias` | (32,) | meta_reflective | buckets | codebook 0 | 8 | 0.3448 | 0.00123 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.self_attn.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.153 | 0.000634 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.self_attn.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.linear1.weight` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.linear1.bias` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1244 | 0.000495 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.linear2.weight` | (64, 256) | meta_reflective | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.linear2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.06102 | 0.000234 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.norm1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.norm1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.norm2.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.norm2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.self_attn.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.self_attn.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.linear1.weight` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.linear1.bias` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1246 | 0.000488 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.linear2.weight` | (64, 256) | meta_reflective | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.linear2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.05991 | 0.000231 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.norm1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.norm1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.norm2.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.norm2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.self_attn.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000634 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.self_attn.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.linear1.weight` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.linear1.bias` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1248 | 0.000486 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.linear2.weight` | (64, 256) | meta_reflective | base_eps | codebook 0 | 8 | 0.0625 | 0.000259 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.linear2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.06125 | 0.000238 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.norm1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.norm1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.norm2.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.norm2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.self_attn.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.self_attn.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.linear1.weight` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.linear1.bias` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1247 | 0.00049 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.linear2.weight` | (64, 256) | meta_reflective | base_eps | codebook 0 | 8 | 0.06249 | 0.000259 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.linear2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.05848 | 0.000225 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.norm1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.norm1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.norm2.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.norm2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.self_attn.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.self_attn.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.linear1.weight` | (256, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000519 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.linear1.bias` | (256,) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000503 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.linear2.weight` | (64, 256) | meta_reflective | base_eps | codebook 0 | 8 | 0.06249 | 0.000255 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.linear2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.06046 | 0.000237 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.norm1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.norm1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.norm2.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.norm2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.self_attn.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.self_attn.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.linear1.weight` | (128, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.linear1.bias` | (128,) | meta_reflective | buckets | codebook 0 | 8 | 0.1242 | 0.0005 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.linear2.weight` | (64, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.08839 | 0.000365 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.linear2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.08786 | 0.000345 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.norm1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.norm1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.norm2.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.norm2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.self_attn.in_proj_weight` | (192, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.1531 | 0.000635 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.self_attn.in_proj_bias` | (192,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.linear1.weight` | (128, 64) | meta_reflective | base_eps | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.linear1.bias` | (128,) | meta_reflective | buckets | codebook 0 | 8 | 0.1242 | 0.0005 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.linear2.weight` | (64, 128) | meta_reflective | base_eps | codebook 0 | 8 | 0.08839 | 0.000365 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.linear2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 0.08786 | 0.000345 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.norm1.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.norm1.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.norm2.weight` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.norm2.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.metacog_tensor.contradiction_field.paradox_field` | (64, 64) | metacognitive | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.metacog_tensor.contradiction_field.value_tension_matrix` | (64, 64) | metacognitive | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.metacog_tensor.coherence_tracer.information_flow_matrix` | (64, 64) | metacognitive | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.metacog_tensor.reflective_indexer.layer_awareness` | (3,) | metacognitive | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.metacog_tensor.reflective_indexer.cross_layer_connectivity` | (3, 3) | metacognitive | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.backbone.field.metacog_tensor.identity_coherence.core_identity_vector` | (64,) | metacognitive | buckets | codebook 0 | 8 | 2.701 | 0.0109 | 0 |
| `engine.backbone.field.metacog_tensor.identity_coherence.identity_evolution_matrix` | (64, 64) | metacognitive | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.abstraction_ladder.levels['concrete_implementation'].content_representation` | (64,) | iala | buckets | codebook 0 | 8 | 2.459 | 0.00951 | 0 |
| `engine.autodidactic_learner.abstraction_ladder.levels['operational_procedures'].content_representation` | (64,) | iala | buckets | codebook 0 | 8 | 2.719 | 0.0104 | 0 |
| `engine.autodidactic_learner.abstraction_ladder.levels['functional_patterns'].content_representation` | (64,) | iala | buckets | codebook 0 | 8 | 2.411 | 0.00931 | 0 |
| `engine.autodidactic_learner.abstraction_ladder.levels['conceptual_frameworks'].content_representation` | (64,) | iala | buckets | codebook 0 | 8 | 3.269 | 0.0127 | 0 |
| `engine.autodidactic_learner.abstraction_ladder.levels['theoretical_principles'].content_representation` | (64,) | iala | buckets | codebook 0 | 8 | 2.405 | 0.00926 | 0 |
| `engine.autodidactic_learner.abstraction_ladder.levels['philosophical_foundations'].content_representation` | (64,) | iala | buckets | codebook 0 | 8 | 3.03 | 0.011 | 0 |
| `engine.autodidactic_learner.abstraction_ladder.levels['universal_abstractions'].content_representation` | (64,) | iala | buckets | codebook 0 | 8 | 2.507 | 0.00925 | 0 |
| `engine.weight_registry._weights['thought_processor'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['thought_processor'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.027 | 0.00403 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000509 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.multihead_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000503 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.0.multihead_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000509 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.multihead_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000503 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.1.multihead_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000509 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.multihead_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000503 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.2.multihead_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000509 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.multihead_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000503 | 0 |
| `engine.code_generator.code_reasoning_layer.layers.3.multihead_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.0.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.0.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.1.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.1.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.2.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.2.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.3.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.3.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.4.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.4.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.language_generator.language_processor.layers.5.self_attn.out_proj.weight` | (64, 64) | engine | buckets | codebook 0 | 8 | 0.125 | 0.000517 | 0 |
| `engine.language_generator.language_processor.layers.5.self_attn.out_proj.bias` | (64,) | engine | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.self_attn.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000508 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.0.self_attn.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.self_attn.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.1249 | 0.000515 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.1.self_attn.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.self_attn.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000513 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.2.self_attn.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.self_attn.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.00051 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.3.self_attn.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.self_attn.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000518 | 0 |
| `engine.meta_reflective_head.reflection_core.reflection_layers.4.self_attn.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.self_attn.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.0.self_attn.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.self_attn.out_proj.weight` | (64, 64) | meta_reflective | buckets | codebook 0 | 8 | 0.125 | 0.000516 | 0 |
| `engine.meta_reflective_head.temporal_encoder.layers.1.self_attn.out_proj.bias` | (64,) | meta_reflective | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `bayes.beliefs['ethics.alignment']` | (3,) | bayes | buckets | codebook 0 | 8 | 1.354e+04 | 50.5 | 0 |
| `bayes.beliefs['reflection.meta_confidence']` | (3,) | bayes | buckets | codebook 0 | 8 | 1.449e+04 | 53.6 | 0 |
| `bayes.beliefs['reflection.quality']` | (3,) | bayes | buckets | codebook 0 | 8 | 1.318e+04 | 47.3 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00175 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.249 | 0.0049 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_890eaca9778456ec'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3601 | 0.00141 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_890eaca9778456ec'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_890eaca9778456ec'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['thought_processor']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.3352 | 0.00127 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8299ea8542d8aa94148abf1fb83dd67bcf5993804d86ebdcfd12786ab83cab78'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5145 | 0.00202 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8299ea8542d8aa94148abf1fb83dd67bcf5993804d86ebdcfd12786ab83cab78'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8299ea8542d8aa94148abf1fb83dd67bcf5993804d86ebdcfd12786ab83cab78'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['890eaca9778456ec4f1c426acf313d30d2e0e284d828c8aeaef52cde1b0c00df'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5145 | 0.00202 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['890eaca9778456ec4f1c426acf313d30d2e0e284d828c8aeaef52cde1b0c00df'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['890eaca9778456ec4f1c426acf313d30d2e0e284d828c8aeaef52cde1b0c00df'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['98b97f7945d4f8a4a649d3af78c3726752b66809038a6dd18ebad5607181f77f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['98b97f7945d4f8a4a649d3af78c3726752b66809038a6dd18ebad5607181f77f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['98b97f7945d4f8a4a649d3af78c3726752b66809038a6dd18ebad5607181f77f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ae4b616453c78a8258c5fefc2340c147184ff08b7fcca8b733a130db9bb3258'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3746 | 0.00147 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ae4b616453c78a8258c5fefc2340c147184ff08b7fcca8b733a130db9bb3258'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ae4b616453c78a8258c5fefc2340c147184ff08b7fcca8b733a130db9bb3258'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['fa9dfb35-8bf5-46b3-b945-a30009ecdbd2']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5263 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00112 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01293 | 4.91e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ae00e9965f28562d949181de28a4513abe26808e355fc0d474fd1ef1731ee87'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3563 | 0.0014 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ae00e9965f28562d949181de28a4513abe26808e355fc0d474fd1ef1731ee87'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ae00e9965f28562d949181de28a4513abe26808e355fc0d474fd1ef1731ee87'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['66352546-2e62-4dc9-ac8f-95bbfba811e3']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5282 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00145 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7559612c598baccd'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2667 | 0.00105 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7559612c598baccd'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7559612c598baccd'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01283 | 5.03e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['abaee781583194ad89ea63c4aa6050f7921f737000a4a5179c546d688c76a376'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.375 | 0.00147 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['abaee781583194ad89ea63c4aa6050f7921f737000a4a5179c546d688c76a376'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['abaee781583194ad89ea63c4aa6050f7921f737000a4a5179c546d688c76a376'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7559612c598baccda728b031c3cc074ae1f9a840a98a243413a6530ffbad76ef'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.381 | 0.00149 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7559612c598baccda728b031c3cc074ae1f9a840a98a243413a6530ffbad76ef'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7559612c598baccda728b031c3cc074ae1f9a840a98a243413a6530ffbad76ef'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f196cf41928711459e4694a33a6d54d3d6242dda33958d32137c8137d8db4a92'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.433 | 0.0017 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f196cf41928711459e4694a33a6d54d3d6242dda33958d32137c8137d8db4a92'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f196cf41928711459e4694a33a6d54d3d6242dda33958d32137c8137d8db4a92'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['21b52de2-bd6a-4cad-bf48-b91d2d97d7ba']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00148 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.78e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52839738b327de55f894d80c729fb6063ac76314eeab37384a1c9b3a1c8261fe'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3721 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52839738b327de55f894d80c729fb6063ac76314eeab37384a1c9b3a1c8261fe'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52839738b327de55f894d80c729fb6063ac76314eeab37384a1c9b3a1c8261fe'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['310420391e99f7c95dd26a7a9a14641df648a72cbd2f334aeeebaa699c81bc8a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4201 | 0.00165 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['310420391e99f7c95dd26a7a9a14641df648a72cbd2f334aeeebaa699c81bc8a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['310420391e99f7c95dd26a7a9a14641df648a72cbd2f334aeeebaa699c81bc8a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['333f47f82e6933966d8440a380554f2ebd7c7b9622388102a1097fdd4f192ab2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.373 | 0.00539 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['333f47f82e6933966d8440a380554f2ebd7c7b9622388102a1097fdd4f192ab2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['333f47f82e6933966d8440a380554f2ebd7c7b9622388102a1097fdd4f192ab2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['892d52dc30f75e3c95831ed26bc559cf51cb56b28e623df5ee0bac61cb048775'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.359 | 0.00533 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['892d52dc30f75e3c95831ed26bc559cf51cb56b28e623df5ee0bac61cb048775'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['892d52dc30f75e3c95831ed26bc559cf51cb56b28e623df5ee0bac61cb048775'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['33a6a5e5-4f67-4344-96f6-be0fa87ace07']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5279 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00132 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_37c6bde13f892c48'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2625 | 0.00103 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_37c6bde13f892c48'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_37c6bde13f892c48'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['thought_processor']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.4463 | 0.00173 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.63e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['51a06f415244367f92cc90a697c092cc9b78ac9349351b6a9fb75e9a2ef4cc19'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.465 | 0.00182 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['51a06f415244367f92cc90a697c092cc9b78ac9349351b6a9fb75e9a2ef4cc19'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['51a06f415244367f92cc90a697c092cc9b78ac9349351b6a9fb75e9a2ef4cc19'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['37c6bde13f892c48f914fcd9b5c32acd2c11b6a98a04e7da8fc02860a85b361e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.375 | 0.00147 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['37c6bde13f892c48f914fcd9b5c32acd2c11b6a98a04e7da8fc02860a85b361e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['37c6bde13f892c48f914fcd9b5c32acd2c11b6a98a04e7da8fc02860a85b361e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fc9353efb2e5d32397426a5c9d65abe01a1c98190af8e5b4b49b538d7ee009f1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fc9353efb2e5d32397426a5c9d65abe01a1c98190af8e5b4b49b538d7ee009f1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fc9353efb2e5d32397426a5c9d65abe01a1c98190af8e5b4b49b538d7ee009f1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['7c699c3d-fdef-48bf-a8df-59a8137c06b4']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5284 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00122 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7a7793c54d1d5d91'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5009 | 0.00196 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7a7793c54d1d5d91'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7a7793c54d1d5d91'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_1']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01293 | 5e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.73e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b0a9826b8e486a3fbe351d69c525a6677f755cc47d49013e2b8a851de46e085'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.699 | 0.00274 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b0a9826b8e486a3fbe351d69c525a6677f755cc47d49013e2b8a851de46e085'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b0a9826b8e486a3fbe351d69c525a6677f755cc47d49013e2b8a851de46e085'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7a7793c54d1d5d9165ba3ee7c95b275e4b5e8a3addca703e6cd47bf0be38b883'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7155 | 0.00281 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7a7793c54d1d5d9165ba3ee7c95b275e4b5e8a3addca703e6cd47bf0be38b883'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7a7793c54d1d5d9165ba3ee7c95b275e4b5e8a3addca703e6cd47bf0be38b883'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c2e465d846470bc421d82231f67267493abfcbc0ef2c967ff6466db6c00efed9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6767 | 0.00265 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c2e465d846470bc421d82231f67267493abfcbc0ef2c967ff6466db6c00efed9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c2e465d846470bc421d82231f67267493abfcbc0ef2c967ff6466db6c00efed9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['6740749c-5025-4d18-954c-9e588284d859']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00133 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_96db99161c5748fb'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2646 | 0.00104 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_96db99161c5748fb'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_96db99161c5748fb'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_2']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01283 | 3.72e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.79e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f774f4dcd5305724c65eee6d53637325baa67e581cd825c717c356278d078121'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f774f4dcd5305724c65eee6d53637325baa67e581cd825c717c356278d078121'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f774f4dcd5305724c65eee6d53637325baa67e581cd825c717c356278d078121'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['96db99161c5748fbf17d5828355323a2ce9e382ec6366dfee0f432e9be5ac567'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['96db99161c5748fbf17d5828355323a2ce9e382ec6366dfee0f432e9be5ac567'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['96db99161c5748fbf17d5828355323a2ce9e382ec6366dfee0f432e9be5ac567'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f3f0b8d65717b9f88dca7f70423f8d4bbd6439c98325f793df4f0d566ba3b9d9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f3f0b8d65717b9f88dca7f70423f8d4bbd6439c98325f793df4f0d566ba3b9d9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f3f0b8d65717b9f88dca7f70423f8d4bbd6439c98325f793df4f0d566ba3b9d9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff373c251cab92f109f9a1b7616175ef84b9d3a784c69505c2fe087f3ba588ed'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.61 | 0.00239 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff373c251cab92f109f9a1b7616175ef84b9d3a784c69505c2fe087f3ba588ed'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff373c251cab92f109f9a1b7616175ef84b9d3a784c69505c2fe087f3ba588ed'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5c6081dfa4211a419db6c7c6347d503823fd5e9c7e21fb2befc623c5aba18dd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5208 | 0.00204 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5c6081dfa4211a419db6c7c6347d503823fd5e9c7e21fb2befc623c5aba18dd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5c6081dfa4211a419db6c7c6347d503823fd5e9c7e21fb2befc623c5aba18dd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9657044a9865f7e1124d4b5a3dfbb8c99b69501ff60f093a3f6cac09f1ab84f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9657044a9865f7e1124d4b5a3dfbb8c99b69501ff60f093a3f6cac09f1ab84f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9657044a9865f7e1124d4b5a3dfbb8c99b69501ff60f093a3f6cac09f1ab84f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0dc7ab051d93859b51ac933970a1a62659e6eae1bb9f8b44840846b77d722d06'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.594 | 0.00625 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0dc7ab051d93859b51ac933970a1a62659e6eae1bb9f8b44840846b77d722d06'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0dc7ab051d93859b51ac933970a1a62659e6eae1bb9f8b44840846b77d722d06'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3035a8cf9ba6b90ccfbdf6b21350c63f176e347a7e88e50b36a3280628fc8b28'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.646 | 0.00663 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3035a8cf9ba6b90ccfbdf6b21350c63f176e347a7e88e50b36a3280628fc8b28'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3035a8cf9ba6b90ccfbdf6b21350c63f176e347a7e88e50b36a3280628fc8b28'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['cc69499e-7f4e-486f-bdf8-ea0a138d5bf9']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5289 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00138 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fb276bc5723c6679'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4636 | 0.00182 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fb276bc5723c6679'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fb276bc5723c6679'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_3']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.96e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.77e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['69bafe9740ac746bcfb015ffbe9824be70d446b9d67eac79161813793b9ed214'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6402 | 0.00251 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['69bafe9740ac746bcfb015ffbe9824be70d446b9d67eac79161813793b9ed214'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['69bafe9740ac746bcfb015ffbe9824be70d446b9d67eac79161813793b9ed214'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fb276bc5723c6679fc9f6ffe5a7bd4b4feebb2cdeef06ae5e579a9ec5cbe48de'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6623 | 0.0026 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fb276bc5723c6679fc9f6ffe5a7bd4b4feebb2cdeef06ae5e579a9ec5cbe48de'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fb276bc5723c6679fc9f6ffe5a7bd4b4feebb2cdeef06ae5e579a9ec5cbe48de'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7e5c6ceb082caf7fcd90dd71b0b16133b79b3df129f8523a70ec1f088932447c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4975 | 0.00195 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7e5c6ceb082caf7fcd90dd71b0b16133b79b3df129f8523a70ec1f088932447c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7e5c6ceb082caf7fcd90dd71b0b16133b79b3df129f8523a70ec1f088932447c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2478ee0b-b454-435c-86f5-95584701d96c']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5269 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00159 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.0049 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_4']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 3.49e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 5.06e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8ac115b8a22ed29f31e0cee8c3b2802c639b3eac0538c61a436641b0cb542ad6'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6155 | 0.00241 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8ac115b8a22ed29f31e0cee8c3b2802c639b3eac0538c61a436641b0cb542ad6'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8ac115b8a22ed29f31e0cee8c3b2802c639b3eac0538c61a436641b0cb542ad6'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0bc503d262b67c9106c26adffb500379037771075e8b46f4d70796465e83d273'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6682 | 0.00262 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0bc503d262b67c9106c26adffb500379037771075e8b46f4d70796465e83d273'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0bc503d262b67c9106c26adffb500379037771075e8b46f4d70796465e83d273'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['52435a91-3856-4a93-90e7-119962189f44']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5288 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00147 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_986b3cde3069463f'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4818 | 0.00189 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_986b3cde3069463f'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_986b3cde3069463f'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_5']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.37e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 5.04e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ea33a79cb8f0b929fde55b0429156a2ac51209e249920532314e5141a76da7cd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7071 | 0.00277 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ea33a79cb8f0b929fde55b0429156a2ac51209e249920532314e5141a76da7cd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ea33a79cb8f0b929fde55b0429156a2ac51209e249920532314e5141a76da7cd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['986b3cde3069463ffab9caf5e6ad79153ab66adb6bf6b6fe9ae09c0201efe3c3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6882 | 0.0027 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['986b3cde3069463ffab9caf5e6ad79153ab66adb6bf6b6fe9ae09c0201efe3c3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['986b3cde3069463ffab9caf5e6ad79153ab66adb6bf6b6fe9ae09c0201efe3c3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f1d624db0a9049384a497515ed1e83fa75bca3ad4b02c36b2d1d9ec111bb8245'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7071 | 0.00277 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f1d624db0a9049384a497515ed1e83fa75bca3ad4b02c36b2d1d9ec111bb8245'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f1d624db0a9049384a497515ed1e83fa75bca3ad4b02c36b2d1d9ec111bb8245'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['383653a6-4775-4e3b-8a8f-4b5509a12626']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0014 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_6']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 2.29e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.78e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['098bba8ae657887129d14d9c3de67c525dc06cbb11e9b211184f79271355f626'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5361 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['098bba8ae657887129d14d9c3de67c525dc06cbb11e9b211184f79271355f626'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['098bba8ae657887129d14d9c3de67c525dc06cbb11e9b211184f79271355f626'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e1bb81c4c98fda4fbc7b99c36ea0177b11fabab8b81858e17d76ef3d6d88f7ec'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4815 | 0.00189 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e1bb81c4c98fda4fbc7b99c36ea0177b11fabab8b81858e17d76ef3d6d88f7ec'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e1bb81c4c98fda4fbc7b99c36ea0177b11fabab8b81858e17d76ef3d6d88f7ec'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['14d6844a0b3c4ee34f1622270ecd8f977047aadbe25fed0ebca7de81c3c3190a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.418 | 0.00556 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['14d6844a0b3c4ee34f1622270ecd8f977047aadbe25fed0ebca7de81c3c3190a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['14d6844a0b3c4ee34f1622270ecd8f977047aadbe25fed0ebca7de81c3c3190a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['285d1e7db9e14f25389b15bfbc0fc5f596f2a78e6bb5ade5a9ee4dcca9386d08'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.379 | 0.00557 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['285d1e7db9e14f25389b15bfbc0fc5f596f2a78e6bb5ade5a9ee4dcca9386d08'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['285d1e7db9e14f25389b15bfbc0fc5f596f2a78e6bb5ade5a9ee4dcca9386d08'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bc1808d6212568e9f44751ee2ce41e9b98df6fddfa0967b2653e87761eb0861f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.345 | 0.00528 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bc1808d6212568e9f44751ee2ce41e9b98df6fddfa0967b2653e87761eb0861f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bc1808d6212568e9f44751ee2ce41e9b98df6fddfa0967b2653e87761eb0861f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['93f23447-19a2-4561-9ccb-5dcdf4fd4199']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00138 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_7']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.12e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.73e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['376a77406f8993a77659799089b0f62b143767a41aaa0bfe0620b09c7e074c7c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.647 | 0.00254 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['376a77406f8993a77659799089b0f62b143767a41aaa0bfe0620b09c7e074c7c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['376a77406f8993a77659799089b0f62b143767a41aaa0bfe0620b09c7e074c7c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f9096a3c03a767f19ecb2baefb6baa811845f478710df169837d5db1f87ed92d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6155 | 0.00241 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f9096a3c03a767f19ecb2baefb6baa811845f478710df169837d5db1f87ed92d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f9096a3c03a767f19ecb2baefb6baa811845f478710df169837d5db1f87ed92d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2a201b48-e0c6-435d-bf7b-29b88c19505d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00122 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_8']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 3.83e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.83e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1266802f5f21e56495f5a17267685eae38ecdf1737530aa1837b262232455963'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3203 | 0.00126 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1266802f5f21e56495f5a17267685eae38ecdf1737530aa1837b262232455963'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1266802f5f21e56495f5a17267685eae38ecdf1737530aa1837b262232455963'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ef8f436acee93617e1924bb97da41defbc2af9798940dea96ce275f081e38cb3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ef8f436acee93617e1924bb97da41defbc2af9798940dea96ce275f081e38cb3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ef8f436acee93617e1924bb97da41defbc2af9798940dea96ce275f081e38cb3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['570f388c-336e-47bd-ab5e-422e1f946cb2']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5269 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00154 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_9']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 4.9e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.93e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1ec8de4ae390a3f3cc2b1babf62eb7ccd930ad11a00ebaf2d5d4a505b509e07c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5213 | 0.00204 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1ec8de4ae390a3f3cc2b1babf62eb7ccd930ad11a00ebaf2d5d4a505b509e07c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1ec8de4ae390a3f3cc2b1babf62eb7ccd930ad11a00ebaf2d5d4a505b509e07c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['540f3759afeea7b759b121c070f389c2352b9492eda45fbb0ee3b1ff2cc260cc'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4417 | 0.00173 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['540f3759afeea7b759b121c070f389c2352b9492eda45fbb0ee3b1ff2cc260cc'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['540f3759afeea7b759b121c070f389c2352b9492eda45fbb0ee3b1ff2cc260cc'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a2ac27704f8061d6acc1e106f8f279cab2fcdd7cbdad431cefae1eb73fc8d5e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5423 | 0.00213 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a2ac27704f8061d6acc1e106f8f279cab2fcdd7cbdad431cefae1eb73fc8d5e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a2ac27704f8061d6acc1e106f8f279cab2fcdd7cbdad431cefae1eb73fc8d5e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9a068d1a020d63308d50b443b7729e7e8e4f42a8ad6abfc8eebda74f393f2e95'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6019 | 0.00236 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9a068d1a020d63308d50b443b7729e7e8e4f42a8ad6abfc8eebda74f393f2e95'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9a068d1a020d63308d50b443b7729e7e8e4f42a8ad6abfc8eebda74f393f2e95'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a81a30da2bd770127a41c79aa9749bf7c7f0f4a707c21f10ff476269ebb01bdb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5669 | 0.00222 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a81a30da2bd770127a41c79aa9749bf7c7f0f4a707c21f10ff476269ebb01bdb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a81a30da2bd770127a41c79aa9749bf7c7f0f4a707c21f10ff476269ebb01bdb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['58b1c7c51eb7fab63cae27006ad9f01bcc410c44aa6dd1c9674ac960d69f809c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.606 | 0.0063 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['58b1c7c51eb7fab63cae27006ad9f01bcc410c44aa6dd1c9674ac960d69f809c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['58b1c7c51eb7fab63cae27006ad9f01bcc410c44aa6dd1c9674ac960d69f809c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e38c7bace0d6717acefbcd4bb8ac7c7844074f374cbb382bc57a4dc9b0c2f6ef'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.595 | 0.00625 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e38c7bace0d6717acefbcd4bb8ac7c7844074f374cbb382bc57a4dc9b0c2f6ef'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e38c7bace0d6717acefbcd4bb8ac7c7844074f374cbb382bc57a4dc9b0c2f6ef'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['3de44d2c-2ed9-444d-9989-9f374a902c2e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5271 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00151 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_10']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.92e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6a3252ca14507b1d91909f68844dba0c5de7187862795c090e15d3288a0e0fbe'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4423 | 0.00173 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6a3252ca14507b1d91909f68844dba0c5de7187862795c090e15d3288a0e0fbe'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6a3252ca14507b1d91909f68844dba0c5de7187862795c090e15d3288a0e0fbe'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['85cb7652cebde0bd87fa5027119556054e6acdc1c369bd225782f24f4c647519'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4867 | 0.00191 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['85cb7652cebde0bd87fa5027119556054e6acdc1c369bd225782f24f4c647519'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['85cb7652cebde0bd87fa5027119556054e6acdc1c369bd225782f24f4c647519'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9f51417b309853862cf417ed9d34ae06636099c8212f1407ee6a7fdcc2addc9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4725 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9f51417b309853862cf417ed9d34ae06636099c8212f1407ee6a7fdcc2addc9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9f51417b309853862cf417ed9d34ae06636099c8212f1407ee6a7fdcc2addc9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['b0e3cb85-4c0b-4b95-a88a-d1984f6d4510']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5286 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5edbe23e5391716f'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2646 | 0.00104 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5edbe23e5391716f'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5edbe23e5391716f'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_11']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 3.61e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 5.03e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7565f4d1365765564d4ab491b1284001dd1a8a48aa0bdb7b789744cb04023a4d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7565f4d1365765564d4ab491b1284001dd1a8a48aa0bdb7b789744cb04023a4d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7565f4d1365765564d4ab491b1284001dd1a8a48aa0bdb7b789744cb04023a4d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5edbe23e5391716fd401b2e98ef1d8b47f4a5b2a4e8bbf12d8ea9d00f5ce01fe'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5edbe23e5391716fd401b2e98ef1d8b47f4a5b2a4e8bbf12d8ea9d00f5ce01fe'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5edbe23e5391716fd401b2e98ef1d8b47f4a5b2a4e8bbf12d8ea9d00f5ce01fe'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c4d2cff9d77345ab73abcb44710ecbe24029e2d6962d74b6e29d310ecc85a2a3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c4d2cff9d77345ab73abcb44710ecbe24029e2d6962d74b6e29d310ecc85a2a3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c4d2cff9d77345ab73abcb44710ecbe24029e2d6962d74b6e29d310ecc85a2a3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['a8668476-d07d-4e7e-a98c-7b44b494a900']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5289 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00136 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2efb8794f2dc74fa'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1871 | 0.000734 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2efb8794f2dc74fa'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2efb8794f2dc74fa'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_12']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.74e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d9daa527c097e45bf7074ef9dfbb8ee253381c36d631f6c46d90b56f1f99aff5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d9daa527c097e45bf7074ef9dfbb8ee253381c36d631f6c46d90b56f1f99aff5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d9daa527c097e45bf7074ef9dfbb8ee253381c36d631f6c46d90b56f1f99aff5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2efb8794f2dc74fa65b6052962fe961664c1bd76d7019b8987ae05fe2e247c05'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2673 | 0.00105 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2efb8794f2dc74fa65b6052962fe961664c1bd76d7019b8987ae05fe2e247c05'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2efb8794f2dc74fa65b6052962fe961664c1bd76d7019b8987ae05fe2e247c05'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['74f9dce889a981fc8facd58e81da2b0ddd8e6cce07daa0585c3b83784b97e5b1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3162 | 0.00124 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['74f9dce889a981fc8facd58e81da2b0ddd8e6cce07daa0585c3b83784b97e5b1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['74f9dce889a981fc8facd58e81da2b0ddd8e6cce07daa0585c3b83784b97e5b1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e39bcec8-8578-406e-b1e2-c5e79c8aeb0d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00132 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5df5ac010dce40e2'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4041 | 0.00158 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5df5ac010dce40e2'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5df5ac010dce40e2'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_13']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.89e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.8e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['321ae03f4905f63b88276b5ffe2935c531a316c36bb62119283ae2c4c24cf82b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5721 | 0.00224 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['321ae03f4905f63b88276b5ffe2935c531a316c36bb62119283ae2c4c24cf82b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['321ae03f4905f63b88276b5ffe2935c531a316c36bb62119283ae2c4c24cf82b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5df5ac010dce40e2d8b62bdf0044a5d0420bd7f97527c6adcae102437ba85016'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5774 | 0.00226 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5df5ac010dce40e2d8b62bdf0044a5d0420bd7f97527c6adcae102437ba85016'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5df5ac010dce40e2d8b62bdf0044a5d0420bd7f97527c6adcae102437ba85016'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d288d7ea861e8d637d99e8cd797ba4765304c3541da863dadd4313d018e3906'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6325 | 0.00248 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d288d7ea861e8d637d99e8cd797ba4765304c3541da863dadd4313d018e3906'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d288d7ea861e8d637d99e8cd797ba4765304c3541da863dadd4313d018e3906'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['7bd3984c-f178-4bd0-a7a7-3b78653500fc']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5286 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00145 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_753e6b78e68f99a3'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3742 | 0.00147 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_753e6b78e68f99a3'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_753e6b78e68f99a3'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_14']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 3.9e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.77e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e1b4702c8cf06676b9ce874ea383e679fc6c9a81ef3c67c63a38ec7d001e0c7c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e1b4702c8cf06676b9ce874ea383e679fc6c9a81ef3c67c63a38ec7d001e0c7c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e1b4702c8cf06676b9ce874ea383e679fc6c9a81ef3c67c63a38ec7d001e0c7c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['753e6b78e68f99a36f16ed821865d67dc9d0e3d338bda3823ce3df1b8d3b068e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5345 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['753e6b78e68f99a36f16ed821865d67dc9d0e3d338bda3823ce3df1b8d3b068e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['753e6b78e68f99a36f16ed821865d67dc9d0e3d338bda3823ce3df1b8d3b068e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3fc14c0d1f6f38adffe40e1b02caba00a8e66641f3b7e75d757d8992886a8d9e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5898 | 0.00231 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3fc14c0d1f6f38adffe40e1b02caba00a8e66641f3b7e75d757d8992886a8d9e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3fc14c0d1f6f38adffe40e1b02caba00a8e66641f3b7e75d757d8992886a8d9e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2b529b13-7ace-4d77-b8b7-2a767cb9896d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5284 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_15']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.93e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ad97fe7deac9e38d5405174749560da3e0ca0448e8b63ef5e73a6eaed36c7cd3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4523 | 0.00177 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ad97fe7deac9e38d5405174749560da3e0ca0448e8b63ef5e73a6eaed36c7cd3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ad97fe7deac9e38d5405174749560da3e0ca0448e8b63ef5e73a6eaed36c7cd3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['db07e0b5e096a03f2a3a65418d1b30272c381187f2310b28314fe6becc22a0e0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['db07e0b5e096a03f2a3a65418d1b30272c381187f2310b28314fe6becc22a0e0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['db07e0b5e096a03f2a3a65418d1b30272c381187f2310b28314fe6becc22a0e0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['bc728232-fb62-404e-9dd0-05870e933410']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.527 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00142 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_16']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.37e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.44e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9b54041586bc91b8af913603b199bc16723ee30c6eb6be96b6ae9276f1c0691b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9b54041586bc91b8af913603b199bc16723ee30c6eb6be96b6ae9276f1c0691b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9b54041586bc91b8af913603b199bc16723ee30c6eb6be96b6ae9276f1c0691b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['576b8e7ee2d13a21f78201264c221a91ace30d988c4cd8c6e3280a13d18cc24d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2774 | 0.00109 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['576b8e7ee2d13a21f78201264c221a91ace30d988c4cd8c6e3280a13d18cc24d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['576b8e7ee2d13a21f78201264c221a91ace30d988c4cd8c6e3280a13d18cc24d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['166e52a8f8b28d2600aab991930a3b7db00ca890247a735f43940419089799dc'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['166e52a8f8b28d2600aab991930a3b7db00ca890247a735f43940419089799dc'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['166e52a8f8b28d2600aab991930a3b7db00ca890247a735f43940419089799dc'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b19d14241104f97e5b4176af215ac53bf6d33e7a3d636ca3069196ae6b74770d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b19d14241104f97e5b4176af215ac53bf6d33e7a3d636ca3069196ae6b74770d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b19d14241104f97e5b4176af215ac53bf6d33e7a3d636ca3069196ae6b74770d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['60333379fabb803306b8d85104e0f61c5ddcf942ca669f98fd63f334a4d4b12f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2774 | 0.00109 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['60333379fabb803306b8d85104e0f61c5ddcf942ca669f98fd63f334a4d4b12f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['60333379fabb803306b8d85104e0f61c5ddcf942ca669f98fd63f334a4d4b12f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2ef278812e7ca907c4e689a95f59c3f79b3e58bc43000f6ffa3e60d068cffb82'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.601 | 0.00628 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2ef278812e7ca907c4e689a95f59c3f79b3e58bc43000f6ffa3e60d068cffb82'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2ef278812e7ca907c4e689a95f59c3f79b3e58bc43000f6ffa3e60d068cffb82'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e6dce778-0a3f-4f53-b206-481914192156']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5275 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00157 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_17']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.79e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.91e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e016cbecd2fc0e5e3837b34a5d054ac33073adc1e50573c73fb4b8a2c50390b3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5601 | 0.0022 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e016cbecd2fc0e5e3837b34a5d054ac33073adc1e50573c73fb4b8a2c50390b3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e016cbecd2fc0e5e3837b34a5d054ac33073adc1e50573c73fb4b8a2c50390b3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['39ce7cb010a47740221ebd4869e1e2214ae18f11635cb613c29346ae0839c33f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5222 | 0.00205 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['39ce7cb010a47740221ebd4869e1e2214ae18f11635cb613c29346ae0839c33f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['39ce7cb010a47740221ebd4869e1e2214ae18f11635cb613c29346ae0839c33f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eb9b1f2d1e2575252c3477c0ffbfa3b93c3df5f403aae8ce9fd00d60f47f06d6'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5298 | 0.00208 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eb9b1f2d1e2575252c3477c0ffbfa3b93c3df5f403aae8ce9fd00d60f47f06d6'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eb9b1f2d1e2575252c3477c0ffbfa3b93c3df5f403aae8ce9fd00d60f47f06d6'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['06f0dbfa-65d2-460d-9d1c-5a24cd30f43d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00153 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2e11a0abbcddb25d'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.355 | 0.00139 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2e11a0abbcddb25d'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2e11a0abbcddb25d'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_18']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.75e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.89e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['148ab544ffe3d6b87dbc58e5f5c23cb922f2db4ca20fac2eb4881fb7621c724b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5571 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['148ab544ffe3d6b87dbc58e5f5c23cb922f2db4ca20fac2eb4881fb7621c724b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['148ab544ffe3d6b87dbc58e5f5c23cb922f2db4ca20fac2eb4881fb7621c724b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2e11a0abbcddb25d723b666de5c5bb36d765885769fc98c1577daec37fecc0bf'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5071 | 0.00199 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2e11a0abbcddb25d723b666de5c5bb36d765885769fc98c1577daec37fecc0bf'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2e11a0abbcddb25d723b666de5c5bb36d765885769fc98c1577daec37fecc0bf'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c02392ef882504e78e8ef6e3f56fac827ef5ddff87e6c8f78502078d872b60b4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c02392ef882504e78e8ef6e3f56fac827ef5ddff87e6c8f78502078d872b60b4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c02392ef882504e78e8ef6e3f56fac827ef5ddff87e6c8f78502078d872b60b4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['30a79e42-ebce-4059-9a10-3bd8ecb05445']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5282 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0014 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1e5a1cd934e64def'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.35 | 0.00137 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1e5a1cd934e64def'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1e5a1cd934e64def'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_19']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 3.38e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 5.04e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fb9c24149c6bd6b60a91d409b612b89bdd30f8194c219efa94746476a4b05746'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5477 | 0.00215 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fb9c24149c6bd6b60a91d409b612b89bdd30f8194c219efa94746476a4b05746'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fb9c24149c6bd6b60a91d409b612b89bdd30f8194c219efa94746476a4b05746'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1e5a1cd934e64defb1163b85cbc27ae3266b5ff9d2c4399524dae5c9d25f3f11'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1e5a1cd934e64defb1163b85cbc27ae3266b5ff9d2c4399524dae5c9d25f3f11'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1e5a1cd934e64defb1163b85cbc27ae3266b5ff9d2c4399524dae5c9d25f3f11'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52687ff3afd51bf1272fb31966486628bf549355de2fc47873fc8c807532d4e4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52687ff3afd51bf1272fb31966486628bf549355de2fc47873fc8c807532d4e4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52687ff3afd51bf1272fb31966486628bf549355de2fc47873fc8c807532d4e4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2bbd7b08-8b79-4ea8-9a6f-49e2b69d49c1']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5264 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_aba9686ff303c6a9'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.33 | 0.00129 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_aba9686ff303c6a9'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_aba9686ff303c6a9'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_20']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.75e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.87e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fbd5dd18e5b4a32c4fd440bf03b565128150e560fb9bc43edfeaca5e0bb2a5b3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fbd5dd18e5b4a32c4fd440bf03b565128150e560fb9bc43edfeaca5e0bb2a5b3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fbd5dd18e5b4a32c4fd440bf03b565128150e560fb9bc43edfeaca5e0bb2a5b3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['aba9686ff303c6a9961b371732ff0966237bda83218e50052c15cb0a70fcdeac'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['aba9686ff303c6a9961b371732ff0966237bda83218e50052c15cb0a70fcdeac'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['aba9686ff303c6a9961b371732ff0966237bda83218e50052c15cb0a70fcdeac'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f555ae4beb16174b125e2ea6354e2368c010cc43a49dc967b01b381b79b4034d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f555ae4beb16174b125e2ea6354e2368c010cc43a49dc967b01b381b79b4034d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f555ae4beb16174b125e2ea6354e2368c010cc43a49dc967b01b381b79b4034d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['7b754c27-2e23-42a4-951e-51ef78b19273']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5273 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00156 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_21']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 5.03e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b0619eb0b72a1318c727d95f46056f38fba8cb1aa1e50bff6f8c4345f4233cab'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4264 | 0.00167 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b0619eb0b72a1318c727d95f46056f38fba8cb1aa1e50bff6f8c4345f4233cab'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b0619eb0b72a1318c727d95f46056f38fba8cb1aa1e50bff6f8c4345f4233cab'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3eba2a8318dfe2232c382065da580b8081faa387d7a63f0df446d68039bbb99f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3eba2a8318dfe2232c382065da580b8081faa387d7a63f0df446d68039bbb99f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3eba2a8318dfe2232c382065da580b8081faa387d7a63f0df446d68039bbb99f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c77f35f8-e0b3-41cf-b865-1ae7516a66c6']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5278 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00151 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_22']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.17e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.8e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2f67e092d6440b97048e2e24e0f2fe489348d8833210f2f95cba311311bc79b3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2f67e092d6440b97048e2e24e0f2fe489348d8833210f2f95cba311311bc79b3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2f67e092d6440b97048e2e24e0f2fe489348d8833210f2f95cba311311bc79b3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5525c67a4534ae08c50fbcd370d4d9237318a4dfb2970aa0c8babc796bf126e8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5345 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5525c67a4534ae08c50fbcd370d4d9237318a4dfb2970aa0c8babc796bf126e8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5525c67a4534ae08c50fbcd370d4d9237318a4dfb2970aa0c8babc796bf126e8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['ae730ed0-143f-4230-82b1-df8e4a443e40']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.527 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00142 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_de81d044d859a82b'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2746 | 0.00108 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_de81d044d859a82b'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_de81d044d859a82b'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_23']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 3.01e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.76e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e7489060f2a16a0700d81e1889dd8b361cd7ec15f67ce6a819a42362944fd2fb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e7489060f2a16a0700d81e1889dd8b361cd7ec15f67ce6a819a42362944fd2fb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e7489060f2a16a0700d81e1889dd8b361cd7ec15f67ce6a819a42362944fd2fb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['de81d044d859a82b56a003f2604a41c4046cefde34a5966bb92a75052bffb58a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['de81d044d859a82b56a003f2604a41c4046cefde34a5966bb92a75052bffb58a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['de81d044d859a82b56a003f2604a41c4046cefde34a5966bb92a75052bffb58a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe4cc8dd149da04651156f4335a46707562928813c5ef0d6a9fc05a263928cf8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe4cc8dd149da04651156f4335a46707562928813c5ef0d6a9fc05a263928cf8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe4cc8dd149da04651156f4335a46707562928813c5ef0d6a9fc05a263928cf8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['913b3fc91fec3ded0808c2ec09bee1d431891344c527d6e18556aad557e609bb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4685 | 0.00184 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['913b3fc91fec3ded0808c2ec09bee1d431891344c527d6e18556aad557e609bb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['913b3fc91fec3ded0808c2ec09bee1d431891344c527d6e18556aad557e609bb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['75053766b1de92f36d147e3fab5640c7f047aab791e3cf697f5038018be57075'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3721 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['75053766b1de92f36d147e3fab5640c7f047aab791e3cf697f5038018be57075'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['75053766b1de92f36d147e3fab5640c7f047aab791e3cf697f5038018be57075'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['33b6951daccd62f7ede003a5a8451ed112b265ee70c1021a326fd9c2108c57ae'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4193 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['33b6951daccd62f7ede003a5a8451ed112b265ee70c1021a326fd9c2108c57ae'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['33b6951daccd62f7ede003a5a8451ed112b265ee70c1021a326fd9c2108c57ae'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['aff432477e1d9456368052d3ca3232b98e9f85858457c0aaa62803b81f0035b4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.599 | 0.00627 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['aff432477e1d9456368052d3ca3232b98e9f85858457c0aaa62803b81f0035b4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['aff432477e1d9456368052d3ca3232b98e9f85858457c0aaa62803b81f0035b4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['59a3775f-5734-4e30-8125-1d879e3ec1b0']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5277 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00145 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_393be22b9048de8f'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_393be22b9048de8f'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_393be22b9048de8f'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_24']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 3.71e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.75e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cbe0b552b226a8bc9b080719c45c583ade6b8c3007a0a351a35ac119f82b7e30'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5208 | 0.00204 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cbe0b552b226a8bc9b080719c45c583ade6b8c3007a0a351a35ac119f82b7e30'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cbe0b552b226a8bc9b080719c45c583ade6b8c3007a0a351a35ac119f82b7e30'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['393be22b9048de8f42cc06001fd46a3d47266e7e315e8b5b02842d0adf4db0f2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5714 | 0.00224 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['393be22b9048de8f42cc06001fd46a3d47266e7e315e8b5b02842d0adf4db0f2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['393be22b9048de8f42cc06001fd46a3d47266e7e315e8b5b02842d0adf4db0f2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['88e6607254c04d88481894bfbf27162f94dfdba6a2d77fe8ec97b0b4692e2ac7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4417 | 0.00173 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['88e6607254c04d88481894bfbf27162f94dfdba6a2d77fe8ec97b0b4692e2ac7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['88e6607254c04d88481894bfbf27162f94dfdba6a2d77fe8ec97b0b4692e2ac7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['17123320-fd7f-4f2b-8c45-18fc48e1d53e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00137 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_25']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 3.57e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 5.03e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d40e726e77162913050546f7249730166bdbc506b75559731999b8e379803b04'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5183 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d40e726e77162913050546f7249730166bdbc506b75559731999b8e379803b04'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d40e726e77162913050546f7249730166bdbc506b75559731999b8e379803b04'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['78a5693d-e667-4088-ae5d-472e4f1e4af4']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5286 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00117 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_654cbeadb565d638'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2132 | 0.000836 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_654cbeadb565d638'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_654cbeadb565d638'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_26']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.39e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 5.01e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['64d629e3cea28a962409cead0573bd05b6bb12853e7e3df7fc3191843fdb52d0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.318 | 0.00125 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['64d629e3cea28a962409cead0573bd05b6bb12853e7e3df7fc3191843fdb52d0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['64d629e3cea28a962409cead0573bd05b6bb12853e7e3df7fc3191843fdb52d0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['654cbeadb565d638e295db0e54501e46047fb751a83f8879f882709e9de36877'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3046 | 0.00119 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['654cbeadb565d638e295db0e54501e46047fb751a83f8879f882709e9de36877'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['654cbeadb565d638e295db0e54501e46047fb751a83f8879f882709e9de36877'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['23177287f1b9021f577333af79b270a634caa7998ac98d8b69f763e844bfa655'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3419 | 0.00134 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['23177287f1b9021f577333af79b270a634caa7998ac98d8b69f763e844bfa655'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['23177287f1b9021f577333af79b270a634caa7998ac98d8b69f763e844bfa655'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1f6ef4d5-6253-4d3d-8a3b-45800446a212']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5278 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00147 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_27']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.13e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.94e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['325dd79ebbe8a4026c0a77a13313df71d42c34a4f0e6e0c4232447924e5c0cce'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7213 | 0.00283 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['325dd79ebbe8a4026c0a77a13313df71d42c34a4f0e6e0c4232447924e5c0cce'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['325dd79ebbe8a4026c0a77a13313df71d42c34a4f0e6e0c4232447924e5c0cce'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['84b1cc105ffa0ee8434a69cc0eecd663a9b7481d942cd4076b69b4b3a1deb27c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7338 | 0.00288 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['84b1cc105ffa0ee8434a69cc0eecd663a9b7481d942cd4076b69b4b3a1deb27c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['84b1cc105ffa0ee8434a69cc0eecd663a9b7481d942cd4076b69b4b3a1deb27c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['9201e48c-8c48-4694-a277-04408c4ac418']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5292 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00161 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.25 | 0.0049 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_42f6c30d30f30a98'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2919 | 0.00114 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_42f6c30d30f30a98'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_42f6c30d30f30a98'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_28']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 3.31e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.61e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7dc28c3c9a2feeaa9fb8fe5e2cf1a2174770b075cf0e6c30513c9e89b7bc2767'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7dc28c3c9a2feeaa9fb8fe5e2cf1a2174770b075cf0e6c30513c9e89b7bc2767'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7dc28c3c9a2feeaa9fb8fe5e2cf1a2174770b075cf0e6c30513c9e89b7bc2767'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42f6c30d30f30a98cd282c66c9f10a6e96cf6ae1570746066e1cfb3174d664d6'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.417 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42f6c30d30f30a98cd282c66c9f10a6e96cf6ae1570746066e1cfb3174d664d6'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42f6c30d30f30a98cd282c66c9f10a6e96cf6ae1570746066e1cfb3174d664d6'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0b33b5cddda8953397ca9d7f9e236d5bed0e9f08a741c521273bfab34cd647b8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3333 | 0.00131 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0b33b5cddda8953397ca9d7f9e236d5bed0e9f08a741c521273bfab34cd647b8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0b33b5cddda8953397ca9d7f9e236d5bed0e9f08a741c521273bfab34cd647b8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['9d0d9085-4b5f-43d3-852d-1b4f3acc7767']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_29']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 2.83e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9ecc174149cf850110f3dab9aa7e2fbf2ef5ce38afbf3356c716966820ae9f2a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6156 | 0.00241 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9ecc174149cf850110f3dab9aa7e2fbf2ef5ce38afbf3356c716966820ae9f2a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9ecc174149cf850110f3dab9aa7e2fbf2ef5ce38afbf3356c716966820ae9f2a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['5d448d98-8873-464b-a7b6-98d2d68cf1fa']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5287 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00142 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_30']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 3.62e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.89e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff978231850a1f7941f32ae849dd5b6bae8027afd4b4818471ba66b1010129cd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.562 | 0.0022 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff978231850a1f7941f32ae849dd5b6bae8027afd4b4818471ba66b1010129cd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff978231850a1f7941f32ae849dd5b6bae8027afd4b4818471ba66b1010129cd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['592c0d5f0217c9e19a8a4783a99b136fa2736c3ec8058242865ed38989cfc748'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5051 | 0.00198 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['592c0d5f0217c9e19a8a4783a99b136fa2736c3ec8058242865ed38989cfc748'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['592c0d5f0217c9e19a8a4783a99b136fa2736c3ec8058242865ed38989cfc748'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0672565367f360b87280b06395b1c20a8a28cc9d0f9dbad03289a4b635e3fef3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5241 | 0.00206 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0672565367f360b87280b06395b1c20a8a28cc9d0f9dbad03289a4b635e3fef3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0672565367f360b87280b06395b1c20a8a28cc9d0f9dbad03289a4b635e3fef3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['13a10c0e86d076a6e8a3fa044d93c2b0357e5c3f9d2914050ceed058dd1f75ec'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6838 | 0.00268 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['13a10c0e86d076a6e8a3fa044d93c2b0357e5c3f9d2914050ceed058dd1f75ec'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['13a10c0e86d076a6e8a3fa044d93c2b0357e5c3f9d2914050ceed058dd1f75ec'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1380c1aec4d70bbe061b7009828b332226785da3b5d91d0fe4f8af90e2309a7a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4045 | 0.00159 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1380c1aec4d70bbe061b7009828b332226785da3b5d91d0fe4f8af90e2309a7a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1380c1aec4d70bbe061b7009828b332226785da3b5d91d0fe4f8af90e2309a7a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3666fb4d98ed252ddcdfbf69b5e99bd7d2b2e5824e3c2d11e4fbeeb0d9fab9e7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 1.6 | 0.00627 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3666fb4d98ed252ddcdfbf69b5e99bd7d2b2e5824e3c2d11e4fbeeb0d9fab9e7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3666fb4d98ed252ddcdfbf69b5e99bd7d2b2e5824e3c2d11e4fbeeb0d9fab9e7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['9f1f8fce-65de-4084-b2e6-edd9deede5da']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5284 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00142 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_34fc2e4d1fb740ce'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4925 | 0.00193 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_34fc2e4d1fb740ce'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_34fc2e4d1fb740ce'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_31']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.89e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['deea1a6cba56f85c7f47a36aab476c841b29d2f15f4ded0a9b6d5cdc07512992'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7107 | 0.00279 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['deea1a6cba56f85c7f47a36aab476c841b29d2f15f4ded0a9b6d5cdc07512992'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['deea1a6cba56f85c7f47a36aab476c841b29d2f15f4ded0a9b6d5cdc07512992'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['34fc2e4d1fb740cef7e4c097021f3ccc9a86416702fd6abb5a5486a1f69670ce'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7035 | 0.00276 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['34fc2e4d1fb740cef7e4c097021f3ccc9a86416702fd6abb5a5486a1f69670ce'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['34fc2e4d1fb740cef7e4c097021f3ccc9a86416702fd6abb5a5486a1f69670ce'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c365e6216864cdd86b2ea179d3b8a4f4af29e10d693004ac9a96e56b3a02cd8d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3665 | 0.00144 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c365e6216864cdd86b2ea179d3b8a4f4af29e10d693004ac9a96e56b3a02cd8d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c365e6216864cdd86b2ea179d3b8a4f4af29e10d693004ac9a96e56b3a02cd8d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['bd03f86c-737d-4b86-ac13-06864e400b48']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5293 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fe47d5d70d61faed'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3963 | 0.00155 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fe47d5d70d61faed'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fe47d5d70d61faed'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_32']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.59e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b1fa7fcf0152e48674f5e627e2378721729e9370809a10c5b88ba9450cdf1fe9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5661 | 0.00222 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b1fa7fcf0152e48674f5e627e2378721729e9370809a10c5b88ba9450cdf1fe9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b1fa7fcf0152e48674f5e627e2378721729e9370809a10c5b88ba9450cdf1fe9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['970f940be18b09ea10b72dc46526a8a1c7f3b858060300c5167f1a79762e7b4c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5934 | 0.00233 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['970f940be18b09ea10b72dc46526a8a1c7f3b858060300c5167f1a79762e7b4c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['970f940be18b09ea10b72dc46526a8a1c7f3b858060300c5167f1a79762e7b4c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe47d5d70d61faed893c5824192ed7761d1f98a4929f4c425a65085943b2b371'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5661 | 0.00222 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe47d5d70d61faed893c5824192ed7761d1f98a4929f4c425a65085943b2b371'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe47d5d70d61faed893c5824192ed7761d1f98a4929f4c425a65085943b2b371'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1fe78c56-9361-49bd-be08-05bf9d553dc6']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5289 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00119 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6758f61f4558b113'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1627 | 0.000638 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6758f61f4558b113'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6758f61f4558b113'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_33']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 3.79e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.76e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['93c44272b3efca757efb336de589d750651729069ff14d23466a2edc8a5caaff'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2182 | 0.000856 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['93c44272b3efca757efb336de589d750651729069ff14d23466a2edc8a5caaff'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['93c44272b3efca757efb336de589d750651729069ff14d23466a2edc8a5caaff'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6758f61f4558b113c9c6d12b676fba2d220edf7f8db7e0e8c9c706d299656e3d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2325 | 0.000912 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6758f61f4558b113c9c6d12b676fba2d220edf7f8db7e0e8c9c706d299656e3d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6758f61f4558b113c9c6d12b676fba2d220edf7f8db7e0e8c9c706d299656e3d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fde164f810de5718bfdd6876266650e6244a3a5c93166a24d9d5b9581b503671'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.239 | 0.000937 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fde164f810de5718bfdd6876266650e6244a3a5c93166a24d9d5b9581b503671'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fde164f810de5718bfdd6876266650e6244a3a5c93166a24d9d5b9581b503671'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['80438d36-6de0-449a-bbef-78508e9776b7']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5291 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6bceb5cac87f85b0'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1528 | 0.000599 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6bceb5cac87f85b0'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6bceb5cac87f85b0'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_34']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.24e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.97e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1c67e83055f52c62d774fcb0194e81b42de3b5bedcadae1c212da35082148edd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1c67e83055f52c62d774fcb0194e81b42de3b5bedcadae1c212da35082148edd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1c67e83055f52c62d774fcb0194e81b42de3b5bedcadae1c212da35082148edd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6bceb5cac87f85b056c4fd4ff9b21379c020935e05071bf8307aa080fac280da'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2182 | 0.000856 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6bceb5cac87f85b056c4fd4ff9b21379c020935e05071bf8307aa080fac280da'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6bceb5cac87f85b056c4fd4ff9b21379c020935e05071bf8307aa080fac280da'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['12a6787e9559157a9bc186e77ad9eb9352c7e9e11021bcd7891a94869d73b8cf'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2774 | 0.00109 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['12a6787e9559157a9bc186e77ad9eb9352c7e9e11021bcd7891a94869d73b8cf'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['12a6787e9559157a9bc186e77ad9eb9352c7e9e11021bcd7891a94869d73b8cf'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['565818c0-858e-4dee-ad3b-57443c2e06a9']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5277 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00118 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_315847063812b6b4'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1854 | 0.000727 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_315847063812b6b4'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_315847063812b6b4'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_35']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.63e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.8e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['95ee2133037d408c94164430ee9b8708adcc86e5064f779a8d9afee016eb7771'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3464 | 0.00136 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['95ee2133037d408c94164430ee9b8708adcc86e5064f779a8d9afee016eb7771'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['95ee2133037d408c94164430ee9b8708adcc86e5064f779a8d9afee016eb7771'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['315847063812b6b41315d67bc60ef203d05fe28ad024fa7b87791ad2d8b58fc1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2649 | 0.00104 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['315847063812b6b41315d67bc60ef203d05fe28ad024fa7b87791ad2d8b58fc1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['315847063812b6b41315d67bc60ef203d05fe28ad024fa7b87791ad2d8b58fc1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['f83f9418-e3f1-4d1f-9e08-b1ac898d6148']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5286 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00153 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_79d01b0673377ea5'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2646 | 0.00104 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_79d01b0673377ea5'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_79d01b0673377ea5'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_36']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.41e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.81e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['941af1e9fa24fc5c5e6d09010855838b2c635438987b719e4a9873296df11fb3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3651 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['941af1e9fa24fc5c5e6d09010855838b2c635438987b719e4a9873296df11fb3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['941af1e9fa24fc5c5e6d09010855838b2c635438987b719e4a9873296df11fb3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['79d01b0673377ea5a763a7439b65d461d83290b9604770d9a26b2e5252d8d0b5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['79d01b0673377ea5a763a7439b65d461d83290b9604770d9a26b2e5252d8d0b5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['79d01b0673377ea5a763a7439b65d461d83290b9604770d9a26b2e5252d8d0b5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4bfb4cca9938b782da3834d9ff01f4c056ec29dbcaf76fc7dd0feb9193f78bd6'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2357 | 0.000924 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4bfb4cca9938b782da3834d9ff01f4c056ec29dbcaf76fc7dd0feb9193f78bd6'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4bfb4cca9938b782da3834d9ff01f4c056ec29dbcaf76fc7dd0feb9193f78bd6'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['43cd73e4-2774-4fff-9523-ec89f2083061']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00151 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_611d0a4b3014013e'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2556 | 0.001 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_611d0a4b3014013e'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_611d0a4b3014013e'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_37']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.63e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.84e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['82f18448692b77f9119cab36276e4664a395c36cc9396e7f5d433c4bbec9f134'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['82f18448692b77f9119cab36276e4664a395c36cc9396e7f5d433c4bbec9f134'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['82f18448692b77f9119cab36276e4664a395c36cc9396e7f5d433c4bbec9f134'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['611d0a4b3014013eb5f5f517f48c5108cee9d2383e3d680030fcd8da6ce19bcb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3651 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['611d0a4b3014013eb5f5f517f48c5108cee9d2383e3d680030fcd8da6ce19bcb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['611d0a4b3014013eb5f5f517f48c5108cee9d2383e3d680030fcd8da6ce19bcb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ccd3cccfad3ddfa77ce65b6baf1b84b0b3558fac95fba21c6247334f6cd15a34'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ccd3cccfad3ddfa77ce65b6baf1b84b0b3558fac95fba21c6247334f6cd15a34'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ccd3cccfad3ddfa77ce65b6baf1b84b0b3558fac95fba21c6247334f6cd15a34'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e3f97681e175d14217fa1ab0ef25d96098dfdb0807ca23206533115102db95ed'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5361 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e3f97681e175d14217fa1ab0ef25d96098dfdb0807ca23206533115102db95ed'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e3f97681e175d14217fa1ab0ef25d96098dfdb0807ca23206533115102db95ed'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bbcd476d1d87b957b7ad76215cd9b237dc0dae48d934074adae14f08e0692f3d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bbcd476d1d87b957b7ad76215cd9b237dc0dae48d934074adae14f08e0692f3d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bbcd476d1d87b957b7ad76215cd9b237dc0dae48d934074adae14f08e0692f3d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01b840cb1f3d26e78a0f3ca85ddd5bd481cb4ad051d63d9c5be28fc4ecca719d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.433 | 0.0017 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01b840cb1f3d26e78a0f3ca85ddd5bd481cb4ad051d63d9c5be28fc4ecca719d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01b840cb1f3d26e78a0f3ca85ddd5bd481cb4ad051d63d9c5be28fc4ecca719d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['8a486690-7769-4d53-8dbb-ec5cf61eb051']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5288 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00124 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_61a83fffc2bc41fa'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3466 | 0.00136 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_61a83fffc2bc41fa'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_61a83fffc2bc41fa'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_38']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.33e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 5.16e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9afaca57978399233066bd43c38a3967fed840bae57cd4c7f5c7d5185526b53f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4856 | 0.0019 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9afaca57978399233066bd43c38a3967fed840bae57cd4c7f5c7d5185526b53f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9afaca57978399233066bd43c38a3967fed840bae57cd4c7f5c7d5185526b53f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['61a83fffc2bc41faf85eb513802eb32fa2a67b28d1ede3dccfce54599b3819a9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4951 | 0.00194 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['61a83fffc2bc41faf85eb513802eb32fa2a67b28d1ede3dccfce54599b3819a9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['61a83fffc2bc41faf85eb513802eb32fa2a67b28d1ede3dccfce54599b3819a9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e63c6cec8c73a944bca4bea2304f2b05b6e46e032492dff6c4f61cf4a6faf28b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5103 | 0.002 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e63c6cec8c73a944bca4bea2304f2b05b6e46e032492dff6c4f61cf4a6faf28b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e63c6cec8c73a944bca4bea2304f2b05b6e46e032492dff6c4f61cf4a6faf28b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d96901a7897b74a26eb0353ba20af405da15051c71ef7ae01d7f85f04d387ac0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2747 | 0.00108 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d96901a7897b74a26eb0353ba20af405da15051c71ef7ae01d7f85f04d387ac0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d96901a7897b74a26eb0353ba20af405da15051c71ef7ae01d7f85f04d387ac0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['95ad526e-ed99-442b-83f5-db7ea1cc4138']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5286 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00151 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_687efa352acbe27e'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.28 | 0.0011 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_687efa352acbe27e'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_687efa352acbe27e'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_39']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5efcd5a765a8ee9e1c68d97e0609c53a10c069b0390b3c3ddbce62968ed35f0b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3849 | 0.00151 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5efcd5a765a8ee9e1c68d97e0609c53a10c069b0390b3c3ddbce62968ed35f0b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5efcd5a765a8ee9e1c68d97e0609c53a10c069b0390b3c3ddbce62968ed35f0b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['687efa352acbe27e005b15fdb955323aebc6bff0e14621f3875d15bab81c20fa'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['687efa352acbe27e005b15fdb955323aebc6bff0e14621f3875d15bab81c20fa'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['687efa352acbe27e005b15fdb955323aebc6bff0e14621f3875d15bab81c20fa'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fc97bf7e6e0da81d82842743d65531b3eab92f884780cba33f1da5c895c54027'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5547 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fc97bf7e6e0da81d82842743d65531b3eab92f884780cba33f1da5c895c54027'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fc97bf7e6e0da81d82842743d65531b3eab92f884780cba33f1da5c895c54027'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['3e8a6a7b-1f8b-4dc9-8517-5447768408fc']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00111 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.257 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_3e043c30df40bc59'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.28 | 0.0011 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_3e043c30df40bc59'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_3e043c30df40bc59'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_40']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.97e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.36e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2ee028c0819c4946d3df8bd4702898b006e283568676ff8f19aa9cb20a0a2d0a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2ee028c0819c4946d3df8bd4702898b006e283568676ff8f19aa9cb20a0a2d0a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2ee028c0819c4946d3df8bd4702898b006e283568676ff8f19aa9cb20a0a2d0a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3e043c30df40bc591a613e209560c7ed2df20b8253789e758d4520b00d35c42d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3e043c30df40bc591a613e209560c7ed2df20b8253789e758d4520b00d35c42d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3e043c30df40bc591a613e209560c7ed2df20b8253789e758d4520b00d35c42d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b4b30da9ef4dbc5495a485354acefc412c1264c3fa4f07c609d2a91c694ae239'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b4b30da9ef4dbc5495a485354acefc412c1264c3fa4f07c609d2a91c694ae239'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b4b30da9ef4dbc5495a485354acefc412c1264c3fa4f07c609d2a91c694ae239'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['463e5bd0-0c1a-4d58-af64-134d6091b43d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5291 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00126 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_f5e165e681b36e0a'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2689 | 0.00105 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_f5e165e681b36e0a'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_f5e165e681b36e0a'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_41']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.68e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01283 | 4.6e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ddbc2f0d734a59f288ec6268b03251bf862acd75df8ceec32e4c92ac44bd4d27'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2747 | 0.00108 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ddbc2f0d734a59f288ec6268b03251bf862acd75df8ceec32e4c92ac44bd4d27'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ddbc2f0d734a59f288ec6268b03251bf862acd75df8ceec32e4c92ac44bd4d27'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5e165e681b36e0a1ec968e0298e3cb7ea31627d2750c66f1e73888302b85a86'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3841 | 0.00151 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5e165e681b36e0a1ec968e0298e3cb7ea31627d2750c66f1e73888302b85a86'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5e165e681b36e0a1ec968e0298e3cb7ea31627d2750c66f1e73888302b85a86'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['05027f19ca5a99b893f2e97da40ee4015c63b98156bcaa06b01dbc4f974e10ed'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2857 | 0.00112 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['05027f19ca5a99b893f2e97da40ee4015c63b98156bcaa06b01dbc4f974e10ed'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['05027f19ca5a99b893f2e97da40ee4015c63b98156bcaa06b01dbc4f974e10ed'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['9e822776-b562-4a79-9f94-438504b36225']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5283 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00127 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_42']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 5.06e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.22e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6035fd505fe675848e260ce8b34fb2760896c5ef3cbe327da371191d66121b69'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4767 | 0.00187 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6035fd505fe675848e260ce8b34fb2760896c5ef3cbe327da371191d66121b69'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6035fd505fe675848e260ce8b34fb2760896c5ef3cbe327da371191d66121b69'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c7a213b3-2417-4081-97be-32e33075c21c']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0013 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1c05a68c85a8c0d7'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1764 | 0.000692 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1c05a68c85a8c0d7'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1c05a68c85a8c0d7'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_43']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.39e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.77e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['784d394e5422bceb7b9b7d3ba50082cf372cacc4bdc2477b0e525f8b8a8c7e04'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3511 | 0.00138 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['784d394e5422bceb7b9b7d3ba50082cf372cacc4bdc2477b0e525f8b8a8c7e04'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['784d394e5422bceb7b9b7d3ba50082cf372cacc4bdc2477b0e525f8b8a8c7e04'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1c05a68c85a8c0d71780d4054c060343b478180a349c4e9e23778b81eb0fc4e2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.252 | 0.000988 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1c05a68c85a8c0d71780d4054c060343b478180a349c4e9e23778b81eb0fc4e2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1c05a68c85a8c0d71780d4054c060343b478180a349c4e9e23778b81eb0fc4e2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e50beccb-5342-4814-bd4f-859424a45ba2']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00135 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_44']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ae4c0bc2118c14d124078489268bec0a2c82aa74d1c7128b2b31ef59ed5cdb89'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.424 | 0.00166 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ae4c0bc2118c14d124078489268bec0a2c82aa74d1c7128b2b31ef59ed5cdb89'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ae4c0bc2118c14d124078489268bec0a2c82aa74d1c7128b2b31ef59ed5cdb89'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bfda224364f0864321fe548da9a0aa7892fbc3ca866b25b50d136252baa9fae0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bfda224364f0864321fe548da9a0aa7892fbc3ca866b25b50d136252baa9fae0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bfda224364f0864321fe548da9a0aa7892fbc3ca866b25b50d136252baa9fae0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eec68df27a6ae961d0a8e8dd708d6caa0f3b77484c9932c7984ccf99b36baecd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5556 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eec68df27a6ae961d0a8e8dd708d6caa0f3b77484c9932c7984ccf99b36baecd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eec68df27a6ae961d0a8e8dd708d6caa0f3b77484c9932c7984ccf99b36baecd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68d7be02554a9cc0f2c651e89d1bddc045112fb869095bf75e3f59b0f4a5b173'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4743 | 0.00186 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68d7be02554a9cc0f2c651e89d1bddc045112fb869095bf75e3f59b0f4a5b173'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68d7be02554a9cc0f2c651e89d1bddc045112fb869095bf75e3f59b0f4a5b173'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['826654650b77c82f7000727aa536adbf0ada7721f50672380e344466316caca0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4009 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['826654650b77c82f7000727aa536adbf0ada7721f50672380e344466316caca0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['826654650b77c82f7000727aa536adbf0ada7721f50672380e344466316caca0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['dbb6bf93-99b0-4019-be8e-c7cd0d5ba110']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5289 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00116 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c84d8ff835aa8418'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2475 | 0.000971 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c84d8ff835aa8418'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c84d8ff835aa8418'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_45']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01283 | 4.71e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 5.02e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['da37b32c05d8dd77524d47911da85ecf0464faa3e414d9443bfb5e1288417bc5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4417 | 0.00173 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['da37b32c05d8dd77524d47911da85ecf0464faa3e414d9443bfb5e1288417bc5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['da37b32c05d8dd77524d47911da85ecf0464faa3e414d9443bfb5e1288417bc5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c84d8ff835aa84186e051d1ba650690468d8150f86bf52a6226f6e090b3c3d38'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c84d8ff835aa84186e051d1ba650690468d8150f86bf52a6226f6e090b3c3d38'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c84d8ff835aa84186e051d1ba650690468d8150f86bf52a6226f6e090b3c3d38'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2effb00489f50744b225ab098bc574ed776b83abb3aef5cfb69592bd6b78e639'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2effb00489f50744b225ab098bc574ed776b83abb3aef5cfb69592bd6b78e639'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2effb00489f50744b225ab098bc574ed776b83abb3aef5cfb69592bd6b78e639'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['71f993b87cf998745df13e18c7dba5eb740f0344c22006d0a4a506576c045539'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6565 | 0.00257 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['71f993b87cf998745df13e18c7dba5eb740f0344c22006d0a4a506576c045539'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['71f993b87cf998745df13e18c7dba5eb740f0344c22006d0a4a506576c045539'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c8cf8e98-3ebc-4c97-b0d2-39e1902d6007']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00117 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e92da839c53d2ce6'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4244 | 0.00166 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e92da839c53d2ce6'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e92da839c53d2ce6'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_46']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.71e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.71e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['db85b34a0019eaf9a5554006e62f34a40f77ef9ec6d7f13490834e1c77aa74bb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['db85b34a0019eaf9a5554006e62f34a40f77ef9ec6d7f13490834e1c77aa74bb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['db85b34a0019eaf9a5554006e62f34a40f77ef9ec6d7f13490834e1c77aa74bb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e92da839c53d2ce649a8040de0aa8073711f69aa7ce26eca8e7ad14ea9de513e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6063 | 0.00238 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e92da839c53d2ce649a8040de0aa8073711f69aa7ce26eca8e7ad14ea9de513e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e92da839c53d2ce649a8040de0aa8073711f69aa7ce26eca8e7ad14ea9de513e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['3ca7bf6a-d440-47f0-b63d-271f78504333']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5269 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00131 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_169eef45a2055209'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.371 | 0.00145 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_169eef45a2055209'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_169eef45a2055209'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_47']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.04e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f33ca1391776417c06b447931196e9615f3b3709a6178b049214413544948843'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4193 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f33ca1391776417c06b447931196e9615f3b3709a6178b049214413544948843'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f33ca1391776417c06b447931196e9615f3b3709a6178b049214413544948843'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['169eef45a2055209a9555f817cadfbbcfbcec13a980cacc5e9cc6fe4a9aed458'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.53 | 0.00208 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['169eef45a2055209a9555f817cadfbbcfbcec13a980cacc5e9cc6fe4a9aed458'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['169eef45a2055209a9555f817cadfbbcfbcec13a980cacc5e9cc6fe4a9aed458'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['975c426a5eef18e705bc857ae5656596a3f4aae1aceb4e0a2528737bc8002d23'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4558 | 0.00179 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['975c426a5eef18e705bc857ae5656596a3f4aae1aceb4e0a2528737bc8002d23'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['975c426a5eef18e705bc857ae5656596a3f4aae1aceb4e0a2528737bc8002d23'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1dd00548-4b53-4976-9d46-3cc8acaebe7a']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00117 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_b74698470b78d0c2'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3395 | 0.00133 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_b74698470b78d0c2'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_b74698470b78d0c2'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_48']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.09e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.76e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f0d64b01421445e13c71b5aba020cf40d28b66421cd93518b90dce8300793eb1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f0d64b01421445e13c71b5aba020cf40d28b66421cd93518b90dce8300793eb1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f0d64b01421445e13c71b5aba020cf40d28b66421cd93518b90dce8300793eb1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b74698470b78d0c2aa1bc4a71df7b7e4c286284a2348c2cfa1a3b0f6f23f1feb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4851 | 0.0019 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b74698470b78d0c2aa1bc4a71df7b7e4c286284a2348c2cfa1a3b0f6f23f1feb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b74698470b78d0c2aa1bc4a71df7b7e4c286284a2348c2cfa1a3b0f6f23f1feb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7bd896ffca0d11bc6d2a1973a88775f1c255efa49d997931c2589c52260fb37a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5252 | 0.00206 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7bd896ffca0d11bc6d2a1973a88775f1c255efa49d997931c2589c52260fb37a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7bd896ffca0d11bc6d2a1973a88775f1c255efa49d997931c2589c52260fb37a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1e687314-de15-4854-939a-154366425951']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5281 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_49']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.07e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f86356a7fd57506c3c53d723519995b477771dd81a77634c687c56f60604947e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f86356a7fd57506c3c53d723519995b477771dd81a77634c687c56f60604947e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f86356a7fd57506c3c53d723519995b477771dd81a77634c687c56f60604947e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5c530b348e2021c254ec1d3652e4e815807b6cf1e33c6ed6e591c8ec258dac76'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3162 | 0.00124 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5c530b348e2021c254ec1d3652e4e815807b6cf1e33c6ed6e591c8ec258dac76'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5c530b348e2021c254ec1d3652e4e815807b6cf1e33c6ed6e591c8ec258dac76'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e9989673-2f18-4f31-b75d-5f5d87b88932']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5284 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00105 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.257 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_a9b802d9d0925a3b'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2689 | 0.00105 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_a9b802d9d0925a3b'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_a9b802d9d0925a3b'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_50']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 3.43e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.13e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2b43a373f66f9a8450c6a27be0427ddceae125a0d157e1c3952d6a3a52f98fd0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3906 | 0.00153 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2b43a373f66f9a8450c6a27be0427ddceae125a0d157e1c3952d6a3a52f98fd0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2b43a373f66f9a8450c6a27be0427ddceae125a0d157e1c3952d6a3a52f98fd0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a9b802d9d0925a3bcacdf79e7f8ba6b09aff4de4d328ffcb972c0c1cc71a90f1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3841 | 0.00151 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a9b802d9d0925a3bcacdf79e7f8ba6b09aff4de4d328ffcb972c0c1cc71a90f1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a9b802d9d0925a3bcacdf79e7f8ba6b09aff4de4d328ffcb972c0c1cc71a90f1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['389f98b7-8ba1-4732-b7cf-ac70e66f3db2']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5282 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00148 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7517eb70ab1471af'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4125 | 0.00162 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7517eb70ab1471af'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7517eb70ab1471af'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_51']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.44e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01282 | 5e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42c9be4adca9b61f3f9daf652c8d798160450392b3ebab0248aeca17d8609fbf'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5893 | 0.00231 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42c9be4adca9b61f3f9daf652c8d798160450392b3ebab0248aeca17d8609fbf'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42c9be4adca9b61f3f9daf652c8d798160450392b3ebab0248aeca17d8609fbf'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7517eb70ab1471af395886d3b8e4e31382e966cfdb99aa7d06255c23bf7b51d4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5893 | 0.00231 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7517eb70ab1471af395886d3b8e4e31382e966cfdb99aa7d06255c23bf7b51d4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7517eb70ab1471af395886d3b8e4e31382e966cfdb99aa7d06255c23bf7b51d4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c2842629dff3cda202663fb0beb01cebb62fdce3e29748ab17773af0841e8b22'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5443 | 0.00213 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c2842629dff3cda202663fb0beb01cebb62fdce3e29748ab17773af0841e8b22'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c2842629dff3cda202663fb0beb01cebb62fdce3e29748ab17773af0841e8b22'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['754310db202d1b671267bb91ccc4aff5660787beaf3eac4f37a42ab0e3abb616'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4867 | 0.00191 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['754310db202d1b671267bb91ccc4aff5660787beaf3eac4f37a42ab0e3abb616'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['754310db202d1b671267bb91ccc4aff5660787beaf3eac4f37a42ab0e3abb616'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1db98501db646ffe23eaceafe463e58ecc1ca4561d177ef4d860d39e294fe9b7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7028 | 0.00276 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1db98501db646ffe23eaceafe463e58ecc1ca4561d177ef4d860d39e294fe9b7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1db98501db646ffe23eaceafe463e58ecc1ca4561d177ef4d860d39e294fe9b7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b6fe2c3ba63e785ab2f171d220b4a86d9e78049bd69ae3dbc42486c14300ae62'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b6fe2c3ba63e785ab2f171d220b4a86d9e78049bd69ae3dbc42486c14300ae62'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b6fe2c3ba63e785ab2f171d220b4a86d9e78049bd69ae3dbc42486c14300ae62'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['4f3b721e-ed05-442f-b5db-bb35d8216d7e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_52']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.75e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b1aec1ba7824e6615aa171e6e39c62a4e41c7a04e58f68c5ac2fc23b686db071'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.25 | 0.00098 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b1aec1ba7824e6615aa171e6e39c62a4e41c7a04e58f68c5ac2fc23b686db071'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b1aec1ba7824e6615aa171e6e39c62a4e41c7a04e58f68c5ac2fc23b686db071'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['78d87b5924fbe4eac04ab93aef747dd7d2a31214a3ec8ce14f7f5e878b740d34'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['78d87b5924fbe4eac04ab93aef747dd7d2a31214a3ec8ce14f7f5e878b740d34'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['78d87b5924fbe4eac04ab93aef747dd7d2a31214a3ec8ce14f7f5e878b740d34'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d254002a2b8fa8899799f67e49a53eef4ba61cd5f88ad9246df26547be38adf6'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2673 | 0.00105 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d254002a2b8fa8899799f67e49a53eef4ba61cd5f88ad9246df26547be38adf6'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d254002a2b8fa8899799f67e49a53eef4ba61cd5f88ad9246df26547be38adf6'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['7bdd2f73-4fa1-4017-85e6-06e41e743572']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5279 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00131 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c72c75bb68ec4064'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.198 | 0.000776 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c72c75bb68ec4064'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c72c75bb68ec4064'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_53']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 5.01e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.83e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6ff37fdd934b76f8a803ee685c185fbf470c6656c123700d58243ce2e7876cae'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2887 | 0.00113 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6ff37fdd934b76f8a803ee685c185fbf470c6656c123700d58243ce2e7876cae'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6ff37fdd934b76f8a803ee685c185fbf470c6656c123700d58243ce2e7876cae'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c72c75bb68ec406497b78649e746db5d579b9c3e68d7406271a692847578a483'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2828 | 0.00111 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c72c75bb68ec406497b78649e746db5d579b9c3e68d7406271a692847578a483'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c72c75bb68ec406497b78649e746db5d579b9c3e68d7406271a692847578a483'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['120696044728f1bd4d2fb9f8f833a3a96506ee7e9e54f61dc247ad8f35f5e61f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3244 | 0.00127 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['120696044728f1bd4d2fb9f8f833a3a96506ee7e9e54f61dc247ad8f35f5e61f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['120696044728f1bd4d2fb9f8f833a3a96506ee7e9e54f61dc247ad8f35f5e61f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['974aa9be-b6f7-427e-a5f3-fb2565041608']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5295 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00145 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0568c8660ffdfb26'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3447 | 0.00135 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0568c8660ffdfb26'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0568c8660ffdfb26'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_54']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.46e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.77e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['de266f2897d9866b2c733f582d22c8c513b64e5802c5c3b72f73054ec154ff98'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['de266f2897d9866b2c733f582d22c8c513b64e5802c5c3b72f73054ec154ff98'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['de266f2897d9866b2c733f582d22c8c513b64e5802c5c3b72f73054ec154ff98'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0568c8660ffdfb26e0c370cc85bf1b9683bed29f76750e08b6ba928bdc97f77e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4924 | 0.00193 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0568c8660ffdfb26e0c370cc85bf1b9683bed29f76750e08b6ba928bdc97f77e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0568c8660ffdfb26e0c370cc85bf1b9683bed29f76750e08b6ba928bdc97f77e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['3b636e12-bda8-4dc9-a7d0-b0d61e5bfd69']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5278 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00116 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_41289a34752abbd9'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4379 | 0.00172 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_41289a34752abbd9'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_41289a34752abbd9'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_55']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01282 | 4.48e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.81e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ee14c501fef5a41d54f4eedfa719db4d528f9a6ebd7cd961bbed8db28c09cc68'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6 | 0.00235 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ee14c501fef5a41d54f4eedfa719db4d528f9a6ebd7cd961bbed8db28c09cc68'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ee14c501fef5a41d54f4eedfa719db4d528f9a6ebd7cd961bbed8db28c09cc68'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['41289a34752abbd9eef1f005d51217a6761f8a14a93d6b9318250b2039cc3e9a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6255 | 0.00245 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['41289a34752abbd9eef1f005d51217a6761f8a14a93d6b9318250b2039cc3e9a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['41289a34752abbd9eef1f005d51217a6761f8a14a93d6b9318250b2039cc3e9a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6389d078acd4d5ea28f8ea831dbb12a0d583e8b588a36e4a7a297f6afd53a4bf'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6626 | 0.0026 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6389d078acd4d5ea28f8ea831dbb12a0d583e8b588a36e4a7a297f6afd53a4bf'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6389d078acd4d5ea28f8ea831dbb12a0d583e8b588a36e4a7a297f6afd53a4bf'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['525c0bf8-8478-4772-bfb5-f662b5cf6850']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00126 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0c1a6653f1fd8d7e'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2667 | 0.00105 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0c1a6653f1fd8d7e'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0c1a6653f1fd8d7e'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_56']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 2.97e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.84e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0c400730167690887204ef5477833fbfc8bb9cd032c65a921f0a7238e12e6b8d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3638 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0c400730167690887204ef5477833fbfc8bb9cd032c65a921f0a7238e12e6b8d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0c400730167690887204ef5477833fbfc8bb9cd032c65a921f0a7238e12e6b8d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0c1a6653f1fd8d7e46fcf61286954d2087851f0838f70cdc9d6c19e73478cf6f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.381 | 0.00149 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0c1a6653f1fd8d7e46fcf61286954d2087851f0838f70cdc9d6c19e73478cf6f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0c1a6653f1fd8d7e46fcf61286954d2087851f0838f70cdc9d6c19e73478cf6f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e96e16e0-24c0-47e5-81ae-01d0eb93aa10']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00138 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_57']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.78e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 5e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3fcc7f5de93b4ee604e06a52f25748839ceb2aafc732c146628500df764aba39'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4815 | 0.00189 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3fcc7f5de93b4ee604e06a52f25748839ceb2aafc732c146628500df764aba39'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3fcc7f5de93b4ee604e06a52f25748839ceb2aafc732c146628500df764aba39'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2860421e-022b-4c4b-87ae-1a5e5e27d52f']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00138 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_58']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 3.31e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.91e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['47a729d1152b0670348475eeff67cec40d4d836b803a88e2f78c4045ac8e44f4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5657 | 0.00222 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['47a729d1152b0670348475eeff67cec40d4d836b803a88e2f78c4045ac8e44f4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['47a729d1152b0670348475eeff67cec40d4d836b803a88e2f78c4045ac8e44f4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f80b140467c43c6755059d63f4f4a3b6c0431af630591fa9c15eacf265e2ad80'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f80b140467c43c6755059d63f4f4a3b6c0431af630591fa9c15eacf265e2ad80'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f80b140467c43c6755059d63f4f4a3b6c0431af630591fa9c15eacf265e2ad80'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2cb5ebed5d93b3a4c15b20c553bb7842be03d1a2b4298037e02649759b42f8f9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3244 | 0.00127 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2cb5ebed5d93b3a4c15b20c553bb7842be03d1a2b4298037e02649759b42f8f9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2cb5ebed5d93b3a4c15b20c553bb7842be03d1a2b4298037e02649759b42f8f9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52cc07a780e8854df5e8dfee11f71344312623fc43cb1f97555ae99bf5977473'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.7762 | 0.00304 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52cc07a780e8854df5e8dfee11f71344312623fc43cb1f97555ae99bf5977473'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['52cc07a780e8854df5e8dfee11f71344312623fc43cb1f97555ae99bf5977473'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['9f66c94e-90e6-41d2-a5a3-fc3eb0f70f7f']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5277 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00122 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2a16a26cad292627'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.396 | 0.00155 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2a16a26cad292627'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2a16a26cad292627'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_59']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.72e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ea654e608318cfbf60044157b1767c396d980d0ae7ec46e863d3b70aa577965c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5657 | 0.00222 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ea654e608318cfbf60044157b1767c396d980d0ae7ec46e863d3b70aa577965c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ea654e608318cfbf60044157b1767c396d980d0ae7ec46e863d3b70aa577965c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2a16a26cad292627e80513b927d42c2355dde07ca550d223d2de1b49d213b6bd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5657 | 0.00222 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2a16a26cad292627e80513b927d42c2355dde07ca550d223d2de1b49d213b6bd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2a16a26cad292627e80513b927d42c2355dde07ca550d223d2de1b49d213b6bd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['131d9e4a2a6b5ee0e48e2b5b35f02d4d17d827a81d38717a769825479807e56e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2857 | 0.00112 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['131d9e4a2a6b5ee0e48e2b5b35f02d4d17d827a81d38717a769825479807e56e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['131d9e4a2a6b5ee0e48e2b5b35f02d4d17d827a81d38717a769825479807e56e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['4b7dc3df-0a37-469c-9f0a-3707a9eb7af6']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00112 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00493 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_838dee241ac5cda6'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1627 | 0.000638 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_838dee241ac5cda6'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_838dee241ac5cda6'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_60']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.97e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5457e4af8a0bc2f38c96d6a3419d6b6741cefc1856d8b2559cc17b59953f97d7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5457e4af8a0bc2f38c96d6a3419d6b6741cefc1856d8b2559cc17b59953f97d7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5457e4af8a0bc2f38c96d6a3419d6b6741cefc1856d8b2559cc17b59953f97d7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['838dee241ac5cda6ed720cd3de6fb7bf5fe5bb7a47d6d77f54acd704a454933a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2325 | 0.000912 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['838dee241ac5cda6ed720cd3de6fb7bf5fe5bb7a47d6d77f54acd704a454933a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['838dee241ac5cda6ed720cd3de6fb7bf5fe5bb7a47d6d77f54acd704a454933a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['23fd7cae-fc43-4315-8cbe-186c572a9625']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5278 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00143 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e0dbd37940faf5ab'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2711 | 0.00106 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e0dbd37940faf5ab'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e0dbd37940faf5ab'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_61']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.67e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01283 | 4.9e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['099fdd380dc0cf119ca8182c68d04b0499cce92b5aecae652b5e34dd6bcaed81'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.381 | 0.00149 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['099fdd380dc0cf119ca8182c68d04b0499cce92b5aecae652b5e34dd6bcaed81'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['099fdd380dc0cf119ca8182c68d04b0499cce92b5aecae652b5e34dd6bcaed81'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e0dbd37940faf5ab560313d283da5a95e29f18744e964709309a6bb454425cb4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3873 | 0.00152 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e0dbd37940faf5ab560313d283da5a95e29f18744e964709309a6bb454425cb4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e0dbd37940faf5ab560313d283da5a95e29f18744e964709309a6bb454425cb4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['59930745-79bd-468d-b929-dd85c3375e15']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5277 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00133 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7caf4e798a9be5df'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1854 | 0.000727 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7caf4e798a9be5df'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_7caf4e798a9be5df'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_62']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.93e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.6e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5fa3a0c14a4bc9a254ef52f5c1dede4b1c10e4d8afdbf29dbc95d4cc067c97ea'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3906 | 0.00153 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5fa3a0c14a4bc9a254ef52f5c1dede4b1c10e4d8afdbf29dbc95d4cc067c97ea'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5fa3a0c14a4bc9a254ef52f5c1dede4b1c10e4d8afdbf29dbc95d4cc067c97ea'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7caf4e798a9be5dfbfdbcdf16b63f220bd27fdd06a51a03e0bcbff54f56da444'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2649 | 0.00104 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7caf4e798a9be5dfbfdbcdf16b63f220bd27fdd06a51a03e0bcbff54f56da444'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7caf4e798a9be5dfbfdbcdf16b63f220bd27fdd06a51a03e0bcbff54f56da444'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['a821420e-657a-4b6c-9d82-cb0bd0cd3aa2']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5283 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00124 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_bc043ba631351275'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.317 | 0.00124 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_bc043ba631351275'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_bc043ba631351275'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_63']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 3.92e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 5.08e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2b2927757ae6d26a3606188e59faa41178d383ff339a052db0e1f79f89f00e84'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3693 | 0.00145 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2b2927757ae6d26a3606188e59faa41178d383ff339a052db0e1f79f89f00e84'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2b2927757ae6d26a3606188e59faa41178d383ff339a052db0e1f79f89f00e84'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bc043ba631351275db888a0df00fcc4081671e792a94f7e3a0899dc9f1fb0605'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4529 | 0.00178 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bc043ba631351275db888a0df00fcc4081671e792a94f7e3a0899dc9f1fb0605'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bc043ba631351275db888a0df00fcc4081671e792a94f7e3a0899dc9f1fb0605'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['28435c9a-7d96-476b-8895-6dbd01260776']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5271 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00155 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_a7a3012d15ffe62b'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2858 | 0.00112 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_a7a3012d15ffe62b'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_a7a3012d15ffe62b'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_64']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.94e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.84e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5a085a53d782f5c28ceea7d536d121cec66c440e41d62fed8e91f918844f200'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5a085a53d782f5c28ceea7d536d121cec66c440e41d62fed8e91f918844f200'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f5a085a53d782f5c28ceea7d536d121cec66c440e41d62fed8e91f918844f200'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a7a3012d15ffe62bbaa948b5b107727c9f6921a3311a14cbe3ebf21c5754c277'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a7a3012d15ffe62bbaa948b5b107727c9f6921a3311a14cbe3ebf21c5754c277'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a7a3012d15ffe62bbaa948b5b107727c9f6921a3311a14cbe3ebf21c5754c277'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['10fc9afb7b85d9a8e840072a49fc0553f23141e85077b63cdbf16cc0c7164298'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2887 | 0.00113 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['10fc9afb7b85d9a8e840072a49fc0553f23141e85077b63cdbf16cc0c7164298'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['10fc9afb7b85d9a8e840072a49fc0553f23141e85077b63cdbf16cc0c7164298'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['d447536f-9f78-4197-b3e3-cb8e66c3802f']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5279 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_55d3a55bc6483f21'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3352 | 0.00131 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_55d3a55bc6483f21'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_55d3a55bc6483f21'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_65']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01283 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4feaa87f8462201ff81456de6c4b4a5fd6cefb9c035bb705deac9396e4ddfb22'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.488 | 0.00191 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4feaa87f8462201ff81456de6c4b4a5fd6cefb9c035bb705deac9396e4ddfb22'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4feaa87f8462201ff81456de6c4b4a5fd6cefb9c035bb705deac9396e4ddfb22'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['55d3a55bc6483f21552f9884d516849e348b52897f31fd3861decdd3ffbd93cd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4789 | 0.00188 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['55d3a55bc6483f21552f9884d516849e348b52897f31fd3861decdd3ffbd93cd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['55d3a55bc6483f21552f9884d516849e348b52897f31fd3861decdd3ffbd93cd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7e6e50534c0faa7224afc5a09d87f2d0474a331af81547bfdc1bada83930f470'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5077 | 0.00199 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7e6e50534c0faa7224afc5a09d87f2d0474a331af81547bfdc1bada83930f470'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7e6e50534c0faa7224afc5a09d87f2d0474a331af81547bfdc1bada83930f470'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['92981581b4ab2f8289a0aed492e7908fd6d56b8087c43dc3762ed33467526005'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5345 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['92981581b4ab2f8289a0aed492e7908fd6d56b8087c43dc3762ed33467526005'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['92981581b4ab2f8289a0aed492e7908fd6d56b8087c43dc3762ed33467526005'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['702024d8f07688816e8808269d93ed5368777eb7f8ed01981371450c979fb1d5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['702024d8f07688816e8808269d93ed5368777eb7f8ed01981371450c979fb1d5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['702024d8f07688816e8808269d93ed5368777eb7f8ed01981371450c979fb1d5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['53aeab529755f4ddf5d30a2715d63ba8ad85a7ce255ec388e39cfb80e4914fe9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.9558 | 0.00375 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['53aeab529755f4ddf5d30a2715d63ba8ad85a7ce255ec388e39cfb80e4914fe9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['53aeab529755f4ddf5d30a2715d63ba8ad85a7ce255ec388e39cfb80e4914fe9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['a1657b4a-aec0-4286-8751-e7f6f04015b8']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.53 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0015 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_66']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.37e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.6e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff58dd6b2f4bf3c481028afbe29bb0f33a3cd72ac958ab1ef50da14528bc45d1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.417 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff58dd6b2f4bf3c481028afbe29bb0f33a3cd72ac958ab1ef50da14528bc45d1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ff58dd6b2f4bf3c481028afbe29bb0f33a3cd72ac958ab1ef50da14528bc45d1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ded2e944bace24995df54d5eefa6bd3c115fc3472a79e36590b7a29394c14abc'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ded2e944bace24995df54d5eefa6bd3c115fc3472a79e36590b7a29394c14abc'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ded2e944bace24995df54d5eefa6bd3c115fc3472a79e36590b7a29394c14abc'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0419257838734c9c4fbbfb7dad3eed7a699f185d82360f91da3431d9545eb065'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6882 | 0.0027 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0419257838734c9c4fbbfb7dad3eed7a699f185d82360f91da3431d9545eb065'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0419257838734c9c4fbbfb7dad3eed7a699f185d82360f91da3431d9545eb065'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['971aed5f-382a-47c5-8aed-d22a6236e92b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5287 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00156 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_67']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.02e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.87e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['965618fc0fff12212167383acbb0ffc8e8d4db10e95693653153bb813bab62c1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5494 | 0.00215 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['965618fc0fff12212167383acbb0ffc8e8d4db10e95693653153bb813bab62c1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['965618fc0fff12212167383acbb0ffc8e8d4db10e95693653153bb813bab62c1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c850a4e219c05b7fc24a0551e40338c4b48ad1380c796764a1da9184e933032a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4575 | 0.00179 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c850a4e219c05b7fc24a0551e40338c4b48ad1380c796764a1da9184e933032a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c850a4e219c05b7fc24a0551e40338c4b48ad1380c796764a1da9184e933032a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['01cb31a8-9e43-4aab-8bf1-b225c58618c5']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5282 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_840bfcc535b26df3'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2858 | 0.00112 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_840bfcc535b26df3'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_840bfcc535b26df3'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_68']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 3.84e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 5.03e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['484930cfaf67b71e3cab537a86d6a0aebfdc28a6ab47d2484963c15db8ddb478'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2236 | 0.000877 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['484930cfaf67b71e3cab537a86d6a0aebfdc28a6ab47d2484963c15db8ddb478'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['484930cfaf67b71e3cab537a86d6a0aebfdc28a6ab47d2484963c15db8ddb478'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['840bfcc535b26df32e41e88f12ae55873fe00c10b5c47a1fb71324f1d76ca3e9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['840bfcc535b26df32e41e88f12ae55873fe00c10b5c47a1fb71324f1d76ca3e9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['840bfcc535b26df32e41e88f12ae55873fe00c10b5c47a1fb71324f1d76ca3e9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['edffbd724ed10a425f66c6acde9d8e5f27099aae3eb164a3d5265c8f6ad36c7f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2673 | 0.00105 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['edffbd724ed10a425f66c6acde9d8e5f27099aae3eb164a3d5265c8f6ad36c7f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['edffbd724ed10a425f66c6acde9d8e5f27099aae3eb164a3d5265c8f6ad36c7f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['47431ee1-f935-41a5-bf16-e3e8978d7f64']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00138 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2904dcd0fc50b319'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3772 | 0.00148 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2904dcd0fc50b319'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2904dcd0fc50b319'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_69']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 3.51e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 5.12e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dae289a81a64e351426936d657b43a2f9177138e525a174e6ac5f2214bf8a179'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5571 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dae289a81a64e351426936d657b43a2f9177138e525a174e6ac5f2214bf8a179'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dae289a81a64e351426936d657b43a2f9177138e525a174e6ac5f2214bf8a179'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2904dcd0fc50b319930b442e754f4e87cc8fc10d205eaae2119bedce8d9806c2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5388 | 0.00211 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2904dcd0fc50b319930b442e754f4e87cc8fc10d205eaae2119bedce8d9806c2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2904dcd0fc50b319930b442e754f4e87cc8fc10d205eaae2119bedce8d9806c2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['029cd560-97e4-4e75-bce0-1ab2a18aa513']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5262 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00138 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2d7be5702360ce85'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4118 | 0.00162 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2d7be5702360ce85'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2d7be5702360ce85'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_70']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.28e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.65e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6971c68f43b2f6930d2b3496a515a5f0130a15ddb89de83a740996d981e20543'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5883 | 0.00231 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6971c68f43b2f6930d2b3496a515a5f0130a15ddb89de83a740996d981e20543'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6971c68f43b2f6930d2b3496a515a5f0130a15ddb89de83a740996d981e20543'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2d7be5702360ce85f638436b492cf6dc1ba874263cf9f62f647c09b26f0b3835'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5883 | 0.00231 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2d7be5702360ce85f638436b492cf6dc1ba874263cf9f62f647c09b26f0b3835'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2d7be5702360ce85f638436b492cf6dc1ba874263cf9f62f647c09b26f0b3835'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c780d7a37762861fe47fc6c2ff7553fd780ae9ebf5078f8430371da44a5e7b46'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5345 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c780d7a37762861fe47fc6c2ff7553fd780ae9ebf5078f8430371da44a5e7b46'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c780d7a37762861fe47fc6c2ff7553fd780ae9ebf5078f8430371da44a5e7b46'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['3586b1e2-d775-44b5-90bf-4c1d111e683d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00155 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_71']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.57e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.85e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1fb9767d78f1ae73622878df4cff951d5d943f98f5cf9a81446f541dc7f39b7e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4851 | 0.0019 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1fb9767d78f1ae73622878df4cff951d5d943f98f5cf9a81446f541dc7f39b7e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1fb9767d78f1ae73622878df4cff951d5d943f98f5cf9a81446f541dc7f39b7e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ac071b72ad6fcc84e933ef3b176bb88c799a94cb64782b92d506a8b4dae8ff81'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6667 | 0.00261 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ac071b72ad6fcc84e933ef3b176bb88c799a94cb64782b92d506a8b4dae8ff81'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ac071b72ad6fcc84e933ef3b176bb88c799a94cb64782b92d506a8b4dae8ff81'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e27e67a7-250b-4884-b540-a5f9349af65a']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5292 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00133 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_f97ca60075b6a8cb'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3615 | 0.00142 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_f97ca60075b6a8cb'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_f97ca60075b6a8cb'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_72']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 3.56e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b40e9b7636482e17bf87382767637b269b037b151e8ae838361bcc36c74d667'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2774 | 0.00109 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b40e9b7636482e17bf87382767637b269b037b151e8ae838361bcc36c74d667'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b40e9b7636482e17bf87382767637b269b037b151e8ae838361bcc36c74d667'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f97ca60075b6a8cb190d941a5a8d47e6079ea9bf00fe972d31bb4c0f4ac3fcda'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f97ca60075b6a8cb190d941a5a8d47e6079ea9bf00fe972d31bb4c0f4ac3fcda'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f97ca60075b6a8cb190d941a5a8d47e6079ea9bf00fe972d31bb4c0f4ac3fcda'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['65ca23a3e969c198475e67a1d76302953f356fbf7ff5967016f1922043172f07'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['65ca23a3e969c198475e67a1d76302953f356fbf7ff5967016f1922043172f07'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['65ca23a3e969c198475e67a1d76302953f356fbf7ff5967016f1922043172f07'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d9f2bf9bcd7b8a5591339b7e406f96d0c4159beccad04c44ceb50114afadd9e7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6402 | 0.00251 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d9f2bf9bcd7b8a5591339b7e406f96d0c4159beccad04c44ceb50114afadd9e7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d9f2bf9bcd7b8a5591339b7e406f96d0c4159beccad04c44ceb50114afadd9e7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['16ba3eeac181480cb3771608e827b99020bedd9d969f0453750b5ec5ef58aaba'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4867 | 0.00191 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['16ba3eeac181480cb3771608e827b99020bedd9d969f0453750b5ec5ef58aaba'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['16ba3eeac181480cb3771608e827b99020bedd9d969f0453750b5ec5ef58aaba'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a8e4defe3cc63afba91f1c351a913cbe579c5b03b2b842f35828f809ea36460'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5522 | 0.00217 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a8e4defe3cc63afba91f1c351a913cbe579c5b03b2b842f35828f809ea36460'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a8e4defe3cc63afba91f1c351a913cbe579c5b03b2b842f35828f809ea36460'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['ccd61179-194d-4548-9795-a4a6e49f9e6a']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5278 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0014 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_73']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.65e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 5.01e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f2c699c60b3b6c33a4818cf1badbf2008fc5dc1ab790b406b85b71c900c94407'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f2c699c60b3b6c33a4818cf1badbf2008fc5dc1ab790b406b85b71c900c94407'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f2c699c60b3b6c33a4818cf1badbf2008fc5dc1ab790b406b85b71c900c94407'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c0898165df29171a9dcbaf3264862d67452d9c6148c1a5941cdc4ee0930b47da'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c0898165df29171a9dcbaf3264862d67452d9c6148c1a5941cdc4ee0930b47da'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c0898165df29171a9dcbaf3264862d67452d9c6148c1a5941cdc4ee0930b47da'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ef94894e2d8690671ad6a85360f64b2b83c1fb10045820e6ac39422f33a0a353'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ef94894e2d8690671ad6a85360f64b2b83c1fb10045820e6ac39422f33a0a353'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ef94894e2d8690671ad6a85360f64b2b83c1fb10045820e6ac39422f33a0a353'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['d5bdebc3-18fb-4cb4-b2a4-691d0e796cab']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5281 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_74']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.98e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 5e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5977533488772ff0788183728402f2d57a1cf3597e89f08b810355f3ced5d565'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.417 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5977533488772ff0788183728402f2d57a1cf3597e89f08b810355f3ced5d565'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5977533488772ff0788183728402f2d57a1cf3597e89f08b810355f3ced5d565'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d8a674eed1664f90091d28498ee00562ee834a4f0b6ea0527b7d7601a25ddee6'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d8a674eed1664f90091d28498ee00562ee834a4f0b6ea0527b7d7601a25ddee6'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d8a674eed1664f90091d28498ee00562ee834a4f0b6ea0527b7d7601a25ddee6'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2c27d3d7-23ee-414e-a917-d09660b5cba3']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5289 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00143 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e7606531b36abb10'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2646 | 0.00104 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e7606531b36abb10'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_e7606531b36abb10'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_75']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.92e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.85e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a90dbd6d1f171a30e95f3e46f17c55ec29fab320daaeb8db754e67b1a9a43b2d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3651 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a90dbd6d1f171a30e95f3e46f17c55ec29fab320daaeb8db754e67b1a9a43b2d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a90dbd6d1f171a30e95f3e46f17c55ec29fab320daaeb8db754e67b1a9a43b2d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e7606531b36abb10651531a297e87698fc495c85dae0c4c8213cb80e3756a3cf'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e7606531b36abb10651531a297e87698fc495c85dae0c4c8213cb80e3756a3cf'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e7606531b36abb10651531a297e87698fc495c85dae0c4c8213cb80e3756a3cf'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a2d021952223d80f1db160f9652ec813dd4899d8df8ce0f4dc076a017311f137'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a2d021952223d80f1db160f9652ec813dd4899d8df8ce0f4dc076a017311f137'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a2d021952223d80f1db160f9652ec813dd4899d8df8ce0f4dc076a017311f137'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['4721b3c9-e32e-4892-9540-b677e6702666']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5271 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00148 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_76']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.65e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 5.02e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['99b39c3bb2efb9d18513892cddf7c45835e2c6b5fae6456464e0725840a59b43'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['99b39c3bb2efb9d18513892cddf7c45835e2c6b5fae6456464e0725840a59b43'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['99b39c3bb2efb9d18513892cddf7c45835e2c6b5fae6456464e0725840a59b43'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eb149ae6a9ce6b0dacb2f2ebfaef3474ac3c1ef4b01913eb23db28304074d321'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eb149ae6a9ce6b0dacb2f2ebfaef3474ac3c1ef4b01913eb23db28304074d321'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['eb149ae6a9ce6b0dacb2f2ebfaef3474ac3c1ef4b01913eb23db28304074d321'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['9d0decc7-7420-452c-a69f-4e01ae752e6e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5282 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00151 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fd01efcb933b8811'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3055 | 0.0012 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fd01efcb933b8811'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fd01efcb933b8811'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_77']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.25e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.94e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['29ec72aaacf74f5e431fe0a1f88a557368249a8712f440be5d85ccf893cd0497'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['29ec72aaacf74f5e431fe0a1f88a557368249a8712f440be5d85ccf893cd0497'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['29ec72aaacf74f5e431fe0a1f88a557368249a8712f440be5d85ccf893cd0497'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fd01efcb933b8811fbea989f413ff923ef8cf4680962b60105f5030fd8cb8347'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4364 | 0.00171 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fd01efcb933b8811fbea989f413ff923ef8cf4680962b60105f5030fd8cb8347'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fd01efcb933b8811fbea989f413ff923ef8cf4680962b60105f5030fd8cb8347'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['558dfbd35c197bd20475fca7b660524c5a901e7dca716aab3d4a8c90380059cd'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.603 | 0.00236 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['558dfbd35c197bd20475fca7b660524c5a901e7dca716aab3d4a8c90380059cd'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['558dfbd35c197bd20475fca7b660524c5a901e7dca716aab3d4a8c90380059cd'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['635dcf1f-a862-4ecd-9f7a-ec7c2c4731f7']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5279 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_84156c791b3cfdd3'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2746 | 0.00108 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_84156c791b3cfdd3'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_84156c791b3cfdd3'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_78']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.75e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.84e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b2ec41e48edef0c06f900aa193c776ced1bd18355a7a318207722dc9bf773904'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b2ec41e48edef0c06f900aa193c776ced1bd18355a7a318207722dc9bf773904'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b2ec41e48edef0c06f900aa193c776ced1bd18355a7a318207722dc9bf773904'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['84156c791b3cfdd3a3008f63aaf2090e68599c89a608949bef152415ba09f4e7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['84156c791b3cfdd3a3008f63aaf2090e68599c89a608949bef152415ba09f4e7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['84156c791b3cfdd3a3008f63aaf2090e68599c89a608949bef152415ba09f4e7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['463ef9490ffa85bc86f0612273fe57edce11c5265073483d863def4a591093d5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['463ef9490ffa85bc86f0612273fe57edce11c5265073483d863def4a591093d5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['463ef9490ffa85bc86f0612273fe57edce11c5265073483d863def4a591093d5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['05c1dce4-0f25-4b0f-b526-27e7d17291c8']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00159 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.0049 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_8a9494a37d708edc'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.35 | 0.00137 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_8a9494a37d708edc'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_8a9494a37d708edc'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_79']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.29e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.8e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dccf7207d43b12b9e4c48ab7279c49f209168b9e456f062eb1dadf289a9c7222'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3651 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dccf7207d43b12b9e4c48ab7279c49f209168b9e456f062eb1dadf289a9c7222'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dccf7207d43b12b9e4c48ab7279c49f209168b9e456f062eb1dadf289a9c7222'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8a9494a37d708edc6d40dc811b4ffad2f6922197cc3024793e96a396fc669147'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8a9494a37d708edc6d40dc811b4ffad2f6922197cc3024793e96a396fc669147'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8a9494a37d708edc6d40dc811b4ffad2f6922197cc3024793e96a396fc669147'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['922439050680915441be2e038d57cd34412b5553a7d6ca528ada8e227cf34f1d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['922439050680915441be2e038d57cd34412b5553a7d6ca528ada8e227cf34f1d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['922439050680915441be2e038d57cd34412b5553a7d6ca528ada8e227cf34f1d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['145ff3fd455c4ba70633c51dcc5d5a112dd4a40d6b471cc5024e6288d4c9227b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4927 | 0.00193 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['145ff3fd455c4ba70633c51dcc5d5a112dd4a40d6b471cc5024e6288d4c9227b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['145ff3fd455c4ba70633c51dcc5d5a112dd4a40d6b471cc5024e6288d4c9227b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['566d402e3e317329bd2125db784208e421720132df65bc57f207c6300a27ce4a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4523 | 0.00177 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['566d402e3e317329bd2125db784208e421720132df65bc57f207c6300a27ce4a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['566d402e3e317329bd2125db784208e421720132df65bc57f207c6300a27ce4a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4afd7fb983e149e49061ad51bc6a9a07427136681a603af3a7b722181634b367'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4804 | 0.00188 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4afd7fb983e149e49061ad51bc6a9a07427136681a603af3a7b722181634b367'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4afd7fb983e149e49061ad51bc6a9a07427136681a603af3a7b722181634b367'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['394843d9-55f0-461e-b53f-8cf197c71859']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5261 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00152 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_80']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 5.13e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 4.96e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['90802888156d6ae41c3c2116f1b738f3820b47d283bd2aa2a27e78377c01c4df'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.417 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['90802888156d6ae41c3c2116f1b738f3820b47d283bd2aa2a27e78377c01c4df'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['90802888156d6ae41c3c2116f1b738f3820b47d283bd2aa2a27e78377c01c4df'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01df98884cc03932a3eeb9f6a2fa97c24ef94f3fdcdedb2a670234ead31bd0e8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5547 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01df98884cc03932a3eeb9f6a2fa97c24ef94f3fdcdedb2a670234ead31bd0e8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01df98884cc03932a3eeb9f6a2fa97c24ef94f3fdcdedb2a670234ead31bd0e8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f01c9c7f7ea173d66a95d61b8a23a0d6dfbabc217a0cda3358ba921fc23758a9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6255 | 0.00245 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f01c9c7f7ea173d66a95d61b8a23a0d6dfbabc217a0cda3358ba921fc23758a9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f01c9c7f7ea173d66a95d61b8a23a0d6dfbabc217a0cda3358ba921fc23758a9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['bbbf1099-b670-421c-9242-8a74249c357b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5281 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0014 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_81']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.47e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 5.03e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b98bf09b0cde915f973d999add9a7845a5eed9b2b5a5a338e525657b96fec34c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b98bf09b0cde915f973d999add9a7845a5eed9b2b5a5a338e525657b96fec34c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b98bf09b0cde915f973d999add9a7845a5eed9b2b5a5a338e525657b96fec34c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cf229904b745f481c2685d5190fd6b79a1eb1dffb96fadd21051c016dc49a417'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cf229904b745f481c2685d5190fd6b79a1eb1dffb96fadd21051c016dc49a417'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cf229904b745f481c2685d5190fd6b79a1eb1dffb96fadd21051c016dc49a417'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['d8b6fd7d-836e-423c-a777-927cbb6aa68e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_94ad1b7ecbebacde'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2556 | 0.001 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_94ad1b7ecbebacde'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_94ad1b7ecbebacde'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_82']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.18e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.98e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ed752ec3066da25cec856693efa8f95703eb662577183489facd9d734fa42fa'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ed752ec3066da25cec856693efa8f95703eb662577183489facd9d734fa42fa'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5ed752ec3066da25cec856693efa8f95703eb662577183489facd9d734fa42fa'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['94ad1b7ecbebacde259a940123d7904ac9984e5fb54e7baa2afc32feaaedf70a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3651 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['94ad1b7ecbebacde259a940123d7904ac9984e5fb54e7baa2afc32feaaedf70a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['94ad1b7ecbebacde259a940123d7904ac9984e5fb54e7baa2afc32feaaedf70a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['386f683fc9a0ebff805e9da86bccc64f382145f80754f809455877246e137b5c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['386f683fc9a0ebff805e9da86bccc64f382145f80754f809455877246e137b5c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['386f683fc9a0ebff805e9da86bccc64f382145f80754f809455877246e137b5c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['8db1b930-f41f-4724-883c-5ffb2621b996']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5265 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00141 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_83']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.93e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.98e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['017bc141466cc706125e6c0d4c9a9176b282dfdd96e63fb32649d891c2f08757'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['017bc141466cc706125e6c0d4c9a9176b282dfdd96e63fb32649d891c2f08757'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['017bc141466cc706125e6c0d4c9a9176b282dfdd96e63fb32649d891c2f08757'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['198eac46a007f9015e1d5cf78b369dde8502a4f3e637d9f348e18caf64e34d6b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2887 | 0.00113 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['198eac46a007f9015e1d5cf78b369dde8502a4f3e637d9f348e18caf64e34d6b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['198eac46a007f9015e1d5cf78b369dde8502a4f3e637d9f348e18caf64e34d6b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['8f2f9cc8-4a33-422f-9c7d-e0aa46984ccb']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5279 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00136 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_84']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 3.79e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 5.19e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['28c7bae1f9012c663643e0d9f58b54d3c31e04f8e092b72f1746c1c8f335a730'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4264 | 0.00167 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['28c7bae1f9012c663643e0d9f58b54d3c31e04f8e092b72f1746c1c8f335a730'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['28c7bae1f9012c663643e0d9f58b54d3c31e04f8e092b72f1746c1c8f335a730'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0d735a20e6978323b5676709ef806294a67cd01377ad6b5058e2d2b73504f427'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2887 | 0.00113 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0d735a20e6978323b5676709ef806294a67cd01377ad6b5058e2d2b73504f427'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0d735a20e6978323b5676709ef806294a67cd01377ad6b5058e2d2b73504f427'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c67687f0-43df-4334-9f96-730e01b949f1']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5283 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_85']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.43e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.11e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a82058bbab454ce0e106a220f51dc0069570cea87bc53a85bd80d6bb619195c9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a82058bbab454ce0e106a220f51dc0069570cea87bc53a85bd80d6bb619195c9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a82058bbab454ce0e106a220f51dc0069570cea87bc53a85bd80d6bb619195c9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8271cad8368ac22963ae6fb9bd66aef2cb1095bc46f44521b76cfeea9f0a1950'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6667 | 0.00261 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8271cad8368ac22963ae6fb9bd66aef2cb1095bc46f44521b76cfeea9f0a1950'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8271cad8368ac22963ae6fb9bd66aef2cb1095bc46f44521b76cfeea9f0a1950'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['3b779440-a593-47c7-9c64-8b9710cc8364']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5286 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00157 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_85e5c3457cd6796d'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.313 | 0.00123 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_85e5c3457cd6796d'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_85e5c3457cd6796d'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_86']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.1e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['562572ac81f6f5f79c438d9f0e34104d714d2d16d93b6508a36b4a19a3b6a138'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['562572ac81f6f5f79c438d9f0e34104d714d2d16d93b6508a36b4a19a3b6a138'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['562572ac81f6f5f79c438d9f0e34104d714d2d16d93b6508a36b4a19a3b6a138'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['85e5c3457cd6796decd9a8a974843c2dbcc4a304b95de7c0c2cafc24e7262dbb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['85e5c3457cd6796decd9a8a974843c2dbcc4a304b95de7c0c2cafc24e7262dbb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['85e5c3457cd6796decd9a8a974843c2dbcc4a304b95de7c0c2cafc24e7262dbb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dafe4c7ead98d6543cf7e0944a7f6fda9975a8af6149ad503fa689306b0de44c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5774 | 0.00226 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dafe4c7ead98d6543cf7e0944a7f6fda9975a8af6149ad503fa689306b0de44c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['dafe4c7ead98d6543cf7e0944a7f6fda9975a8af6149ad503fa689306b0de44c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['176fa83e1efad6e7af5e514c4bec704dea3b6e8bf4cf8208a1522bd4fd2643c2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4286 | 0.00168 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['176fa83e1efad6e7af5e514c4bec704dea3b6e8bf4cf8208a1522bd4fd2643c2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['176fa83e1efad6e7af5e514c4bec704dea3b6e8bf4cf8208a1522bd4fd2643c2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fd64cd109b73162e0b4d3e31af1c80197b8130011e66856b5c6e1a60edda2ed0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3651 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fd64cd109b73162e0b4d3e31af1c80197b8130011e66856b5c6e1a60edda2ed0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fd64cd109b73162e0b4d3e31af1c80197b8130011e66856b5c6e1a60edda2ed0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2879e93cd2ad4528cd9f14fab30d36f981a91533f0639ac2a4c0e8fff93389d1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.533 | 0.00209 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2879e93cd2ad4528cd9f14fab30d36f981a91533f0639ac2a4c0e8fff93389d1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2879e93cd2ad4528cd9f14fab30d36f981a91533f0639ac2a4c0e8fff93389d1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['de8e27a9-f1dc-4314-b922-5cb135c18c60']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5289 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_87']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 5.02e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.98e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['369b3535edb9cd3e8f0892163c77a06d8667def6a65d7f9f28b9dd33923e1269'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['369b3535edb9cd3e8f0892163c77a06d8667def6a65d7f9f28b9dd33923e1269'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['369b3535edb9cd3e8f0892163c77a06d8667def6a65d7f9f28b9dd33923e1269'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e93e9cbd677d285af5e991b10db41f546ebbfad3a7ec90b50dc4edb485c622c3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e93e9cbd677d285af5e991b10db41f546ebbfad3a7ec90b50dc4edb485c622c3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e93e9cbd677d285af5e991b10db41f546ebbfad3a7ec90b50dc4edb485c622c3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['ec9800ee-bc2c-4854-be00-79144db432a9']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5281 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00122 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_88']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e9dd868a861ad25363a29275ac8d11c29dae464e7df248e56257fa3552b00525'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e9dd868a861ad25363a29275ac8d11c29dae464e7df248e56257fa3552b00525'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e9dd868a861ad25363a29275ac8d11c29dae464e7df248e56257fa3552b00525'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bfc13405be7e57f96a3b2ad2cb83c73bb546e1ee90081b5c25a5b8ccb8e9acb7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bfc13405be7e57f96a3b2ad2cb83c73bb546e1ee90081b5c25a5b8ccb8e9acb7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['bfc13405be7e57f96a3b2ad2cb83c73bb546e1ee90081b5c25a5b8ccb8e9acb7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['95066e74-d58b-4404-aa9f-0e47061914f3']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00136 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_945565f72ecad77e'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.146 | 0.000572 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_945565f72ecad77e'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_945565f72ecad77e'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_89']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.29e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.97e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d27898f264101266b7bc57a3c34051e91055aad0cd657828580a78f94ad21487'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2182 | 0.000856 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d27898f264101266b7bc57a3c34051e91055aad0cd657828580a78f94ad21487'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d27898f264101266b7bc57a3c34051e91055aad0cd657828580a78f94ad21487'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['945565f72ecad77edfaa7e5760bc5065307c176bedcf7633109db6a946696fee'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2085 | 0.000818 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['945565f72ecad77edfaa7e5760bc5065307c176bedcf7633109db6a946696fee'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['945565f72ecad77edfaa7e5760bc5065307c176bedcf7633109db6a946696fee'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7dabce21510a8b1686a06aba7ad6db81ee158337a288a1fa2d0f287e200f4ceb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2774 | 0.00109 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7dabce21510a8b1686a06aba7ad6db81ee158337a288a1fa2d0f287e200f4ceb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7dabce21510a8b1686a06aba7ad6db81ee158337a288a1fa2d0f287e200f4ceb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['cfbe26e6-596b-4c4d-98a6-10c68611550b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5273 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_67c7f6b500f84c60'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2646 | 0.00104 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_67c7f6b500f84c60'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_67c7f6b500f84c60'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_90']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 5e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a0a442ea8456ccbdd0a35f7a9f630268c7b657d89bae0aeb1c3074e513877bc'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5303 | 0.00208 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a0a442ea8456ccbdd0a35f7a9f630268c7b657d89bae0aeb1c3074e513877bc'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4a0a442ea8456ccbdd0a35f7a9f630268c7b657d89bae0aeb1c3074e513877bc'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['67c7f6b500f84c606311f3ebf6d9689757e72167ac92fad7d7209ab0a7eae85f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['67c7f6b500f84c606311f3ebf6d9689757e72167ac92fad7d7209ab0a7eae85f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['67c7f6b500f84c606311f3ebf6d9689757e72167ac92fad7d7209ab0a7eae85f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e37072660ff1f1bc9dcf31649d890e8c4f889bb2755aad27d3bdcdbd21564c18'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e37072660ff1f1bc9dcf31649d890e8c4f889bb2755aad27d3bdcdbd21564c18'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e37072660ff1f1bc9dcf31649d890e8c4f889bb2755aad27d3bdcdbd21564c18'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['4f86089b-00b5-4160-887d-8f954802f7c8']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5266 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4d33b93f9d2d3eac'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.26 | 0.00102 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4d33b93f9d2d3eac'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4d33b93f9d2d3eac'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_91']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.74e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.87e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['63d8f8d05ceb5fd6222da11469896a41605c3c276b7c1c358120a1074a04e059'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3849 | 0.00151 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['63d8f8d05ceb5fd6222da11469896a41605c3c276b7c1c358120a1074a04e059'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['63d8f8d05ceb5fd6222da11469896a41605c3c276b7c1c358120a1074a04e059'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d33b93f9d2d3eacf886f48a40a9aad733ae8cef00c7c4df65f8d1a38dc8904f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d33b93f9d2d3eacf886f48a40a9aad733ae8cef00c7c4df65f8d1a38dc8904f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d33b93f9d2d3eacf886f48a40a9aad733ae8cef00c7c4df65f8d1a38dc8904f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['37da2a982266fe587f09fbe5b7c91846a2ad0600ca8bd1451c820873b236d2b7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5164 | 0.00203 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['37da2a982266fe587f09fbe5b7c91846a2ad0600ca8bd1451c820873b236d2b7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['37da2a982266fe587f09fbe5b7c91846a2ad0600ca8bd1451c820873b236d2b7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1dcab539-6a06-457d-831f-e0f9452e035b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5285 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00133 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_92']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.65e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b160eb9e02791c3bd273f670b17914d74190d3847738ea2ff5e432baf192e3f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b160eb9e02791c3bd273f670b17914d74190d3847738ea2ff5e432baf192e3f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3b160eb9e02791c3bd273f670b17914d74190d3847738ea2ff5e432baf192e3f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['608509cf-0caa-4267-9852-639304439edc']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00137 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_93']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.62e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.75e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68e2202dd7f534ca285132cbd6073cf75df02ee91b80eb4d30a7dc29f39a5a2a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68e2202dd7f534ca285132cbd6073cf75df02ee91b80eb4d30a7dc29f39a5a2a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68e2202dd7f534ca285132cbd6073cf75df02ee91b80eb4d30a7dc29f39a5a2a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['791f74a36637d47eab2c50a2445b826b2135e51f9ab4b1dd3c3244ea780b9b97'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5547 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['791f74a36637d47eab2c50a2445b826b2135e51f9ab4b1dd3c3244ea780b9b97'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['791f74a36637d47eab2c50a2445b826b2135e51f9ab4b1dd3c3244ea780b9b97'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4864e886642e3bfc1a73b3faf044ac15d2848bab3503759fc3fe3c56dde59c21'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4864e886642e3bfc1a73b3faf044ac15d2848bab3503759fc3fe3c56dde59c21'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4864e886642e3bfc1a73b3faf044ac15d2848bab3503759fc3fe3c56dde59c21'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1f2bc35a6fcd80cf0950cca0744efa20241dbba1563c0260cf78d0dc9885b048'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2582 | 0.00101 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1f2bc35a6fcd80cf0950cca0744efa20241dbba1563c0260cf78d0dc9885b048'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1f2bc35a6fcd80cf0950cca0744efa20241dbba1563c0260cf78d0dc9885b048'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01c10abb2b78eb1685aac1b58d038756d058d9850dd186a14d3b49b07a37e652'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3885 | 0.00152 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01c10abb2b78eb1685aac1b58d038756d058d9850dd186a14d3b49b07a37e652'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['01c10abb2b78eb1685aac1b58d038756d058d9850dd186a14d3b49b07a37e652'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['b8176945-be57-418d-9e6f-252005241b06']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5288 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00141 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_94']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.6e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.98e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3d6be46fcf390d37b02b8726d4ca5c2f3de3af712e250f6503619d67b8db84f8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4364 | 0.00171 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3d6be46fcf390d37b02b8726d4ca5c2f3de3af712e250f6503619d67b8db84f8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3d6be46fcf390d37b02b8726d4ca5c2f3de3af712e250f6503619d67b8db84f8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['476fc3de3c09550def90eadba4db936341f1d764239dafc4fdf8fadba4374f25'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3333 | 0.00131 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['476fc3de3c09550def90eadba4db936341f1d764239dafc4fdf8fadba4374f25'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['476fc3de3c09550def90eadba4db936341f1d764239dafc4fdf8fadba4374f25'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5fa96c5945d6a657f9cdfd06ec31edb3248dc7889953cf4f71b37d365ebe8e15'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3873 | 0.00152 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5fa96c5945d6a657f9cdfd06ec31edb3248dc7889953cf4f71b37d365ebe8e15'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5fa96c5945d6a657f9cdfd06ec31edb3248dc7889953cf4f71b37d365ebe8e15'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c17acd1b-987b-4483-965c-adf96b2c724e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5259 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_95']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 5.34e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.83e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7ca3f90283c949fb9e0f5b644c83e74214a03f9da7f6c520ef6c8b2d4254cb8e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4264 | 0.00167 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7ca3f90283c949fb9e0f5b644c83e74214a03f9da7f6c520ef6c8b2d4254cb8e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7ca3f90283c949fb9e0f5b644c83e74214a03f9da7f6c520ef6c8b2d4254cb8e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['512f0dfa-bac4-4669-9a27-ad2599643ca9']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5269 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00159 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.0049 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_680d6a7d7339067f'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1528 | 0.000599 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_680d6a7d7339067f'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_680d6a7d7339067f'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_96']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.76e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['18fe166f8d30d767fbaf1bc39a43b954a0d6f7d96da27e88458ff0e4928a7718'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2182 | 0.000856 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['18fe166f8d30d767fbaf1bc39a43b954a0d6f7d96da27e88458ff0e4928a7718'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['18fe166f8d30d767fbaf1bc39a43b954a0d6f7d96da27e88458ff0e4928a7718'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['680d6a7d7339067f49adf3cab26d5bfc86c5caf74113f71846a477aefe4996ac'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2182 | 0.000856 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['680d6a7d7339067f49adf3cab26d5bfc86c5caf74113f71846a477aefe4996ac'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['680d6a7d7339067f49adf3cab26d5bfc86c5caf74113f71846a477aefe4996ac'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9c81edfd65bd7ff5421428ef509f1dbb76c4a12cb4cd2b42ddee0ae5fd5462ad'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2774 | 0.00109 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9c81edfd65bd7ff5421428ef509f1dbb76c4a12cb4cd2b42ddee0ae5fd5462ad'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9c81edfd65bd7ff5421428ef509f1dbb76c4a12cb4cd2b42ddee0ae5fd5462ad'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e13227e9-8a65-410f-9129-05749674fc86']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00131 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_97']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.62e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 4.96e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['029e96af7033878161619a59bc22a9e2109b8bf86561ae3a65b2e0755a1336ce'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4264 | 0.00167 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['029e96af7033878161619a59bc22a9e2109b8bf86561ae3a65b2e0755a1336ce'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['029e96af7033878161619a59bc22a9e2109b8bf86561ae3a65b2e0755a1336ce'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f01076540f0bf411d03df6d78baf230d8a70888d3b2753e257da02fa03ac60df'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3162 | 0.00124 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f01076540f0bf411d03df6d78baf230d8a70888d3b2753e257da02fa03ac60df'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f01076540f0bf411d03df6d78baf230d8a70888d3b2753e257da02fa03ac60df'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['90c7d181-7812-4bd3-99c8-02b66c28a427']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5267 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00134 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1ec03ae70aa132be'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3055 | 0.0012 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1ec03ae70aa132be'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_1ec03ae70aa132be'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_98']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.89e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9240b2c1974392807242126ec6ae6feac601d71198a93552d053a2803bed1fd8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9240b2c1974392807242126ec6ae6feac601d71198a93552d053a2803bed1fd8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9240b2c1974392807242126ec6ae6feac601d71198a93552d053a2803bed1fd8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1ec03ae70aa132bed481d15757e9a7665966bdfeb968947edb3edd072734d879'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4364 | 0.00171 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1ec03ae70aa132bed481d15757e9a7665966bdfeb968947edb3edd072734d879'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1ec03ae70aa132bed481d15757e9a7665966bdfeb968947edb3edd072734d879'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b52545bf29a20cf8b6d600b1d9bf17059858960e84bb0f3dbf051dfa0e361787'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3015 | 0.00118 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b52545bf29a20cf8b6d600b1d9bf17059858960e84bb0f3dbf051dfa0e361787'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b52545bf29a20cf8b6d600b1d9bf17059858960e84bb0f3dbf051dfa0e361787'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c6168010-9363-4e6b-83a2-6f768f91cc3e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5265 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0015 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_99']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.87e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 5.02e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2cd53f789bfa6962306d86d41df4f689197425f91384b8473c6fbc92b22fe53d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.25 | 0.00098 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2cd53f789bfa6962306d86d41df4f689197425f91384b8473c6fbc92b22fe53d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2cd53f789bfa6962306d86d41df4f689197425f91384b8473c6fbc92b22fe53d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['88ad890e51be995fa2393be45f5af067d36a22fc5d59c8e43699e3e1d2664af8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['88ad890e51be995fa2393be45f5af067d36a22fc5d59c8e43699e3e1d2664af8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['88ad890e51be995fa2393be45f5af067d36a22fc5d59c8e43699e3e1d2664af8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2305252a-689f-4745-a8af-a4c7779194ee']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5271 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00156 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_100']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.61e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.98e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3a1d313067ede917e88475fa893a4ee777d031b29861dbd510668cb2d54fe920'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3a1d313067ede917e88475fa893a4ee777d031b29861dbd510668cb2d54fe920'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3a1d313067ede917e88475fa893a4ee777d031b29861dbd510668cb2d54fe920'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['541cbdf29ca18ce0d0d4a29752323b4e5bc2dc7306526bec8dccee671d8e00ee'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3612 | 0.00142 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['541cbdf29ca18ce0d0d4a29752323b4e5bc2dc7306526bec8dccee671d8e00ee'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['541cbdf29ca18ce0d0d4a29752323b4e5bc2dc7306526bec8dccee671d8e00ee'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['22c95512de07bfafac7ff87a0510592e55c1203aec6c6071f799e9480714faf4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4303 | 0.00169 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['22c95512de07bfafac7ff87a0510592e55c1203aec6c6071f799e9480714faf4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['22c95512de07bfafac7ff87a0510592e55c1203aec6c6071f799e9480714faf4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f9845a9920b6c5a65122b27a829cc23945052dcfb609bfa63ca65f469322996d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4121 | 0.00162 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f9845a9920b6c5a65122b27a829cc23945052dcfb609bfa63ca65f469322996d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f9845a9920b6c5a65122b27a829cc23945052dcfb609bfa63ca65f469322996d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['d19d260a-8767-4959-ab41-935459bedf68']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5278 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00138 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_101']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 2.27e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 5.24e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ac876d9679b57e96fb296095e0c1e52249138f66ce12f36b50b04bba3fd1862b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6255 | 0.00245 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ac876d9679b57e96fb296095e0c1e52249138f66ce12f36b50b04bba3fd1862b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ac876d9679b57e96fb296095e0c1e52249138f66ce12f36b50b04bba3fd1862b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2866ca7f5359517e47694b217350c44c22e8d0efacad85dbd6169ad7956e47b9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6667 | 0.00261 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2866ca7f5359517e47694b217350c44c22e8d0efacad85dbd6169ad7956e47b9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2866ca7f5359517e47694b217350c44c22e8d0efacad85dbd6169ad7956e47b9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8566bedd96e2833593d2c6e4da1dd531059abfbaa9b4ebad67b4f2a1fd1232ea'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8566bedd96e2833593d2c6e4da1dd531059abfbaa9b4ebad67b4f2a1fd1232ea'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8566bedd96e2833593d2c6e4da1dd531059abfbaa9b4ebad67b4f2a1fd1232ea'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['fa5490cb-d769-43d5-b2d4-0b3421856da3']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5261 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_b523422294b1ed59'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2858 | 0.00112 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_b523422294b1ed59'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_b523422294b1ed59'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_102']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.54e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['87b29cd3fb7cb939b7c548ec7f3a5332489a72d39623ac7fbf140b18ee4f40dc'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['87b29cd3fb7cb939b7c548ec7f3a5332489a72d39623ac7fbf140b18ee4f40dc'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['87b29cd3fb7cb939b7c548ec7f3a5332489a72d39623ac7fbf140b18ee4f40dc'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b523422294b1ed59e938cc0aa3d30a9dc1a73afc4d7e01c84e2d7bf290a1be3b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b523422294b1ed59e938cc0aa3d30a9dc1a73afc4d7e01c84e2d7bf290a1be3b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b523422294b1ed59e938cc0aa3d30a9dc1a73afc4d7e01c84e2d7bf290a1be3b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d5f4bc7178d844047957971929237bb4a3e39064e6a73a67e95617772f26b04'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3162 | 0.00124 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d5f4bc7178d844047957971929237bb4a3e39064e6a73a67e95617772f26b04'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d5f4bc7178d844047957971929237bb4a3e39064e6a73a67e95617772f26b04'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['670d4174-185e-47d1-963a-3c2ba9cbdcf7']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5277 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00129 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_103']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.15e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.82e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ab10b9317fc5c92df65e7575321426e6b03690f3d514e274bac8d5132a7793b7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3162 | 0.00124 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ab10b9317fc5c92df65e7575321426e6b03690f3d514e274bac8d5132a7793b7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['ab10b9317fc5c92df65e7575321426e6b03690f3d514e274bac8d5132a7793b7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['f2b09491-8f96-407a-8119-b399a2543a8b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00154 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4d4e645890e3497e'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.26 | 0.00102 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4d4e645890e3497e'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4d4e645890e3497e'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_104']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 3.69e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.77e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f225bef6f068c530618137e4008f2ef71bd141100d6247b3d01ed12ff4d6411a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5222 | 0.00205 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f225bef6f068c530618137e4008f2ef71bd141100d6247b3d01ed12ff4d6411a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f225bef6f068c530618137e4008f2ef71bd141100d6247b3d01ed12ff4d6411a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d4e645890e3497e1944c29b40c8656aaa8c2a0ca3dec576312e1095d3babb6a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d4e645890e3497e1944c29b40c8656aaa8c2a0ca3dec576312e1095d3babb6a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d4e645890e3497e1944c29b40c8656aaa8c2a0ca3dec576312e1095d3babb6a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['ec623745-3529-42f3-b85f-7b92d7310b67']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5292 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00162 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.25 | 0.0049 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_105']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 2.1e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 5.33e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['67fbae7ca34df72008a505693a0975e57fd6c300e29cf50e68f7d5665bffb51b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3849 | 0.00151 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['67fbae7ca34df72008a505693a0975e57fd6c300e29cf50e68f7d5665bffb51b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['67fbae7ca34df72008a505693a0975e57fd6c300e29cf50e68f7d5665bffb51b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['194d20fb2d8adfcc91133d143786998fdc1847f3d391836b7d4c4405dda491fe'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2774 | 0.00109 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['194d20fb2d8adfcc91133d143786998fdc1847f3d391836b7d4c4405dda491fe'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['194d20fb2d8adfcc91133d143786998fdc1847f3d391836b7d4c4405dda491fe'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c7e41222-c6f0-4705-b30c-9698df354639']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5288 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_3356a1112d7d6359'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3395 | 0.00133 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_3356a1112d7d6359'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_3356a1112d7d6359'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_106']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 2.21e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 4.71e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7d088bb89a587ec1cdc0d5b8815a188cd8c466018fc79b1ed877174ccff2c0c1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.465 | 0.00182 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7d088bb89a587ec1cdc0d5b8815a188cd8c466018fc79b1ed877174ccff2c0c1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7d088bb89a587ec1cdc0d5b8815a188cd8c466018fc79b1ed877174ccff2c0c1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3356a1112d7d63591ee6828ae92bdbf0970ab56cf646e56bf72d823fdded6635'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4851 | 0.0019 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3356a1112d7d63591ee6828ae92bdbf0970ab56cf646e56bf72d823fdded6635'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3356a1112d7d63591ee6828ae92bdbf0970ab56cf646e56bf72d823fdded6635'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['46a0533e-34fd-4d63-a8ed-bb68241b20d7']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5284 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00123 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_107']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.87e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.53e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['539b2cf4e9c665965ec65f22e5ffeb13741482b1547f186e36bd89377c29eedc'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4629 | 0.00182 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['539b2cf4e9c665965ec65f22e5ffeb13741482b1547f186e36bd89377c29eedc'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['539b2cf4e9c665965ec65f22e5ffeb13741482b1547f186e36bd89377c29eedc'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f48109d8ddf2871ab032fbe5fe47c92ce931b67af1ab01682c351087a60da12f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.305 | 0.0012 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f48109d8ddf2871ab032fbe5fe47c92ce931b67af1ab01682c351087a60da12f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f48109d8ddf2871ab032fbe5fe47c92ce931b67af1ab01682c351087a60da12f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9b1ca72bdd9fa182c3d965daab60c1a380982fb4d52621018b48cbee51f7338'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4472 | 0.00175 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9b1ca72bdd9fa182c3d965daab60c1a380982fb4d52621018b48cbee51f7338'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c9b1ca72bdd9fa182c3d965daab60c1a380982fb4d52621018b48cbee51f7338'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['63fdc1b5ec0cb051cb3bb264c009ef890e686b0035ee06961ff601330ec75894'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5934 | 0.00233 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['63fdc1b5ec0cb051cb3bb264c009ef890e686b0035ee06961ff601330ec75894'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['63fdc1b5ec0cb051cb3bb264c009ef890e686b0035ee06961ff601330ec75894'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['c9b729b5-bdf8-47c5-92b6-0008b080774b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00155 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.251 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_79c3ff2a1ad98c2b'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3212 | 0.00126 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_79c3ff2a1ad98c2b'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_79c3ff2a1ad98c2b'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_108']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 3.78e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e8474e6a35cae908b30aecb6d427395c758e7d2482f4ca2cc88aa94ae6044360'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e8474e6a35cae908b30aecb6d427395c758e7d2482f4ca2cc88aa94ae6044360'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e8474e6a35cae908b30aecb6d427395c758e7d2482f4ca2cc88aa94ae6044360'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['79c3ff2a1ad98c2be3cef5d7646812791cc01c156e171fb87f4cf3a1fa128612'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['79c3ff2a1ad98c2be3cef5d7646812791cc01c156e171fb87f4cf3a1fa128612'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['79c3ff2a1ad98c2be3cef5d7646812791cc01c156e171fb87f4cf3a1fa128612'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c6256240663598fd5b62ac71f3509d6c960b9a34e46ded37018a173f3931842c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5547 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c6256240663598fd5b62ac71f3509d6c960b9a34e46ded37018a173f3931842c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c6256240663598fd5b62ac71f3509d6c960b9a34e46ded37018a173f3931842c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['946e50d625933bf7e957880771d3d38f330d817dc1cf265b7122414c044c30fe'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4264 | 0.00167 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['946e50d625933bf7e957880771d3d38f330d817dc1cf265b7122414c044c30fe'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['946e50d625933bf7e957880771d3d38f330d817dc1cf265b7122414c044c30fe'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['9302db89-ebd6-4bf7-b82a-ab2cff9f95f3']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5277 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0014 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_109']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.51e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.87e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['739c981afe4feed0cad2a8b0a6d4886ed9aa009b20ccf9c32f48dd0e0264fdb3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5222 | 0.00205 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['739c981afe4feed0cad2a8b0a6d4886ed9aa009b20ccf9c32f48dd0e0264fdb3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['739c981afe4feed0cad2a8b0a6d4886ed9aa009b20ccf9c32f48dd0e0264fdb3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['108140fd1515df477b0d91a29d30f23edd01aff852cde24ef7d9c22b07212466'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6255 | 0.00245 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['108140fd1515df477b0d91a29d30f23edd01aff852cde24ef7d9c22b07212466'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['108140fd1515df477b0d91a29d30f23edd01aff852cde24ef7d9c22b07212466'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['a0d3a2e5-a42d-4513-9eca-b51fc401bc20']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5272 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fedde4d325a932ee'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.324 | 0.00127 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fedde4d325a932ee'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_fedde4d325a932ee'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_110']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01291 | 3.9e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['728808fbea7de5b7f3521b148ee342cb25e081add56b23b8c4b82bdfba1809b9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4629 | 0.00182 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['728808fbea7de5b7f3521b148ee342cb25e081add56b23b8c4b82bdfba1809b9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['728808fbea7de5b7f3521b148ee342cb25e081add56b23b8c4b82bdfba1809b9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fedde4d325a932ee71ac31d21e33e195f33cd7df13de3a8380d6e45dd0bbfed2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4629 | 0.00182 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fedde4d325a932ee71ac31d21e33e195f33cd7df13de3a8380d6e45dd0bbfed2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fedde4d325a932ee71ac31d21e33e195f33cd7df13de3a8380d6e45dd0bbfed2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4bce9b0eed75b12dbf717c35452c0305799edd4cf4ec947ff2f0741fdf339c9e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5303 | 0.00208 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4bce9b0eed75b12dbf717c35452c0305799edd4cf4ec947ff2f0741fdf339c9e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4bce9b0eed75b12dbf717c35452c0305799edd4cf4ec947ff2f0741fdf339c9e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['8481cddf-1ed4-48a6-8d0a-6ef205ac04bc']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5266 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_83eb105175530928'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2475 | 0.000971 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_83eb105175530928'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_83eb105175530928'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_111']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.51e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.93e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2d71fa1ccdb917739c029065429905d5382c3daf79b2622166caa27246a3fa7d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2d71fa1ccdb917739c029065429905d5382c3daf79b2622166caa27246a3fa7d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2d71fa1ccdb917739c029065429905d5382c3daf79b2622166caa27246a3fa7d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['83eb105175530928ccd2cfad056949741ad0ae3ca68bba180618012f6353831c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['83eb105175530928ccd2cfad056949741ad0ae3ca68bba180618012f6353831c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['83eb105175530928ccd2cfad056949741ad0ae3ca68bba180618012f6353831c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['031b03009d294e4bb1ab0485ee0c0796d6573aff032fad25ab7b1ca31d2325a2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4714 | 0.00185 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['031b03009d294e4bb1ab0485ee0c0796d6573aff032fad25ab7b1ca31d2325a2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['031b03009d294e4bb1ab0485ee0c0796d6573aff032fad25ab7b1ca31d2325a2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['8cac8430-c667-49c7-911b-61fd651752d4']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00132 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_112']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.27e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.76e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['34f3f8b81fd2b73ef788031d119f21dbf10bb2f57b144c390517f824187e46a6'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['34f3f8b81fd2b73ef788031d119f21dbf10bb2f57b144c390517f824187e46a6'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['34f3f8b81fd2b73ef788031d119f21dbf10bb2f57b144c390517f824187e46a6'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['d4a45838-fabd-43f8-a983-1ceb07c1a03f']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5271 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00166 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.25 | 0.0049 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_231811a2598b54c0'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3055 | 0.0012 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_231811a2598b54c0'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_231811a2598b54c0'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_113']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.06e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.66e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['afa6fdc834df69dd0560e599e34d940723adf06b1e4da8691482ebb3950675e9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.417 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['afa6fdc834df69dd0560e599e34d940723adf06b1e4da8691482ebb3950675e9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['afa6fdc834df69dd0560e599e34d940723adf06b1e4da8691482ebb3950675e9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['231811a2598b54c01f3565aed85e8fdffbb2d81c95113f9b7a8dc3699faaba87'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4364 | 0.00171 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['231811a2598b54c01f3565aed85e8fdffbb2d81c95113f9b7a8dc3699faaba87'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['231811a2598b54c01f3565aed85e8fdffbb2d81c95113f9b7a8dc3699faaba87'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['838d0969d09d91e6459368267728607fe263ac7879c7264775a5cca1289e1a88'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5547 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['838d0969d09d91e6459368267728607fe263ac7879c7264775a5cca1289e1a88'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['838d0969d09d91e6459368267728607fe263ac7879c7264775a5cca1289e1a88'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['f5427b86-2423-40d8-891a-9ce9a5f53d6d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5281 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_35e8b6c8abc10a8d'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2646 | 0.00104 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_35e8b6c8abc10a8d'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_35e8b6c8abc10a8d'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_114']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 2.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01292 | 5.03e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7b5cdc6cfd2b97e9f1107f2bb66fe7e6087a4a40e1a55fd8004a221c7da7f4f5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7b5cdc6cfd2b97e9f1107f2bb66fe7e6087a4a40e1a55fd8004a221c7da7f4f5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7b5cdc6cfd2b97e9f1107f2bb66fe7e6087a4a40e1a55fd8004a221c7da7f4f5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['35e8b6c8abc10a8daec3e94a8146ea92b4dea7d857a3b19f5f6838c68f3e9681'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.378 | 0.00148 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['35e8b6c8abc10a8daec3e94a8146ea92b4dea7d857a3b19f5f6838c68f3e9681'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['35e8b6c8abc10a8daec3e94a8146ea92b4dea7d857a3b19f5f6838c68f3e9681'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['19c917fed95f59d67c6b75d0f421d74763f6e0a5035652977d7e0c9584304eb8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['19c917fed95f59d67c6b75d0f421d74763f6e0a5035652977d7e0c9584304eb8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['19c917fed95f59d67c6b75d0f421d74763f6e0a5035652977d7e0c9584304eb8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6c6e1571b62c54c68c377a00546234c4f95549c9f70565e6360035fdda5d01a7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3841 | 0.00151 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6c6e1571b62c54c68c377a00546234c4f95549c9f70565e6360035fdda5d01a7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6c6e1571b62c54c68c377a00546234c4f95549c9f70565e6360035fdda5d01a7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b3c5acd2d35efb924161b34a01d77215dd59da513374f80e8c2f201e281fd32b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b3c5acd2d35efb924161b34a01d77215dd59da513374f80e8c2f201e281fd32b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['b3c5acd2d35efb924161b34a01d77215dd59da513374f80e8c2f201e281fd32b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['857fac5e5085a159b06d02dd3779e91cff811992a361c23061f9398c6386f0f5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3288 | 0.00129 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['857fac5e5085a159b06d02dd3779e91cff811992a361c23061f9398c6386f0f5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['857fac5e5085a159b06d02dd3779e91cff811992a361c23061f9398c6386f0f5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['180f7c71-876b-48de-a33d-9e1f5e0c7d0b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5268 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00151 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_115']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.93e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['10530dfe756259d279d08fb7a9ad5a72b68da8fe95b2eef2d13f3a3ebae08c46'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3536 | 0.00139 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['10530dfe756259d279d08fb7a9ad5a72b68da8fe95b2eef2d13f3a3ebae08c46'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['10530dfe756259d279d08fb7a9ad5a72b68da8fe95b2eef2d13f3a3ebae08c46'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0afd08c413c9d13f664bf1f3551965d5998bc9bc12f0c7dbd552435895292b59'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.25 | 0.00098 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0afd08c413c9d13f664bf1f3551965d5998bc9bc12f0c7dbd552435895292b59'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0afd08c413c9d13f664bf1f3551965d5998bc9bc12f0c7dbd552435895292b59'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c090762990084ab0e10bd5c44a2a94fc6944df54e2cd12a8fbdc6a129e3b4ade'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5774 | 0.00226 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c090762990084ab0e10bd5c44a2a94fc6944df54e2cd12a8fbdc6a129e3b4ade'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c090762990084ab0e10bd5c44a2a94fc6944df54e2cd12a8fbdc6a129e3b4ade'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['33fd2294-a0b9-476c-b372-370a4dd2a6db']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5283 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00128 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4ab2e9a9ddb7ce3c'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2111 | 0.000828 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4ab2e9a9ddb7ce3c'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_4ab2e9a9ddb7ce3c'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_116']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.95e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.52e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e3e65aa97a091219d98753ec31936dcb3a7a51d8e1b70a3ae3029973cd7cb3ae'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3086 | 0.00121 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e3e65aa97a091219d98753ec31936dcb3a7a51d8e1b70a3ae3029973cd7cb3ae'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['e3e65aa97a091219d98753ec31936dcb3a7a51d8e1b70a3ae3029973cd7cb3ae'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4ab2e9a9ddb7ce3cdb24394db0589e629e82a60ef74de8154e5cc250447b3650'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3015 | 0.00118 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4ab2e9a9ddb7ce3cdb24394db0589e629e82a60ef74de8154e5cc250447b3650'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4ab2e9a9ddb7ce3cdb24394db0589e629e82a60ef74de8154e5cc250447b3650'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3d2f208ca051338ffda0f530d855db6e8233c9381c260cb65e8b190fe7e511b0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3d2f208ca051338ffda0f530d855db6e8233c9381c260cb65e8b190fe7e511b0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3d2f208ca051338ffda0f530d855db6e8233c9381c260cb65e8b190fe7e511b0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['ea057707-be4c-4c55-a1ee-02b2c68f7eac']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5277 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_9da8015f4babf31b'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2437 | 0.000956 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_9da8015f4babf31b'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_9da8015f4babf31b'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_117']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.2e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.36e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['854d61764876140eab1fb09b6edd843485bd6f23e7d9eb59145c13192abd9d8d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['854d61764876140eab1fb09b6edd843485bd6f23e7d9eb59145c13192abd9d8d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['854d61764876140eab1fb09b6edd843485bd6f23e7d9eb59145c13192abd9d8d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9da8015f4babf31b7522f0780c5c71184feb0e6bbbd0428a2b0d1607660694d8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3482 | 0.00137 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9da8015f4babf31b7522f0780c5c71184feb0e6bbbd0428a2b0d1607660694d8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9da8015f4babf31b7522f0780c5c71184feb0e6bbbd0428a2b0d1607660694d8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68e83117778ad7403e6738b746e06413120e6dd8c16f996e4f97c9138475b244'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68e83117778ad7403e6738b746e06413120e6dd8c16f996e4f97c9138475b244'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['68e83117778ad7403e6738b746e06413120e6dd8c16f996e4f97c9138475b244'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['deea0079-4ff1-4d38-ab52-16314f6547c2']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5275 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00152 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_118']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01292 | 4.9e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.51e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6778c724869926158eb0f166d5f1150eefcda2b74c3902214c4fe0073e95584f'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5222 | 0.00205 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6778c724869926158eb0f166d5f1150eefcda2b74c3902214c4fe0073e95584f'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6778c724869926158eb0f166d5f1150eefcda2b74c3902214c4fe0073e95584f'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['e052ba95-f9c6-4058-bb82-86d98783191b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5291 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00148 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_119']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.81e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.97e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9abafefb7f3aef28c829331cc960931a2e78703527f500d4bbca29b8d0b10f0e'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3592 | 0.00141 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9abafefb7f3aef28c829331cc960931a2e78703527f500d4bbca29b8d0b10f0e'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9abafefb7f3aef28c829331cc960931a2e78703527f500d4bbca29b8d0b10f0e'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fcbc7c886cd007bbc141206bb3dfd36f39d82e8cf3fb50e43d647611926a187a'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fcbc7c886cd007bbc141206bb3dfd36f39d82e8cf3fb50e43d647611926a187a'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fcbc7c886cd007bbc141206bb3dfd36f39d82e8cf3fb50e43d647611926a187a'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1263e40f-a1e4-4f64-b147-6c65f5b0f1e5']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5301 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00152 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_120']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 3.15e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.76e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5bc84bd44b15441b9a02f136dd1b344cecd578632495ae458be629dbbb3f8f1b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.417 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5bc84bd44b15441b9a02f136dd1b344cecd578632495ae458be629dbbb3f8f1b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5bc84bd44b15441b9a02f136dd1b344cecd578632495ae458be629dbbb3f8f1b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1d4b6920e532caf2a6e005d51dba2ce94c96afcd5ed731c369613f0ff5d748f8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4851 | 0.0019 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1d4b6920e532caf2a6e005d51dba2ce94c96afcd5ed731c369613f0ff5d748f8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['1d4b6920e532caf2a6e005d51dba2ce94c96afcd5ed731c369613f0ff5d748f8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1d32c407-2448-4f40-91b8-03849c6c78ee']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.527 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0014 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_121']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.12e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.58e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6a7d3c744c6619e6fd3753ce0a56a237627aef8c7987c21bd1f2dd49f609cb65'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4009 | 0.00157 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6a7d3c744c6619e6fd3753ce0a56a237627aef8c7987c21bd1f2dd49f609cb65'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6a7d3c744c6619e6fd3753ce0a56a237627aef8c7987c21bd1f2dd49f609cb65'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['56322b069966255b66d8ed2ebf5a31801fc86b103b5ae29ce2cde302dc1c5182'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3333 | 0.00131 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['56322b069966255b66d8ed2ebf5a31801fc86b103b5ae29ce2cde302dc1c5182'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['56322b069966255b66d8ed2ebf5a31801fc86b103b5ae29ce2cde302dc1c5182'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3a99ae4c9b37e807a649e6ffe14ed21788cbe188454e01f583440033571245c3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5345 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3a99ae4c9b37e807a649e6ffe14ed21788cbe188454e01f583440033571245c3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['3a99ae4c9b37e807a649e6ffe14ed21788cbe188454e01f583440033571245c3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d319bd527ee8bea7a795b72bc0e6ee3e0c0f121d5a8c6119f9d81500ee75da3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3203 | 0.00126 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d319bd527ee8bea7a795b72bc0e6ee3e0c0f121d5a8c6119f9d81500ee75da3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4d319bd527ee8bea7a795b72bc0e6ee3e0c0f121d5a8c6119f9d81500ee75da3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['09d00e95-61b4-4b50-a452-b03efcf212a3']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5295 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_122']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.07e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.55e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['13574cbd76094567c3a25f8fd22cd24c9f8cbde98e259c22114e5bb6a25db7d1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6576 | 0.00258 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['13574cbd76094567c3a25f8fd22cd24c9f8cbde98e259c22114e5bb6a25db7d1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['13574cbd76094567c3a25f8fd22cd24c9f8cbde98e259c22114e5bb6a25db7d1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['43d5a5c25a763f0f9aec54c492cd88906ab0568717f1d2abe510b01a7e83bd08'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6255 | 0.00245 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['43d5a5c25a763f0f9aec54c492cd88906ab0568717f1d2abe510b01a7e83bd08'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['43d5a5c25a763f0f9aec54c492cd88906ab0568717f1d2abe510b01a7e83bd08'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['17efcdaa68f116f6bf97579b1067e6fb4456bc7319a8c657601e8246c36e95bb'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3849 | 0.00151 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['17efcdaa68f116f6bf97579b1067e6fb4456bc7319a8c657601e8246c36e95bb'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['17efcdaa68f116f6bf97579b1067e6fb4456bc7319a8c657601e8246c36e95bb'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['4aeae174-6075-4754-bfd1-7187b345314f']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5288 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00151 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_123']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 2.44e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.67e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a475f6b4a54e960983fb1eb3e23a048a446a0c9f58e7ee7b1f9024c08927da41'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5 | 0.00196 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a475f6b4a54e960983fb1eb3e23a048a446a0c9f58e7ee7b1f9024c08927da41'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a475f6b4a54e960983fb1eb3e23a048a446a0c9f58e7ee7b1f9024c08927da41'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['19e208ff125736813f7427da96781674519b9aec4a3e0f9ec75d99d99da720b7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3922 | 0.00154 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['19e208ff125736813f7427da96781674519b9aec4a3e0f9ec75d99d99da720b7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['19e208ff125736813f7427da96781674519b9aec4a3e0f9ec75d99d99da720b7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['542b3072-ca0a-4a00-a89e-32652b318343']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5268 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00147 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_124']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.73e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.93e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5f43bfd1c6f0336924f28f483bbd8d7ee48d8e356f7958c705069344b67aa356'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4264 | 0.00167 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5f43bfd1c6f0336924f28f483bbd8d7ee48d8e356f7958c705069344b67aa356'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5f43bfd1c6f0336924f28f483bbd8d7ee48d8e356f7958c705069344b67aa356'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8045046aeece3101ebafed34b744d9bdff48d556f2346ebd573e2b54e928cc4d'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3162 | 0.00124 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8045046aeece3101ebafed34b744d9bdff48d556f2346ebd573e2b54e928cc4d'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8045046aeece3101ebafed34b744d9bdff48d556f2346ebd573e2b54e928cc4d'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['1fc4e3be-f262-4a6f-a86b-6b8badb86d73']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5275 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00136 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0876e88262b5babf'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2135 | 0.000837 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0876e88262b5babf'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_0876e88262b5babf'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_125']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.71e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.69e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['20f2312e196463416d689ca0d235b5f90ba46b668a4ca313279dda1b07a249e4'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.305 | 0.0012 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['20f2312e196463416d689ca0d235b5f90ba46b668a4ca313279dda1b07a249e4'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['20f2312e196463416d689ca0d235b5f90ba46b668a4ca313279dda1b07a249e4'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0876e88262b5babf60d68ed6fe1f81b8b38691cec2260ed2316e819875e34255'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.305 | 0.0012 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0876e88262b5babf60d68ed6fe1f81b8b38691cec2260ed2316e819875e34255'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['0876e88262b5babf60d68ed6fe1f81b8b38691cec2260ed2316e819875e34255'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['ebf500d9-6793-4d3e-b521-4f42744682a6']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5275 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.0015 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6f5ae7c4beeb672e'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3166 | 0.00124 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6f5ae7c4beeb672e'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6f5ae7c4beeb672e'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_126']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.86e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.87e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['45529811c807e0d5be5c94a1bb5c11d4ac8bd8b21943364be261a5d7db6ba5d0'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4523 | 0.00177 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['45529811c807e0d5be5c94a1bb5c11d4ac8bd8b21943364be261a5d7db6ba5d0'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['45529811c807e0d5be5c94a1bb5c11d4ac8bd8b21943364be261a5d7db6ba5d0'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6f5ae7c4beeb672e2eca5c56ecebb8e3ab1d81d3c38cae004c9c454a0c0a1263'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4523 | 0.00177 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6f5ae7c4beeb672e2eca5c56ecebb8e3ab1d81d3c38cae004c9c454a0c0a1263'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6f5ae7c4beeb672e2eca5c56ecebb8e3ab1d81d3c38cae004c9c454a0c0a1263'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['39a61a84cd0301111e3db770f49e753410c078e9844dde75e65fb60622bf3c32'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5477 | 0.00215 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['39a61a84cd0301111e3db770f49e753410c078e9844dde75e65fb60622bf3c32'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['39a61a84cd0301111e3db770f49e753410c078e9844dde75e65fb60622bf3c32'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['4da13193-f0e9-4b4a-8d8b-426b7d1d0833']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.527 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00139 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5b5c028ee3686f65'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.39 | 0.00153 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5b5c028ee3686f65'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_5b5c028ee3686f65'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_127']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.76e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.85e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['155967ff56c078f734a285434ce9323164484599a33892573b50479044a22c6c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.417 | 0.00164 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['155967ff56c078f734a285434ce9323164484599a33892573b50479044a22c6c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['155967ff56c078f734a285434ce9323164484599a33892573b50479044a22c6c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5b5c028ee3686f651fa90037a0007406a290341c9977044cb21349bea3616347'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5571 | 0.00218 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5b5c028ee3686f651fa90037a0007406a290341c9977044cb21349bea3616347'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5b5c028ee3686f651fa90037a0007406a290341c9977044cb21349bea3616347'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['baf28e1105e83bc5598bff80f9b7e67388291e5c7111fab1ffad2d565c53e7b2'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.603 | 0.00236 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['baf28e1105e83bc5598bff80f9b7e67388291e5c7111fab1ffad2d565c53e7b2'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['baf28e1105e83bc5598bff80f9b7e67388291e5c7111fab1ffad2d565c53e7b2'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['a5ed8367-993c-42ed-b769-b82d55d0ed0b']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00119 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.256 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c5c6e34114cf8c7d'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1373 | 0.000538 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c5c6e34114cf8c7d'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_c5c6e34114cf8c7d'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_128']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.0129 | 4.47e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.73e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['621bc45dbc8bf1ea12892fe33f70c0186807bf290e1aab73fdbfe0bf2cfa48f3'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3651 | 0.00143 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['621bc45dbc8bf1ea12892fe33f70c0186807bf290e1aab73fdbfe0bf2cfa48f3'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['621bc45dbc8bf1ea12892fe33f70c0186807bf290e1aab73fdbfe0bf2cfa48f3'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c5c6e34114cf8c7d38b6629d0e4217c19f706ee7ea586b91f5bfad8482d43da7'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.1961 | 0.000769 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c5c6e34114cf8c7d38b6629d0e4217c19f706ee7ea586b91f5bfad8482d43da7'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c5c6e34114cf8c7d38b6629d0e4217c19f706ee7ea586b91f5bfad8482d43da7'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['41dd6c0dca8eedd14c1aa42fec8fd9b8c08d16551cd32e36c4da55648cbc50e9'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2357 | 0.000924 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['41dd6c0dca8eedd14c1aa42fec8fd9b8c08d16551cd32e36c4da55648cbc50e9'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['41dd6c0dca8eedd14c1aa42fec8fd9b8c08d16551cd32e36c4da55648cbc50e9'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8c6c3f53f1ff5387773fbf2567d65fb520e3d4f77c1d664031c5f3f9a2cb00b5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8c6c3f53f1ff5387773fbf2567d65fb520e3d4f77c1d664031c5f3f9a2cb00b5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['8c6c3f53f1ff5387773fbf2567d65fb520e3d4f77c1d664031c5f3f9a2cb00b5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9cbffc7700f5cdb2d9e06b2bb7d60dd6b79034d4e30edbf70cf7ba586dd7c08c'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4364 | 0.00171 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9cbffc7700f5cdb2d9e06b2bb7d60dd6b79034d4e30edbf70cf7ba586dd7c08c'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9cbffc7700f5cdb2d9e06b2bb7d60dd6b79034d4e30edbf70cf7ba586dd7c08c'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a7bd2557e523bbc4df373cb75745f42d8515c54363b399597ee5f36480c59934'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5345 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a7bd2557e523bbc4df373cb75745f42d8515c54363b399597ee5f36480c59934'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['a7bd2557e523bbc4df373cb75745f42d8515c54363b399597ee5f36480c59934'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['6df246af-0872-4b76-a2a8-787ef2d72ea5']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00129 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.254 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_129']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.96e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 4.69e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cf7cfe66421e668a19812b0526ee50b0f1b292aa955b59d3b1f992278267c5b5'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2425 | 0.000951 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cf7cfe66421e668a19812b0526ee50b0f1b292aa955b59d3b1f992278267c5b5'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['cf7cfe66421e668a19812b0526ee50b0f1b292aa955b59d3b1f992278267c5b5'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7d1638d2cacdba70b22acf603988cc80e25f98647936de859fe06126fe630cc8'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3333 | 0.00131 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7d1638d2cacdba70b22acf603988cc80e25f98647936de859fe06126fe630cc8'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7d1638d2cacdba70b22acf603988cc80e25f98647936de859fe06126fe630cc8'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4af3011d4130acf241740e7f739c9839b80189229c97cac4e2149aa8ecf75448'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3288 | 0.00129 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4af3011d4130acf241740e7f739c9839b80189229c97cac4e2149aa8ecf75448'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4af3011d4130acf241740e7f739c9839b80189229c97cac4e2149aa8ecf75448'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['62f378d1-24d1-4f8e-b5db-905dad40d076']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5273 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00146 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_130']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.15e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 3.8e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['048bcfef38f9b3afe6ee7cbe2b2776efbef08887d352e23ba27b87cb41563802'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4588 | 0.0018 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['048bcfef38f9b3afe6ee7cbe2b2776efbef08887d352e23ba27b87cb41563802'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['048bcfef38f9b3afe6ee7cbe2b2776efbef08887d352e23ba27b87cb41563802'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7979c949a201f03d657ff18a328cec812a5915e2e06830881478714a7743ef3b'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3333 | 0.00131 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7979c949a201f03d657ff18a328cec812a5915e2e06830881478714a7743ef3b'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['7979c949a201f03d657ff18a328cec812a5915e2e06830881478714a7743ef3b'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['f31fab0c-ad5e-49f1-9c29-f660ad64f14d']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5276 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00147 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_131']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.02e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.74e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f1bc9753de6172993fa046318c4aa06f7d40bef2bd6a2b081bec7434dccf78cc'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3714 | 0.00146 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f1bc9753de6172993fa046318c4aa06f7d40bef2bd6a2b081bec7434dccf78cc'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['f1bc9753de6172993fa046318c4aa06f7d40bef2bd6a2b081bec7434dccf78cc'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4156459c14fddbd3c48391e610cb3121003eff1163d97a74c01ce7f0520fe489'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2582 | 0.00101 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4156459c14fddbd3c48391e610cb3121003eff1163d97a74c01ce7f0520fe489'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['4156459c14fddbd3c48391e610cb3121003eff1163d97a74c01ce7f0520fe489'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['bf34adf9-b32c-4678-b4dd-c629e02c123f']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5274 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00141 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.253 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6712a64b24496043'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2985 | 0.00117 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6712a64b24496043'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_6712a64b24496043'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_132']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01287 | 4.9e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_136']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.85e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d5c77fb09a8bf7c46cbb107e5fa0f80f96f32637d0782940c47f80df9b220336'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4082 | 0.0016 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d5c77fb09a8bf7c46cbb107e5fa0f80f96f32637d0782940c47f80df9b220336'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['d5c77fb09a8bf7c46cbb107e5fa0f80f96f32637d0782940c47f80df9b220336'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6712a64b244960435ba410fc0ee9e91d9ac73cebe9e9fba682556aadfdad1bf1'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4264 | 0.00167 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6712a64b244960435ba410fc0ee9e91d9ac73cebe9e9fba682556aadfdad1bf1'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['6712a64b244960435ba410fc0ee9e91d9ac73cebe9e9fba682556aadfdad1bf1'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9aaf5cfeb8cf4a8ff3f45a8fe84eaf7f866dd10a014c4b96e5f6b40fba4cdd88'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5345 | 0.0021 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9aaf5cfeb8cf4a8ff3f45a8fe84eaf7f866dd10a014c4b96e5f6b40fba4cdd88'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['9aaf5cfeb8cf4a8ff3f45a8fe84eaf7f866dd10a014c4b96e5f6b40fba4cdd88'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['2bf866a7-ae03-43e5-8d81-25af58e7a515']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5268 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00149 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.252 | 0.00491 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_133']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01284 | 2.99e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_137']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01288 | 4.78e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5d5ea64051afa5fe0af50d68e50a8050aae65445daa8d171f067524a92647385'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3288 | 0.00129 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5d5ea64051afa5fe0af50d68e50a8050aae65445daa8d171f067524a92647385'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['5d5ea64051afa5fe0af50d68e50a8050aae65445daa8d171f067524a92647385'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe23de4863eab359ebf1c80abb7001905304677aaa7d4f55dfd491f24efe4a38'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4364 | 0.00171 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe23de4863eab359ebf1c80abb7001905304677aaa7d4f55dfd491f24efe4a38'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['fe23de4863eab359ebf1c80abb7001905304677aaa7d4f55dfd491f24efe4a38'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['3c5d8071-d86a-4148-b166-3eb739ef650e']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5287 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00127 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_42e49b9d11261a8e'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4427 | 0.00174 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_42e49b9d11261a8e'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_42e49b9d11261a8e'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_134']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01286 | 4.77e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_138']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.29e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['af4bac149d49c30e717368a86177cb1afeb403d8edb0511686c2fe5c65d35638'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4867 | 0.00191 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['af4bac149d49c30e717368a86177cb1afeb403d8edb0511686c2fe5c65d35638'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['af4bac149d49c30e717368a86177cb1afeb403d8edb0511686c2fe5c65d35638'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42e49b9d11261a8e8e0e71edf543b9af42c71d3f933305a738a57ae2ba9cf966'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.6325 | 0.00248 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42e49b9d11261a8e8e0e71edf543b9af42c71d3f933305a738a57ae2ba9cf966'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['42e49b9d11261a8e8e0e71edf543b9af42c71d3f933305a738a57ae2ba9cf966'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['950aca9fd9eefd366190b67ff8bbeec916c573a1378395e36f8af68adba48178'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.5669 | 0.00222 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['950aca9fd9eefd366190b67ff8bbeec916c573a1378395e36f8af68adba48178'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['950aca9fd9eefd366190b67ff8bbeec916c573a1378395e36f8af68adba48178'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['73af2669-bea3-411d-bf34-1b0710662bbf']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.528 | 0 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].tensor_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].error_preservation` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.02989 | 0.000113 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].base_phase` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.1251 | 0.000479 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].harmonic_amplitudes` | (2, 64) | rw_registry | buckets | codebook 0 | 8 | 0.1016 | 0.000395 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].frequencies` | (2,) | rw_registry | buckets | codebook 0 | 8 | 0.515 | 0.00127 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].phase_offsets` | (2,) | rw_registry | buckets | codebook 0 | 8 | 1.255 | 0.00492 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].base_delta` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].delta_adaptive_factor` | (64,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2959f02d734a5b69'].base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.2271 | 0.000891 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2959f02d734a5b69'].phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.rwa_store['rw_content_2959f02d734a5b69'].error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_135']._last_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01289 | 4.83e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_139']._ema_effective_weight` | (64,) | rw_registry | buckets | codebook 0 | 8 | 0.01285 | 4.7e-05 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].recursive_refs.0.relative_position` | (5,) | rw_registry | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.weight_registry._weights['evolution_cycle_140'].recursive_refs.0.transformation_matrix` | (64, 64) | rw_registry | buckets | codebook 0 | 8 | 1.013 | 0.00397 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c51a14d40387b4e323c3b7a2322ebf11e7bcf0bb8dc00b0f55d76e47a9daa328'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3333 | 0.00131 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c51a14d40387b4e323c3b7a2322ebf11e7bcf0bb8dc00b0f55d76e47a9daa328'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c51a14d40387b4e323c3b7a2322ebf11e7bcf0bb8dc00b0f55d76e47a9daa328'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2959f02d734a5b69fe1ab1570a3dade3589426f820bd71daa3e77327c6738b13'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3244 | 0.00127 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2959f02d734a5b69fe1ab1570a3dade3589426f820bd71daa3e77327c6738b13'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['2959f02d734a5b69fe1ab1570a3dade3589426f820bd71daa3e77327c6738b13'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['554f18bc196d436e3f664dbb0da5c92f1495701a186a0612c071c51f39d8b454'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.343 | 0.00135 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['554f18bc196d436e3f664dbb0da5c92f1495701a186a0612c071c51f39d8b454'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['554f18bc196d436e3f664dbb0da5c92f1495701a186a0612c071c51f39d8b454'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c6819fd887e8cae415989de426c3b1bcefa8979fbde0574833cb538914ac2dbe'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4851 | 0.0019 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c6819fd887e8cae415989de426c3b1bcefa8979fbde0574833cb538914ac2dbe'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['c6819fd887e8cae415989de426c3b1bcefa8979fbde0574833cb538914ac2dbe'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['12fe32e72140134a24929aa0292772c69e7c344a91f11809ed9caa6de7532d51'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.4804 | 0.00188 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['12fe32e72140134a24929aa0292772c69e7c344a91f11809ed9caa6de7532d51'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['12fe32e72140134a24929aa0292772c69e7c344a91f11809ed9caa6de7532d51'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['da6f121e18f517af04c21e512ee1ce1bd620ddba1575aaaf236e66ad41b612bf'].recursive_weight.base_representation` | (64,) | iala | buckets | codebook 0 | 8 | 0.3482 | 0.00137 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['da6f121e18f517af04c21e512ee1ce1bd620ddba1575aaaf236e66ad41b612bf'].recursive_weight.phase_transformation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `engine.autodidactic_learner.knowledge_graph.entities['da6f121e18f517af04c21e512ee1ce1bd620ddba1575aaaf236e66ad41b612bf'].recursive_weight.error_preservation` | (64,) | iala | buckets | codebook 0 | 8 | 1 | 0.00392 | 0 |
| `motivation.value_formation_system.patterns['104b0152-bc25-4d39-9da8-e7fe05c07940']` | (1,) | motivation | buckets | codebook 0 | 8 | 0.5266 | 0 | 0 |
