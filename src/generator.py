from os import mkdir, path, listdir
from shutil import rmtree, copy


def copy_file(file_name: str, src: str, dest: str, file_path: str) -> None:
    srcPath, destPath = [
        path.join(src, file_path, file_name),
        path.join(dest, file_path, file_name),
    ]
    if not path.exists(srcPath):
        raise FileExistsError(f"File: {srcPath} not found")
    if not path.isfile(srcPath):
        raise ValueError(f"{srcPath} is not a file")
    copy(srcPath, destPath)
    print(f"Copied from {srcPath} to {destPath}")


def copy_folder(src: str, dest: str, folder_path: str = ""):
    structure = listdir(path.join(src, folder_path))
    for f in structure:
        if path.isfile(path.join(src, folder_path, f)):
            copy_file(f, src, dest, folder_path)
            continue
        if not path.exists(path.join(dest, folder_path, f)):
            mkdir(path.join(dest, folder_path, f))
            print(f"created new folder at: {path.join(dest,folder_path,f)}")
        copy_folder(src, dest, path.join(folder_path, f))


def sync_folder(src: str, dest: str) -> None:
    if path.isfile(src):
        raise ValueError(f"{src} is a file")
    if path.exists(dest):
        rmtree(dest)
    mkdir(dest)
    print(f"created destination folder: {dest}")
    copy_folder(src, dest)
