from pathlib import Path

from medusa.picture import SUPPORTED_EXTENSIONS


def FolderTraverse(
    path: str, extensions: set[str] = SUPPORTED_EXTENSIONS
) -> list[Path]:
    files = []
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(path)
    root = root if root.is_dir() else root.parent
    for fileinfo in root.rglob("*"):
        if fileinfo.is_dir():
            continue

        suffix = fileinfo.suffix.upper()
        if suffix not in extensions:
            continue

        files.append(fileinfo)

    return files


if __name__ == "__main__":
    original_path = "/shared/FotosVarias"
    picture_files = FolderTraverse(original_path, SUPPORTED_EXTENSIONS)
    for x in picture_files:
        print(x)

    print(len(picture_files))
