import json

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QTextEdit,
    QLineEdit,
    QMessageBox
)

from ui.base_tab import BaseTab

from core.json_viewer import *

class LoadJsonTab(BaseTab):
    def __init__(self):
        super().__init__()

        self.files = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        row = QHBoxLayout()

        self.folder_edit = QLineEdit()

        btn_folder = QPushButton("Выбрать папку с json")
        btn_folder.clicked.connect(self.select_json_folder)

        row.addWidget(self.folder_edit)
        row.addWidget(btn_folder)

        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.show_json)

        self.viewer = QLineEdit()
        self.viewer.setReadOnly(True)

        layout.addLayout(row)
        layout.addWidget(self.file_list)
        layout.addWidget(self.viewer)

        self.setLayout(layout)

    def select_json_folder(self):
        folder = self.select_folder()
        
        if not folder:
            QMessageBox.critical(self, "Ошибка", "Выберите папку с json")
            return
        
        self.folder_edit.setText(folder)

        self.file_list.clear()

        self.files = get_json_files(folder)

        for file_path in self.files:
            self.file_list.addItem(file_path)
    
    def show_json(self, item):
        try:
            file_path = item.text()
            data = load_json_file(file_path)

            pretty = json.dumps(data, ensure_ascii = False, indent = 4)

            self.viewer.setPlainText(pretty)

        except Exception as e:
            self.viewer.setPlainText(f"Ошибка: {e}")