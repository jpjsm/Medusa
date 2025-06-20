"""Find all images in a starting folder and subfolders.

:source: https://practicaldatascience.co.uk/data-science/how-to-use-image-hashing-to-identify-visually-similar-or-duplicate-images
:author: Matt Clarke (https://practicaldatascience.co.uk/about)
"""

from os import walk
from pathlib import Path
from sys import exit

import dlib
import numpy as np
from PIL import Image
from PIL.ExifTags import Base, GPS, Interop, IFD, LightSource, TAGS, GPSTAGS

IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".gif", ".tiff", ".bmp", ".heif", ".svg"}

photoslocation = "C:/medusa-test-images"
cnn_face_detection_model_v_location = "C:/medusa/models/mmod_human_face_detector.dat"

image_paths = []
for (dir_path, _, file_names) in walk(photoslocation):
    _dir_path = Path(dir_path)
    image_paths.extend(
        [
            str(_dir_path.joinpath(file_name))
            for file_name in file_names
            if Path(file_name).suffix in IMAGE_TYPES
        ]
    )

image_count = len(image_paths)
print(f"{image_count=}")

for image_path in image_paths:
    image_path_parts = Path(image_path).parts[1:]
    print(f"{image_path_parts=}")
    tmp_location = Path("C:/tmp/thumbnails").joinpath(*image_path_parts)
    tmp_location.parent.mkdir(parents=True, exist_ok=True)
    print(f"generating thumbnail for '{image_path}' -> '{tmp_location}'")
    with Image.open(image_path).convert('RGB') as img:
        # np_array = np.array(img)


exit()        

first100_paths = image_paths[:100]

detector = dlib.get_frontal_face_detector()
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model_v_location)

# win = dlib.image_window()

faces = {}
for i in range(20):
    faces[i] = []

for path in first100_paths:
    print(f"Processing file: {path}")
    img = dlib.load_rgb_image(path)
    # win.clear_overlay()
    # win.set_image(img)
    # The 1 in the second argument indicates that we should upsample the image
    # 1 time.  This will make everything bigger and allow us to detect more
    # faces.
    dets = cnn_face_detector(img, 1)
    faces_detected = len(dets)
    print(f"Number of faces detected: {faces_detected,4} -> {path}")
    image_info = {'path': path, 'detections': dets}
    if faces_detected in faces:
        faces[faces_detected].append(image_info)
    else:
        faces[faces_detected] = [image_info]

    """
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
            i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

    rects = dlib.rectangles()
    rects.extend([d.rect for d in dets])

    win.add_overlay(rects)
    dlib.hit_enter_to_continue()
    """

