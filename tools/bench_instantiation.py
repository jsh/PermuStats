import timeit
from permustats.analysis import decompose_cycles


# The Baseline: Raw decomposition logic without AnalysisResult instantiation
def raw_decompose(permutation, base=1):
    n = len(permutation)
    visited = [False] * n
    count = 0
    for i in range(n):
        if not visited[i]:
            count += 1
            curr_idx = i
            while not visited[curr_idx]:
                visited[curr_idx] = True
                curr_idx = permutation[curr_idx] - base
    return count


# The Production: Current AnalysisResult flow
def production_decompose(permutation):
    return decompose_cycles(permutation)


def run_bench():
    p = list(range(1, 10))  # N=9
    # Run 100k times
    raw_time = timeit.timeit(lambda: raw_decompose(p), number=100000)
    prod_time = timeit.timeit(lambda: production_decompose(p), number=100000)

    tax = (prod_time - raw_time) / prod_time * 100
    print(f"Raw Math: {raw_time:.4f}s")
    print(f"Production: {prod_time:.4f}s")
    print(f"Constructor Tax: {tax:.2f}%")


if __name__ == "__main__":
    run_bench()
