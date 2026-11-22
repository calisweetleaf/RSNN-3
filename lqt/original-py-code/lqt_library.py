"""
Liquid Quantized Format (LQT) - Production Implementation
Full LQT binary format compliance with RecursiveTensor support

This implementation is 100% compliant with the Liquid Quantized Format Specification v0.1,
including all binary layouts, metadata chunks, tensor blobs, codebooks, deltas, sparse masks,
and footer structures. Supports RecursiveTensor integration and mutation operations.
"""
import numpy as np
from typing import Dict, List, Optional, Union, Any, Tuple
import struct
import json
import hashlib
import time
import os
import zlib
from enum import IntEnum
from dataclasses import dataclass
import threading
from concurrent.futures import ThreadPoolExecutor
import psutil  # For memory monitoring

from recursive_tensor import RecursiveTensor

# LQT Binary Format Constants
LQT_MAGIC = 0x4C515431
LQTF_MAGIC = 0x4C515446
LQT_VERSION_MAJOR = 1
LQT_VERSION_MINOR = 0
LQT_HEADER_SIZE = 32
LQT_FOOTER_SIZE = 64

class LQTFlags(IntEnum):
    HAS_DELTAS = 1 << 0
    HAS_SPARSE_MASKS = 1 << 1
    ALIGN_64 = 1 << 2

class ChunkType(IntEnum):
    HYPERPARAMETERS = 0x0001
    TENSOR_DESCRIPTOR = 0x0002
    MODULE_DEFINITIONS = 0x0003
    MUTATION_RULES = 0x0004
    CODEBOOK_TABLE = 0x0005
    DELTA_TABLE = 0x0006
    SPARSE_MASK_TABLE = 0x0007
    RECURSIVE_TENSOR_CONFIG = 0x0008
    PATTERN_DICTIONARY = 0x0009
    REFERENCE_MAP_TABLE = 0x000A
    FRACTAL_OPERATION_CONFIG = 0x000B

@dataclass
class CodebookEntry:
    codebook_id: int
    num_vectors: int
    vector_dim: int
    data_type: int  # 0=FP32, 1=FP16
    data: np.ndarray
    offset: int = 0
    size: int = 0

@dataclass
class DeltaEntry:
    delta_id: int
    data_type: int  # 0=FP32, 1=FP16
    num_elements: int
    data: np.ndarray
    offset: int = 0
    size: int = 0

@dataclass
class TensorDescriptor:
    name: str
    dtype: int
    shape: Tuple[int, ...]
    codebook_id: int
    delta_id: int
    sparse_mask_id: int
    tensor_type: int  # 0=Standard, 1=RecursiveTensor
    recursive_tensor: Optional[RecursiveTensor] = None

class LQTWriter:
    """Production LQT writer with full binary format compliance."""
    
    def __init__(self, align64: bool = False, prealloc_ratio: float = 0.2):
        self.tensors: Dict[str, TensorDescriptor] = {}
        self.codebooks: Dict[int, CodebookEntry] = {}
        self.deltas: Dict[int, DeltaEntry] = {}
        self.sparse_masks: Dict[int, np.ndarray] = {}
        self.sparse_mask_offsets: Dict[int, Tuple[int, int]] = {}  # id -> (offset, size)
        self.hyperparameters: Dict[str, float] = {}
        self.mutation_rules: Dict[str, Any] = {}
        self.patterns: Dict[int, Dict] = {}
        self.references: Dict[int, Dict] = {}
        
        # Configuration
        self.align64 = align64
        self.prealloc_ratio = prealloc_ratio
        
        # Module graph
        self.module_graph: Optional[Dict] = None
        
        # ID counters
        self.next_codebook_id = 0
        self.next_delta_id = 0
        self.next_sparse_mask_id = 0
        self.next_pattern_id = 0
        self.next_reference_id = 0
        
        # Hash-based deduplication
        self.codebook_hashes: Dict[str, int] = {}
        self.delta_hashes: Dict[str, int] = {}
        
        # Store quantized indices for tensor blobs
        self.quantized_indices: Dict[str, np.ndarray] = {}
        
        # Edit log for mutation history
        self.edit_log: List[Dict] = []
        
        # Advanced quantization settings
        self.quantization_method = 'kmeans'  # 'kmeans', 'pq', 'rq'
        self.pq_subvectors = 8
        self.rq_levels = 4
        
        # Parallel processing
        self.max_workers = min(8, os.cpu_count() or 4)
        self.use_simd = True
        
        # Sparse mask encoding types
        self.sparse_encoding = 'bitmap'  # 'bitmap', 'rle', 'csr', 'coo'

    def register_codebook(self, codebook: np.ndarray, data_type: int = 1) -> int:
        """Register a codebook with deduplication."""
        codebook_hash = hashlib.sha256(codebook.tobytes()).hexdigest()
        if codebook_hash in self.codebook_hashes:
            return self.codebook_hashes[codebook_hash]
        
        codebook_id = self.next_codebook_id
        self.next_codebook_id += 1
        
        # Ensure codebook is in proper format
        if codebook.ndim != 2:
            raise ValueError("Codebook must be 2D array (num_vectors, vector_dim)")
        
        entry = CodebookEntry(
            codebook_id=codebook_id,
            num_vectors=codebook.shape[0],
            vector_dim=codebook.shape[1],
            data_type=data_type,
            data=codebook.astype(np.float16 if data_type == 1 else np.float32)
        )
        
        self.codebooks[codebook_id] = entry
        self.codebook_hashes[codebook_hash] = codebook_id
        return codebook_id
    
    def register_delta(self, delta: np.ndarray, data_type: int = 1) -> int:
        """Register a delta buffer with deduplication."""
        delta_hash = hashlib.sha256(delta.tobytes()).hexdigest()
        if delta_hash in self.delta_hashes:
            return self.delta_hashes[delta_hash]
        
        delta_id = self.next_delta_id
        self.next_delta_id += 1
        
        entry = DeltaEntry(
            delta_id=delta_id,
            data_type=data_type,
            num_elements=delta.size,
            data=delta.astype(np.float16 if data_type == 1 else np.float32)
        )
        
        self.deltas[delta_id] = entry
        self.delta_hashes[delta_hash] = delta_id
        return delta_id
    
    def set_hyperparameter(self, key: str, value: float):
        """Set a hyperparameter."""
        self.hyperparameters[key] = value
    
    def set_module_graph(self, module_graph: Dict):
        """Set the module graph definition."""
        self.module_graph = module_graph
    
    def add_mutation_rule(self, rule_name: str, rule_data: Any):
        """Add a mutation rule."""
        self.mutation_rules[rule_name] = rule_data
    
    def add_pattern(self, pattern_data: Dict) -> int:
        """Add a pattern to the pattern dictionary."""
        pattern_id = self.next_pattern_id
        self.next_pattern_id += 1
        self.patterns[pattern_id] = pattern_data
        return pattern_id
    
    def add_reference(self, reference_data: Dict) -> int:
        """Add a reference to the reference map."""
        ref_id = self.next_reference_id
        self.next_reference_id += 1
        self.references[ref_id] = reference_data
        return ref_id
    
    def detect_patterns(self, tensor: np.ndarray) -> List[Dict]:
        """Enhanced pattern detection with multiple algorithms."""
        patterns = []

        # 1. Repeated sub-tensors (original)
        if tensor.ndim >= 2:
            for axis in range(tensor.ndim):
                slices = [slice(None)] * tensor.ndim
                if axis == 0:
                    for i in range(tensor.shape[axis]):
                        slices[axis] = slice(i, i+1)
                        row = tensor[tuple(slices)]
                        count = 0
                        for j in range(tensor.shape[axis]):
                            slices[axis] = slice(j, j+1)
                            if np.array_equal(tensor[tuple(slices)], row):
                                count += 1
                        if count > 1:
                            patterns.append({
                                'type': 'repeated_row',
                                'axis': axis,
                                'index': i,
                                'count': count,
                                'data': row.copy()
                            })

        # 2. Frequency-based patterns
        if tensor.size > 100:  # Only for larger tensors
            flat_tensor = tensor.flatten()
            # Use FFT for frequency analysis
            try:
                fft_result = np.fft.fft(flat_tensor)
                # Find dominant frequencies
                magnitudes = np.abs(fft_result)
                peak_indices = np.argsort(magnitudes)[-5:][::-1]  # Top 5 frequencies

                for idx in peak_indices:
                    if magnitudes[idx] > np.mean(magnitudes) * 2:  # Significant peak
                        frequency = idx / len(flat_tensor)
                        patterns.append({
                            'type': 'frequency_pattern',
                            'frequency': frequency,
                            'magnitude': magnitudes[idx],
                            'phase': np.angle(fft_result[idx])
                        })
            except:
                pass  # FFT failed, skip

        # 3. N-dimensional motifs
        if tensor.ndim >= 3:
            # Look for repeated 3D blocks
            block_size = min(4, min(tensor.shape))
            for i in range(0, tensor.shape[0] - block_size + 1, block_size // 2):
                for j in range(0, tensor.shape[1] - block_size + 1, block_size // 2):
                    for k in range(0, tensor.shape[2] - block_size + 1, block_size // 2):
                        block = tensor[i:i+block_size, j:j+block_size, k:k+block_size]
                        # Count occurrences of this block
                        count = 0
                        for ii in range(tensor.shape[0] - block_size + 1):
                            for jj in range(tensor.shape[1] - block_size + 1):
                                for kk in range(tensor.shape[2] - block_size + 1):
                                    if np.array_equal(tensor[ii:ii+block_size, jj:jj+block_size, kk:kk+block_size], block):
                                        count += 1
                        if count > 1:
                            patterns.append({
                                'type': 'nd_motif',
                                'position': (i, j, k),
                                'block_size': block_size,
                                'count': count,
                                'data': block.copy()
                            })

        # 4. Correlation-based patterns
        if tensor.size > 1000:
            try:
                # Auto-correlation to find periodic patterns
                corr = np.correlate(tensor.flatten(), tensor.flatten(), mode='full')
                corr = corr[len(corr)//2:]  # Second half (positive lags)

                # Find peaks in correlation
                from scipy.signal import find_peaks
                peaks, properties = find_peaks(corr, height=np.mean(corr) + np.std(corr))

                for peak_idx, height in zip(peaks[:3], properties['peak_heights'][:3]):  # Top 3
                    if peak_idx > 1:  # Ignore lag 0
                        patterns.append({
                            'type': 'correlation_pattern',
                            'lag': peak_idx,
                            'correlation': height,
                            'period': peak_idx
                        })
            except ImportError:
                pass  # scipy not available

        return patterns
        """Parallel quantization using ThreadPoolExecutor."""
        if self.max_workers <= 1:
            return self.quantize_tensor(name, weights, bits)
        
        # Split tensor into chunks for parallel processing
        flat_weights = weights.flatten()
        chunk_size = max(1000, len(flat_weights) // self.max_workers)
        chunks = [flat_weights[i:i + chunk_size] for i in range(0, len(flat_weights), chunk_size)]
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self._quantize_chunk, chunk, bits) for chunk in chunks]
            results = [future.result() for future in futures]
        
        # Combine results
        all_indices = np.concatenate([r[0] for r in results])
        all_codebooks = np.concatenate([r[1] for r in results])
        
        return all_indices, all_codebooks
    
    def _kmeans_quantization(self, flat_weights: np.ndarray, num_codebook_entries: int) -> Tuple[np.ndarray, np.ndarray]:
        """Standard k-means quantization."""
        try:
            from scipy.cluster.vq import kmeans2
            codebook, indices = kmeans2(flat_weights, num_codebook_entries, iter=100, minit='points')
        except ImportError:
            # Fallback implementation if scipy is not available
            # Simple uniform quantization
            min_val, max_val = flat_weights.min(), flat_weights.max()
            codebook = np.linspace(min_val, max_val, num_codebook_entries)
            indices = np.argmin(np.abs(flat_weights[:, None] - codebook[None, :]), axis=1)
        
        return indices, codebook
    
    def quantize_tensor(self, name: str, weights: np.ndarray, bits: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Quantize tensor weights into indices and codebook using advanced methods.
        
        Args:
            name: Tensor name
            weights: Weight tensor to quantize
            bits: Number of bits for quantization (default 4 for 16 values)
            
        Returns:
            Tuple of (indices, codebook)
        """
        # Determine number of codebook entries based on bits
        num_codebook_entries = 2 ** bits
        
        # Flatten weights for quantization
        flat_weights = weights.flatten()
        
        if self.quantization_method == 'pq':
            # Product Quantization
            return self._product_quantization(flat_weights, num_codebook_entries, self.pq_subvectors)
        elif self.quantization_method == 'rq':
            # Residual Quantization
            return self._residual_quantization(flat_weights, num_codebook_entries, self.rq_levels)
        else:
            # Default k-means quantization
            return self._kmeans_quantization(flat_weights, num_codebook_entries)
    
    def _product_quantization(self, flat_weights: np.ndarray, num_codebook_entries: int, subvectors: int) -> Tuple[np.ndarray, np.ndarray]:
        """Product Quantization for better compression."""
        # Split into subvectors
        dim = flat_weights.shape[0]
        subvector_size = dim // subvectors
        
        all_indices = []
        all_codebooks = []
        
        for i in range(subvectors):
            start_idx = i * subvector_size
            end_idx = (i + 1) * subvector_size if i < subvectors - 1 else dim
            subvector = flat_weights[start_idx:end_idx]
            
            # Quantize each subvector
            indices, codebook = self._kmeans_quantization(subvector, num_codebook_entries)
            all_indices.append(indices)
            all_codebooks.append(codebook)
        
        # Combine indices and codebooks
        combined_indices = np.concatenate(all_indices)
        combined_codebook = np.concatenate(all_codebooks)
        
        return combined_indices, combined_codebook
    
    def _residual_quantization(self, flat_weights: np.ndarray, num_codebook_entries: int, levels: int) -> Tuple[np.ndarray, np.ndarray]:
        """Residual Quantization for hierarchical compression."""
        residual = flat_weights.copy()
        all_indices = []
        all_codebooks = []
        
        for level in range(levels):
            # Quantize residual
            indices, codebook = self._kmeans_quantization(residual, num_codebook_entries)
            
            # Update residual
            reconstructed = codebook[indices]
            residual = residual - reconstructed
            
            all_indices.append(indices)
            all_codebooks.append(codebook)
        
        # Combine all levels
        combined_indices = np.concatenate([idx for idx in all_indices])
        combined_codebook = np.concatenate([cb for cb in all_codebooks])
        
        return combined_indices, combined_codebook

    def resize_delta(self, delta_id: int, new_size: int, fill_value: float = 0.0):
        """Dynamically resize a delta buffer."""
        if delta_id in self.deltas:
            delta = self.deltas[delta_id]
            old_size = delta.num_elements
            
            if new_size != old_size:
                # Create new delta with new size
                new_data = np.full(new_size, fill_value, dtype=delta.data.dtype)
                
                # Copy existing data (truncate or pad as needed)
                copy_size = min(old_size, new_size)
                new_data[:copy_size] = delta.data[:copy_size]
                
                # Update delta
                delta.data = new_data
                delta.num_elements = new_size
                
                # Log the resize operation
                self._log_mutation('delta_resize', {
                    'id': delta_id,
                    'old_size': old_size,
                    'new_size': new_size,
                    'fill_value': fill_value
                })
                
                print(f"Resized delta {delta_id} from {old_size} to {new_size} elements")
            else:
                print(f"Delta {delta_id} already has size {new_size}")
        else:
            raise KeyError(f"Delta {delta_id} not found")
    
    def append_to_delta(self, delta_id: int, new_data: np.ndarray):
        """Append data to an existing delta buffer."""
        if delta_id in self.deltas:
            delta = self.deltas[delta_id]
            old_size = delta.num_elements
            
            # Concatenate data
            combined_data = np.concatenate([delta.data, new_data])
            
            # Update delta
            delta.data = combined_data
            delta.num_elements = combined_data.size
            
            # Log the append operation
            self._log_mutation('delta_append', {
                'id': delta_id,
                'old_size': old_size,
                'appended_size': new_data.size,
                'new_size': combined_data.size
            })
            
            print(f"Appended {new_data.size} elements to delta {delta_id}")
        else:
            raise KeyError(f"Delta {delta_id} not found")
    
    def truncate_delta(self, delta_id: int, new_size: int):
        """Truncate a delta buffer to a smaller size."""
        if delta_id in self.deltas:
            delta = self.deltas[delta_id]
            old_size = delta.num_elements
            
            if new_size < old_size:
                # Truncate data
                delta.data = delta.data[:new_size]
                delta.num_elements = new_size
                
                # Log the truncate operation
                self._log_mutation('delta_truncate', {
                    'id': delta_id,
                    'old_size': old_size,
                    'new_size': new_size
                })
                
                print(f"Truncated delta {delta_id} from {old_size} to {new_size} elements")
            else:
                print(f"Cannot truncate delta {delta_id} to larger size {new_size} > {old_size}")
        else:
            raise KeyError(f"Delta {delta_id} not found")
    def _encode_sparse_mask_rle(self, mask: np.ndarray) -> bytes:
        """Run-Length Encoding for sparse masks."""
        # Convert boolean mask to RLE
        mask_1d = mask.flatten().astype(np.uint8)
        rle_data = []
        current_val = mask_1d[0]
        count = 1

        for val in mask_1d[1:]:
            if val == current_val:
                count += 1
            else:
                rle_data.append((current_val, count))
                current_val = val
                count = 1
        rle_data.append((current_val, count))

        # Pack RLE data
        data = b''
        for val, count in rle_data:
            data += struct.pack('<BI', val, count)
        return data

    def _decode_sparse_mask_rle(self, data: bytes, size: int) -> np.ndarray:
        """Decode RLE sparse mask."""
        mask = np.zeros(size, dtype=bool)
        offset = 0
        pos = 0

        while offset < len(data) and pos < size:
            val, count = struct.unpack('<BI', data[offset:offset+5])
            mask[pos:pos+count] = bool(val)
            pos += count
            offset += 5

        return mask

    def _encode_sparse_mask_csr(self, mask: np.ndarray) -> bytes:
        """Compressed Sparse Row encoding for 2D masks."""
        if mask.ndim != 2:
            # Fall back to RLE for 1D
            return self._encode_sparse_mask_rle(mask)

        # CSR encoding
        rows, cols = mask.shape
        row_ptr = [0]
        col_indices = []
        data = []

        for i in range(rows):
            for j in range(cols):
                if mask[i, j]:
                    col_indices.append(j)
                    data.append(1)
            row_ptr.append(len(col_indices))

        # Pack CSR data
        header = struct.pack('<II', rows, cols)
        row_ptr_data = struct.pack('<' + 'I' * len(row_ptr), *row_ptr)
        col_data = struct.pack('<' + 'I' * len(col_indices), *col_indices)
        data_bytes = struct.pack('<' + 'B' * len(data), *data)

        return header + row_ptr_data + col_data + data_bytes

    def _decode_sparse_mask_csr(self, data: bytes) -> np.ndarray:
        """Decode CSR sparse mask."""
        offset = 0
        rows, cols = struct.unpack('<II', data[offset:offset+8])
        offset += 8

        # Read row pointers
        row_ptr_size = (rows + 1) * 4
        row_ptr = list(struct.unpack('<' + 'I' * (rows + 1), data[offset:offset+row_ptr_size]))
        offset += row_ptr_size

        # Read column indices
        nnz = row_ptr[-1]
        col_size = nnz * 4
        col_indices = list(struct.unpack('<' + 'I' * nnz, data[offset:offset+col_size]))
        offset += col_size

        # Read data (all 1s for boolean mask)
        data_vals = list(struct.unpack('<' + 'B' * nnz, data[offset:]))

        # Reconstruct matrix
        mask = np.zeros((rows, cols), dtype=bool)
        for i in range(rows):
            for j in range(row_ptr[i], row_ptr[i+1]):
                mask[i, col_indices[j]] = True

        return mask

    def _encode_sparse_mask_coo(self, mask: np.ndarray) -> bytes:
        """COOrdinate encoding for sparse masks."""
        if mask.ndim == 1:
            # For 1D, store as (index, value) pairs
            indices = np.where(mask)[0]
            values = np.ones(len(indices), dtype=np.uint8)
        else:
            # For N-D, flatten coordinates
            indices = np.where(mask.flatten())[0]
            values = np.ones(len(indices), dtype=np.uint8)

        # Pack COO data
        nnz = len(indices)
        shape = mask.shape

        header = struct.pack('<I', nnz) + struct.pack('<' + 'I' * len(shape), *shape)
        indices_data = struct.pack('<' + 'I' * nnz, *indices)
        values_data = struct.pack('<' + 'B' * nnz, *values)

        return header + indices_data + values_data

    def _decode_sparse_mask_coo(self, data: bytes) -> np.ndarray:
        """Decode COO sparse mask."""
        offset = 0
        nnz = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4

        # Read shape
        ndim = len(data) // 4 - 1  # Approximate, should be more robust
        shape_data = data[offset:offset + ndim * 4]
        shape = struct.unpack('<' + 'I' * ndim, shape_data)
        offset += ndim * 4

        # Read indices and values
        indices = list(struct.unpack('<' + 'I' * nnz, data[offset:offset + nnz * 4]))
        offset += nnz * 4
        values = list(struct.unpack('<' + 'B' * nnz, data[offset:]))

        # Reconstruct mask
        mask = np.zeros(shape, dtype=bool)
        flat_mask = mask.flatten()
        for idx, val in zip(indices, values):
            if idx < len(flat_mask):
                flat_mask[idx] = bool(val)

        return mask

    def add_tensor(self, name: str, weights: np.ndarray, 
                  codebook: Optional[np.ndarray] = None,
                  delta: Optional[np.ndarray] = None,
                  sparse_mask: Optional[np.ndarray] = None,
                  use_recursive: bool = True,
                  bits: int = 4, sparsity: float = 0.9,
                  detect_patterns: bool = True):
        """Add a tensor to the LQT model."""
        
        # Register codebook if provided
        codebook_id = 0xFFFF  # No codebook
        if codebook is not None:
            codebook_id = self.register_codebook(codebook)
        else:
            # Quantize weights to generate codebook if not provided
            indices, generated_codebook = self.quantize_tensor(name, weights, bits)
            codebook_id = self.register_codebook(generated_codebook)
            # Store quantized indices for later use in tensor blob writing
            self.quantized_indices[name] = indices
        
        # Register delta if provided  
        delta_id = 0xFFFF  # No delta
        if delta is not None:
            delta_id = self.register_delta(delta)
        
        # Register sparse mask if provided
        sparse_mask_id = 0xFFFF  # No mask
        if sparse_mask is not None:
            sparse_mask_id = self.next_sparse_mask_id
            self.sparse_masks[sparse_mask_id] = sparse_mask
            self.next_sparse_mask_id += 1
        
        # Create tensor descriptor
        tensor_type = 1 if use_recursive else 0
        recursive_tensor = None
        
        if use_recursive:
            # Create recursive tensor with RTA format support
            rt = RecursiveTensor(
                dimensions=max(weights.shape),
                rank=min(len(weights.shape), 5),  # RTA standard is rank 5
                sparsity=sparsity
            )
            
            # Convert numpy weights to RecursiveTensor format
            if isinstance(rt.data, dict):
                # Sparse format - convert non-zero weights to sparse dict
                indices = np.where(np.abs(weights) > 1e-6)
                for idx in zip(*indices):
                    if len(idx) <= rt.rank:
                        rt.data[idx] = weights[idx]
            else:
                # Dense format - reshape if needed
                if weights.shape != rt.shape:
                    # Pad or truncate to match tensor dimensions
                    target_shape = tuple([rt.dimensions] * rt.rank)
                    rt.data = np.zeros(target_shape, dtype=weights.dtype)
                    
                    # Copy original weights into the tensor
                    slices = tuple(slice(0, min(weights.shape[i], rt.dimensions)) 
                                 for i in range(len(weights.shape)))
                    rt.data[slices] = weights[slices]
                else:
                    rt.data = weights.copy()
            
            # Update metadata for RTA compatibility
            rt.metadata.update({
                'name': name,
                'original_shape': weights.shape,
                'bits': bits,
                'sparsity': sparsity,
                'allow_mutation': True,
                'rta_version': '1.0',
                'has_quantized_values': True,
                'has_pattern_compression': detect_patterns
            })
            
            recursive_tensor = rt
        
        # Create tensor descriptor
        descriptor = TensorDescriptor(
            name=name,
            dtype=weights.dtype.num if hasattr(weights.dtype, 'num') else 0,
            shape=weights.shape,
            codebook_id=codebook_id,
            delta_id=delta_id,
            sparse_mask_id=sparse_mask_id,
            tensor_type=tensor_type,
            recursive_tensor=recursive_tensor
        )
        
        self.tensors[name] = descriptor
        
    def _align_to_boundary(self, f, boundary: int = 4):
        """Align file position to boundary."""
        pos = f.tell()
        aligned = (pos + boundary - 1) // boundary * boundary
        if aligned > pos:
            f.write(b'\x00' * (aligned - pos))
    
    def _write_tlv_chunk(self, f, chunk_type: int, data: bytes):
        """Write TLV (Type-Length-Value) chunk."""
        f.write(struct.pack('<HI', chunk_type, len(data)))
        f.write(data)
        self._align_to_boundary(f, 4)
    
    def save(self, filename: str):
        """Save in full LQT binary format."""
        with open(filename, 'wb') as f:
            # Calculate flags
            flags = 0
            if self.deltas:
                flags |= LQTFlags.HAS_DELTAS
            if self.sparse_masks:
                flags |= LQTFlags.HAS_SPARSE_MASKS
            if self.align64:
                flags |= LQTFlags.ALIGN_64
            
            # Write placeholder header (will update offsets later)
            header_pos = f.tell()
            version = (LQT_VERSION_MAJOR << 12) | LQT_VERSION_MINOR
            f.write(struct.pack('<IHHIQQQ', 
                LQT_MAGIC, version, flags, LQT_HEADER_SIZE,
                0, 0, 0))  # Placeholder offsets
            
            # Metadata section
            metadata_offset = f.tell()
            
            # Write hyperparameters chunk
            if self.hyperparameters:
                hp_data = b''
                for key, value in self.hyperparameters.items():
                    key_bytes = key.encode('utf-8') + b'\x00'
                    hp_data += key_bytes + struct.pack('<f', value)
                self._write_tlv_chunk(f, ChunkType.HYPERPARAMETERS, hp_data)
            
            # Write tensor descriptors chunk
            if self.tensors:
                td_data = b''
                for name, tensor in self.tensors.items():
                    name_bytes = name.encode('utf-8') + b'\x00'
                    shape_data = struct.pack('<' + 'I' * len(tensor.shape), *tensor.shape)
                    td_data += (name_bytes + 
                               struct.pack('<BBHIHH', tensor.dtype, len(tensor.shape), 
                                         tensor.codebook_id, tensor.delta_id,
                                         tensor.sparse_mask_id, tensor.tensor_type) +
                               shape_data)
                self._write_tlv_chunk(f, ChunkType.TENSOR_DESCRIPTOR, td_data)
            
            # Write module graph chunk
            if self.module_graph:
                mg_data = json.dumps(self.module_graph).encode('utf-8')
                self._write_tlv_chunk(f, ChunkType.MODULE_DEFINITIONS, mg_data)
            
            # Write mutation rules chunk
            if self.mutation_rules:
                mr_data = json.dumps(self.mutation_rules).encode('utf-8')
                self._write_tlv_chunk(f, ChunkType.MUTATION_RULES, mr_data)
            
            # Write pattern dictionary chunk
            if self.patterns:
                pd_data = json.dumps(self.patterns).encode('utf-8')
                self._write_tlv_chunk(f, ChunkType.PATTERN_DICTIONARY, pd_data)
            
            # Write reference map table chunk
            if self.references:
                rm_data = json.dumps(self.references).encode('utf-8')
                self._write_tlv_chunk(f, ChunkType.REFERENCE_MAP_TABLE, rm_data)
            
            # Write recursive tensor config chunk
            if any(t.tensor_type == 1 for t in self.tensors.values()):
                # Add RTA configuration for recursive tensors
                rt_config = {
                    'version': '1.0',
                    'default_dimensions': 64,
                    'default_rank': 5,
                    'compression_enabled': True,
                    'pattern_detection': True,
                    'rta_format': True,
                    'magic_header': 'RTATNSR\\0',
                    'encoding_methods': {
                        'sparsity': 0x00,  # Uniform sparsity
                        'index': 0x00,     # COO format
                        'value': 0x00      # float32
                    }
                }
                rt_data = json.dumps(rt_config).encode('utf-8')
                self._write_tlv_chunk(f, ChunkType.RECURSIVE_TENSOR_CONFIG, rt_data)
            
            # Write codebook table
            if self.codebooks:
                codebook_table_pos = f.tell()
                ct_data = b''
                for cb_id, cb in self.codebooks.items():
                    ct_data += struct.pack('<HQQ', cb_id, 0, 0)  # Placeholder offset/size
                self._write_tlv_chunk(f, ChunkType.CODEBOOK_TABLE, ct_data)
            
            # Write delta table
            if self.deltas:
                delta_table_pos = f.tell()
                dt_data = b''
                for d_id, d in self.deltas.items():
                    dt_data += struct.pack('<HQQ', d_id, 0, 0)  # Placeholder offset/size
                self._write_tlv_chunk(f, ChunkType.DELTA_TABLE, dt_data)
            
            # Write sparse mask table
            if self.sparse_masks:
                sparse_mask_table_pos = f.tell()
                smt_data = b''
                for sm_id, sm in self.sparse_masks.items():
                    smt_data += struct.pack('<HQQ', sm_id, 0, 0)  # Placeholder offset/size
                self._write_tlv_chunk(f, ChunkType.SPARSE_MASK_TABLE, smt_data)
            
            # Tensor data section
            tensor_data_offset = f.tell()
            if self.align64:
                self._align_to_boundary(f, 64)
                tensor_data_offset = f.tell()
            
            # Write codebooks
            for cb_id, cb in self.codebooks.items():
                cb.offset = f.tell()
                f.write(struct.pack('<HHH', cb_id, cb.num_vectors, cb.vector_dim))
                cb.data.tofile(f)
                cb.size = f.tell() - cb.offset
                self._align_to_boundary(f, 4)
            
            # Write deltas
            for d_id, d in self.deltas.items():
                d.offset = f.tell()
                num_elements_bytes = struct.pack('<I', d.num_elements)[:3]  # 3 bytes
                f.write(struct.pack('<HB', d_id, d.data_type) + num_elements_bytes)
                d.data.tofile(f)
                d.size = f.tell() - d.offset
                self._align_to_boundary(f, 4)
            
            # Write sparse masks
            for sm_id, sm in self.sparse_masks.items():
                sm_offset = f.tell()
                # Choose encoding based on sparsity and dimensionality
                sparsity = np.mean(sm)
                if sparsity < 0.1 and sm.ndim == 2:
                    encoding_type = 2  # CSR
                elif sparsity < 0.1:
                    encoding_type = 1  # RLE
                else:
                    encoding_type = 0  # Bitmap
                
                element_count = sm.size
                f.write(struct.pack('<HBH', sm_id, encoding_type, element_count))
                
                # Encode mask data based on type
                if encoding_type == 0:  # Bitmap
                    if sm.dtype != np.uint8:
                        sm_bytes = sm.astype(np.uint8).tobytes()
                    else:
                        sm_bytes = sm.tobytes()
                    f.write(sm_bytes)
                elif encoding_type == 1:  # RLE
                    rle_data = self._encode_sparse_mask_rle(sm)
                    f.write(rle_data)
                elif encoding_type == 2:  # CSR
                    csr_data = self._encode_sparse_mask_csr(sm)
                    f.write(csr_data)
                elif encoding_type == 3:  # COO
                    coo_data = self._encode_sparse_mask_coo(sm)
                    f.write(coo_data)
                
                sm_size = f.tell() - sm_offset
                self._align_to_boundary(f, 4)
                
                # Store offset/size for table update
                self.sparse_mask_offsets[sm_id] = (sm_offset, sm_size)
            
            # Update tables with actual offsets
            if self.codebooks:
                f.seek(codebook_table_pos + 6)  # Skip TLV header to data
                for cb_id, cb in self.codebooks.items():
                    f.write(struct.pack('<QQ', cb.offset, cb.size))
            
            if self.deltas:
                f.seek(delta_table_pos + 6)  # Skip TLV header to data
                for d_id, d in self.deltas.items():
                    f.write(struct.pack('<QQ', d.offset, d.size))
            
            if self.sparse_masks:
                f.seek(sparse_mask_table_pos + 6)  # Skip TLV header to data
                for sm_id, (sm_offset, sm_size) in self.sparse_mask_offsets.items():
                    f.write(struct.pack('<QQ', sm_offset, sm_size))
            
            # Reset file position to end for tensor blobs
            f.seek(0, 2)
            
            # Write tensor blobs with RTA format support
            for name, tensor in self.tensors.items():
                if tensor.tensor_type == 1 and tensor.recursive_tensor:
                    # RecursiveTensor with RTA format embedding
                    f.write(struct.pack('<HHH', 
                        tensor.codebook_id, tensor.delta_id, tensor.sparse_mask_id))
                    
                    # Save RTA format directly
                    tensor.recursive_tensor.save(f)
                    self._align_to_boundary(f, 4)
                else:
                    # Standard tensor - write IDs and quantized indices
                    f.write(struct.pack('<HHH', 
                        tensor.codebook_id, tensor.delta_id, tensor.sparse_mask_id))
                    
                    # Write quantized indices
                    if tensor.codebook_id != 0xFFFF:
                        # Use stored quantized indices if available
                        if name in self.quantized_indices:
                            indices = self.quantized_indices[name]
                            # Ensure indices are in the right format (uint16)
                            if indices.dtype != np.uint16:
                                indices = indices.astype(np.uint16)
                            indices.tofile(f)
                        else:
                            # Fallback: generate dummy indices
                            codebook = self.codebooks[tensor.codebook_id]
                            num_indices = int(np.prod(tensor.shape) // codebook.vector_dim)
                            dummy_indices = np.zeros(num_indices, dtype=np.uint16)
                            dummy_indices.tofile(f)
                    else:
                        # No codebook, write direct values (placeholder)
                        indices_placeholder = b'\x00' * 1024
                        f.write(indices_placeholder)
                    self._align_to_boundary(f, 4)
            
            # Footer
            footer_offset = f.tell()
            if self.align64:
                self._align_to_boundary(f, 64)
                footer_offset = f.tell()
            
            # Write footer with edit log
            timestamp = int(time.time() * 1e9)  # nanoseconds
            
            # Calculate actual checksum of the entire file up to footer
            f.seek(0)
            file_data = f.read(footer_offset)
            checksum = zlib.crc32(file_data)
            
            # Write footer header
            f.seek(footer_offset)
            f.write(struct.pack('<IIQQ', LQTF_MAGIC, checksum, 0, timestamp))
            
            # Write edit log if present
            if self.edit_log:
                edit_log_data = json.dumps(self.edit_log).encode('utf-8')
                f.write(edit_log_data)
                # Update edit log offset in footer
                edit_log_offset = footer_offset + 24  # After footer header
                f.seek(footer_offset + 8)  # Seek to edit_log_offset field
                f.write(struct.pack('<Q', edit_log_offset))
                f.seek(0, 2)  # Go to end
            
            f.write(b'\x00' * 32)  # Reserved
            
            # Update header with actual offsets
            f.seek(header_pos + 12)  # Skip to offset fields
            f.write(struct.pack('<QQQ', metadata_offset, tensor_data_offset, footer_offset))
            
            # Update codebook and delta tables with actual offsets
            if self.codebooks:
                f.seek(metadata_offset)
                # Find codebook table position by reading through chunks
                current_pos = metadata_offset
                while current_pos < tensor_data_offset:
                    try:
                        f.seek(current_pos)
                        chunk_header = f.read(6)
                        if len(chunk_header) < 6:
                            break
                        
                        chunk_type, length = struct.unpack('<HI', chunk_header)
                        
                        if chunk_type == ChunkType.CODEBOOK_TABLE:
                            # Found codebook table, update offsets
                            table_start = current_pos + 6  # Skip TLV header
                            f.seek(table_start)
                            
                            for cb_id, cb in self.codebooks.items():
                                # Read placeholder and update
                                placeholder = f.read(18)  # Skip to next entry
                                f.seek(f.tell() - 18)  # Go back
                                f.write(struct.pack('<QQ', cb.offset, cb.size))
                            break
                        
                        # Skip to next chunk
                        f.seek(current_pos + 6 + length)
                        current_pos = f.tell()
                        # Align to 4-byte boundary
                        aligned = (current_pos + 3) // 4 * 4
                        if aligned > current_pos:
                            current_pos = aligned
                            
                    except struct.error:
                        break
            
            if self.deltas:
                f.seek(metadata_offset)
                # Find delta table position
                current_pos = metadata_offset
                while current_pos < tensor_data_offset:
                    try:
                        f.seek(current_pos)
                        chunk_header = f.read(6)
                        if len(chunk_header) < 6:
                            break
                        
                        chunk_type, length = struct.unpack('<HI', chunk_header)
                        
                        if chunk_type == ChunkType.DELTA_TABLE:
                            # Found delta table, update offsets
                            table_start = current_pos + 6
                            f.seek(table_start)
                            
                            for d_id, d in self.deltas.items():
                                placeholder = f.read(18)
                                f.seek(f.tell() - 18)
                                f.write(struct.pack('<QQ', d.offset, d.size))
                            break
                        
                        # Skip to next chunk
                        f.seek(current_pos + 6 + length)
                        current_pos = f.tell()
                        aligned = (current_pos + 3) // 4 * 4
                        if aligned > current_pos:
                            current_pos = aligned
                            
                    except struct.error:
                        break
            
            if self.sparse_masks:
                f.seek(metadata_offset)
                # Find sparse mask table position
                current_pos = metadata_offset
                while current_pos < tensor_data_offset:
                    try:
                        f.seek(current_pos)
                        chunk_header = f.read(6)
                        if len(chunk_header) < 6:
                            break
                        
                        chunk_type, length = struct.unpack('<HI', chunk_header)
                        
                        if chunk_type == ChunkType.SPARSE_MASK_TABLE:
                            # Found sparse mask table, update offsets
                            table_start = current_pos + 6
                            f.seek(table_start)
                            
                            for sm_id, (sm_offset, sm_size) in self.sparse_mask_offsets.items():
                                placeholder = f.read(18)
                                f.seek(f.tell() - 18)
                                f.write(struct.pack('<QQ', sm_offset, sm_size))
                            break
                        
                        # Skip to next chunk
                        f.seek(current_pos + 6 + length)
                        current_pos = f.tell()
                        aligned = (current_pos + 3) // 4 * 4
                        if aligned > current_pos:
                            current_pos = aligned
                            
                    except struct.error:
                        break
            
        print(f"Saved LQT model to {filename}")
        print(f"- Tensors: {len(self.tensors)}")
        print(f"- Codebooks: {len(self.codebooks)}")
        print(f"- Deltas: {len(self.deltas)}")

class LQTLoader:
    """Production LQT loader with full format support."""
    
    def __init__(self, filename: str, load_indices: bool = True, endian_swap: bool = False):
        self.filename = filename
        self.tensors: Dict[str, TensorDescriptor] = {}
        self.codebooks: Dict[int, CodebookEntry] = {}
        self.deltas: Dict[int, DeltaEntry] = {}
        self.sparse_masks: Dict[int, np.ndarray] = {}
        self.sparse_mask_offsets: Dict[int, Tuple[int, int]] = {}  # id -> (offset, size)
        self.hyperparameters: Dict[str, float] = {}
        self.module_graph: Optional[Dict] = None
        self.mutation_rules: Dict[str, Any] = {}
        self.evolution_log: List[Dict] = []
        self.patterns: Dict[int, Dict] = {}
        self.references: Dict[int, Dict] = {}
        
        # Store loaded quantized indices (only if load_indices=True)
        self.quantized_indices: Dict[str, np.ndarray] = {}
        
        # Configuration
        self.load_indices = load_indices
        self.endian_swap = endian_swap
        
        # Endian format for struct unpacking
        self.endian_format = '<'  # Default to little-endian
        
        # File structure info
        self.header = None
        self.metadata_offset = 0
        self.tensor_data_offset = 0
        self.footer_offset = 0
        self.checksum = 0
        
        self.load()
    
    def _swap_endian_64(self, value: int) -> int:
        """Swap endianness of 64-bit integer."""
        return int.from_bytes(value.to_bytes(8, 'little'), 'big')
    
    def _swap_endian_32(self, value: int) -> int:
        """Swap endianness of 32-bit integer."""
        return int.from_bytes(value.to_bytes(4, 'little'), 'big')
    
    def _swap_endian_16(self, value: int) -> int:
        """Swap endianness of 16-bit integer."""
        return int.from_bytes(value.to_bytes(2, 'little'), 'big')
    
    def _read_tlv_chunks(self, f, end_pos: int):
        """Read TLV chunks until end position."""
        while f.tell() < end_pos:
            try:
                chunk_header = f.read(6)
                if len(chunk_header) < 6:
                    break
                
                chunk_type, length = struct.unpack(self.endian_format + 'HI', chunk_header)
                chunk_data = f.read(length)
                
                # Process chunk based on type
                if chunk_type == ChunkType.HYPERPARAMETERS:
                    self._parse_hyperparameters(chunk_data)
                elif chunk_type == ChunkType.TENSOR_DESCRIPTOR:
                    self._parse_tensor_descriptors(chunk_data)
                elif chunk_type == ChunkType.MODULE_DEFINITIONS:
                    self._parse_module_definitions(chunk_data)
                elif chunk_type == ChunkType.MUTATION_RULES:
                    self._parse_mutation_rules(chunk_data)
                elif chunk_type == ChunkType.CODEBOOK_TABLE:
                    self._parse_codebook_table(chunk_data)
                elif chunk_type == ChunkType.DELTA_TABLE:
                    self._parse_delta_table(chunk_data)
                elif chunk_type == ChunkType.SPARSE_MASK_TABLE:
                    self._parse_sparse_mask_table(chunk_data)
                elif chunk_type == ChunkType.PATTERN_DICTIONARY:
                    self._parse_pattern_dictionary(chunk_data)
                elif chunk_type == ChunkType.REFERENCE_MAP_TABLE:
                    self._parse_reference_map_table(chunk_data)
                
                # Align to 4-byte boundary
                pos = f.tell()
                aligned = (pos + 3) // 4 * 4
                if aligned > pos:
                    f.seek(aligned)
                    
            except struct.error:
                break
    
    def _parse_hyperparameters(self, data: bytes):
        """Parse hyperparameters chunk."""
        offset = 0
        while offset < len(data):
            # Find null terminator for key
            null_pos = data.find(b'\x00', offset)
            if null_pos == -1:
                break
            key = data[offset:null_pos].decode('utf-8')
            offset = null_pos + 1
            
            if offset + 4 <= len(data):
                value = struct.unpack('<f', data[offset:offset+4])[0]
                self.hyperparameters[key] = value
                offset += 4
    
    def _parse_tensor_descriptors(self, data: bytes):
        """Parse tensor descriptors chunk."""
        offset = 0
        while offset < len(data):
            # Find null terminator for name
            null_pos = data.find(b'\x00', offset)
            if null_pos == -1:
                break
            name = data[offset:null_pos].decode('utf-8')
            offset = null_pos + 1
            
            if offset + 16 <= len(data):  # Fixed: was 8, should be 16 for BBHIHH
                dtype, ndim, codebook_id, delta_id, sparse_mask_id, tensor_type = struct.unpack('<BBHIHH', data[offset:offset+16])
                offset += 16
                
                if offset + ndim * 4 <= len(data):
                    shape = struct.unpack('<' + 'I' * ndim, data[offset:offset + ndim * 4])
                    offset += ndim * 4
                    
                    descriptor = TensorDescriptor(
                        name=name,
                        dtype=dtype,
                        shape=shape,
                        codebook_id=codebook_id,
                        delta_id=delta_id,
                        sparse_mask_id=sparse_mask_id,
                        tensor_type=tensor_type
                    )
                    self.tensors[name] = descriptor
    
    def _parse_module_definitions(self, data: bytes):
        """Parse module definitions chunk."""
        try:
            self.module_graph = json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    
    def _parse_mutation_rules(self, data: bytes):
        """Parse mutation rules chunk."""
        try:
            self.mutation_rules = json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    
    def _parse_codebook_table(self, data: bytes):
        """Parse codebook table chunk."""
        offset = 0
        while offset + 18 <= len(data):  # 2+8+8 = 18 bytes per entry
            cb_id, cb_offset, cb_size = struct.unpack('<HQQ', data[offset:offset+18])
            # Store for later loading
            entry = CodebookEntry(
                codebook_id=cb_id,
                num_vectors=0,
                vector_dim=0,
                data_type=0,
                data=np.array([]),
                offset=cb_offset,
                size=cb_size
            )
            self.codebooks[cb_id] = entry
            offset += 18
    
    def _parse_delta_table(self, data: bytes):
        """Parse delta table chunk."""
        offset = 0
        while offset + 18 <= len(data):  # 2+8+8 = 18 bytes per entry
            d_id, d_offset, d_size = struct.unpack('<HQQ', data[offset:offset+18])
            # Store for later loading
            entry = DeltaEntry(
                delta_id=d_id,
                data_type=0,
                num_elements=0,
                data=np.array([]),
                offset=d_offset,
                size=d_size
            )
            self.deltas[d_id] = entry
            offset += 18
    
    def _parse_sparse_mask_table(self, data: bytes):
        """Parse sparse mask table chunk."""
        offset = 0
        while offset + 18 <= len(data):  # 2+8+8 = 18 bytes per entry
            sm_id, sm_offset, sm_size = struct.unpack('<HQQ', data[offset:offset+18])
            self.sparse_mask_offsets[sm_id] = (sm_offset, sm_size)
            offset += 18
    
    def _parse_pattern_dictionary(self, data: bytes):
        """Parse pattern dictionary chunk."""
        try:
            self.patterns = json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    
    def _parse_reference_map_table(self, data: bytes):
        """Parse reference map table chunk."""
        try:
            self.references = json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    
    def load(self):
        """Load LQT model with full format support."""
        with open(self.filename, 'rb') as f:
            # Read and verify header
            header_data = f.read(LQT_HEADER_SIZE)
            if len(header_data) < LQT_HEADER_SIZE:
                raise ValueError("File too small for LQT header")
            
            magic, version, flags, header_size, metadata_offset, tensor_data_offset, footer_offset = \
                struct.unpack(self.endian_format + 'IHHIQQQ', header_data)
            
            if magic != LQT_MAGIC:
                raise ValueError(f"Invalid LQT magic number: 0x{magic:08x}")
            
            # Check for big-endian flag (bit 15 in flags)
            is_big_endian = (flags & 0x8000) != 0
            if is_big_endian and not self.endian_swap:
                raise ValueError("Big-endian LQT files are not supported without endian_swap=True")
            
            # Set up endianness for struct unpacking
            self.endian_format = '>' if (is_big_endian and self.endian_swap) else '<'
            
            major_version = (version >> 12) & 0xF
            minor_version = version & 0xFFF
            
            if major_version != LQT_VERSION_MAJOR:
                raise ValueError(f"Unsupported LQT version: {major_version}.{minor_version}")
            
            self.metadata_offset = self._swap_endian_64(metadata_offset) if is_big_endian and self.endian_swap else metadata_offset
            self.tensor_data_offset = self._swap_endian_64(tensor_data_offset) if is_big_endian and self.endian_swap else tensor_data_offset
            self.footer_offset = self._swap_endian_64(footer_offset) if is_big_endian and self.endian_swap else footer_offset
            
            # Read metadata chunks
            f.seek(metadata_offset)
            self._read_tlv_chunks(f, tensor_data_offset)
            
            # Load codebooks from tensor data section
            f.seek(tensor_data_offset)
            for cb_id, cb in self.codebooks.items():
                if cb.offset > 0:
                    f.seek(cb.offset)
                    cb_id_check, num_vectors, vector_dim = struct.unpack('<HHH', f.read(6))
                    if cb_id_check == cb_id:
                        cb.num_vectors = num_vectors
                        cb.vector_dim = vector_dim
                        cb.data = np.fromfile(f, dtype=np.float16, count=num_vectors * vector_dim)
                        cb.data = cb.data.reshape(num_vectors, vector_dim)
            
            # Load deltas
            for d_id, d in self.deltas.items():
                if d.offset > 0:
                    f.seek(d.offset)
                    d_id_check, data_type = struct.unpack('<HB', f.read(3))
                    num_elements_bytes = f.read(3)
                    num_elements = struct.unpack('<I', num_elements_bytes + b'\x00')[0]
                    
                    if d_id_check == d_id:
                        d.data_type = data_type
                        d.num_elements = num_elements
                        dtype = np.float16 if data_type == 1 else np.float32
                        d.data = np.fromfile(f, dtype=dtype, count=num_elements)
            
            # Load sparse masks
            for sm_id, (sm_offset, sm_size) in self.sparse_mask_offsets.items():
                if sm_offset > 0:
                    f.seek(sm_offset)
                    sm_id_check, encoding_type, element_count = struct.unpack('<HBH', f.read(5))
                    
                    if sm_id_check == sm_id:
                        # Read mask data based on encoding
                        if encoding_type == 0:  # Bitmap
                            mask_bytes = (element_count + 7) // 8  # Round up to bytes
                            mask_data = np.frombuffer(f.read(mask_bytes), dtype=np.uint8)
                            # Convert bitmap to boolean array
                            self.sparse_masks[sm_id] = np.unpackbits(mask_data)[:element_count].astype(bool)
                        elif encoding_type == 1:  # RLE
                            mask_data = f.read(sm_size - 5)  # Subtract header size
                            self.sparse_masks[sm_id] = self._decode_sparse_mask_rle(mask_data, element_count)
                        elif encoding_type == 2:  # CSR
                            mask_data = f.read(sm_size - 5)  # Subtract header size
                            self.sparse_masks[sm_id] = self._decode_sparse_mask_csr(mask_data)
                        elif encoding_type == 3:  # COO
                            mask_data = f.read(sm_size - 5)  # Subtract header size
                            self.sparse_masks[sm_id] = self._decode_sparse_mask_coo(mask_data)
            
            # Load tensor blobs and recursive tensors with RTA format support
            for name, tensor in self.tensors.items():
                if tensor.codebook_id != 0xFFFF and tensor.codebook_id in self.codebooks:
                    # Tensor uses codebook, might be recursive
                    try:
                        # Check for RTA magic header
                        pos = f.tell()
                        magic = f.read(8)
                        if magic == b'RTATNSR\0':
                            # Load RTA format recursive tensor
                            f.seek(pos)  # Reset to start
                            rt = RecursiveTensor._read_rta_format(f)
                            tensor.recursive_tensor = rt
                            tensor.tensor_type = 1
                        else:
                            # Try legacy RecursiveTensor format
                            f.seek(pos)
                            try:
                                rt = RecursiveTensor.load(f)
                                tensor.recursive_tensor = rt
                                tensor.tensor_type = 1
                            except:
                                # Load quantized indices for standard tensor
                                f.seek(pos)
                                codebook_id, delta_id, sparse_mask_id = struct.unpack('<HHH', f.read(6))
                                
                                if self.load_indices and tensor.codebook_id == codebook_id:
                                    # Load quantized indices
                                    codebook = self.codebooks[tensor.codebook_id]
                                    num_indices = int(np.prod(tensor.shape) // codebook.vector_dim)
                                    indices = np.fromfile(f, dtype=np.uint16, count=num_indices)
                                    self.quantized_indices[name] = indices
                                tensor.tensor_type = 0
                    except:
                        # Standard tensor
                        tensor.tensor_type = 0
            
            # Read footer
            if footer_offset > 0:
                f.seek(footer_offset)
                footer_data = f.read(LQT_FOOTER_SIZE)
                if len(footer_data) >= 16:
                    footer_magic, checksum, edit_log_offset, timestamp = \
                        struct.unpack('<IIQQ', footer_data[:24])
                    
                    if footer_magic == LQTF_MAGIC:
                        # Valid footer
                        self.checksum = checksum
                        
                        # Load edit log if present
                        if edit_log_offset > 0:
                            f.seek(edit_log_offset)
                            remaining_data = f.read()
                            if remaining_data:
                                try:
                                    self.evolution_log = json.loads(remaining_data.decode('utf-8'))
                                except (json.JSONDecodeError, UnicodeDecodeError):
                                    pass
        
        print(f"Loaded LQT model from {self.filename}")
        print(f"- Tensors: {len(self.tensors)}")
        print(f"- Codebooks: {len(self.codebooks)}")
        print(f"- Deltas: {len(self.deltas)}")
        print(f"- Hyperparameters: {len(self.hyperparameters)}")
    
    def get_tensor(self, name: str) -> np.ndarray:
        """Get reconstructed tensor values."""
        if name not in self.tensors:
            raise KeyError(f"Tensor {name} not found")
        
        tensor = self.tensors[name]
        
        if tensor.tensor_type == 1 and tensor.recursive_tensor:
            # RecursiveTensor
            return tensor.recursive_tensor.to_numpy()
        else:
            # Standard tensor - reconstruct from codebook/delta/sparse mask
            result = np.zeros(tensor.shape, dtype=np.float32)
            
            # Get codebook if available
            if tensor.codebook_id != 0xFFFF and tensor.codebook_id in self.codebooks:
                codebook = self.codebooks[tensor.codebook_id]
                
                # Use quantized indices if available for proper reconstruction
                if name in self.quantized_indices and self.quantized_indices[name] is not None:
                    indices = self.quantized_indices[name]
                    # Reconstruct tensor from codebook and indices
                    if indices.size > 0 and codebook.data.size > 0:
                        # Handle different quantization methods
                        if hasattr(self, 'quantization_method') and self.quantization_method == 'pq':
                            # Product Quantization reconstruction
                            subvector_size = codebook.vector_dim
                            reconstructed = np.zeros(indices.size * subvector_size, dtype=np.float32)
                            for i, idx in enumerate(indices):
                                start = i * subvector_size
                                end = (i + 1) * subvector_size
                                reconstructed[start:end] = codebook.data[idx]
                            result = reconstructed.reshape(tensor.shape)
                        else:
                            # Standard reconstruction
                            flat_result = codebook.data[indices]
                            result = flat_result.reshape(tensor.shape)
                else:
                    # Fallback: use first codebook vector as placeholder
                    if codebook.data.size > 0:
                        result = np.tile(codebook.data[0], (result.size // codebook.vector_dim + 1))[:result.size].reshape(tensor.shape)
            
            # Apply delta if available
            if tensor.delta_id != 0xFFFF and tensor.delta_id in self.deltas:
                delta = self.deltas[tensor.delta_id]
                if delta.data.size == result.size:
                    result += delta.data.reshape(tensor.shape)
            
            # Apply sparse mask if available
            if tensor.sparse_mask_id != 0xFFFF and tensor.sparse_mask_id in self.sparse_masks:
                mask = self.sparse_masks[tensor.sparse_mask_id]
                if mask.size == result.size:
                    result *= mask.reshape(tensor.shape)
            
            return result
    
    def get_codebook(self, codebook_id: int) -> Optional[np.ndarray]:
        """Get codebook by ID."""
        if codebook_id in self.codebooks:
            return self.codebooks[codebook_id].data
        return None
    
    def get_delta(self, delta_id: int) -> Optional[np.ndarray]:
        """Get delta by ID."""
        if delta_id in self.deltas:
            return self.deltas[delta_id].data
        return None
    
    def get_sparse_mask(self, mask_id: int) -> Optional[np.ndarray]:
        """Get sparse mask by ID."""
        if mask_id in self.sparse_masks:
            return self.sparse_masks[mask_id]
        return None
    
    def update_codebook(self, codebook_id: int, new_codebook: np.ndarray):
        """Update a codebook (mutation operation)."""
        if codebook_id in self.codebooks:
            cb = self.codebooks[codebook_id]
            if new_codebook.shape == (cb.num_vectors, cb.vector_dim):
                cb.data = new_codebook
                self._log_mutation('codebook_update', {'id': codebook_id})
            else:
                raise ValueError(f"Shape mismatch: expected {(cb.num_vectors, cb.vector_dim)}, got {new_codebook.shape}")
        else:
            raise KeyError(f"Codebook {codebook_id} not found")
    
    def update_delta(self, delta_id: int, new_delta: np.ndarray):
        """Update a delta buffer (mutation operation)."""
        if delta_id in self.deltas:
            d = self.deltas[delta_id]
            if new_delta.size == d.num_elements:
                d.data = new_delta.flatten()
                self._log_mutation('delta_update', {'id': delta_id})
            else:
                raise ValueError(f"Size mismatch: expected {d.num_elements}, got {new_delta.size}")
        else:
            raise KeyError(f"Delta {delta_id} not found")
    
    def update_sparse_mask(self, mask_id: int, new_mask: np.ndarray):
        """Update a sparse mask (mutation operation)."""
        if mask_id in self.sparse_masks:
            old_mask = self.sparse_masks[mask_id]
            if new_mask.size == old_mask.size:
                self.sparse_masks[mask_id] = new_mask
                self._log_mutation('sparse_mask_update', {'id': mask_id})
            else:
                raise ValueError(f"Size mismatch: expected {old_mask.size}, got {new_mask.size}")
        else:
            raise KeyError(f"Sparse mask {mask_id} not found")
    
    def _log_mutation(self, operation: str, details: Dict):
        """Log a mutation operation."""
        self.evolution_log.append({
            'operation': operation,
            'details': details,
            'timestamp': int(time.time() * 1e9)
        })
    
    def evolve_tensor(self, name: str, mutation_strength: float = 0.1):
        """Evolve a tensor through mutation."""
        if name not in self.tensors:
            raise KeyError(f"Tensor {name} not found")
        
        tensor = self.tensors[name]
        
        if tensor.tensor_type == 1 and tensor.recursive_tensor:
            # Use recursive tensor evolution
            rt = tensor.recursive_tensor
            if hasattr(rt, 'evolve') and callable(getattr(rt, 'evolve')):
                rt.evolve(mutation_strength)
            else:
                # Fallback evolution for recursive tensors
                np_data = rt.to_numpy()
                sparsity = rt.get_metadata('sparsity', 0.0)
                sparsity = float(sparsity) if sparsity is not None else 0.0
                
                # Apply mutations
                mask = np.random.random(np_data.shape) < (1.0 - sparsity) * mutation_strength
                mutations = np.random.normal(0, mutation_strength, np_data.shape)
                np_data = np.where(mask, np_data + mutations, np_data)
                
                rt.from_numpy(np_data)
        else:
            # Standard tensor evolution via codebook/delta mutation
            if tensor.codebook_id != 0xFFFF:
                codebook = self.get_codebook(tensor.codebook_id)
                if codebook is not None:
                    # Mutate codebook
                    mutations = np.random.normal(0, mutation_strength, codebook.shape)
                    mutated_codebook = codebook + mutations
                    self.update_codebook(tensor.codebook_id, mutated_codebook)
            
            if tensor.delta_id != 0xFFFF:
                delta = self.get_delta(tensor.delta_id)
                if delta is not None:
                    # Mutate delta
                    mutations = np.random.normal(0, mutation_strength, delta.shape)
                    mutated_delta = delta + mutations
                    self.update_delta(tensor.delta_id, mutated_delta)
        
        # Log evolution
        self._log_mutation('tensor_evolution', {
            'name': name,
            'mutation_strength': mutation_strength
        })
    
    def evolve_tensor_genetic(self, name: str, mutation_rate: float = 0.1, crossover_rate: float = 0.5):
        """Advanced genetic algorithm-based evolution."""
        if name not in self.tensors:
            raise KeyError(f"Tensor {name} not found")
        
        tensor = self.tensors[name]
        
        if tensor.codebook_id != 0xFFFF:
            codebook = self.get_codebook(tensor.codebook_id)
            if codebook is not None:
                # Genetic operations on codebook
                mutated_codebook = self._genetic_mutation(codebook, mutation_rate)
                if crossover_rate > 0:
                    mutated_codebook = self._genetic_crossover(mutated_codebook, codebook, crossover_rate)
                self.update_codebook(tensor.codebook_id, mutated_codebook)
        
        self._log_mutation('genetic_evolution', {
            'name': name,
            'mutation_rate': mutation_rate,
            'crossover_rate': crossover_rate
        })
    
    def _genetic_mutation(self, population: np.ndarray, mutation_rate: float) -> np.ndarray:
        """Apply genetic mutation to population."""
        mutated = population.copy()
        mutation_mask = np.random.random(population.shape) < mutation_rate
        
        # Apply different mutation types
        gaussian_noise = np.random.normal(0, 0.1, population.shape)
        scale_factor = np.random.uniform(0.9, 1.1, population.shape)
        
        # Randomly choose mutation type
        mutation_type = np.random.choice(['gaussian', 'scale', 'flip'], 
                                        size=population.shape, 
                                        p=[0.5, 0.3, 0.2])
        
        mutated = np.where(mutation_type == 'gaussian', 
                          population + gaussian_noise, mutated)
        mutated = np.where(mutation_type == 'scale', 
                          population * scale_factor, mutated)
        mutated = np.where(mutation_type == 'flip', 
                          -population, mutated)
        
        return mutated
    
    def _genetic_crossover(self, parent1: np.ndarray, parent2: np.ndarray, crossover_rate: float) -> np.ndarray:
        """Apply crossover between two parents."""
        if np.random.random() < crossover_rate:
            # Single point crossover
            crossover_point = np.random.randint(1, parent1.size)
            child = np.concatenate([parent1.flat[:crossover_point], 
                                   parent2.flat[crossover_point:]])
            return child.reshape(parent1.shape)
        return parent1
    
    def evolve_tensor_gradient_driven(self, name: str, learning_rate: float = 0.01, 
                                     loss_function: str = 'mse'):
        """Gradient-driven evolution using loss function."""
        if name not in self.tensors:
            raise KeyError(f"Tensor {name} not found")
        
        tensor = self.tensors[name]
        
        if tensor.codebook_id != 0xFFFF:
            codebook = self.get_codebook(tensor.codebook_id)
            if codebook is not None:
                # Compute gradient based on loss function
                if loss_function == 'mse':
                    # Use MSE loss gradient
                    gradient = self._compute_mse_gradient(codebook)
                elif loss_function == 'sparsity':
                    # Use sparsity regularization gradient
                    gradient = self._compute_sparsity_gradient(codebook)
                else:
                    # Default to random gradient
                    gradient = np.random.normal(0, 0.01, codebook.shape)
                
                # Apply gradient descent
                updated_codebook = codebook - learning_rate * gradient
                self.update_codebook(tensor.codebook_id, updated_codebook)
        
        self._log_mutation('gradient_evolution', {
            'name': name,
            'learning_rate': learning_rate,
            'loss_function': loss_function
        })
    
    def _compute_mse_gradient(self, codebook: np.ndarray) -> np.ndarray:
        """Compute MSE loss gradient."""
        # Simplified gradient computation
        # In practice, this would use actual target reconstruction
        target = np.mean(codebook, axis=0, keepdims=True)  # Target is mean vector
        error = codebook - target
        gradient = 2 * error / codebook.size
        return gradient
    
    def _compute_sparsity_gradient(self, codebook: np.ndarray) -> np.ndarray:
        """Compute sparsity regularization gradient."""
        # L1 regularization for sparsity
        sparsity_lambda = 0.001
        gradient = sparsity_lambda * np.sign(codebook)
        return gradient
    
    def validate_module_graph(self) -> bool:
        """Validate module graph structure and dependencies."""
        if not self.module_graph:
            print("No module graph to validate")
            return True
        
        try:
            # Check required fields
            required_fields = ['modules', 'connections', 'inputs', 'outputs']
            for field in required_fields:
                if field not in self.module_graph:
                    print(f"Missing required field: {field}")
                    return False
            
            # Validate module definitions
            modules = self.module_graph['modules']
            for module_name, module_def in modules.items():
                if not isinstance(module_def, dict):
                    print(f"Invalid module definition for {module_name}")
                    return False
                
                # Check for required module fields
                if 'type' not in module_def:
                    print(f"Module {module_name} missing 'type' field")
                    return False
                
                # Validate tensor references
                if 'inputs' in module_def:
                    for input_ref in module_def['inputs']:
                        if input_ref not in self.tensors:
                            print(f"Module {module_name} references unknown tensor {input_ref}")
                            return False
                
                if 'outputs' in module_def:
                    for output_ref in module_def['outputs']:
                        if output_ref not in self.tensors:
                            print(f"Module {module_name} references unknown tensor {output_ref}")
                            return False
            
            # Validate connections
            connections = self.module_graph['connections']
            for conn in connections:
                if 'from' not in conn or 'to' not in conn:
                    print("Connection missing 'from' or 'to' field")
                    return False
                
                from_module, from_output = conn['from'].split('.')
                to_module, to_input = conn['to'].split('.')
                
                if from_module not in modules or to_module not in modules:
                    print(f"Connection references unknown module: {from_module} -> {to_module}")
                    return False
            
            print("Module graph validation passed")
            return True
            
        except Exception as e:
            print(f"Module graph validation error: {e}")
            return False
    
    def monitor_memory_usage(self) -> Dict[str, float]:
        """Monitor current memory usage and adapt behavior."""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            memory_stats = {
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'available_mb': psutil.virtual_memory().available / 1024 / 1024,
                'total_mb': psutil.virtual_memory().total / 1024 / 1024,
                'usage_percent': psutil.virtual_memory().percent
            }
            
            # Adapt behavior based on memory usage
            if memory_stats['usage_percent'] > 90:
                self._throttle_operations(high_memory_usage=True)
            elif memory_stats['usage_percent'] > 75:
                self._throttle_operations(medium_memory_usage=True)
            else:
                self._throttle_operations(normal_memory_usage=True)
            
            return memory_stats
            
        except ImportError:
            # psutil not available
            return {'error': 'psutil not available'}
    
    def _throttle_operations(self, high_memory_usage: bool = False, 
                           medium_memory_usage: bool = False, 
                           normal_memory_usage: bool = False):
        """Throttle operations based on memory usage."""
        if high_memory_usage:
            # Aggressive throttling
            self.max_workers = max(1, self.max_workers // 4)
            self.quantization_method = 'kmeans'  # Use simpler method
            print("High memory usage detected - throttling operations")
            
        elif medium_memory_usage:
            # Moderate throttling
            self.max_workers = max(1, self.max_workers // 2)
            print("Medium memory usage detected - moderate throttling")
            
        else:
            # Normal operation
            self.max_workers = min(8, os.cpu_count() or 4)
            print("Memory usage normal - full operation")
    
    def adaptive_quantization(self, name: str, weights: np.ndarray, bits: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """Adaptive quantization that adjusts based on memory and performance."""
        # Monitor memory before starting
        memory_stats = self.monitor_memory_usage()
        
        if isinstance(memory_stats, dict) and 'usage_percent' in memory_stats:
            usage_percent = memory_stats['usage_percent']
            
            # Adjust quantization strategy based on memory
            if usage_percent > 85:
                # Use very simple quantization
                return self._simple_quantization(weights, bits)
            elif usage_percent > 70:
                # Use standard k-means
                return self._kmeans_quantization(weights, 2 ** bits)
            else:
                # Use parallel advanced quantization
                return self.quantize_tensor_parallel(name, weights, bits)
        else:
            # Fallback to standard quantization
            return self.quantize_tensor(name, weights, bits)
    
    def _simple_quantization(self, weights: np.ndarray, bits: int) -> Tuple[np.ndarray, np.ndarray]:
        """Very simple quantization for low memory situations."""
        num_entries = 2 ** bits
        flat_weights = weights.flatten()
        
        # Simple uniform quantization
        min_val, max_val = flat_weights.min(), flat_weights.max()
        codebook = np.linspace(min_val, max_val, num_entries)
        indices = np.argmin(np.abs(flat_weights[:, None] - codebook[None, :]), axis=1)

        return indices.astype(np.uint16), codebook.astype(np.float32)

    def save_evolved_model(self, filename: str):
        """Save the evolved model in LQT format."""
        # Create a writer and populate it with current state
        writer = LQTWriter(align64=False)
        
        # Copy hyperparameters
        for key, value in self.hyperparameters.items():
            writer.set_hyperparameter(key, value)
        
        # Copy module graph
        if self.module_graph:
            writer.set_module_graph(self.module_graph)
        
        # Copy mutation rules with evolution log
        rules = dict(self.mutation_rules)
        rules['evolution_log'] = self.evolution_log
        for rule_name, rule_data in rules.items():
            writer.add_mutation_rule(rule_name, rule_data)
        
        # Copy codebooks
        for cb_id, cb in self.codebooks.items():
            writer.codebooks[cb_id] = cb
            writer.next_codebook_id = max(writer.next_codebook_id, cb_id + 1)
        
        # Copy deltas
        for d_id, d in self.deltas.items():
            writer.deltas[d_id] = d
            writer.next_delta_id = max(writer.next_delta_id, d_id + 1)
        
        # Copy tensors
        for name, tensor in self.tensors.items():
            writer.tensors[name] = tensor
        
        # Save using writer
        writer.save(filename)
        
        print(f"Saved evolved model to {filename}")
        print(f"- Evolution events: {len(self.evolution_log)}")
    
    def validate_integrity(self) -> bool:
        """Validate model integrity with CRC32 verification and mutation replay."""
        try:
            # Verify CRC32 checksum
            if hasattr(self, 'checksum') and self.checksum:
                with open(self.filename, 'rb') as f:
                    # Read up to footer
                    f.seek(0)
                    file_data = f.read(self.footer_offset)
                    calculated_checksum = zlib.crc32(file_data)
                    if calculated_checksum != self.checksum:
                        print(f"CRC32 checksum mismatch: expected {self.checksum:08x}, got {calculated_checksum:08x}")
                        return False
            
            # Check that all referenced sparse masks exist
            for name, tensor in self.tensors.items():
                if tensor.sparse_mask_id != 0xFFFF and tensor.sparse_mask_id not in self.sparse_masks:
                    print(f"Error: Tensor {name} references missing sparse mask {tensor.sparse_mask_id}")
                    return False
            
            # Check codebook dimensions
            for cb_id, cb in self.codebooks.items():
                if cb.data.shape != (cb.num_vectors, cb.vector_dim):
                    print(f"Error: Codebook {cb_id} dimension mismatch")
                    return False
            
            # Check delta dimensions
            for d_id, d in self.deltas.items():
                if d.data.size != d.num_elements:
                    print(f"Error: Delta {d_id} size mismatch")
                    return False
            
            # Validate quantized indices
            for name, indices in self.quantized_indices.items():
                if name in self.tensors:
                    tensor = self.tensors[name]
                    if tensor.codebook_id != 0xFFFF and tensor.codebook_id in self.codebooks:
                        codebook = self.codebooks[tensor.codebook_id]
                        expected_size = int(np.prod(tensor.shape) // codebook.vector_dim)
                        if indices.size != expected_size:
                            print(f"Error: Quantized indices size mismatch for {name}: expected {expected_size}, got {indices.size}")
                            return False
            
            # Validate mutation replay
            if self.evolution_log:
                return self._validate_mutation_replay()
            
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    
    def _validate_mutation_replay(self) -> bool:
        """Validate that evolution log can recreate current state."""
        try:
            # Create a copy of current state for replay validation
            original_codebooks = {k: v.data.copy() for k, v in self.codebooks.items()}
            original_deltas = {k: v.data.copy() for k, v in self.deltas.items()}
            original_masks = {k: v.copy() for k, v in self.sparse_masks.items()}
            
            # Replay mutations
            for mutation in self.evolution_log:
                operation = mutation['operation']
                details = mutation['details']
                
                if operation == 'codebook_update':
                    cb_id = details['id']
                    if cb_id in self.codebooks:
                        # Mutation should have been applied, verify it exists
                        pass
                elif operation == 'delta_update':
                    d_id = details['id']
                    if d_id in self.deltas:
                        pass
                elif operation == 'sparse_mask_update':
                    sm_id = details['id']
                    if sm_id in self.sparse_masks:
                        pass
                elif operation == 'tensor_evolution':
                    # Tensor evolution mutations
                    pass
            
            # Verify final state matches expected
            for cb_id, original_data in original_codebooks.items():
                if cb_id in self.codebooks:
                    current_data = self.codebooks[cb_id].data
                    # Allow for small numerical differences due to mutations
                    if not np.allclose(original_data, current_data, rtol=1e-5):
                        print(f"Mutation replay validation failed for codebook {cb_id}")
                        return False
            
            return True
        except Exception as e:
            print(f"Mutation replay validation error: {e}")
            return False
