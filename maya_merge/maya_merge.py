from . import maya_file
from . import maya_cleanup
from . import maya_nodes


def merge(asset_name: str, target_folder: str = "", reset_pivots: bool = False):
    """
    Initializes a new file, imports files from a specified directory,
    and processes the scene nodes.

    Args:
        asset_name (str): Asset name to use for output.
        target_folder (str): Path to the folder containing .ma files.
        reset_pivots (bool): Determines whether to reset the pivots.
    """
    maya_file.new()
    maya_file.import_all_from_directory(target_folder)

    maya_nodes.unlock_all_nodes()
    maya_nodes.delete_all_history()

    mesh_nodes = filter(maya_nodes.Node.is_valid_mesh, maya_nodes.get_scene_nodes())

    _extract_and_cleanup_meshes(mesh_nodes, asset_name, reset_pivots)

    maya_nodes.clear_selection()
    maya_cleanup.delete_foreign_namespaces()


def _extract_and_cleanup_meshes(nodes, asset_name, reset_pivots):
    """
    Extracts and merges given nodes under a new parent node, renaming
    and processing them based on the instructions on the test brief.

    Args:
        nodes (List[Node]): List of node objects to process.
        asset_name (str): Base name to use for naming and grouping.
        reset_pivots (bool): Determines whether to reset the pivots.
    """
    parent_node = maya_nodes.Node.new(f"|{asset_name}_GRP")

    i = 0

    for node in nodes:
        new_name = f":C_{asset_name}{i:04}_GEO"
        node.rename(new_name)
        node.unlock_channels()
        node.reparent(parent_node)
        node.delete_history()
        node.reset_shading_group()
        node.zero_transforms()

        if reset_pivots:
            node.reset_pivots()
        i += 1
