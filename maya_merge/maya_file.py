import maya.cmds as cmds
import glob
import os
from typing import List


def new(force: bool = False):
    """
    Creates a new file in Maya. If 'force' is not True, it prompts the
    user with a dialog to confirm the action,warning that it will
    discard all unsaved progress.

    Parameters:
    - force (bool): If True, the new file is created without asking.
    Defaults to False.
    """
    if not force:
        result = cmds.confirmDialog(
            title="New File",
            message=(
                "This will create a new file and lose all unsaved "
                "progress.\n"
                "Are you sure?"
            ),
            button=["Yes", "No"],
            defaultButton="No",
            cancelButton="No",
            dismissString="No",
        )
        if result == "No":
            print("User canceled the new file operation.")
            return
    cmds.file(newFile=True, force=True)
    print("New file created.")


def import_files(files: List[str]):
    """
    Imports multiple files into the current Maya scene, each under a
    namespace. Gracefully handles wrong file types and other errors.

    Parameters:
    - files (list of str): A list of file paths to import.
    """
    for file in files:
        if ".ma" not in file.lower():
            print(f"{file} does not have the correct file extension, ignoring")
            continue
        try:
            cmds.file(file, i=1, namespace="import")
        except Exception as e:
            print(f"Exception: Couldn't import file {file}: {e}")


def import_all_from_directory(target_folder: str):
    """
    Searches for all files in the specified directory path and imports
    them into the current Maya scene.

    Parameters:
    - target_folder (str): The directory from which all files will be
    imported.
    """
    if not target_folder:
        raise Exception("No target folder provided.")
    files = glob.glob(f"{target_folder}{os.path.sep}*")

    if not files:
        raise Exception("No files at target directory")
    
    import_files(files)
