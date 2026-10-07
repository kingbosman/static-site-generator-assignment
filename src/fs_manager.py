from os import mkdir, path, listdir
from shutil import rmtree, copy


def copy_file(src: str, dest: str) -> None:
    if not path.exists(src):
        raise FileExistsError(f"File: {src} not found")
    if not path.isfile(src):
        raise ValueError(f"{src} is not a file")
    copy(src, dest)
    print(f"Copied from {src} to {dest}")


def copy_folder(src: str, dest: str) -> None:
    if not path.exists(dest):
        mkdir(dest)
        print(f"created new folder at: {dest}")

    structure = listdir(src)
    for f in structure:
        srcPath, destPath = [path.join(src, f), path.join(dest, f)]
        if path.isfile(srcPath):
            copy_file(srcPath, destPath)
            continue
        copy_folder(srcPath, destPath)


def sync_folder(src: str, dest: str) -> None:
    if path.isfile(src):
        raise ValueError(f"{src} is a file")
    print(f"starting sync from {src} to {dest}")
    if path.exists(dest):
        rmtree(dest)
    copy_folder(src, dest)
