"""Genetic algorithm for the TSP: evolve city orderings toward the shortest closed tour."""
import random
import time
from dataclasses import dataclass, field

import numpy as np


@dataclass
class GAResult:
    """Bundle of everything one GA run produces (mirrors ChristofidesResult)."""

    route: list[int]
    total_distance: float
    history: list[float] = field(repr=False)
    elapsed_seconds: float
    parameters: dict


def route_distance(route, matrix):
    """Total length in km of the closed tour visiting cities in `route` order."""
    indices = np.asarray(route)
    return float(matrix[indices, np.roll(indices, -1)].sum())


def create_random_route(n, rng):
    """One individual: a random permutation of the n city indices."""
    route = list(range(n))
    rng.shuffle(route)
    return route


def tournament_selection(population, distances, tournament_size, rng):
    """Pick `tournament_size` individuals at random; return (a copy of) the best one."""
    contenders = rng.sample(range(len(population)), tournament_size)
    winner = min(contenders, key=lambda i: distances[i])
    return population[winner][:]


def ordered_crossover(parent_a, parent_b, rng):
    """OX crossover: keep a slice of A in place, fill the rest in B's order (no duplicates)."""
    n = len(parent_a)
    start, end = sorted(rng.sample(range(n), 2))
    child = [None] * n
    child[start:end + 1] = parent_a[start:end + 1]
    kept = set(child[start:end + 1])
    fill = [city for city in parent_b if city not in kept]
    position = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[position]
            position += 1
    return child


def inversion_mutation(route, mutation_rate, rng):
    """With probability `mutation_rate`, reverse a random segment of the route."""
    if rng.random() < mutation_rate:
        start, end = sorted(rng.sample(range(len(route)), 2))
        route[start:end + 1] = reversed(route[start:end + 1])
    return route


def run_genetic_algorithm(
    matrix,
    population_size=300,
    generations=800,
    tournament_size=5,
    mutation_rate=0.25,
    elitism=5,
    seed=None,
):
    """Evolve routes for `generations` iterations; return the best tour found as a GAResult."""
    rng = random.Random(seed)
    n = matrix.shape[0]
    start_time = time.perf_counter()

    population = [create_random_route(n, rng) for _ in range(population_size)]
    distances = [route_distance(route, matrix) for route in population]
    history = []

    for _ in range(generations):
        ranked = sorted(range(population_size), key=lambda i: distances[i])
        history.append(distances[ranked[0]])

        next_population = [population[i][:] for i in ranked[:elitism]]
        while len(next_population) < population_size:
            parent_a = tournament_selection(population, distances, tournament_size, rng)
            parent_b = tournament_selection(population, distances, tournament_size, rng)
            child = ordered_crossover(parent_a, parent_b, rng)
            child = inversion_mutation(child, mutation_rate, rng)
            next_population.append(child)

        population = next_population
        distances = [route_distance(route, matrix) for route in population]

    best_index = min(range(population_size), key=lambda i: distances[i])
    best_distance = distances[best_index]
    history.append(best_distance)
    elapsed = time.perf_counter() - start_time

    return GAResult(
        route=population[best_index],
        total_distance=best_distance,
        history=history,
        elapsed_seconds=elapsed,
        parameters={
            "population_size": population_size,
            "generations": generations,
            "tournament_size": tournament_size,
            "mutation_rate": mutation_rate,
            "elitism": elitism,
            "seed": seed,
        },
    )


if __name__ == "__main__":
    from cities import load_cities
    from distances import build_distance_matrix
    from visualization import plot_route

    all_cities = load_cities()
    matrix = build_distance_matrix(all_cities)

    result = run_genetic_algorithm(matrix, seed=42)

    print("GENETIC ALGORITHM — TSP ON 20 FRENCH CITIES")
    print(f"Best distance : {result.total_distance:.2f} km")
    print(f"Time          : {result.elapsed_seconds:.2f} s")
    print(f"Start of run  : {result.history[0]:.0f} km -> end: {result.history[-1]:.0f} km")
    route_names = " -> ".join(all_cities[i][0] for i in result.route)
    print(f"Route         : {route_names}")
    map_path = plot_route(result.route, all_cities, result.total_distance, filename="genetic_route.html")
    print(f"Map           : {map_path}")