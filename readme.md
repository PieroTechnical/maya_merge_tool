# MayaMerge Tool Installation and Usage Guide

## Introduction

Welcome to the MayaMerge Tool Installation and Usage Guide. This tool
is designed to simplify the process of merging
multiple Maya ASCII (.ma) files into a single, clean, production-ready
asset. The tool ensures that all meshes conform to naming conventions,
have transformations frozen, and are devoid of unnecessary nodes or
history, streamlining the workflow in Autodesk Maya 2024.

## Prerequisites

Before installing and using this tool, please ensure you have:

- Autodesk Maya 2024 installed on your system

## Simple Installation (may require administrator privileges)

### Install The Tool

- Download and extract `maya_merge_tool.zip` anywhere on your computer
- Run `__installer__.bat`
- Follow the instructions in the command window
- Start (or restart) Maya 2024

### Install the Shelf

- Drag and drop `maya_shelf.py` from `maya_merge_tool` into the
  Maya window to install or update the shelf

## Advanced Installation (skip if you completed the previous step)

### Step 1: Download the Tool

- Download the file `maya_merge_tool.zip`

### Step 2: Extract the Tool

- Locate and extract `maya_merge` from `maya_merge_tool.zip` file
  to a valid maya scripts path (ie.):
  `C:\Users\<username>\Documents\maya\scripts`
- Ensure `maya_merge` is correctly located in the `scripts` folder

### Step 3: Launch Maya

- Start (or restart) Maya 2024

### Install the Shelf

- Drag and drop `maya_shelf.py` from `maya_merge` into the
  Maya window to install or update the shelf

## Usage

### Step 1: Launch the Tool

- Click on the MayaMerge Tool icon in the 'PieroTechnical' shelf to
  open the user interface

### Step 2: Configure the Tool

- In the tool's interface, enter the desired asset name in the
  `<asset_name>` field
- Select the folder containing your .ma files by using the
  `Select Folder` button

### Step 3: Execute the Merge

- Once the asset name is specified and the folder is selected, click the
  `Merge` button
- The tool will process all .ma files in the selected folder, merging
  only the polygon meshes under groups named `geo_GRP`
- Each mesh will be renamed according to the `C_<asset_name>####_GEO`
  convention, where #### represents a sequential number
- All meshes will be parented to a new group named `<asset_name>_GRP`,
  positioned at the world level

### Step 4: Verify the Output

- Check the `<asset_name>_GRP` in the Outliner to ensure all meshes are
  correctly merged and named
- Verify that no unnecessary nodes, including shaders, remain in the
  scene and that the default lambert1 material is applied

## Support

For any issues related to installation or usage of the MayaMerge Tool,
please contact the creator at `support@pierotechnical.com`
