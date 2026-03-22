from __future__ import annotations

import argparse
import sys

from permustats.analysis import Analyzer
from permustats.engine import PermuStatsEngine
from permustats.bridge import OEISLookup
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
        choices=[
            "fixed-points",
            "cycle-counts",
            "cycle-lengths",
            "inversions",
            "descents",
            "exceedances",
            "major-index",
        ],
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

    # 1. Periculum Safety Valve
    if args.size > 11 and args.samples is None:
        print(
            f"Periculum! N={args.size} (> 11) requires --samples to avoid the heat death of your CPU."
        )
        sys.exit(1)

    # 2. Engine Initialization
    # The Engine now handles core metrics (inversions, descents, etc.) via the decomposer
    engine = PermuStatsEngine(
        plugin=None,
        seed=args.seed,
    )

    # 3. Pipeline Execution
    tap = ValidationTap(args.size) if args.validate else None
    results = []

    for result in engine.run_study(n=args.size, num_samples=args.samples):
        if tap:
            tap.observe(result)
        results.append(result)

    # 4. Parameters Reporting (Matches existing test expectations)
    print(f"Parameters: N={args.size}, Mode={engine.mode}, Stat={args.stat}")

    analyzer = Analyzer(results)
    lookup = OEISLookup()

    # 5. Metric Mapping
    metric_map = {
        "cycle-counts": "total_cycles",
        "fixed-points": "fixed_points",
        "cycle-lengths": "lengths_sequence",
    }
    target_metric = metric_map.get(args.stat, args.stat.replace("-", "_"))

    # 6. Unified Statistical Report
    print(f"\n--- Statistics Report [{target_metric}] ---")

    mean = analyzer.mean(target_metric)
    variance = analyzer.variance(target_metric)
    dist = analyzer.frequency_distribution(target_metric)

    print(f"Sample Size:   {analyzer._count}")
    print(f"Mean:          {mean:.4f}")
    print(f"Variance:      {variance:.4f}")

    # Sort distribution for readability and test stability
    sorted_dist = {k: dist[k] for k in sorted(dist.keys())}
    print(f"Distribution:  {sorted_dist}")

    # 7. OEIS Bridge
    dist_vals = [str(dist[k]) for k in sorted(dist.keys())]
    match = lookup.search(",".join(dist_vals))
    if match:
        print(f"OEIS:          {match.id} ({match.name})")

    # 8. Validation Tap Report
    if tap:
        tap.report()


def main() -> None:
    run_analysis()


if __name__ == "__main__":
    main()
