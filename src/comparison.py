"""Compare Christofides vs the genetic algorithm: distance, time, robustness, configurations."""
import json
import statistics
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cities import load_cities
from christofides import christofides
from distances import build_distance_matrix
from genetic_algorithm import run_genetic_algorithm
from graph import build_graph

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"

ROBUSTNESS_RUNS = 10

CONFIGURATIONS = {
    "A (rapide)": {"population_size": 100, "generations": 300, "mutation_rate": 0.15},
    "B (équilibrée)": {"population_size": 300, "generations": 800, "mutation_rate": 0.25},
    "C (intensive)": {"population_size": 600, "generations": 1500, "mutation_rate": 0.30},
}
CONFIG_SEEDS = [1, 2, 3]


def time_christofides(graph):
    """Run Christofides once and measure it (deterministic: once is enough)."""
    start = time.perf_counter()
    result = christofides(graph, start=0)
    elapsed = time.perf_counter() - start
    return result, elapsed


def robustness_study(matrix):
    """Run the default GA many times; return per-run results and summary statistics."""
    runs = []
    for seed in range(1, ROBUSTNESS_RUNS + 1):
        result = run_genetic_algorithm(matrix, seed=seed)
        runs.append(result)
        print(f"  run {seed:2d}/{ROBUSTNESS_RUNS}: {result.total_distance:8.2f} km  ({result.elapsed_seconds:.1f} s)")
    distances = [r.total_distance for r in runs]
    times = [r.elapsed_seconds for r in runs]
    summary = {
        "runs": ROBUSTNESS_RUNS,
        "best_km": min(distances),
        "mean_km": statistics.mean(distances),
        "worst_km": max(distances),
        "stdev_km": statistics.stdev(distances),
        "mean_time_s": statistics.mean(times),
    }
    best_run = min(runs, key=lambda r: r.total_distance)
    return best_run, summary


def configuration_study(matrix):
    """Run each named configuration with several seeds; return summary rows."""
    rows = []
    for name, params in CONFIGURATIONS.items():
        distances = []
        times = []
        for seed in CONFIG_SEEDS:
            result = run_genetic_algorithm(matrix, seed=seed, **params)
            distances.append(result.total_distance)
            times.append(result.elapsed_seconds)
        row = {
            "config": name,
            **params,
            "best_km": min(distances),
            "mean_km": statistics.mean(distances),
            "mean_time_s": statistics.mean(times),
        }
        rows.append(row)
        print(f"  {name}: best {row['best_km']:.2f} km, mean {row['mean_km']:.2f} km, ~{row['mean_time_s']:.1f} s/run")
    return rows


def plot_convergence(history, filename="convergence.png"):
    """Save the best-distance-per-generation curve as a PNG for the slides."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5), facecolor="#0b0f1a")
    ax.set_facecolor("#0b0f1a")
    ax.plot(range(len(history)), history, color="#e8192c", linewidth=2.2)
    ax.set_xlabel("Générations", color="white")
    ax.set_ylabel("Distance (km)", color="white")
    ax.set_title("Convergence observée — meilleure distance par génération", color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("#444444")
    ax.grid(color="#333333", linewidth=0.5)
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path


def main():
    all_cities = load_cities()
    matrix = build_distance_matrix(all_cities)
    graph = build_graph(all_cities, matrix)

    print("1/3 — Christofides (référence déterministe)")
    christo_result, christo_time = time_christofides(graph)
    print(f"  distance {christo_result.total_distance:.2f} km in {christo_time*1000:.1f} ms")

    print(f"2/3 — Robustesse GA ({ROBUSTNESS_RUNS} runs, configuration B par défaut)")
    best_run, robustness = robustness_study(matrix)

    print("3/3 — Configurations")
    config_rows = configuration_study(matrix)

    convergence_path = plot_convergence(best_run.history)

    gain_km = christo_result.total_distance - best_run.total_distance
    gain_pct = 100 * gain_km / christo_result.total_distance

    report = {
        "christofides": {
            "distance_km": round(christo_result.total_distance, 2),
            "time_s": round(christo_time, 4),
            "deterministic": True,
        },
        "genetic_best": {
            "distance_km": round(best_run.total_distance, 2),
            "time_s": round(best_run.elapsed_seconds, 2),
            "parameters": best_run.parameters,
        },
        "gain_vs_christofides": {"km": round(gain_km, 2), "percent": round(gain_pct, 2)},
        "robustness": {k: round(v, 2) for k, v in robustness.items()},
        "configurations": config_rows,
    }
    report_path = OUTPUT_DIR / "comparison_results.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print("=" * 60)
    print(f"Christofides : {christo_result.total_distance:.2f} km ({christo_time*1000:.1f} ms, déterministe)")
    print(f"GA (meilleur): {best_run.total_distance:.2f} km ({best_run.elapsed_seconds:.1f} s, seed {best_run.parameters['seed']})")
    print(f"Gain         : {gain_km:.2f} km ({gain_pct:.1f} %)")
    print(f"Robustesse   : best {robustness['best_km']:.0f} / mean {robustness['mean_km']:.0f} / worst {robustness['worst_km']:.0f} / ±{robustness['stdev_km']:.0f} km")
    print(f"Convergence  : {convergence_path}")
    print(f"Rapport JSON : {report_path}")


if __name__ == "__main__":
    main()