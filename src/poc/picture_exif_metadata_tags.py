from exiftool import ExifToolHelper
from pathlib import Path
import pickle
import re
from folder_trasverse import FolderTraverse


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


picture_paths = FolderTraverse("/shared/FotosVarias/")
print(f"Total pictures: {len(picture_paths):,}")

i = 0
with ExifToolHelper() as eth:
    for picture_path in picture_paths:
        picture_path_str = str(picture_path)
        i += 1
        print(f"\r{i: >12,} {picture_path_str: <200}", end="", sep="")
        metadata_list = eth.get_metadata(picture_path)
        for d in metadata_list:
            for tag, value in d.items():
                if tag not in all_tags:
                    all_tags.add(tag)
                    with open(all_tags_file, "wb") as outfile:
                        pickle.dump(all_tags, outfile)

                if re.search("(date|time|zone|offset)", tag, re.IGNORECASE):
                    if tag not in date_tags:
                        date_tags.add(tag)
                        with open(date_tags_file, "wb") as outfile:
                            pickle.dump(date_tags, outfile)

                if re.search("(latitude|longitude|coor|gps)", tag, re.IGNORECASE):
                    if picture_path_str not in pictures_with_coordinates:
                        pictures_with_coordinates.add(picture_path_str)
                        with open(pictures_with_coordinates_file, "wb") as outfile:
                            pickle.dump(pictures_with_coordinates, outfile)

                    if tag not in coordinates_tags:
                        coordinates_tags.add(tag)
                        with open(coordinates_tags_file, "wb") as outfile:
                            pickle.dump(coordinates_tags, outfile)

print()
print(f"{'='*40} DONE {'='*40}")
