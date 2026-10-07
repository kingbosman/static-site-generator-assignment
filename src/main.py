from fs_manager import sync_folder


dir_path_static = "./static"
dir_path_public = "./public"


def main() -> None:
    sync_folder(dir_path_static, dir_path_public)


main()
