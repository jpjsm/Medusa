from pathlib import Path
import pickle
import re


date_tags = set()
date_tags_file = Path("/medusa/data/date_tags.pkl")
if date_tags_file.exists():
    with open(date_tags_file, "rb") as infile:
        date_tags = pickle.load(infile)


coordinates_tags = set()
coordinates_tags_file = Path("/medusa/data/coordinates_tags.pkl")
if coordinates_tags_file.exists():
    with open(coordinates_tags_file, "rb") as infile:
        coordinates_tags = pickle.load(infile)

all_tags = set()
all_tags_file = Path("/medusa/data/all_tags.pkl")
if all_tags_file.exists():
    with open(all_tags_file, "rb") as infile:
        all_tags = pickle.load(infile)


pictures_with_coordinates = set()
pictures_with_coordinates_file = Path("/medusa/data/pictures_with_coordinates.pkl")
if pictures_with_coordinates_file.exists():
    with open(pictures_with_coordinates_file, "rb") as infile:
        pictures_with_coordinates = pickle.load(infile)

print()
print(f"{'='*40} DATE Tags {'='*40}")
print()
for dt in sorted(date_tags):
    print(dt)
print()
print(f"{'='*40} COORDINATES Tags {'='*40}")
print()
for ct in sorted(coordinates_tags):
    print(ct)
print()
print(f"{'='*40} ALL Tags {'='*40}")
print()
print(sorted(all_tags))

print()
print(f"{'='*40} LOCATION Tags {'='*40}")
print()
for tag in all_tags:
    if re.search("(city|country|location|province)", tag, re.IGNORECASE):
        print(tag)

print()
print(f"{'='*40} Pictures with geolocation data {'='*40}")
print()

print(f"Fotos con geolocation tags: {len(pictures_with_coordinates)}")
# for ct in sorted(pictures_with_coordinates):
#     print(ct)


print()
print(f"{'='*40} DONE {'='*40}")
