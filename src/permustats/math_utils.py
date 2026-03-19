from __future__ import annotations

import functools
import math


@functools.lru_cache(maxsize=None)
def harmonic_number(n: int) -> float:
    """
    Returns the n-th Harmonic number: H_n = sum_{k=1}^n 1/k.

    Uses math.fsum for improved floating-point precision over long sequences.
    """
    if n <= 0:
        return 0.0
    return math.fsum(1.0 / k for k in range(1, n + 1))


@functools.lru_cache(maxsize=None)
def subfactorial(n: int) -> int:
    """
    Returns !n (the number of derangements of n elements).

    Implemented iteratively to avoid recursion depth limits.
    Formula: !n = round(n! / e)
    """
    if n == 0:
        return 1
    if n == 1:
        return 0

    # Using the iterative recurrence: a[n] = (n-1)(a[n-1] + a[n-2])
    a, b = 1, 0  # !0, !1
    for i in range(2, n + 1):
        a, b = b, (i - 1) * (a + b)
    return b


@functools.lru_cache(maxsize=None)
def stirling_first(n: int, k: int) -> int:
    """
    Returns the unsigned Stirling numbers of the first kind [n, k].

    Recurrence: [n, k] = (n - 1) * [n-1, k] + [n-1, k-1]
    Implemented iteratively to handle large N without stack overflows.
    """
    if k == 0 and n == 0:
        return 1
    if k <= 0 or k > n:
        return 0

    # dp[j] will represent [i, j]
    dp = [0] * (k + 1)
    dp[0] = 0

    # Base case for the iteration: [1, 1] = 1
    # We start from i=1 and build up to n.
    current_k_max = 1
    dp[1] = 1

    for i in range(2, n + 1):
        # We must iterate backwards through the row to update in-place,
        # similar to the Knapsack problem, to use only O(k) space.
        current_k_max = min(i, k)
        for j in range(current_k_max, 0, -1):
            # [i, j] = (i - 1) * [i-1, j] + [i-1, j-1]
            dp[j] = (i - 1) * dp[j] + dp[j - 1]

        # [i, 0] is always 0 for i > 0
        dp[0] = 0

    return dp[k]


@functools.lru_cache(maxsize=None)
def mahonian(n: int, k: int) -> int:
    """
    Calculates the Mahonian number T(n, k).

    T(n, k) is the number of permutations of n elements with exactly k inversions.
    Base Cases:
        T(n, 0) = 1
        T(n, k) = 0 if k < 0 or k > n(n-1)/2
    Recurrence:
        T(n, k) = sum_{i=0}^{min(k, n-1)} T(n-1, k-i)
    """
    # 1. Base Case: Zero inversions is always the identity permutation (1 way)
    if k == 0:
        return 1

    # 2. Boundary Check: k cannot be negative or exceed the maximum inversions (n choose 2)
    if k < 0 or k > (n * (n - 1) // 2):
        return 0

    # 3. Base Case: n=1 can only have 0 inversions (handled above)
    if n == 1:
        return 0

    # 4. Recursive Step with Symmetry Optimization
    # T(n, k) = T(n, max_inv - k)
    max_inv = n * (n - 1) // 2
    if k > max_inv // 2:
        return mahonian(n, max_inv - k)

    # Standard recurrence: sum of previous row values
    total = 0
    for i in range(min(k, n - 1) + 1):
        total += mahonian(n - 1, k - i)

    return total


@functools.lru_cache(maxsize=None)
def eulerian(n: int, k: int) -> int:
    """
    Computes Eulerian numbers A(n, k) using the recurrence:
    A(n, k) = (k + 1)A(n-1, k) + (n - k)A(n-1, k-1)
    """
    if k < 0 or k >= n:
        return 0
    if n == 0:
        return 1 if k == 0 else 0
    if k == 0:
        return 1

    return (k + 1) * eulerian(n - 1, k) + (n - k) * eulerian(n - 1, k - 1)
