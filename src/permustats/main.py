import argparse
from permustats.engine import PermuStatsEngine
from permustats.transformers import CycleTransformer
from permustats.plugins import FixedPointPlugin, CycleLengthsPlugin, CycleCountPlugin
from permustats.analysis import Analyzer, decompose_cycles
from permustats.validation import validate_results, OEISLookup


def run_analysis(args_list: list[str] | None = None):
    parser = argparse.ArgumentParser(description="PermuStats CLI")

    parser.add_argument(
        "-n",
        "--size",
        type=int,
        required=True,
        help="Sample size (number of elements) for the permutations.",
    )
    parser.add_argument(
        "-s",
        "--samples",
        type=int,
        default=1000,
        help="Number of permutations to sample if N! > 1000 (default: 1000).",
    )
    parser.add_argument(
        "-t",
        "--stat",
        type=str,
        default="fixed_points",
        help="The statistical plugin to use (default: 'fixed_points').",
    )
    parser.add_argument(
        "-e",
        "--seed",
        type=int,
        default=None,
        help="Integer seed for reproducibility (default: None).",
    )

    args = parser.parse_args(args_list)

    # Selecting the measure and the necessary shaper
    if args.stat == "fixed-points":
        plugin = FixedPointPlugin()
        transformer = None
    else:
        plugin = CycleLengthsPlugin()
        transformer = CycleTransformer()

    if args.stat == "fixed-points":
        plugin = FixedPointPlugin()
        transformer = None
    elif args.stat == "cycle-counts":  # <--- Check this string!
        # Needs to see [[0, 1], [2]] to count "2"
        plugin = CycleCountPlugin()
        transformer = CycleTransformer()
    elif args.stat == "cycle-lengths":
        # Needs to see [[0, 1], [2]] to return [2, 1]
        plugin = CycleLengthsPlugin()
        transformer = CycleTransformer()

    engine = PermuStatsEngine(
        plugin=plugin,  # Your existing plugin resolution logic
        transformer=transformer,  # Your existing transformer
        seed=args.seed,  # seed for random
    )

    raw_permutations = engine.run_study(n=args.size, num_samples=args.samples)
    results = [decompose_cycles(p) for p in raw_permutations]
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution()

    # Print Output
    mode = "Sample" if args.samples else "Exhaustive"
    print(f"Parameters: N={args.size}, Mode={mode}, Stat={args.stat}")
    print(f"Mean:       {analyzer.mean():.4f}")

    # Only format OEIS string if the results are simple integers (not tuples/lists)
    # This prevents the lookup error for cycle-counts
    if args.stat in ["fixed-points", "cycle-counts"]:
        oeis_str = OEISLookup.format_sequence(args.size, dist)
        print(f"OEIS Sequence: {oeis_str}")
    else:
        # For cycle-lengths, OEIS search is more complex (Partitions)
        # We can just print the distribution directly for now
        print(f"Distribution:  {dist}")

    if not args.samples and args.stat == "fixed-points":
        print(f"Validation: {validate_results(args.size, dist)}")

    print(f"DEBUG RESULTS: {analyzer.results}")


def main():
    run_analysis()  # Calls it with None, picking up sys.argv


if __name__ == "__main__":
    main()  # Calls it with None, picking up sys.argv
