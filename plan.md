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
* Create the engine that wires the Generator to Plugins and collects results for the Analyzer.


5. **Phase 5: Refinement & CLI**
* Add a command-line interface to configure , the mode, and the pipeline stages.



---

### Step-by-Step Implementation Prompts

The following prompts are designed for an LLM to implement the project incrementally using Test-Driven Development (TDD).

#### Prompt 1: The Core Permutation Generator

`Task: Implement the foundation of PermuStats. Create a class `PermutationGenerator` that can yield permutations of size N.

* Requirement 1: Use a Python generator (yield) to ensure memory efficiency.
* Requirement 2: Implement `exhaustive()` mode using lexicographic order (you may use itertools.permutations for this initial step).
* Requirement 3: Implement `random(samples: int)` mode using the Fisher-Yates shuffle to provide a Monte Carlo stream.
* Testing: Write unit tests to verify that `exhaustive(N=3)` yields exactly 6 unique permutations and `random(N=10, samples=100)` yields exactly 100 permutations.
* Architecture: Ensure the output of the generator is a simple List[int].`

#### Prompt 2: The Plugin Interface and First Transformer

`Task: Building on the previous code, define the Plugin architecture.

* Requirement 1: Create an abstract base class `PermuPlugin`. It should have a method `process(permutation: List[int])` that returns a processed result.
* Requirement 2: Create a `Transformer` subclass called `CycleFormTransformer`. It should take a standard permutation (e.g., [1, 0, 2]) and return its cycle decomposition (e.g., [[0, 1], [2]]).
* Testing: Write tests for `CycleFormTransformer` ensuring it correctly identifies cycles in permutations of various lengths.
* Integration: Ensure the `Transformer` can receive the output directly from the `PermutationGenerator`.`

#### Prompt 3: The Counter Plugin

`Task: Implement the "Counter" type of plugin to extract statistics.

* Requirement 1: Create a `FixedPointCounter` (a subclass of `PermuPlugin`). It should count elements that map to themselves (where p[i] == i).
* Requirement 2: The `process` method should return an integer.
* Requirement 3: Create a `CycleLengthCounter` that takes the output of the `CycleFormTransformer` and returns a list of the lengths of the cycles.
* Testing: Test `FixedPointCounter` with [0, 1, 2] (result: 3) and [1, 2, 0] (result: 0).`

#### Prompt 4: The Pipeline Controller (The "Agent")

`Task: Create the `PermuStatsEngine` to wire the components together.

* Requirement 1: The engine should accept a `Generator`, a list of `Transformers`, and a `Counter`.
* Requirement 2: It should iterate through the generator, pass the data through the chain of transformers, and finally to the counter.
* Requirement 3: It should aggregate the results (e.g., a list of counts) to be ready for analysis.
* Testing: Mock a pipeline where `Exhaustive(3)` -> `FixedPointCounter` results in the list [3, 1, 1, 1, 1, 0] (for permutations of N=3).`

#### Prompt 5: Wiring and Integration

`Task: Finalize the project by adding an "Analyzer" and a simple CLI.

* Requirement 1: Create an `Analyzer` that takes the list of results from the `PermuStatsEngine` and calculates the Mean and Variance.
* Requirement 2: Create a main entry point where a user can specify N, the mode (Exhaustive/Monte Carlo), and which statistics they want to track.
* Requirement 3: Ensure all components are type-hinted and follow the stream-based approach defined in the spec.
* Testing: Run an end-to-end test verifying that for N=3, the average number of fixed points is 1.0.`
