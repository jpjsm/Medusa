from functools import partial
from pathlib import Path
import pickle
from time import sleep
from datetime import datetime, timedelta

from geopy.geocoders import Nominatim
from geopy.location import Location

geolocator = Nominatim(user_agent="medusa by juanpablo.jofre@live.com")
geocode = partial(geolocator.geocode, language="es")
reverse = partial(geolocator.reverse, language="es", zoom=14)
last_access = datetime.now() - timedelta(hours=1)

reverse_location_cache_file = Path("/medusa/data/reverse_location_cache.pkl")
if reverse_location_cache_file.exists():
    with open(reverse_location_cache_file, "rb") as infile:
        reverse_location_cache = pickle.load(infile)
else:
    reverse_location_cache = {}

raw_address_keys = set()

points = [
    ("47.543908", "-122.376512"),
    ("47.54390", "-122.376512"),
    ("47.561173", "-122.386039"),
    ("47.519343", "-122.092519"),
    ("47.521741", "-121.986034"),
    ("46.845798", "-121.769623"),
]
for latitude, longitude in points:
    lat_dot = latitude.find(".") + 1
    lon_dot = longitude.find(".") + 1

    for i in range(1, 7):
        coordinates = f"{latitude[:lat_dot+i]:<12}, {longitude[:lon_dot+i]:<12}"
        if coordinates not in reverse_location_cache:
            last_access_elapsed = (datetime.now() - last_access).total_seconds()
            if last_access_elapsed < 1.0:
                sleep(1.0)
            rl: Location = reverse(f"{latitude[:lat_dot+i]},{longitude[:lon_dot+i]}")
            last_access = datetime.now()
            reverse_location_cache[coordinates] = rl.raw["address"]
            with open(reverse_location_cache_file, "wb") as outfile:
                pickle.dump(reverse_location_cache, outfile)

        address_components = reverse_location_cache[coordinates]
        print(
            f"{latitude[:lat_dot+i]:<12}, {longitude[:lon_dot+i]:<12} ==> {address_components}"
        )

        for (
            l
        ) in (
            address_components.keys()
        ):  # ['neighbourhood', 'village', 'county', 'state', 'ISO3166-2-lvl4', 'postcode', 'country', 'country_code']:
            raw_address_keys.add(l)
            print(f"\tlocation type: {l:<16} -> {address_components.get(l)} ")


print(sorted(raw_address_keys))
