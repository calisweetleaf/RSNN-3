### LQT Binary File Format Specification (v1.3): Technical Reference for Systems Engineers

##### 1\. Architectural Foundation and Design Intent

The Liquid Quantized Format (LQT) is a high-performance binary container designed to transcend the limitations of "static artifact" formats like GGUF and ONNX. While traditional formats freeze weights into immutable blocks post-quantization, LQT treats model parameters as dynamic primitives. This architectural shift enables  **O(1) module swapping**  and  **zero-copy weight injection** , allowing models to evolve at runtime without the computationally expensive overhead of full re-quantization or total memory reloads.By utilizing a modular architecture anchored by the Recursive Tensor Architecture (RTA), LQT provides the infrastructure for self-modifying AI systems. The format preserves the mathematical integrity of weights while allowing surgical adjustments through delta buffers and codebook mutations.| Feature | GGUF/ONNX | LQT | Engineering Impact || \------ | \------ | \------ | \------ || **Editability** | Frozen | **Comprehensive** | Enables O(1) weight updates and runtime fine-tuning. || **Architecture** | Static | **Modular/DAG** | Supports zero-copy injection of hot-swappable modules. || **Foundation** | Dense/Sparse | **Recursive (RTA)** | Native hardware-accelerated fractal and self-referential logic. || **Mutability** | None | **Built-in Hooks** | Direct support for federated adaptation and self-modification. || **Sparsity** | Fixed/Optional | **Dynamic (90%)** | Targeted 90% sparsity reduces memory footprint by 35-65%. |  
The following sections define the low-level binary layout required to support these modular, evolving structures.

##### 2\. The Primary File Container: Header and Bitmask Definitions

The LQT file is accessed via a 32-byte fixed-size header. This entry point is designed for optimal memory-mapped (mmap) performance, allowing the parser to determine global state and segment offsets without traversing the entire file.

###### *Header Structure (32 bytes)*

Offset,Field Name,Type,Value / Description  
0x00,Magic,uint32,"0x4C515431 (""LQT1"" in ASCII)"  
0x04,Version,uint16,"0x0103 (Major 1, Minor 3: (1 \<\< 8\) \\| 3)"  
0x06,Flags,uint16,Global capability bitmask.  
0x08,Header Size,uint32,Fixed at 32 bytes (0x20).  
0x0C,Metadata Offset,uint64,Offset to the TLV Metadata Chunks.  
0x14,Tensor Offset,uint64,Offset to the Tensor Data Blobs.  
0x1C,Footer Offset,uint64,Offset to the 64-byte file footer.

###### *Flags Bitmask (uint16)*

* **Bit 0 (HAS\_DELTAS):**  High-precision adjustment buffers present.  
* **Bit 1 (HAS\_SPARSE\_MASKS):**  Pruning bitmasks included.  
* **Bit 2 (ALIGN\_64):**  Forces 64-byte alignment for SIMD-heavy sections.  
* **Bit 3 (BIG\_ENDIAN):**  Byte order indicator (1=Big, 0=Little).  
* **Bit 4 (SELF\_MODIFYING):**  Contains self-optimization logic.  
* **Bit 5 (SIGNED\_EDITS):**  Edit log utilizes cryptographic signatures.  
* **Bit 6 (COMPRESSED):**  Sections utilize Zlib/Lossless compression.  
* **Bit 7 (SHARDED):**  Model distributed across multiple files.  
* **Bits 8-15:**   **RESERVED**  for future protocol expansion.**System Impact:**  The ALIGN\_64 flag dictates whether the loader must enforce cache-line alignment for AVX/NEON operations, while the BIG\_ENDIAN flag ensures the parser handles cross-platform bit-ordering during weight reconstruction.

##### 3\. Type-Length-Value (TLV) Metadata System

LQT employs a Type-Length-Value (TLV) system to ensure forward compatibility and extreme extensibility. This layer contains the structural definitions of the model, including the  **Module Graph** , a JSON-like UTF-8 structure that defines the model's topology for module hot-swapping.

###### *TLV Entry Structure*

* **Type (uint16):**  2 bytes defining the chunk purpose.  
* **Length (uint32):**  4 bytes defining value size.  
* **Value (Variable):**  Data payload, padded to 4-byte alignment.

###### *Tensor Descriptor (The Logic Switch)*

The Tensor Descriptor includes the critical tensor\_type field, which acts as a switch for the reconstruction engine:

1. **Name:**  Variable string (UTF-8).  
2. **Tensor Type (uint8):**  0 \= Standard, 1 \= RecursiveTensor (RTA).  
3. **DType (uint8):**  Precision (FP16, INT8, etc.).  
4. **NDim (uint8):**  Rank of the tensor.  
5. **Shape:**  uint32ndim array.  
6. **IDs:**  uint16 links for codebook\_id, delta\_id, and sparse\_mask\_id.  
7. **Quantization Params:**  float32 scale and int32 zero\_point.

###### *Chunk Type Registry*

* **0x0001 Hyperparameters:**  Global model configurations.  
* **0x0002 Tensor Descriptor:**  Individual weight mapping and type flags.  
* **0x0003 Module Definitions:**  The Module Graph DAG for hot-swapping.  
* **0x0005 Codebook Table:**  Vector quantization lookup tables.  
* **0x0006 Delta Table:**  Sparse high-precision adjustment values.  
* **0x0012 Recursive Weight Metadata:**  Specialized chunk for RTA-specific configuration.**Efficiency Insight:**  Linkages within the metadata allow the engine to perform single-pass weight reconstruction, significantly reducing memory latency by fetching indices and deltas concurrently.

##### 4\. Recursive Tensor Architecture (RTA) Block Specifications

RTA blocks are specialized 5-dimensional storage units targeting a 90% sparsity threshold. They represent the core of LQT's "liquid" weights, allowing for self-referential patterns.

###### *RTA Internal Structure*

* **Magic Header:**  8-byte ASCII RTATNSR\\0.  
* **Metadata Block (TLV):**  An internal TLV block for tensor-local metadata (key-value pairs, UTF-8).  
* **Dimension Block (24 bytes):**  
* **Rank:**  Fixed at  **5** .  
* **Distribution (uint32):**  0=Normal, 1=Uniform, 2=Exponential, 3=Custom.  
* **Byte 17 (Flags):**  Bit 0 (Custom Dist), Bit 1 (Pattern Comp), Bit 2 (Quantized), Bit 3 (Self-Ref), Bit 4 (Fractal), Bit 5 (Double Precision).

###### *Sparsity & Indexing (Encoding Methods)*

LQT supports six specific encoding methods for sparse data (Offsets 0x00-0x05):

1. **0x00 Uniform:**  No density map required.  
2. **0x01 Per-Dimension:**  Individual density maps per axis.  
3. **0x02 Hierarchical:**  Multi-level density maps.  
4. **0x03 RLE:**  Run-Length Encoding for contiguous blocks.  
5. **0x04 Compressed Bitmap:**  Efficient for high-sparsity masks.  
6. **0x05 CSR/CSC/CSF:**  Compressed Sparse Row/Column/Fiber.

###### *Reference Block*

Contains  **Direct** ,  **Transformed**  (matrix-based), and  **Fractal**  (iterative) references. This allows a tensor to reuse its own internal structures, dramatically reducing file size while enabling complex iterative behaviors.**Performance Impact:**  RTA indexing achieves  $O(\\log n)$  lookup and  $O(k)$  iteration, where  $k$  is the number of non-zero elements, ensuring computational cost scales with active data rather than total tensor volume.

##### 5\. Five-Dimensional Semantic Logic and Recursive Operations

The RTA foundation is built upon a  **Mathematical Quintuple**  **$W \= \\{B, \\Phi, R, T, \\epsilon\\}**$ :

* **B (Base):**  Codebook indices.  
* **$\\Phi**$  **(Phase):**  Temporal/sequential modulation vectors.  
* **R (Reference):**  Recursive 3D reference matrix.  
* **T (Tensor Position):**  5D position embedding vector.  
* **$\\epsilon**$  **(Error):**  Residual error preservation term for high-fidelity reconstruction.

###### *The Semantic Dimensions*

* **d0 (Feature Space):**  Conceptual/embedding dimension.  
* **d1 (Pattern):**  Used for template matching and motif recognition.  
* **d2 (Temporal):**  Supports sequential and iterative recursive steps.  
* **d3 (Scale/Fractal):**  Enables multi-scale transformations and self-similarity.  
* **d4 (Channel):**  Handles multi-modal information streams.**Operations:**  Support for  **Project**  (dimensionality reduction),  **Contract**  (tensor fusion), and  **Fractal Iteration**  allows LQT to generate complex patterns from simple recursive rules. Dimension-aware quantization ensures these properties (like fractal self-similarity) are preserved even at 4-bit precision.

##### 6\. Quantization Mechanics: Codebooks and Delta Buffers

Weight reconstruction is a multi-stage process where base quantized indices are refined by high-precision sparse adjustments.

* **Codebooks:**  Support for  **Global** ,  **Local** ,  **Hierarchical** , and  **Expandable**  types. Expandable codebooks reserve entries for runtime evolution, allowing the model to learn new representations without structure changes.  
* **Delta Buffers:**  Store sparse FP16/FP32 adjustments.  
* **Multi-Stage Reconstruction:**  The engine reconstructs the base weight via codebook lookup and then applies the Delta adjustment. This allows for surgical "fine-tuning" of a model by simply updating the sparse Delta buffer or expanding the Codebook vector.**Architectural Trade-off:**  While this introduces a 3-5% inference penalty, it grants the system total runtime mutability—allowing weights to be updated via deltas without a model restart.

##### 7\. Memory Management and Concurrency Protocol

LQT is optimized for zero-copy mmap execution, with strict alignment rules to facilitate SIMD acceleration.

* **Alignment Rules:**  
* **Codebooks:**  Must align to  **64-byte**  boundaries for SIMD/cache-line efficiency.  
* **Tensor Indices:**  Must align to  **16-byte**  boundaries.  
* **Delta Buffers:**  4-byte alignment.  
* **Concurrency:**  Implements  **Reader-Writer Locks**  combined with  **Double-buffering** . This allows inference threads (Readers) to maintain  $O(1)$  access while Mutation threads (Writers) prepare a new version of a codebook or module in a secondary buffer for a seamless atomic swap.  
* **Lazy Evaluation:**  Fractal transformations and weight expansions are deferred until the moment of computation to minimize the active memory footprint.

##### 8\. Security, Integrity, and the Edit Log

A self-modifying format requires rigorous safety protocols to prevent divergence or malicious weight injection.

###### *The Footer (64 bytes)*

* **0x00 Magic:**  0x4C515446 ("LQTF").  
* **0x04 Checksum:**  CRC32 of the full file.  
* **0x08 Edit Log Offset:**  Pointer to an append-only record of every change.  
* **0x10 Timestamp:**  Unix epoch of the last modification (nanoseconds).

###### *Safety Guardrails*

* **Sandboxed Modification Trials:**  Changes are applied to a temporary buffer and validated for stability/performance before being committed to the main weight set.  
* **Mutation Quotas:**  Limits on the rate of change per epoch to prevent catastrophic forgetting.  
* **Critical Path Protection:**  Core model layers can be flagged as "immutable" to prevent corruption.

##### 9\. Implementation Conformance Checklist

###### *Binary & Structural Compliance*

*  Correctly parse 32-byte Header and 64-byte Footer.  
*  Implement TLV chunk skipping and Module Graph JSON parsing.  
*  Support Big/Little Endian byte-swapping logic.  
*  Verify CRC32 checksums and Edit Log signatures.

###### *Reconstruction & RTA*

*  Implement 5D RTA blocks with Rank 5 enforcement.  
*  Support all 6 sparsity encoding methods (COO, CSR, RLE, etc.).  
*  Multi-stage reconstruction (Base Index \+ Codebook \+ Delta).  
*  Implement Fractal Iteration and self-reference resolution.

###### *Memory & Optimization*

*  Enforce 64B (Codebook) and 16B (Index) memory alignment.  
*  Implement Reader-Writer locks with Double-buffering for hot-swaps.  
*  Utilize mmap for zero-copy file access.

###### *Security & Evolution*

*  Implement Sandboxed Trial logic for weight mutations.  
*  Log all modifications to the append-only Edit Log.  
*  Enforce Mutation Quotas and Critical Path protection.LQT v1.3 provides the definitive framework for the next generation of evolving AI, bridging the gap between high-efficiency inference and the fluid requirements of adaptive machine intelligence.

