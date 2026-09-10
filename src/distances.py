"""Calcul des distances Haversine et de la matrice des distances."""

import math
import numpy as np


# Rayon moyen de la Terre en kilomètres.
EARTH_RADIUS_KM = 6371.0


def haversine(lat1, lon1, lat2, lon2):
    """
    Calcule la distance entre deux villes
    à partir de leurs coordonnées GPS.
    """

    # Les fonctions trigonométriques utilisent des radians,
    # donc on convertit les degrés en radians.
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    # Différence de latitude.
    delta_phi = math.radians(
        lat2 - lat1
    )

    # Différence de longitude.
    delta_lambda = math.radians(
        lon2 - lon1
    )

    # Formule de Haversine.
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(delta_lambda / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    # Distance finale en kilomètres.
    return EARTH_RADIUS_KM * c


def build_distance_matrix(cities):
    """
    Construit une matrice contenant
    la distance entre chaque paire de villes.
    """

    # Nombre de villes.
    n = len(cities)

    # Matrice n x n initialisée avec des zéros.
    matrix = np.zeros(
        (n, n)
    )

    # On parcourt toutes les villes.
    for i in range(n):

        # On ne calcule que la moitié de la matrice,
        # car distance Paris-Lyon = distance Lyon-Paris.
        for j in range(i + 1, n):

            # Calcul de la distance entre la ville i et la ville j.
            distance = haversine(
                cities[i][1],
                cities[i][2],
                cities[j][1],
                cities[j][2],
            )

            # Distance i -> j.
            matrix[i][j] = distance

            # Même distance dans l'autre sens.
            matrix[j][i] = distance

    return matrix
