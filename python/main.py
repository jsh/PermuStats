import argparse
import sys
from generator import PermutationGenerator
from engine import PermuStatsEngine
from transformers import CycleTransformer
from plugins import FixedPointPlugin, CycleLengthPlugin
from analysis import Analyzer
from validation import validate_results, OEISLookup

def run_analysis():
    parser = argparse.ArgumentParser(description="PermuStats CLI")
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--samples", type=int)
    parser.add_argument("--stat", choices=["fixed-points", "cycle-lengths"], required=True)
    args = parser.parse_args()

    gen = PermutationGenerator()
    
    # Selecting the measure and the necessary shaper
    if args.stat == "fixed-points":
        plugin = FixedPointPlugin()
        transformer = None
    else:
        plugin = CycleLengthPlugin()
        transformer = CycleTransformer()

    engine = PermuStatsEngine(plugin, transformer)
    data_stream = gen.sample(args.n, args.samples) if args.samples else gen.exhaustive(args.n)

    results = list(engine.process(data_stream))
    analyzer = Analyzer(results)
    dist = analyzer.frequency_distribution()
    
    # Print Output
    mode = "Sample" if args.samples else "Exhaustive"
    print(f"Parameters: N={args.n}, Mode={mode}, Stat={args.stat}")
    print(f"Mean:       {analyzer.mean():.4f}")
    
    oeis_str = OEISLookup.format_sequence(args.n, dist)
    print(f"OEIS Sequence: {oeis_str}")
    
    if not args.samples and args.stat == "fixed-points":
        print(f"Validation: {validate_results(args.n, dist)}")

if __name__ == "__main__":
    run_analysis()
