from os import walk
from pathlib import Path
import re

from PIL import Image
from PIL.ExifTags import Base, GPS, Interop, IFD, LightSource, TAGS, GPSTAGS
from exiftool import ExifToolHelper

## Base.DateTimeOriginal
SUPPORTED_EXTENSIONS = { ex for ex, _ in Image.registered_extensions().items()}

image_path = '/shared/FotosVarias/Camera Roll/2009-05-23 183206_IMG_7589.JPG'

with Image.open(image_path) as img:
    exif_data = img.getexif()
    print(f"{image_path}")
    for exif_id in exif_data:
        #print(f"-   {exif_id}: {exif_data[exif_id]}")
        print(f"   PIL  :   {exif_id:x} {TAGS[exif_id] if exif_id in TAGS else (GPSTAGS[exif_id] if exif_id in GPSTAGS else 'unknown tag')}")

    print()
    print(f"   ----:   {"\u00b7"*120}")
    print()

    date_metadata = {}
    with ExifToolHelper() as eth:
        for d in eth.get_metadata(image_path):
            for k, v in d.items():
                print(f"   EXIF:   {k} = {v}")

                if re.search('date', k, re.IGNORECASE):
                    date_metadata[k] = v

    print()
    print(f"   {"="*128}")
    print()
    for m, d in date_metadata.items():
        print(f"{m:<40} {d}")
