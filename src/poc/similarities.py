import copy
import hashlib
from pathlib import Path

class dup_files():
    def __init__(self, dir_path:str):
        self.hash_groups = {}
        self.name_groups = {}
        self.basename_groups = {}
        self.extension_groups = {}
        self.paths = set()
        self.files = []
        self._load_dir(dir_path)

    def _load_dir(self, dir_path:str):
        if Path(dir_path).exists():
            self.root = Path(dir_path) if Path(dir_path).is_dir() else Path(dir_path).parent
            _files = [x for x in self.root.rglob("*") if x.is_file()]
            self._load_files(_files)

    def _load_files(self, files):       
        for _file in files:
            _path = str(_file.absolute().resolve(strict=True))
            if _path not in self.paths:
                self.files.append(_file)
                self.paths.add(_path)
                with open(_file, 'rb', buffering=0) as in_file:
                    _hash = hashlib.file_digest(in_file, 'sha256').hexdigest()

                # build duplicate hash groups
                if _hash not in self.hash_groups:
                    self.hash_groups[_hash] = []

                self.hash_groups[_hash].append(_file)

                # build duplicate name groups (includes extension)
                _name = _file.name
                if _name not in self.name_groups:
                    self.name_groups[_name] = []

                self.name_groups[_name].append(_file)

                # build duplicate basename groups (EXcludes extension)
                _basename = _file.stem
                if _basename not in self.basename_groups:
                    self.basename_groups[_basename] = []

                self.basename_groups[_basename].append(_file)

                # build extension groups 
                _extension = _file.suffix
                if _extension not in self.extension_groups:
                    self.extension_groups[_extension] = []

                self.extension_groups[_extension].append(_file)

    def HashGroups(self):
        return copy.deepcopy(self.hash_groups)
    
    def NameGroups(self):
        return copy.deepcopy(self.name_groups)
    
    def BasenameGroups(self):
        return copy.deepcopy(self.basename_groups)
    
    def Paths(self):
        return list(copy.deepcopy(self.paths))
    
    def Files(self):
        return copy.deepcopy(self.files)
    