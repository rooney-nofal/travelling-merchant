"""Création de cartes Folium pour visualiser les villes et la tournée."""
from pathlib import Path

import folium

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
FRANCE_CENTER = (46.6, 2.4)


def plot_cities(cities, filename="cities_map.html"):
    """Enregistre une carte contenant les 20 villes."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    fmap = folium.Map(
        location=FRANCE_CENTER,
        zoom_start=6,
    )

    for name, lat, lon in cities:
        folium.Marker(
            location=(lat, lon),
            tooltip=name,
        ).add_to(fmap)

    output_path = OUTPUT_DIR / filename
    fmap.save(str(output_path))
    return output_path


def plot_route(route, cities, total_distance, filename="christofides_route.html"):
    """Enregistre la tournée fermée sur une carte interactive."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    fmap = folium.Map(
        location=FRANCE_CENTER,
        zoom_start=6,
    )

    for index in route:
        name, lat, lon = cities[index]
        folium.CircleMarker(
            location=(lat, lon),
            radius=5,
            tooltip=name,
            color="red",
            fill=True,
            fill_color="red",
        ).add_to(fmap)

    points = [
        (cities[index][1], cities[index][2])
        for index in route
    ]
    points.append(points[0])

    folium.PolyLine(
        points,
        color="red",
        weight=3,
        tooltip=f"{total_distance:.2f} km",
    ).add_to(fmap)

    output_path = OUTPUT_DIR / filename
    fmap.save(str(output_path))
    return output_path
