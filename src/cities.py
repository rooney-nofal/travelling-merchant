"""Chargement des 20 villes françaises depuis le fichier CSV."""
import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "villes_france_lat_long.csv"


def load_cities(csv_path=DATA_FILE):
    """Retourne une liste de tuples (nom, latitude, longitude)."""
    cities = []

    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row = {key.strip(): value.strip() for key, value in row.items()}
            cities.append(
                (
                    row["Ville"],
                    float(row["Latitude"]),
                    float(row["Longitude"]),
                )
            )

    return cities


if __name__ == "__main__":
    all_cities = load_cities()
    print(f"{len(all_cities)} villes chargées :")
    for name, lat, lon in all_cities:
        print(f"- {name}: ({lat}, {lon})")
