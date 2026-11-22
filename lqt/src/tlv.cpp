// src/tlv.cpp — TLV metadata system implementation (A2).
//
// Council module: A2 (TLV metadata).
// Canon: lqt.md §2.3 "Metadata Chunks (TLV Format)"; Binary Spec v1.3 §3.
//
// All hot-path logic (serialize, parse, encode/decode helpers) lives in tlv.h
// as inline functions to allow inlining at call sites.  This translation unit
// satisfies the build system's src/*.cpp glob and provides a compilation unit
// for any future non-inline definitions.
//
// DESIGN DECISION (non-inline split):
//   The TLV layer is entirely stateless — every operation takes arguments and
//   returns values.  Placing all code inline in the header avoids a link-time
//   dependency between modules that only include lqt/tlv.h, and keeps the
//   binary footprint minimal.  This .cpp file is intentionally thin.

#include "lqt/tlv.h"

// No out-of-line definitions are currently required; all are inline in tlv.h.
// This file intentionally left as a compilation unit placeholder that confirms
// the header is self-contained and compiles cleanly as a standalone TU.
