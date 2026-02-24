Here is a clean `README.md` that summarizes the foundation we've built. This serves as your "Project Milestone" marker so you can pick back up exactly where you left off.

---

# PermuStats: Foundation

This repository contains the core generation logic for **PermuStats**, a library designed for generating and analyzing permutations efficiently using Python generators.

## 🚀 Components

### 1. `generator.py`

Contains the `PermutationGenerator` class, which leverages Python generators to provide memory-efficient access to permutations.

* **`exhaustive(n)`**: Yields all  permutations in lexicographic order using `itertools`.
* **`sample(n, num_samples)`**: Yields a specific number of random permutations using `random.sample` (optimized C-implementation of the Fisher-Yates shuffle).

### 2. `test_generator.py`

A comprehensive test suite using `pytest` to ensure:

* Correct permutation counts for exhaustive sets.
* Requested sample sizes are met.
* Data integrity (each permutation is a valid zero-indexed set of integers from  to ).

## 🛠 Usage

To generate all permutations of size 3:

```python
from generator import PermutationGenerator

for p in PermutationGenerator.exhaustive(3):
    print(p)

```


## ✅ Status: Milestone 1 Complete

* [x] Core Generator Class
* [x] Lexicographic Generator
* [x] Random Sampling Generator
* [x] Unit Tests

---

# PermuStats: Modular Analysis

**PermuStats** is a Python library for generating and analyzing permutations. It uses a plugin-based architecture to allow for extensible mathematical transformations and statistical analysis.

## 🚀 Components

### 1. Generation (`generator.py`)

Memory-efficient generators for permutation data.

* **`exhaustive(n)`**: All  permutations in lexicographic order.
* **`sample(n, num_samples)`**: Randomly sampled permutations.

### 2. Plugin Architecture (`plugin.py`)

The project uses an Abstract Base Class (`PermuPlugin`) to ensure all analysis tools follow a consistent interface. This makes it easy to "plug and play" new mathematical transformers.

### 3. Transformers (`transformers.py`)

* **`CycleFormTransformer`**: Converts standard one-line notation (e.g., `[1, 0, 2]`) into **Canonical Cycle Form** (e.g., `[[0, 1], [2]]`). This is essential for studying the decomposition of permutations into disjoint cycles.

## 🛠 Usage

To transform a permutation into its cycle form:

```python
from transformers import CycleFormTransformer

transformer = CycleFormTransformer()
p = [1, 2, 0]
print(f"Standard: {p} -> Cycles: {transformer.process(p)}")
# Output: Standard: [1, 2, 0] -> Cycles: [[0, 1, 2]]

```

To run the test suite:

```bash
pytest test_generator.py test_plugins.py

```

## ✅ Status: Milestone 2 Complete

* [x] Core Generator Class
* [x] Abstract Plugin Interface
* [x] Cycle Form Transformer
* [x] Unit Tests for Generators & Plugins

---

That’s another milestone in the bag. With these counters, **PermuStats** is now capable of extracting specific quantitative data from the qualitative structures we built in Phase 2.

Here is the updated `README.md`, now featuring the **Analysis & Statistics** section.

---

# PermuStats: Analysis & Statistics

**PermuStats** is a modular Python library for generating, transforming, and extracting statistics from permutations. It uses a decorator-inspired plugin architecture to keep mathematical logic decoupled and testable.

## 🚀 Components

### 1. Generation (`generator.py`)

Memory-efficient generators for permutation data.

* **`exhaustive(n)`**: All  permutations in lexicographic order.
* **`sample(n, num_samples)`**: Randomly sampled permutations using `random.sample`.

### 2. Plugin Architecture (`plugin.py`)

All tools inherit from the `PermuPlugin` Abstract Base Class, ensuring a consistent `.process()` interface across the library.

### 3. Transformers & Counters (`transformers.py`)

The library separates **structural transformations** from **numerical counters**:

* **`CycleFormTransformer`**: Converts standard notation to disjoint cycles (e.g., `[1, 0, 2]` → `[[0, 1], [2]]`).
* **`FixedPointCounter`**: Returns the count of elements that map to themselves ().
* **`CycleLengthCounter`**: Takes cycle-form data and returns a list of cycle lengths (e.g., `[[0, 1], [2]]` → `[2, 1]`).

## 🛠 Usage

### Statistical Extraction

```python
from transformers import FixedPointCounter, CycleFormTransformer, CycleLengthCounter

# 1. Count Fixed Points
fp = FixedPointCounter()
print(fp.process([0, 1, 2])) # Output: 3

# 2. Get Cycle Lengths (Pipelined)
transformer = CycleFormTransformer()
cl_counter = CycleLengthCounter()

p = [1, 0, 2]
cycles = transformer.process(p)
lengths = cl_counter.process(cycles)
print(lengths) # Output: [2, 1]

```

To run the full test suite:

```bash
pytest test_generator.py test_plugins.py

```

## ✅ Status: Milestone 3 Complete

* [x] Core Generator Class
* [x] Abstract Plugin Interface
* [x] Cycle Form Transformer
* [x] **Fixed Point Counter**
* [x] **Cycle Length Counter**
* [x] Expanded Unit Tests

---


