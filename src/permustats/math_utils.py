import sys
import functools

# Increase recursion depth for deep Stirling/Subfactorial trees
sys.setrecursionlimit(2000)


@functools.lru_cache(maxsize=None)
def harmonic_number(n: int) -> float:
    """Returns the n-th Harmonic number: H_n = sum_{k=1}^n 1/k."""
    if n == 0:
        return 0.0
    return sum(1.0 / k for k in range(1, n + 1))


@functools.lru_cache(maxsize=None)
def subfactorial(n: int) -> int:
    """
    Returns !n (the number of derangements of n elements).
    Recurrence: !n = (n - 1) * (!(n - 1) + !(n - 2))
    """
    if n == 0:
        return 1
    if n == 1:
        return 0
    return (n - 1) * (subfactorial(n - 1) + subfactorial(n - 2))


@functools.lru_cache(maxsize=None)
def stirling_first(n: int, k: int) -> int:
    """
    Returns the unsigned Stirling numbers of the first kind [n, k].
    Recurrence: [n, k] = (n - 1) * [n-1, k] + [n-1, k-1]
    """
    if k == 0 and n == 0:
        return 1
    if k <= 0 or k > n:
        return 0
    if n == k:
        return 1
    return (n - 1) * stirling_first(n - 1, k) + stirling_first(n - 1, k - 1)
