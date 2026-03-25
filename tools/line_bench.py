import line_profiler
from permustats.engine import PermuStatsEngine
from permustats.analysis import Analyzer, decompose_cycles
from permustats.generator import PermutationGenerator


def run_profile():
    lp = line_profiler.LineProfiler()

    # Register the methods
    lp.add_function(decompose_cycles)
    lp.add_function(Analyzer.add_result)  # Point to the class method
    lp.add_function(PermuStatsEngine.run_and_analyze)
    lp.add_function(PermutationGenerator.exhaustive)

    # Initialize the specific instance
    analyzer = Analyzer([])
    engine = PermuStatsEngine(plugin=None)

    print("🚀 Starting PUSH-MODEL Line-Level Scan...")

    # Wrap the call to the engine instance
    lp_wrapper = lp(engine.run_and_analyze)
    lp_wrapper(n=9, analyzer=analyzer, target_metric="total_cycles")

    lp.print_stats()


if __name__ == "__main__":
    run_profile()
