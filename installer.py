import os
import shutil
import platform
import errno
import stat

MOD_FILENAME = "maya_merge_module.mod"
MODULE_FOLDER_NAME = "maya_merge_module"
SOURCE_FOLDER = "modules"

def main():
    print_header("MayaMerge Tool Installer")

    modules_path = find_maya_modules_path()
    if not modules_path:
        modules_path = input("Maya modules directory not found. Enter manually: ")
        if not os.path.exists(modules_path):
            print("ERROR: Invalid path. Installation aborted.")
            return

    repo_root = os.path.dirname(__file__)
    source_root = os.path.join(repo_root, SOURCE_FOLDER)

    mod_file_src = os.path.join(source_root, MOD_FILENAME)
    payload_src = os.path.join(source_root, MODULE_FOLDER_NAME)

    mod_file_dest = os.path.join(modules_path, MOD_FILENAME)
    payload_dest = os.path.join(modules_path, MODULE_FOLDER_NAME)

    if os.path.exists(mod_file_dest) or os.path.exists(payload_dest):
        response = input("Existing installation found. Overwrite? (yes/no): ")
        if response.strip().lower() != "yes":
            print("Installation aborted.")
            return

    copy_file(mod_file_src, mod_file_dest)
    copy_folder(payload_src, payload_dest)

    print("\n✅ Installed successfully:")
    print(f"• {mod_file_dest}")
    print(f"• {payload_dest}")


def find_maya_modules_path():
    if platform.system() == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Documents", "maya", "modules")
    elif platform.system() in ("Darwin", "Linux"):
        return os.path.join(os.environ["HOME"], "maya", "modules")
    return None


def copy_file(src, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)


def copy_folder(src, dest):
    def handle_remove_readonly(func, path, exc_info):
        if exc_info[1].errno == errno.EACCES:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise
    if os.path.exists(dest):
        shutil.rmtree(dest, onerror=handle_remove_readonly)
    shutil.copytree(src, dest)


def print_header(message):
    print(f"\n{'=' * len(message)}\n{message}\n{'=' * len(message)}\n")


if __name__ == "__main__":
    main()
