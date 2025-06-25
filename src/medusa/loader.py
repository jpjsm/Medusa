from pydantic import (field_validator, Field, PrivateAttr)
from pydantic import (BaseModel, AfterValidator)
from typing import Annotated, Any, Tuple

import copy

from medusa.picture import SUPPORTED_EXTENSIONS, DEFINED_PERCEPTUAL_HASHES, Picture
from medusa.utilities import FolderTraverse, Hexadecimal2BitList

class Loader(BaseModel):
    Locations: list[str]
    Ids: dict[str, list[Picture]]
    ColorHashes: dict[str, list[str]]
    PerceptionHashes: dict[str, list[Tuple[str,str]]]
    Names: dict[str, list[str]]
    Basenames: dict[str, list[str]]
    Extensions: dict[str, list[str]]


    def __init__(self, paths: list[str]):
        location_files = {}
        for path in paths:
            try:
                location_files[path] = FolderTraverse(path, SUPPORTED_EXTENSIONS)
            except FileNotFoundError as fnfx:
                print(f"WARNING: {fnfx}")
                continue

        if not location_files:
            raise FileNotFoundError(paths)
        
        ids = {}
        color_hashes = {}
        perception_hashes = {}
        names = {}
        basenames = {}
        extensions = {}

        _counter = 0
        for l in location_files:
            for __counter, p in enumerate(location_files[l]):
                pic = Picture(path=p)
                id = pic.Id
                print(f"{__counter+_counter:10,}   -> loaded picture '{id}'")
                if id not in ids:
                    ids[id] = []
                
                ids[id].append(pic)

                color_hash = pic.Hashes['COLOR']
                if color_hash not in color_hashes:
                    color_hashes[color_hash] = set()

                color_hashes[color_hash].add(id)

                for hash_name in DEFINED_PERCEPTUAL_HASHES:
                    image_hash = pic.Hashes[hash_name]
                    if image_hash not in perception_hashes:
                        perception_hashes[image_hash] = set()

                    perception_hashes[image_hash].add((id, hash_name))

                if pic.FileName not in names:
                    names[pic.FileName] = set()

                names[pic.FileName].add(id)

                if pic.Basename not in basenames:
                    basenames[pic.Basename] = set()

                basenames[pic.Basename].add(id)

                if pic.Extension not in extensions:
                    extensions[pic.Extension] = set()

                extensions[pic.Extension].add(id)
            _counter += __counter

        super().__init__(
            Locations=[k for k in location_files],
            Ids=ids,
            ColorHashes=color_hashes,
            PerceptionHashes=perception_hashes,
            Names=names,
            Basenames=basenames,
            Extensions=extensions
        )

    @property
    def Duplicate(self) -> dict[str, list[Picture]]:
        dups = {}
        for i, a in self.Ids.items():
            if len(a) > 1:
                dups[i] = a
        
        return dups
    
    @property
    def Identical(self) -> dict[str, list[str]]:
        identical = {}
        for h, a in self.PerceptionHashes.items():
            if len(a) > 1:
                identical[h] = [i for i, _ in a]

        return identical

    @property
    def ColorSimilar(self) -> dict[str, list[str]]:
        similar = {}
        for h, a in self.ColorHashes.items():
            if len(a) > 1:
                similar[h] = a
                
        return similar

    @property
    def PictureCount(self) -> int:
        return sum([len(v) for v in self.Ids.values()])
    
if __name__ == "__main__":
    import pickle
    pictures_path = '/shared/FotosVarias'
    loaded_pictures = Loader([pictures_path])
    with open('./output/fotosvarias.pkl', 'wb') as outfile:
        pickle.dump(loaded_pictures, outfile)
    
    print("Total pictures      : ", loaded_pictures.PictureCount)
    print("Duplicate groups    : ", len(loaded_pictures.Duplicate))
    print("Identical groups    : ", len(loaded_pictures.Identical))
    print("Color similar groups: ", len(loaded_pictures.ColorSimilar))
