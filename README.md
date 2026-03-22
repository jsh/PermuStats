# PermuStats

A high-performance Python engine for analyzing combinatorial statistics of permutations. Designed for $O(1)$ memory streaming and deep integration with the Online Encyclopedia of Integer Sequences (OEIS).

## 🚀 Installation

Ensure you have [uv](https://github.com/astral-sh/uv) installed, then clone and install:

```bash
git clone https://github.com/jsh/PermuStats.git
cd PermuStats
uv sync
```

## 🛠️ Usage

### Quick Start
Analyze the distribution of descents (Eulerian numbers) for all permutations of $N=4$:


```bash
python -m permustats.main -n 4 --stat descents
```

```text
Parameters: N=4, Mode=Exhaustive, Stat=descents

--- Statistics Report [descents] ---
Sample Size:   24
Mean:          1.5000
Variance:      0.4167
Distribution:  {0: 1, 1: 11, 2: 11, 3: 1}
OEIS:          A008292 (Eulerian numbers: A(n,k) is the number of permutations of {1..n} with k descents)
```


```bash
python -m permustats.main -n 100 --samples 10000 --stat cycle-counts
```

```text
Parameters: N=100, Mode=Sample, Stat=cycle-counts

--- Statistics Report [total_cycles] ---
Sample Size:   10000
Mean:          5.1856
Variance:      3.6034
Distribution:  {1: 102, 2: 547, 3: 1269, 4: 1869, 5: 2125, 6: 1751, 7: 1207, 8: 666, 9: 261, 10: 137, 11: 49, 12: 11, 13: 5, 14: 1}
```

## 📊 Available Metrics

| Flag | Mathematical Property | Ground Truth |
| :--- | :--- | :--- |
| `cycle-counts` | Number of disjoint cycles | Stirling Numbers (1st Kind) |
| `inversions` | Pairs $(i, j)$ where $i < j$ and $\sigma(i) > \sigma(j)$ | Mahonian Numbers |
| `descents` | Count of $i$ where $\sigma(i) > \sigma(i+1)$ | Eulerian Numbers |
| `exceedances` | Count of $i$ where $\sigma(i) > i$ | Eulerian Numbers |
| `fixed-points` | Count of $i$ where $\sigma(i) = i$ | Rencontres Numbers |

## 🏗️ Architecture

PermuStats is built on a **Streaming JIT Engine** that processes permutations as an iterable, maintaining $O(1)$ memory overhead regardless of the sample size. 

- **The Decomposer:** Efficiently extracts multiple statistics in a single pass.
- **The Analyzer:** Uses Welford's algorithm for numerically stable online variance calculation.
- **The Bridge:** Automatically fingerprints distributions and identifies matching OEIS sequences.
