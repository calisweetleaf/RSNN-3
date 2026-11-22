// lqt/error.h — Exception hierarchy for the LQT reference implementation.
//
// Council module: A1/A10 (shared foundation).
// Canon: lqt.md §8 (Security/Integrity), §5.2 (Mutation Validation).
//
// Design intent: parse/format problems, integrity failures, validation
// rejections, and access-control denials are distinct, catchable categories.
// All derive from LqtError so callers can catch broadly or narrowly.
#pragma once

#include <stdexcept>
#include <string>

namespace lqt {

// Base for every error this library raises.
class LqtError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

// Bad magic, truncated buffers, malformed TLV, impossible offsets, etc.
class FormatError : public LqtError {
public:
    using LqtError::LqtError;
};

// Checksum / signature mismatch, tamper-evident edit-log failure.
class IntegrityError : public LqtError {
public:
    using LqtError::LqtError;
};

// Mutation rejected by the validation framework (dimension/value/topology).
class ValidationError : public LqtError {
public:
    using LqtError::LqtError;
};

// Attempt to modify a PROTECTED tensor / critical-path module without rights.
class AccessError : public LqtError {
public:
    using LqtError::LqtError;
};

} // namespace lqt
