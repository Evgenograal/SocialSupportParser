import json

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTreeWidget,
    QTextEdit,
    QLineEdit,
    QMessageBox,
    QSplitter
)

from PyQt5.QtCore import Qt

from ui.base_tab import BaseTab

from core.json_viewer import *

class LoadJsonTab(BaseTab):
    def __init__(self):
        super().__init__()

        self.current_folder = ""

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        folder_row = QHBoxLayout()

        self.folder_edit = QLineEdit()

        btn_folder = QPushButton(
            "Папка JSON"
        )

        btn_folder.clicked.connect(
            self.select_json_folder
        )

        folder_row.addWidget(
            self.folder_edit
        )

        folder_row.addWidget(
            btn_folder
        )

        self.search_edit = QLineEdit()

        self.search_edit.setPlaceholderText(
            "Поиск по JSON..."
        )

        self.search_edit.textChanged.connect(
            self.search_json
        )

        splitter = QSplitter()

        self.file_tree = QTreeWidget()

        self.file_tree.setHeaderLabel(
            "Файлы"
        )

        self.file_tree.itemClicked.connect(
            self.show_json
        )

        self.json_tree = QTreeWidget()

        self.json_tree.setHeaderLabels(
            ["Фильтр", "Значение"]
        )

        splitter.addWidget(
            self.file_tree
        )

        splitter.addWidget(
            self.json_tree
        )

        splitter.setSizes(
            [300, 700]
        )

        layout.addLayout(folder_row)

        layout.addWidget(
            self.search_edit
        )

        layout.addWidget(
            splitter
        )

        self.setLayout(layout)

    def select_json_folder(self):
        folder = self.select_folder()
        
        if not folder:
            QMessageBox.critical(self, "Ошибка", "Выберите папку с json")
            return
        
        self.current_folder = folder

        self.folder_edit.setText(folder)

        build_folder_tree(self.file_tree, folder)
    
    def show_json(self, item):
        file_path = item.data(0, Qt.UserRole)

        if not file_path:
            QMessageBox.critical(self, "Ошибка", "Выберите папку")
            return
        
        try:
            self.json_tree.clear()

            data = load_json_file(file_path)

            build_json_tree(self.json_tree.invisibleRootItem(), data)

            self.json_tree.expandToDepth(1)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def search_json(self, text):
        text = text.lower()

        root = self.json_tree.invisibleRootItem()

        filter_json_tree(root, text)