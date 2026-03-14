import argparse
from permustats.engine import PermuStatsEngine
from permustats.transformers import CycleTransformer
from permustats.plugins import FixedPointPlugin, CycleLengthsPlugin, CycleCountPlugin
from permustats.analysis import Analyzer
from permustats.validation import ValidationTap


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
    parser.add_argument(
        "-v",
        "--validate",
        action="store_true",
        default=False,  # Explicit default matches the others
        help="Run validation tap against theoretical truths (default: False).",
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

    # 1. Instantiate Tap if requested
    tap = ValidationTap(args.size) if args.validate else None

    engine = PermuStatsEngine(
        plugin=plugin,  # Your existing plugin resolution logic
        transformer=transformer,  # Your existing transformer
        seed=args.seed,  # seed for random
    )

    tap = ValidationTap(args.size) if args.validate else None
    results = []

    # One loop to rule them all
    for result in engine.run_study(n=args.size, num_samples=args.samples):
        if tap:
            tap.observe(result)
        results.append(result)

    # Let the Engine report its own metadata
    print(f"Parameters: N={args.size}, Mode={engine.mode}, Stat={args.stat}")

    analyzer = Analyzer(results)

    # Map CLI flag to internal attribute
    metric_map = {
        "cycle-counts": "total_cycles",
        "fixed-points": "fixed_points",
        "cycle-lengths": "lengths_sequence",
    }
    target_metric = metric_map.get(args.stat, "total_cycles")

    # The Analyzer handles the heavy lifting of formatting
    analyzer.report(target_metric, args.size)

    if tap:
        tap.report()


def main():
    run_analysis()  # Calls it with None, picking up sys.argv


if __name__ == "__main__":
    main()  # Calls it with None, picking up sys.argv
