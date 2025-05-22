import os
import shutil
import platform
import errno
import stat

# Constants
MODULE_NAME = "maya_merge"

def main():
    print_header("MayaMerge Tool Installation")
    maya_script_path = find_maya_script_path()
    if not maya_script_path:
        maya_script_path = input(
            "Maya scripts directory not found. Please enter the path manually: "
        )

        if not os.path.exists(maya_script_path):
            print("ERROR: Invalid path provided. Installation aborted.")
            return

    # Prepare the paths for the module and target folder
    module_path = os.path.join(os.path.dirname(__file__), MODULE_NAME)
    target_folder = os.path.join(
        maya_script_path, os.path.basename(module_path))

    # Check and copy the folder
    check_and_copy_folder(module_path, target_folder)

    print("\n")  # Prints a new line at the end, looks nicer in the terminal


def find_maya_script_path():
    if platform.system() == "Windows":
        return os.path.join(
            os.environ.get("USERPROFILE", ""), "Documents", "maya", "scripts"
        )
    elif platform.system() in ["Linux", "Darwin"]:  # Darwin is macOS
        return os.path.join(os.environ.get("HOME", ""), "maya", "scripts")
    return None


def check_and_copy_folder(src, dest):
    if os.path.exists(dest):
        response = input(
            "Folder already exists. Do you want to overwrite?\nEnter (yes/no): ")
        if response.lower() != "yes":
            print("WARNING: Installation aborted by the user.")
            return
    copy_folder(src, dest)
    print(f"SUCCESS: MayaMerge Tool successfully installed to {dest}")


def copy_folder(src, dest):
    def handle_remove_readonly(func, path, exc_info):
        if exc_info[1].errno == errno.EACCES:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        else:
            raise exc_info[1]

    if os.path.exists(dest):
        shutil.rmtree(dest, onexc=handle_remove_readonly)
    shutil.copytree(src, dest)


def print_header(message):
    print(f"\n{'=' * len(message)}")
    print(message)
    print(f"{'=' * len(message)}\n")


if __name__ == "__main__":
    main()
