import threading

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QProgressBar
)

from core.json_merger import merge_json_to_md

class MergeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.json_dirs = []
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Объединение JSON и MD")

        self.resize(800, 700)

        layout = QVBoxLayout()

        md_row = QHBoxLayout()
        self.md_edit = QLineEdit()
        btn_md = QPushButton("Папка с md")
        btn_md.clicked.connect(self.select_md_folder)
        md_row.addWidget(self.md_edit)
        md_row.addWidget(btn_md)

        json_label = QLabel("Папки с json")
        self.json_list = QListWidget()
        btn_add_json = QPushButton("Добавить папку")
        btn_add_json.clicked.connect(self.add_json_folder)

        self.run_btn = QPushButton("Объединить файлы")
        self.run_btn.clicked.connect(self.start_merge)

        self.progress = QProgressBar()

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        layout.addLayout(md_row)

        layout.addWidget(json_label)
        layout.addWidget(self.json_list)
        layout.addWidget(btn_add_json)

        layout.addWidget(self.run_btn)

        layout.addWidget(self.progress)

        layout.addWidget(self.logs)

        self.setLayout(layout)

    def select_md_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с md")

        if folder:
            self.md_edit.setText(folder)
    
    def add_json_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с json")

        if folder:
            self.json_dirs.append(folder)
            self.json_list.addItem(folder)
    
    def log(self, text):
        self.logs.append(text)
    
    def update_progress(self, current, total):
        if total == 0:
            percent = 0
        
        else:
            percent = int((current/total) * 100)

        self.progress.setValue(percent)

    def start_merge(self):
        md_dir = self.md_edit.text()

        if not md_dir:
            self.log("Папка с md файлами не выбрана")

        if not self.json_dirs:
            self.log("Папки с json не выбраны")

        self.logs.clear()

        self.log("=== НАЧАЛО ===")

        self.run_btn.setEnabled(False)

        self.thread = threading.Thread(
            target = self.merge_worker,
            args=(
                md_dir, self.json_dirs
            ),
            daemon = True
        )

        self.thread.start()

    def merge_worker(self, md_dir, json_dirs):
        merge_json_to_md(md_dir, json_dirs, self.log, self.update_progress)

        self.run_btn.setEnabled(True)