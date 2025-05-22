import maya.cmds as cmds
from typing import Generator, List


class Node:
    """
    A class to handle Maya node operations.
    This is really just an excuse to show that I know how to use OOP and
    because PyMel can be controversial.
    """

    def __init__(self, name: str):
        """Initializes a Node for a maya node with the provided name.
        Use Node.new(name) if you want to create a new node.
        """
        self.name = name

    @classmethod
    def new(node, name: str):
        """Creates a new Node with the provided name."""
        if cmds.objExists(name):
            raise RuntimeError(
                (f"Cannot create {name}, a maya node already exists by that name")
            )
        cmds.group(em=1, name=name)
        return node(name)

    def delete_history(self):
        cmds.delete(self.name, ch=True)

    def unlock_node(self):
        cmds.lockNode(self.name, l=False)

    def unlock_channels(self):
        channels = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        for channel in channels:
            cmds.setAttr(f"{self.name}.{channel}", lock=False, keyable=True)

    def reparent(self, parent: "Node"):
        cmds.parent(self.name, parent.name)

    def zero_transforms(self):
        cmds.makeIdentity(self.name, apply=True, t=True, r=True, s=True)

    def reset_pivots(self):
        cmds.xform(self.name, worldSpace=True, pivots=[0, 0, 0])

    def rename(self, new_name: str) -> str:
        self.name = cmds.rename(self.name, new_name)
        return self.name

    def exists(self) -> bool:
        return cmds.objExists(self.name)

    def contains_component(self, target_type: str = "mesh") -> bool:
        """Check if the node or any descendent is of specific type."""
        if cmds.objectType(self.name) == target_type:
            return True
        children = cmds.listRelatives(self.name, children=True, fullPath=True)
        if children:
            return any(
                Node(child).contains_component(target_type) for child in children
            )
        return False

    def has_parent(self, target_name: str = "geo_GRP") -> bool:
        """Check if the node's parent matches the specified name."""
        parent = cmds.listRelatives(self.name, parent=True, fullPath=True)
        if not parent:
            return False
        parent_name = parent[0].split(":")[-1]
        return parent_name == target_name

    def is_valid_mesh(self):
        return all(
            [self.exists(), self.contains_component("mesh"), self.has_parent("geo_GRP")]
        )

    def reset_shading_group(self, shading_group: str = "initialShadingGroup"):
        """Assign the node to a specific shading group."""
        cmds.sets(self.name, edit=True, forceElement=shading_group)


def list_scene_nodes(type_of: str = "transform") -> List[Node]:
    """Return a list of Node objects for every node of the specified
    type in the scene.
    """
    transform_nodes = cmds.ls(type=type_of, long=True)
    return [Node(name) for name in transform_nodes]


def get_scene_nodes(type_of: str = "transform") -> Generator[Node, None, None]:
    """Yield Node objects one at a time for every node of the specified
    type in the scene, resulting in heavily improved memory usage."""
    transform_nodes = cmds.ls(type=type_of, long=True)
    yield from (Node(name) for name in transform_nodes)


def clear_selection():
    """Clear the current selection in the scene."""
    cmds.select(clear=True)


def unlock_all_nodes():
    """Unlock all nodes of type 'transform' in the scene."""
    nodes = cmds.ls(type="transform")
    for node in nodes:
        cmds.lockNode(node, lock=False)


def delete_all_history():
    """Delete all history in scene"""
    cmds.delete(ch=True, all=True)
