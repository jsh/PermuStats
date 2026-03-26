import time
from collections import Counter


def test_aggregation_speed():
    # 1. Test 'get' overhead
    dist_dict = {}
    start = time.perf_counter()
    for _ in range(1_000_000):
        val = 3
        dist_dict[val] = dist_dict.get(val, 0) + 1
    get_time = time.perf_counter() - start

    # 2. Test 'Counter' speed
    dist_counter = Counter()
    start = time.perf_counter()
    for _ in range(1_000_000):
        val = 3
        dist_counter[val] += 1
    counter_time = time.perf_counter() - start

    print(f"⏱️  Dict.get() Time: {get_time:.4f}s")
    print(f"⏱️  Counter Time:    {counter_time:.4f}s")
    print(f"🚀 Speedup: {(get_time / counter_time - 1) * 100:.1f}%")


if __name__ == "__main__":
    test_aggregation_speed()
