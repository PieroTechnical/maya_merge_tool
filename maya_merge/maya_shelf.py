import os
from maya import cmds


def onMayaDroppedPythonFile(*arg):
    """
    Automatically installs the shelf if you drag and drop the python 
    script into your maya window
    """
    install()


def install():
    """
    Entry function to install a shelf button in Maya for the module.
    Determines paths and parameters, and then creates or updates the
    shelf button.
    """
    script_folder = os.path.dirname(os.path.dirname(__file__))
    module_name = os.path.basename(os.path.dirname(__file__))
    icon = os.path.join(script_folder, module_name, "icon/icon.png")
    script = _generate_python_script(module_name)
    _create_or_update_shelf_button("PieroTechnical", "MayaMerge", script, icon)


def _generate_python_script(module):
    """
    Generates the Python script to be executed by the shelf button.
    Ensures the module path is in sys.path and then launches the UI.
    """
    return f"from {module} import ui\n" "ui.launch()"


def _create_or_update_shelf_button(shelf_name, button_name, command, icon_path):
    """
    Creates or updates a shelf button in Maya.
    """
    try:
        if not _shelf_exists(shelf_name):
            _create_shelf(shelf_name)
        button_id = _find_button(shelf_name, button_name)

        if button_id:
            cmds.deleteUI(button_id, control=True)
            print(f"Button '{button_name}' replaced.")
        cmds.shelfButton(
            l=button_name,
            c=command,
            p=shelf_name,
            ann="Open MayaMerge UI",
            i1=icon_path,
        )

        print(f"Button '{button_name}' added to shelf '{shelf_name}'.")
    except Exception as e:
        print("Failed to create or update shelf button:", str(e))


def _shelf_exists(shelf_name):
    """
    Checks if the given shelf exists in Maya.
    """
    return shelf_name in cmds.shelfTabLayout("ShelfLayout", q=True, tli=True)


def _create_shelf(shelf_name):
    """
    Creates a new shelf in Maya.
    """
    cmds.shelfLayout(shelf_name, parent="ShelfLayout")
    print(f"Shelf '{shelf_name}' created.")


def _find_button(shelf_name, button_name):
    """
    Finds a button on the specified shelf by name.
    """
    existing_buttons = cmds.shelfLayout(
        shelf_name, q=True, childArray=True) or []
    for btn in existing_buttons:
        if cmds.shelfButton(btn, q=True, label=True) == button_name:
            return btn
    return None
