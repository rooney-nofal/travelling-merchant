"""Load the 20 French cities (name, latitude, longitude) from the CSV data file."""
import csv
from pathlib import Path 

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "villes_france_lat_long.csv"


def load_cities(csv_path=DATA_FILE):
    """Read the CSV file and return a list of (name, latitude, longitude) tuples."""
    cities = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {key.strip(): value.strip() for key, value in row.items()}
            cities.append((row["Ville"], float(row["Latitude"]), float(row["Longitude"])))
    return cities

if __name__ == "__main__":
    all_cities = load_cities()
    print(f"Loaded {len(all_cities)} cities:")
    for name, lat, lon in all_cities:
        print(f"  {name}: ({lat}, {lon})") 