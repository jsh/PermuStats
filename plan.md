Based on the project specification, I have drafted a blueprint and a series of prompts for building **PermuStats**.

The architecture follows a Unix-style pipeline: **Generator → Transformer (Plugin) → Counter (Plugin) → Analyzer**. The core will be built using a "Generator-based" approach to handle large sets of permutations efficiently (Monte Carlo vs. Exhaustive).

### The Blueprint

1. **Phase 1: Foundation & The Generator Core**
* Define the internal representation of a permutation (zero-indexed array/list).
* Implement the `PermutationGenerator` with two strategies: `Exhaustive` (Lexicographic) and `Monte Carlo` (Fisher-Yates).


2. **Phase 2: The Plugin Interface & Transformers**
* Define the abstract Base Class/Interface for `Plugin`.
* Implement a `Transformer` plugin (e.g., converting to Canonical Cycle Form).


3. **Phase 3: Counters & Metrics**
* Implement a `Counter` plugin that extracts properties (Fixed Points, Cycle Lengths).


4. **Phase 4: The Pipeline Controller (The Agent)**
* Create the engine that wires the `Generator` to `Plugins` and collects results for the `Analyzer`.


5. **Phase 5 : The Statistical Analyzer & Validation**
* Turn the raw lists from the `Engine` into mathematical insights and verify correctness.


6. **Phase 6: The Command-Line Interface (CLI)**
* Create a professional entry point for users to interact with the `PermuStats` pipeline without touching code.

---

### Step-by-Step Implementation Prompts

The following prompts are designed for an LLM to implement the project incrementally using Test-Driven Development (TDD).

#### Prompt 1: The Core Permutation Generator

Task: Implement the foundation of PermuStats. Create a class `PermutationGenerator` that can yield permutations of size N.

* Requirement 1: Use a Python generator (yield) to ensure memory efficiency.
* Requirement 2: Implement `exhaustive()` mode using lexicographic order (you may use itertools.permutations for this initial step).
* Requirement 3: Implement `random(samples: int)` mode using the Fisher-Yates shuffle to provide a Monte Carlo stream.
* Testing: Write unit tests to verify that `exhaustive(N=3)` yields exactly 6 unique permutations and `random(N=10, samples=100)` yields exactly 100 permutations.
* Architecture: Ensure the output of the generator is a simple List[int].

#### Prompt 2: The Plugin Interface and First Transformer

Task: Building on the previous code, define the `Plugin` architecture.

* Requirement 1: Create an abstract base class `PermuPlugin`. It should have a method `process(permutation: List[int])` that returns a processed result.
* Requirement 2: Create a `Transformer` subclass called `CycleFormTransformer`. It should take a standard permutation (e.g., [1, 0, 2]) and return its cycle decomposition (e.g., [[0, 1], [2]]).
* Testing: Write tests for `CycleFormTransformer` ensuring it correctly identifies cycles in permutations of various lengths.
* Integration: Ensure the `Transformer` can receive the output directly from the `PermutationGenerator`.

#### Prompt 3: The Counter Plugin

Task: Implement the `Counter` type of plugin to extract statistics.

* Requirement 1: Create a `FixedPointCounter` (a subclass of `PermuPlugin`). It should count elements that map to themselves (where p[i] == i).
* Requirement 2: The `process` method should return an integer.
* Requirement 3: Create a `CycleLengthCounter` that takes the output of the `CycleFormTransformer` and returns a list of the lengths of the cycles.
* Testing: Test `FixedPointCounter` with [0, 1, 2] (result: 3) and [1, 2, 0] (result: 0).

#### Prompt 4: The Pipeline Controller (The "Agent")

Task: Create the `PermuStatsEngine` to wire the components together.

* Requirement 1: The engine should accept a `Generator`, a list of `Transformers`, and a `Counter`.
* Requirement 2: It should iterate through the generator, pass the data through the chain of transformers, and finally to the counter.
* Requirement 3: It should aggregate the results (e.g., a list of counts) to be ready for analysis.
* Testing: Mock a pipeline where `Exhaustive(3)` -> `FixedPointCounter` results in the list [3, 1, 1, 1, 1, 0] (for permutations of N=3).

#### Prompt 5: The Statistical Analyzer & Validation (Corrected for Pytest)

Task: Implement the "Analyzer" layer for statistical processing, data validation, and external sequence formatting.

1. **File 1: `analysis.py` (Statistical Core)**
* Create an `Analyzer` class.
* It should take an iterable of integer results (from the `Engine`) and provide the following methods:
* `mean()`: Returns the average value.
* `variance()`: Returns the variance.
* `frequency_distribution()`: Returns a dictionary mapping each value to its count (e.g., `{0: 2, 1: 3, 3: 1}`).

2. **File 2: `validation.py` (Validation Tap)**
* Implement a `validate_results(n, distribution)` utility function.
* For a given N, it must verify two combinatorial identities:
1. Sum of frequencies must equal $N!$ (Total permutations).
2. Sum of (value × frequency) must equal $N!$ (The expected sum of fixed points for $S_n$ is always $1 \times N!$).

3. **OEIS Search Utility:**
* Add an `OEISLookup` class or utility.
* It should take a frequency distribution and return a comma-separated string for searching the Online Encyclopedia of Integer Sequences.
* It must identify the range from $0$ to $N$, filling in zeros for any missing counts (e.g., for $N=3$, `{0: 2, 1: 3, 3: 1}` becomes `"2,3,0,1"`).


4. **Testing (`test_analysis.py`):**
* **Requirement: Use native `pytest` style (standard `assert` statements, no `unittest.TestCase`).**
* Verify that for $N=3$ (Fixed Points), `mean()` is exactly `1.0` and the distribution is `{0: 2, 1: 3, 2: 0, 3: 1}`.
* Verify that `validate_results` returns `True` for $N=4$ exhaustive results.
* Verify that `OEISLookup` correctly transforms the $N=3$ distribution into the exact string `"2,3,0,1"`, ensuring the missing '2' is represented by a '0'.`

#### Prompt 6: The Command-Line Interface (CLI)

Task: Create a robust CLI entry point for PermuStats.

* Requirement 1: Create `main.py` using `argparse`. Users should be able to run commands like:
`python main.py --n 4 --mode exhaustive --stat fixed-points`
* Requirement 2: Support a "Monte Carlo" mode for large N where the user specifies `--samples 1000`.
* Requirement 3: Format the output into a "DIGEST.md" or console summary that clearly displays the parameters used, the statistical mean/variance, and the cycle-form distribution.
* Testing: Create a "Smoke Test" that invokes `main.py` via the command line and checks that it exits with code 0 and prints a valid summary table.`
