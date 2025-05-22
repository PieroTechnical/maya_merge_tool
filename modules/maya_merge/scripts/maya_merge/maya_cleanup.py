import maya.cmds as cmds
import maya.mel as mel
from .logger import log


def delete_namespace_and_contents(namespace: str):
    """
    Recursively delete the specified namespace and all its contents in a
    Maya scene.

    This function iterates through each child namespace within the given
    namespace, deletes all objects within these namespaces, and then
    attempts to remove the namespaces themselves. It handles namespaces
    hierarchically from children to parent to avoid dependency issues.

    Parameters:
    namespace (str): The name of the namespace to delete.
    """
    # Fully qualify the child namespaces

    current_namespace = cmds.namespaceInfo(namespace, lon=True, recurse=False)
    if current_namespace:
        full_child_namespaces = [f"{namespace}:{ns}" for ns in current_namespace]
        for child_ns in full_child_namespaces:
            delete_namespace_and_contents(child_ns)
    # List all dependency nodes in the current namespace with full path

    ns_objects = cmds.ls(f"{namespace}:*", long=True)
    if ns_objects:
        cmds.delete(ns_objects)
    # Attempt to remove the namespace if it is not a reserved namespace

    if namespace not in [":", "UI", "shared"]:
        try:
            cmds.namespace(removeNamespace=namespace)
        except RuntimeError as e:
            log.error(f"Couldn't remove namespace: {namespace}: {e}")


def delete_foreign_namespaces():
    """
    Delete all non-reserved namespaces in the Maya scene.

    This function gathers all namespaces in the scene, excluding the
    root and reserved namespaces ('UI', 'shared'), and deletes them
    along with any contents. Namespaces are processed in order of their
    nested depth, from deepest to shallowest, to ensure that child
    namespaces are deleted first.
    """
    # List all non-root namespaces

    all_namespaces = cmds.namespaceInfo(lon=True, recurse=True) or []

    ignore_namespaces = ["UI", "shared"]

    # Filter namespaces to avoid reserved ones

    valid_namespaces = [ns for ns in all_namespaces if ns not in ignore_namespaces]

    # Sorts namespaces based on their depth
    # Nested namespaces will appear first

    valid_namespaces_sorted = sorted(
        valid_namespaces, key=lambda x: x.count(":"), reverse=True
    )

    # Delete namespaces from deepest to root-level

    for ns in valid_namespaces_sorted:
        delete_namespace_and_contents(ns)


def delete_unused_shaders():
    """
    Delete all unused shaders from the scene.

    This function utilizes a MEL command specifically designed to
    identify and remove any shading nodes that are not currently being
    used in the scene.
    """
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
