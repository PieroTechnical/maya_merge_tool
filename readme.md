# MayaMerge Tool – Module Installation Guide

## 🧩 Introduction

**MayaMerge Tool** simplifies the process of merging multiple Maya ASCII (`.ma`) files into a single, clean, production-ready asset. Built for Autodesk Maya 2024+, it ensures:

- Correct naming conventions  
- Frozen transformations  
- Deleted construction history  
- Namespace cleanup  
- Default lambert1 material applied  

---

## 🚀 What's New

- Installs as a proper **Maya module**
- Shelf button is automatically created on launch
- Clean log output in the script editor

---

## 📦 Installation

### Step 1: Download the Tool

[📥 Click here to download the latest version (ZIP)](https://github.com/PieroTechnical/maya_merge_tool/archive/refs/heads/main.zip)

Once downloaded, extract the contents anywhere on your computer.

### Step 2: Run the Installer

Double-click the installer appropriate for your operating system:

- **Windows**: `__installer__.bat`
- **macOS/Linux**: `__installer__.sh`

The tool will be automatically installed into your Maya modules folder.

---

## ▶ Launch Maya

Restart Maya 2024. You’ll see a new shelf tab labeled **MergeTool**. Click the icon to launch the UI.

---

## 🛠️ Usage

### 1. Launch the Tool

Click the **MayaMerge** icon from the `MergeTool` shelf.

### 2. Configure

- Enter an asset name (e.g. `MarsRover`)
- Select a folder containing `.ma` files

### 3. Merge

Click **Merge**. The tool will:

- Import all `.ma` files from the folder
- Find meshes under `geo_GRP`
- Rename them as `C_<asset_name>####_GEO`
- Parent them under a group named `C_<asset_name>_GRP`
- Clean transforms, delete history, and remove namespaces

### 4. Review

- Check the Outliner for `C_<asset_name>_GRP`
- Verify naming, grouping, and cleanup

---

## ❌ Uninstallation

1. Go to:

   `C:\Users\<your_username>\Documents\maya\modules\`

2. Delete:
   - `maya_merge_module.mod`
   - `maya_merge_module\`

3. Restart Maya

---

## 📫 Support

For questions or help, contact:  
📧 **support@pierotechnical.com**
