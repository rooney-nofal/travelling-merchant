"""Haversine (great-circle) distances between cities and the full distance matrix."""
import math

import numpy as np

EARTH_RADIUS_KM = 6371.0


def haversine(lat1, lon1, lat2, lon2):
    """Return the great-circle distance in km between two points given in decimal degrees."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c   

def build_distance_matrix(cities):
    """Return an n x n numpy array of Haversine distances between all city pairs."""
    n = len(cities)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            distance = haversine(cities[i][1], cities[i][2], cities[j][1], cities[j][2])
            matrix[i][j] = distance
            matrix[j][i] = distance
    return matrix

if __name__ == "__main__":
    from cities import load_cities

    all_cities = load_cities()
    m = build_distance_matrix(all_cities)
    print(f"Matrix shape: {m.shape}")
    print(f"Paris -> Marseille: {m[0][1]:.1f} km")
    print(f"Diagonal all zero: {bool((m.diagonal() == 0).all())}")
    print(f"Symmetric: {bool((m == m.T).all())}")

    