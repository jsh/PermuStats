### Project Title: PermuStats – A Stream-Based Mathematical Exploration Agent

**Core Architecture:**
- **System Model:** A Unix-style pipeline where data flows from a **Generator** -> **Transformer** -> **Counter** -> **Analyzer**.
- **Delivery:** A modular library hosted on **GitHub** (Python core, with a clear path for Rust/Go optimization).

**optimizationThe Components:**
1. **The Generator:** Creates permutations of N elements (Exhaustive or Monte Carlo) using a generator-based approach.
2. **Transformers (Plugins):** Standardize permutations into mathematical forms (e.g., Canonical Cycle Form).
3. **Counters (Plugins):** Extract specific metrics from the stream (e.g., fixed points, transpositions, cycle lengths).
4. **The Analyzer:** Performs statistical calculations (Mean, Variance, Frequency Tables) and consults the **OEIS API** to identify sequences.
5. **Validation Tap:** A utility that ensures 100% parity between Python and high-performance implementations by comparing exact outputs for small N.

**Interaction Workflow:**
1. User Request -> 2. Plan of Execution -> 3. Execution -> 4. Project Bundle (Chat Summary + GitHub commit).

Where these components are:

1. User Request: For example, "Expected number of cycles for N=7."
2. Plan of Execution: Agent generates a step-by-step logic plan for your review.
3. Execution: Agent runs the code, tallies the results, and checks OEIS.
4. Project Bundle: Agent provides a chat summary and commits a DIGEST.md to GitHub containing the math, the code, and the findings.
