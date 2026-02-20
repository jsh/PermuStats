# PermuStats Project Evolution: Full History and Specification
    
    ## Section 1: The Initial Request
    The project began with the following vision:
    "I've been thinking about the statistics of permutation cycles. Some of my work is pure mathematics, but knowing the answers beforehand helps. For example, suppose I want to know the expected number of fixed-points in a random permutations of N elements... It would help me to have an agent that accepts requests like these:
    - 'What is the expected number of fixed-points for all permutations on 5 elements? Use exhaustive enumeration.'
    - 'What is the variance of the number of fixed points in permutations on 6 elements? Use exhaustive enumeration.'
    - 'Count the number of transpositions in each possible permutation on 9 elements, show me a table of how many have 0, 1, ..., and graph that table.'
    - 'Estimate the fraction of derangements in random permutations on the integers 1..1,000,000, using a Monte Carlo method.'
    - 'What is the expected number of cycles in permutations on 7 elements?'"
    
    ## Section 2: The Iterative Dialogue (15-Question Specification Process)
    The final specification was built through an iterative Q&A process to define the system's architecture and behavior:
    1. **Plan of Execution:** The agent will provide a formal plan for review before running code.
    2. **Generator Method:** Uses a generator-based approach (e.g., Python’s itertools) for memory efficiency.
    3. **Data Communication:** The Generator passes "tallies" (summaries) to the Analyzer rather than raw permutation lists.
    4. **Analyzer Scope:** The Analyzer follows the user's prompt strictly, avoiding default statistical suites unless requested.
    5. **Validation & TDD:** Includes a 'Validation Tap' to compare Python and high-performance (Rust/Go) outputs for exact parity using small N samples and canonical forms.
    6. **Simulation Budget:** Monte Carlo simulations can be budgeted by time or confidence intervals.
    7. **Storage:** The system functions as a modular library on GitHub rather than a one-off sandbox.
    8. **Design Philosophy:** A plugin-based architecture following the Unix philosophy ("Do one thing and do it well").
    9. **Pipeline Structure:** Core -> Transformer (e.g., convert to canonical cycles) -> Counter (e.g., count cycles).
    10. **Data Handling:** Uses Unix-like streams for low memory footprint.
    11. **Verification:** Testing includes exact matches of permutation lists and cycle decompositions in canonical form.
    12. **Optimization:** The agent follows a "Fail Fast" approach, asking the user before attempting complex optimizations.
    13. **Reporting:** Results are provided via chat summaries and committed to the GitHub repository.
    14. **Integration:** Designed to be compatible with tools like NotebookLM for generating presentations.
    15. **External Knowledge:** The Analyzer integrates with the OEIS (Online Encyclopedia of Integer Sequences) API to verify experimental results.
    
    ## Section 3: The "Ready for Hand-off" Specification
    ### Project Title: PermuStats – A Stream-Based Mathematical Exploration Agent
    
    **Core Architecture:**
    - **System Model:** A Unix-style pipeline where data flows from a **Generator** -> **Transformer** -> **Counter** -> **Analyzer**.
    - **Delivery:** A modular library hosted on **GitHub** (Python core, with a clear path for Rust/Go optimization).
    
    **The Components:**
    1. **The Generator:** Creates permutations of N elements (Exhaustive or Monte Carlo) using a generator-based approach.
    2. **Transformers (Plugins):** Standardize permutations into mathematical forms (e.g., Canonical Cycle Form).
    3. **Counters (Plugins):** Extract specific metrics from the stream (e.g., fixed points, transpositions, cycle lengths).
    4. **The Analyzer:** Performs statistical calculations (Mean, Variance, Frequency Tables) and consults the **OEIS API** to identify sequences.
    5. **Validation Tap:** A utility that ensures 100% parity between Python and high-performance implementations by comparing exact outputs for small N.
    
    **Interaction Workflow:**
    1. User Request -> 2. Plan of Execution -> 3. Execution -> 4. Project Bundle (Chat Summary + GitHub commit).
    
