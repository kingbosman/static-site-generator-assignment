from fs_manager import sync_folder
from generator import generate_multiple_pages
from sys import argv

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
base_path = argv[1] if len(argv) > 1 else "/"

print(base_path)
print(argv)


def main() -> None:
    sync_folder(dir_path_static, dir_path_public)
    generate_multiple_pages(
        f"{dir_path_content}", "./template.html", f"{dir_path_public}", base_path
    )


main()
