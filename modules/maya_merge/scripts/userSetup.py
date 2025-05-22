import maya.utils
import maya.mel as mel
import os
import maya.cmds as cmds

def load_shelf():
    shelves_path = os.path.join(
        cmds.moduleInfo(mn="maya_merge_tool", path=True), 
        "shelves", 
        "shelf_MergeTool.mel"
    ).replace("\\", "/")

    # Source and build the shelf
    mel.eval(f'source "{shelves_path}"; shelf_MergeTool;')

maya.utils.executeDeferred(load_shelf)
