import line_profiler
from permustats.engine import PermuStatsEngine
from permustats.analysis import Analyzer, decompose_cycles
from permustats.generator import PermutationGenerator


def run_profile():
    # 1. Initialize the profiler
    lp = line_profiler.LineProfiler()

    # 2. Manually register the functions we want to 'see' inside
    lp.add_function(decompose_cycles)
    lp.add_function(Analyzer._ensure_processed)
    lp.add_function(PermuStatsEngine.process)
    lp.add_function(PermutationGenerator.exhaustive)

    # 3. Setup the engine
    engine = PermuStatsEngine(plugin=None)
    stream = engine.run_study(n=9)  # 362,880 permutations
    analyzer = Analyzer(stream)

    # 4. Wrap the execution
    print("🚀 Starting Line-Level Scan...")
    lp_wrapper = lp(analyzer.report)
    lp_wrapper("total_cycles", n_size=9)

    # 5. Print the "Smoking Gun" report
    lp.print_stats()


if __name__ == "__main__":
    run_profile()
