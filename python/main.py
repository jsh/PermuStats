import argparse
from generator import PermutationGenerator
from engine import PermuStatsEngine
from transformers import CycleTransformer
from plugins import FixedPointPlugin, CycleLengthsPlugin, CycleCountPlugin
from analysis import Analyzer
from validation import validate_results, OEISLookup


def run_analysis():
    parser = argparse.ArgumentParser(description="PermuStats CLI")
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--samples", type=int)
    parser.add_argument(
        "--stat",
        choices=["fixed-points", "cycle-counts", "cycle-lengths"],
        required=True,
    )
    args = parser.parse_args()

    gen = PermutationGenerator()

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

    engine = PermuStatsEngine(plugin, transformer)
    data_stream = (
        gen.sample(args.n, args.samples) if args.samples else gen.exhaustive(args.n)
    )

    results = list(engine.process(data_stream))
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution()

    # Print Output
    mode = "Sample" if args.samples else "Exhaustive"
    print(f"Parameters: N={args.n}, Mode={mode}, Stat={args.stat}")
    print(f"Mean:       {analyzer.mean():.4f}")

    # Only format OEIS string if the results are simple integers (not tuples/lists)
    # This prevents the lookup error for cycle-lengths
    if args.stat in ["fixed-points", "cycle-counts"]:
        oeis_str = OEISLookup.format_sequence(args.n, dist)
        print(f"OEIS Sequence: {oeis_str}")
    else:
        # For cycle-lengths, OEIS search is more complex (Partitions)
        # We can just print the distribution directly for now
        print(f"Distribution:  {dist}")

    if not args.samples and args.stat == "fixed-points":
        print(f"Validation: {validate_results(args.n, dist)}")

    print(f"DEBUG RESULTS: {analyzer.results}")


if __name__ == "__main__":
    run_analysis()
