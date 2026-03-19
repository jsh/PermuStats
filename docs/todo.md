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
- [x] **Renaming:** Refactor all references from "Agent" to "Engine" across the codebase to reflect core logic focus.
- [x] **Modern Stack Alignment:**
    - [x] Verify `ruff` compliance for all modules.
    - [x] Add `ty` type hints to core permutation logic.
- [x] **Expanded Testing Suite (pytest):**
    - [x] Implement boundary tests (null sets, singletons).
    - [x] Add "Permutation Integrity" tests (ensure no data loss during transformations).
    - [x] Benchmark execution time for large datasets using `uv run pytest`.
- [x] **Architectural Hole Check:** Review Engine-to-UI data flow for potential bottlenecks.

## Phase 5: Statistical Analyzer & Validation
- [x] **Statistical Analysis**
  - [x] Implement `Analyzer` for Mean and Variance.
  - [x] Implement OEIS API lookup for sequence identification.
- [x] **Validation Tap**
  - [x] Implement validation tap utility (Sum of Frequencies and Fixed Point Identity).

### Phase 5.5: Performance Optimization & Memory Hardening

- [x] **Phase 5.5a: Bottleneck Identification (Profiling)**
    - [x] Profile the execution loop using `pyinstrument` or `cProfile`.
    - [x] Identify hot spots in `decompose_cycles` and the `Engine` assembly line.
- [x] **Phase 5.5b: Defusing the Memory Bomb**
    - [x] Refactor `Analyzer` to accept an `Iterable[AnalysisResult]`.
    - [x] Implement Welford’s Online Algorithm for $O(1)$ space complexity statistics.
- [x] **Phase 5.5c: The "Tax" Refund (Execution Speed)**
    - [x] Optimize the `Inspector` registry loop.
    - [x] Refactor `decompose_cycles` to use a boolean "visited" array (bitmask).
    - [x] Bypass redundant object copies in `run_study`.
- [x] **Phase 5.5d: Regression Benchmarking**
    - [x] Compare memory/speed against Phase 4 baseline.

### Phase 6: Rich Metric Expansion
- [x] **Phase 6.1: The Mahonian Metric (Inversions)**
    - [x] Ground Truth: Implement Mahonian recurrence $T(n, k)$ in `math_utils.py`.
    - [x] Analysis: Add `inversions: int` to `AnalysisResult`.
    - [x] Inspector: Create `InversionInspector` and register it.
    - [x] Validation: Distribution check against $T(5, k)$.
- [ ] **Phase 6.2: Eulerian Statistics (Descents)**
    - [ ] Ground Truth: Implement Eulerian Numbers $A(n, k)$ in `math_utils.py`.
    - [ ] Inspector: Create `DescentInspector` (name: "descents").
    - [ ] Validation: Verify mean is $(n-1)/2$.

## Phase 7: User Interface & Refinement
- [ ] **CLI Development**
  - [ ] Create entry point script (`main.py`) with `argparse`.
  - [ ] Implement smart argument switching (Sample vs. Exhaustive).
- [ ] **Testing**
  - [ ] End-to-end integration tests with `pytest` and `capsys`.
- [ ] **Documentation**
  - [ ] Update README with usage instructions.

### Progress Summary
**Total Tasks:** 56 / 67 [COMPLETE]
