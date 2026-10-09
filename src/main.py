from fs_manager import sync_folder
from generator import generate_page


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"


def main() -> None:
    sync_folder(dir_path_static, dir_path_public)
    generate_page(
        f"{dir_path_content}/index.md",
        "./template.html",
        f"{dir_path_public}/index.html",
    )


main()
