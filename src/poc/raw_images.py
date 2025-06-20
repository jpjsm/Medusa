"""
Reading different 'RAW' pictures into pillow.

"""

from PIL import Image
from rawpy import imread
foo = {
    '.dng': {'Description'}
}


with imread('../images/RAW_NIKON_D3X.NEF') as raw:
    rgb = raw.postprocess(use_camera_wb=True, output_bps=16)

Image.fromarray(rgb).save('image.jpg')