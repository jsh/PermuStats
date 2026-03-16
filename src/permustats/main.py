from __future__ import annotations

import argparse
import sys

from permustats.analysis import Analyzer
from permustats.engine import PermuStatsEngine
from permustats.plugins import CycleCountPlugin, CycleLengthsPlugin, FixedPointPlugin
from permustats.transformers import CycleTransformer
from permustats.validation import ValidationTap


def run_analysis(args_list: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="PermuStats CLI: Statistical Analysis of Permutations"
    )

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
        default=None,
        help="Number of permutations to sample if N! > 1000. (default: 0)",
    )
    parser.add_argument(
        "-t",
        "--stat",
        type=str,
        default="fixed-points",
        choices=["fixed-points", "cycle-counts", "cycle-lengths"],
        help="The statistical plugin to use (default: 'fixed-points').",
    )
    parser.add_argument(
        "-e",
        "--seed",
        type=int,
        default=None,
        help="Integer seed for reproducibility.",
    )
    parser.add_argument(
        "-v",
        "--validate",
        action="store_true",
        help="Run validation tap against theoretical truths.",
    )

    args = parser.parse_args(args_list or sys.argv[1:])

    # 1. Unified Plugin/Transformer Resolution
    if args.stat == "cycle-counts":
        plugin, transformer = CycleCountPlugin(), CycleTransformer()
    elif args.stat == "cycle-lengths":
        plugin, transformer = CycleLengthsPlugin(), CycleTransformer()
    else:  # Default: fixed-points
        plugin, transformer = FixedPointPlugin(), None

    engine = PermuStatsEngine(
        plugin=plugin,
        transformer=transformer,
        seed=args.seed,
    )

    # 2. Pipeline Execution
    tap = ValidationTap(args.size) if args.validate else None
    results = []

    for result in engine.run_study(n=args.size, num_samples=args.samples):
        if tap:
            tap.observe(result)
        results.append(result)

    # 3. Reporting
    print(f"Parameters: N={args.size}, Mode={engine.mode}, Stat={args.stat}")

    analyzer = Analyzer(results)

    # Map CLI strings (hyphenated) to AnalysisResult attributes (underscored)
    metric_map = {
        "cycle-counts": "total_cycles",
        "fixed-points": "fixed_points",
        "cycle-lengths": "lengths_sequence",
    }
    target_metric = metric_map.get(args.stat, "total_cycles")

    analyzer.report(target_metric, args.size)

    if tap:
        tap.report()


def main() -> None:
    run_analysis()


if __name__ == "__main__":
    main()
