from PySide2.QtWidgets import (
    QHBoxLayout,
    QToolButton,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QLabel,
    QCheckBox,
)
from PySide2.QtGui import QIcon, QRegExpValidator
from PySide2.QtCore import QRegExp, Qt
import shiboken2
import maya.OpenMayaUI as omui
import os
from . import maya_merge


# Pretty standard Chris Zurbrigg style PyQt setup, with some simplifications


def get_maya_main_window():
    """Return the Maya main window widget as a Python object."""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QWidget)


class MayaMergeUI(QWidget):
    def __init__(self, parent: QWidget = None):
        # Setup UI
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

        # Instantiate variables
        self.selected_folder = None

    def _setup_ui(self):
        """UI setup process broken down into simple steps"""
        self._configure_window()

        layout = QVBoxLayout(self)

        self._add_name_input(layout)
        self._add_folder_picker(layout)

        layout.addStretch()

        self._add_reset_pivots_checkbox(layout)
        self._add_execution_button(layout)

    def _connect_signals(self):
        self.folder_button.clicked.connect(self._handle_folder_selection)
        self.merge_button.clicked.connect(self._merge_button_clicked)

    def _configure_window(self):
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        self.setWindowTitle("MayaMerge Tool")
        self.setWindowIcon(self.create_icon("icon/icon.png"))

    def _add_name_input(self, layout):
        name_label = QLabel("Enter an asset name:", self)
        layout.addWidget(name_label)

        name_edit = QLineEdit(self)
        name_edit.setText("DefaultName")
        name_edit.setValidator(QRegExpValidator(
            QRegExp("^[a-zA-Z0-9_]*$"), self))

        layout.addWidget(name_edit)
        self.name_edit = name_edit

    def _add_folder_picker(self, layout):
        folder_layout = QHBoxLayout()
        layout.addLayout(folder_layout)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(
            "Choose folder containing maya files to import"
        )
        self.line_edit.setReadOnly(True)

        folder_layout.addWidget(self.line_edit, stretch=2)

        self.folder_button = QToolButton()
        self.folder_button.setIcon(self.create_icon("icon/file_open.png"))

        folder_layout.addWidget(self.folder_button)

    def _add_reset_pivots_checkbox(self, layout):
        reset_pivots_cb = QCheckBox("Reset Pivots", self)
        reset_pivots_cb.setChecked(False)
        layout.addWidget(reset_pivots_cb)
        self.reset_pivots_cb = reset_pivots_cb

    def _add_execution_button(self, layout):
        merge_button = QPushButton("Extract and Merge", self)

        # Button disabled until valid file selected
        merge_button.setEnabled(False)

        layout.addWidget(merge_button)

        self.merge_button = merge_button

    def _handle_folder_selection(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folder = folder
            self.line_edit.setText(folder)
            self.merge_button.setEnabled(True)

    def create_icon(self, icon_path):
        icon_path = os.path.join(os.path.dirname(__file__), icon_path)
        return QIcon(icon_path)

    def _merge_button_clicked(self):
        if not self.selected_folder:
            return
        maya_merge.merge(
            self.name_edit.text(),
            target_folder=self.selected_folder,
            reset_pivots=self.reset_pivots_cb.isChecked(),
        )


def show():
    """Instantiate and display the MayaMerge UI."""
    global maya_merge_ui
    try:
        maya_merge_ui.close()
        maya_merge_ui.deleteLater()
    except:
        pass
    maya_merge_ui = MayaMergeUI(parent=get_maya_main_window())
    maya_merge_ui.show()
