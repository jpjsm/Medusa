from typing import Tuple
from typing import Annotated, Any, Tuple
from numpy import ndarray
import numpy as np
from pydantic import BaseModel, Field
from pathlib import Path

from medusa.picture import SUPPORTED_EXTENSIONS

class ExtensionSummary(BaseModel):
    Extension: str
    Count: int
    SupportedInPicture: bool

def SummarizeExtensions(path:str) -> list[ExtensionSummary]:
    extensions_count = {}
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(path)
    root = root if root.is_dir() else root.parent
    for fileinfo in root.rglob('*'):
        if fileinfo.is_dir():
            continue

        suffix = fileinfo.suffix.upper()
        if suffix not in extensions_count:
            extensions_count[suffix] = 0
        extensions_count[suffix] += 1

    results = []
    for k,v in extensions_count.items():
        results.append(ExtensionSummary(Extension=k, Count=v, SupportedInPicture= k in SUPPORTED_EXTENSIONS))
    return results

def Hexadecimal2BitList(hexnumber: Annotated[str, Field(min_length=1, pattern='[0-9a-f]+')]) -> ndarray[int]:
    intnumber = int(f"0x{hexnumber}",16)
    binary_string = np.binary_repr(intnumber, len(hexnumber)*4)
    bits_list = [int(bit) for bit in binary_string]
    return bits_list


def FolderTraverse(path:str, extensions: set[str]) -> list[Path]:
    files = []
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(path)
    root = root if root.is_dir() else root.parent
    for fileinfo in root.rglob('*'):
        if fileinfo.is_dir():
            continue

        suffix = fileinfo.suffix.upper()
        if suffix not in extensions:
            continue

        files.append(fileinfo)

    return files


if __name__ == "__main__":
    original_path = '/shared/FotosVarias'
    extensions_summary = SummarizeExtensions(original_path)
    for x in sorted(extensions_summary, key=lambda i:(i.SupportedInPicture, i.Extension)):
        print(x.Extension, x.Count, x.SupportedInPicture)
            
    picture_files = FolderTraverse(original_path, SUPPORTED_EXTENSIONS)
    #for x in picture_files:
    #    print(x)

    print(len(picture_files))   
    color_hash = '1fff1ffffffffc000000000001e03ff803ff0fff8000000000000000000001f'  
    color_hash_bitarray = Hexadecimal2BitList(color_hash)
    print(len(color_hash),len(color_hash_bitarray), color_hash_bitarray)

    pHash_original = 'fe087c03ee33cb3f141fd23c29a435d01ae9c955359b18b1dcf0a62d86c2cfc3'
    pHash_original_bitarray =  Hexadecimal2BitList(pHash_original)
    print(len(pHash_original), len(pHash_original_bitarray), pHash_original_bitarray)