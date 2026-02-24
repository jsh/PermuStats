# PermuStats Implementation Checklist
    
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
    
    ## Phase 2: Plugin Architecture & Transformers
    - [ ] **Plugin Interface**
        - [ ] Create `PermuPlugin` abstract base class with `process()` method.
    - [ ] **Transformer Implementation**
        - [ ] Implement `CycleFormTransformer` (Standard -> Canonical Cycle Form).
    - [ ] **Testing**
        - [ ] Unit test: Verify cycle decomposition (e.g., `[1, 0, 2]` -> `[[0, 1], [2]]`).
    
    ## Phase 3: Counters & Metrics
    - [ ] **Basic Counters**
        - [ ] Implement `FixedPointCounter` (counts $p[i] == i$).
        - [ ] Implement `CycleLengthCounter` (extracts lengths from cycle form).
    - [ ] **Testing**
        - [ ] Unit test: `FixedPointCounter` on various permutations.
        - [ ] Unit test: `CycleLengthCounter` returns correct list of integers.
    
    ## Phase 4: Pipeline Controller (The Agent)
    - [ ] **Execution Engine**
        - [ ] Create `PermuStatsEngine` to manage data flow.
        - [ ] Implement pipeline wiring: `Generator` -> `Transformer[]` -> `Counter`.
        - [ ] Implement result aggregation logic.
    - [ ] **Testing**
        - [ ] Integration test: Full pipeline for $N=3$ exhaustive fixed-point counting.
    
    ## Phase 5: Analyzer & External Integration
    - [ ] **Statistical Analysis**
        - [ ] Implement `Analyzer` for Mean and Variance.
        - [ ] (Optional) Implement OEIS API lookup for sequence identification.
    - [ ] **Validation Tap**
        - [ ] Implement parity check utility for small $N$ verification.
    
    ## Phase 6: User Interface & Refinement
    - [ ] **CLI Development**
        - [ ] Create entry point script.
        - [ ] Add arguments for $N$, Mode, and Plugin selection.
    - [ ] **Documentation**
        - [ ] Update README with usage instructions.
        - [ ] Finalize `DIGEST.md` output format for findings.
    
    ---
    
    ### Progress Summary
    - **Total Tasks:** 20
    - **Completed:** 0
    - **Current Sprint:** Phase 1: Foundation
    
