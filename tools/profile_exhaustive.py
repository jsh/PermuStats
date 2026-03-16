import pyinstrument
from permustats.main import run_analysis


def main():
    # Setup N=9 Exhaustive (362,880 permutations)
    # We use -n 9 and no -s to trigger exhaustive mode
    test_args = ["-n", "9", "--stat", "cycle-counts"]
    # test_args = ["-n", "9", "--samples", "362880", "--stat", "cycle-counts"]

    profiler = pyinstrument.Profiler()

    print("🚀 Starting Profiling Expedition (N=9 Exhaustive)...")

    profiler.start()
    try:
        run_analysis(test_args)
    finally:
        profiler.stop()

    # Output the results to the console
    print("\n--- 📊 Profiling Results ---")
    profiler.print()


if __name__ == "__main__":
    main()
