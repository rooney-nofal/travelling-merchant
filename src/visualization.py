"""Draw cities and routes on an interactive map of France (folium HTML files)."""
from pathlib import Path

import folium

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
FRANCE_CENTER = (46.6, 2.4)


def plot_cities(cities, filename="cities_map.html"):
    """Save a map with one marker per city; return the file path."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    fmap = folium.Map(location=FRANCE_CENTER, zoom_start=6)
    for name, lat, lon in cities:
        folium.Marker(location=(lat, lon), tooltip=name).add_to(fmap)
    output_path = OUTPUT_DIR / filename
    fmap.save(str(output_path))
    return output_path


def plot_route(route, cities, total_distance, filename="route_map.html"):
    """Save a map showing the route as a closed line over the city markers; return the file path."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    fmap = folium.Map(location=FRANCE_CENTER, zoom_start=6)
    for name, lat, lon in cities:
        folium.Marker(location=(lat, lon), tooltip=name).add_to(fmap)
    points = [(cities[i][1], cities[i][2]) for i in route]
    points.append(points[0])
    folium.PolyLine(points, color="red", weight=3, tooltip=f"{total_distance:.1f} km").add_to(fmap)
    output_path = OUTPUT_DIR / filename
    fmap.save(str(output_path))
    return output_path


if __name__ == "__main__":
    from cities import load_cities
    from distances import build_distance_matrix

    all_cities = load_cities()
    matrix = build_distance_matrix(all_cities)
    naive_route = list(range(len(all_cities)))
    naive_distance = sum(matrix[naive_route[k]][naive_route[k + 1]] for k in range(len(naive_route) - 1))
    naive_distance += matrix[naive_route[-1]][naive_route[0]]
    print(f"Cities map: {plot_cities(all_cities)}")
    print(f"Naive route ({naive_distance:.1f} km): {plot_route(naive_route, all_cities, naive_distance)}")