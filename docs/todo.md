# PermuStats Implementation Checklist

**Current Sprint:** Project Review -- Phase-by-Phase review of the project.

## Phase 1: Foundation & Generator Core
- [x] **Core Permutation Representation**
  - [x] Define internal data structure (List[int]) for permutations.
  - [x] Implement `PermutationGenerator` base class.
- [x] **Generation Strategies**
  - [x] Implement `exhaustive(N)` using lexicographic order.
  - [x] Implement `sample(N, samples)` using Fisher-Yates shuffle (Monte Carlo).
- [x] **Testing**
  - [x] Unit test: `exhaustive(3)` returns 6 unique results.
  - [x] Unit test: `sample(10, 100)` returns exactly 100 results.
  - [x] Unit test: Verify each generated result is a valid permutation of {0...N-1}.

## Phase 2: Architecture (Transformers as Shapers, Plugins as Measurers)
- [x] **Plugins as Measurers Interface**
  - [x] Create `PermuPlugin` abstract base class with `calculate()` method.
- [x] **Transformers as Shapers Implementation**
  - [x] Implement `CycleTransformer` (Standard -> Canonical Cycle Form).
- [x] **Testing**
  - [x] Unit test: `test_transformers.py` verifies cycle decomposition (e.g., `[1, 0, 2]` -> `[[0, 1], [2]]`).
  - [x] Unit test: `test_plugins.py` verifies ABC contract and plugin logic.

## Phase 3: Implementing Core Plugins
- [x] **Basic Counters**
  - [x] Implement `FixedPointPlugin` (counts $p[i] == i$).
  - [x] Implement `CycleLengthsPlugin` (list of lengths).
  - [x] Implement `CycleCountPlugin` (single integer -- number of cycles)
- [x] **Testing**
  - [x] Unit test: Verify `FixedPointPlugin` on various permutations.
  - [x] Unit test: Verify `CycleLengthsPlugin` returns correct list of integers.
  - [x] Unit test: Verify `CycleCountPlugin` returns correct number of cycles.

## Phase 4: The Engine (Refactoring & Hardening)
- [ ] **Renaming:** Refactor all references from "Agent" to "Engine" across the codebase to reflect core logic focus.
- [ ] **Modern Stack Alignment:** - [ ] Verify `ruff` compliance for all modules.
    - [ ] Add `ty` type hints to core permutation logic.
- [ ] **Expanded Testing Suite (pytest):**
    - [ ] Implement boundary tests (null sets, singletons).
    - [ ] Add "Permutation Integrity" tests (ensure no data loss during transformations).
    - [ ] Benchmark execution time for large datasets using `uv run pytest`.
- [ ] **Architectural Hole Check:** Review Engine-to-UI data flow for potential bottlenecks.

## Phase 5: Statistical Analyzer & Validation
- [ ] **Statistical Analysis**
  - [ ] Implement `Analyzer` for Mean and Variance.
  - [ ] Implement OEIS API lookup for sequence identification.
- [ ] **Validation Tap**
  - [ ] Implement validation tap utility (Sum of Frequencies and Fixed Point Identity).

## Phase 6: User Interface & Refinement
- [ ] **CLI Development**
  - [ ] Create entry point script (`main.py`) with `argparse`.
  - [ ] Implement smart argument switching (Sample vs. Exhaustive).
- [ ] **Testing**
  - [ ] End-to-end integration tests with `pytest` and `capsys`.
- [ ] **Documentation**
  - [ ] Update README with usage instructions.

### Progress Summary
**Total Tasks:** 30 / 30 [COMPLETE]
