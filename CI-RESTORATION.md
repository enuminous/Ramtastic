# Diagnostic CI restoration — 23 October 2026

The October 16 upload replaced the complete root with three Bass imports,
including an unavailable `Ramtastic/Bass/CliffordBridge.lean`, and introduced a
second Lake configuration for an absent `RequestProject`. The resulting run
failed before building the project; dependent audit errors were consequences
of that missing build.

## Restored inputs

- `CliffordBridge.lean` is copied byte-for-byte from
  [Aristotle-Ramtastic-Audit at 5363f08](https://github.com/enuminous/Aristotle-Ramtastic-Audit/blob/5363f08e2657c578267274cb1e75e4498993b22d/Ramtastic/Bass/CliffordBridge.lean).
  Its [provenance](https://github.com/enuminous/Aristotle-Ramtastic-Audit/blob/5363f08e2657c578267274cb1e75e4498993b22d/PROVENANCE.md)
  identifies a reconstruction from the uploaded `BassCompletion.lean`, Aristotle
  run `6b97b551-c689-4d49-9ea2-282f6f81a993`. It is not represented as a recovered
  byte-identical original Aristotle export. Existing author credits are retained.
- The complete root imports every source module, including the existing
  `HingeAnalysis` and the restored Clifford extension. The root is copied from
  that same pinned audit revision; missing imports may not be removed to obtain
  a green build.
- The incompatible uploaded `lakefile.toml` is retained under
  `provenance/2026-10-16-upload-lakefile.toml`. The active `lakefile.lean` now names
  the immutable Mathlib revision already in the lock. Lean remains 4.30.0-rc1.
- `audit/check_sources.py` checks complete import coverage, original release
  source hashes, the restored module hash, and dependency agreement before setup.
  Both the original subset and complete-project axiom audits have rejection controls.

## Meaning of a successful run

The [diagnostic workflow](https://github.com/enuminous/Ramtastic/actions/workflows/zoo-audit.yml)
still applies the explicitly disclosed namespace/zero-form correction in its
disposable checkout. The frozen upstream Dolbeault source and its historical
failure remain unchanged. A successful run verifies the reconstructed complete
project **with that diagnostic correction**, its compiled axiom checks, rejection
controls, and semantic counterexamples. It does not retrospectively certify the
unmodified release or establish the broader claims discussed in the audit.

The original October 16 report, evidence counts, and flat archive remain historical
artifacts. Current CI can have additional declarations because it includes the
later HingeAnalysis and Clifford modules. Consult the current run logs for counts.
