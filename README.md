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

Now that we have the infrastructure to "process" permutations, we can actually start looking at the statistics of large sets.

**Would you like me to create an `orchestrator.py` that takes a generator and a plugin to run a batch analysis on 1,000 random samples?**
