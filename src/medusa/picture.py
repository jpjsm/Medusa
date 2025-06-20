from pydantic import (field_validator, Field, PrivateAttr)
from pydantic import (BaseModel, AfterValidator)
from typing import Annotated, Any, Tuple

import io
from pathlib import Path

import hashlib
import imagehash
from PIL import Image
from exiftool import ExifToolHelper
from rawpy import imread

from medusa.CommonRawFormats import COMMON_RAW_FORMATS


PILLOW_SUPPORTED_EXTENSIONS = { ex.upper() for ex, _ in Image.registered_extensions().items()}
RAW_FORMATS_REQUIRING_TRANSFORMATION = {r.Extension.upper() for r in COMMON_RAW_FORMATS} - PILLOW_SUPPORTED_EXTENSIONS
SUPPORTED_EXTENSIONS = PILLOW_SUPPORTED_EXTENSIONS | RAW_FORMATS_REQUIRING_TRANSFORMATION

DEFINED_TRANSPOSITIONS = {
    'FLIP_LR': Image.Transpose.FLIP_LEFT_RIGHT,
    'FLIP_TB': Image.Transpose.FLIP_TOP_BOTTOM,
    'R90': Image.Transpose.ROTATE_90,
    'R180': Image.Transpose.ROTATE_180,
    'R270': Image.Transpose.ROTATE_270,
    'TRANSPOSE': Image.Transpose.TRANSPOSE,
    'TRANSVERSE': Image.Transpose.TRANSVERSE,
}

DEFINED_COLOR_HASHES = {'COLOR'}
DEFINED_PERCEPTUAL_HASHES = {
    'pHASH_ORIGINAL',
    'pHASH_FLIP_LR',
    'pHASH_FLIP_TB',
    'pHASH_R90',
    'pHASH_R180',
    'pHASH_R270',
    'pHASH_TRANSPOSE',
    'pHASH_TRANSVERSE',
}

class Picture(BaseModel):
    _thumbnail: Image = PrivateAttr()
    Id: str = Field(min_length=64, max_length=64, pattern='[0-9a-f]+')
    OriginalPath: Annotated[str, AfterValidator(lambda x: x.strip())] = Field(..., min_length=1)
    OriginalPathHash: str = Field(min_length=64, max_length=64, pattern='[0-9a-f]+')
    FileName: str
    Basename: str
    Extension: str
    Hashes: dict[str,str]
    Metadata: dict[str, dict[str, Any]]
    Date_Taken: str | None
    Coordinates: Tuple[float, float] | None

    @field_validator('OriginalPath')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('OriginalPath cannot be just spaces or other non-visible characters, nor can it be empty string.')
        return v

    def _get_hashes(original: Image.Image) -> dict[str, str]:
        hashes = {}
        hashes['COLOR'] = f"{str(imagehash.colorhash(original, 18))}"
        hashes['pHASH_ORIGINAL'] = f"{str(imagehash.phash(original,16))}"
        for k,v in DEFINED_TRANSPOSITIONS.items():
            _transposed = original.transpose(v)
            _phash = imagehash.phash(_transposed,16)
            _hex_hash = f"{str(_phash)}"
            hashes[F"pHASH_{k}"] = _hex_hash

        return hashes
    
    def _get_metadata(original_path: str) -> dict[str, dict[str, Any]]:
        metadata_dict = {}
        with ExifToolHelper() as eth:
            m =  eth.get_metadata(original_path)[0]
            for k, v in m.items():
                kdata = k.split(':')
                group = kdata[0]
                tag = kdata[1] if len(kdata) > 1 else group
                if group not in metadata_dict:
                    metadata_dict[group] = {}

                metadata_dict[group][tag] = v

        return metadata_dict

    def _get_thumbnail(original: Image.Image, size: Tuple[int, int]=(256,256)) -> Image.Image:
        tmp_image = original.copy()
        tmp_image.thumbnail(size)
        return tmp_image
    
    def _get_image_jpeg_byte_array(image: Image.Image) -> bytes:
        img_mem_stream = io.BytesIO()
        image.save(img_mem_stream, format='JPEG')
        img_byte_arr = img_mem_stream.getvalue()
        return img_byte_arr
    
    def _read_raw(path: str) -> Image:
        with imread(path) as raw:
            rgb = raw.postprocess(use_camera_wb=True, output_bps=8)

        img_mem_stream = io.BytesIO()
        Image.fromarray(rgb).save(img_mem_stream, "TIFF")
        return Image.open(img_mem_stream)

    @property
    def Original(self) -> Image:
        _file = Path(self.OriginalPath)
        if not _file.exists():
            raise Exception(f"Not Found: {self.OriginalPath}")

        if self.Extension in RAW_FORMATS_REQUIRING_TRANSFORMATION:
            original = Picture._read_raw(original_path)
        else:
            original = Image.open(original_path)
        
        return original
    
    @property
    def ThumbnailJpeg(self) -> Image:
        return Picture._get_image_jpeg_byte_array(self._thumbnail)
    
    def __init__(self, path: str):
        _file = Path(path)
        if not _file.exists():
            raise Exception(f"Not Found: {path}")
        
        if not _file.is_file():
            raise Exception(f"Not a file: {path}")
        
        extension = _file.suffix.upper()
        if extension not in SUPPORTED_EXTENSIONS:
            raise Exception(f"Not supported file type: {extension}")
        
        file_name = _file.name
        basename =  _file.stem

        original_path = str(_file.absolute().resolve(strict=True))
        original_path_hash = hashlib.sha256(original_path.encode('utf-8')).hexdigest()
        with open(original_path, 'rb', buffering=0) as infile:
            id = hashlib.file_digest(infile, 'sha256').hexdigest()

        if extension in RAW_FORMATS_REQUIRING_TRANSFORMATION:
            original = Picture._read_raw(original_path)
        else:
            original = Image.open(original_path)

        thumbnail = Picture._get_thumbnail(original)
        hashes = Picture._get_hashes(original=original)
        metadata = Picture._get_metadata(original_path)
        coordinates = None
        if('EXIF'in metadata
           and 'GPSLatitudeRef' in  metadata['EXIF']
           and metadata['EXIF']['GPSLatitudeRef']):
            latitude = float(
                metadata['EXIF']['GPSLatitude'] 
                if metadata['EXIF']['GPSLatitudeRef'].upper() == 'N'
                else f"-{metadata['EXIF']['GPSLatitude']}")
            longitude = float(
                metadata['EXIF']['GPSLongitude'] 
                if metadata['EXIF']['GPSLongitudeRef'].upper() == 'E'
                else f"-{metadata['EXIF']['GPSLongitude']}")
            coordinates = (latitude, longitude)
        super().__init__(
            Id=id,
            OriginalPath=original_path,
            OriginalPathHash=original_path_hash,
            FileName=file_name,
            Basename=basename,
            Extension=extension,
            Hashes=hashes,
            Metadata=metadata,
            Date_Taken=metadata['EXIF']['DateTimeOriginal'] if 'EXIF' in metadata and 'DateTimeOriginal' in metadata['EXIF'] else None,
            Coordinates=coordinates
            #JPG_thumbnail_byte_arr=thumbnail_byte_arr
        )
        self._thumbnail = thumbnail
        original.close()
        original = None


if __name__ == "__main__":
    #pic = Picture()
    original_path = '/shared/FotosVarias/medusa-test-images/2014/12/20141226_024252260_iOS.jpg'
    pic = Picture(path=original_path)
    pic.Original.show()
    pic.ThumbnailJpeg.show()
    print(pic)
    print(pic.Hashes)
    