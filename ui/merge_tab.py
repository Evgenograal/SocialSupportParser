import threading

from PyQt5.QtWidgets import(
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QLabel,
    QListWidget,
    QMessageBox
)

from ui.base_tab import BaseTab

from core.json_merger import merge_json_to_md

class MergeTab(BaseTab):

    def __init__(self):
        super().__init__()

        self.json_dirs = []
        
        self.init_ui()

        self.signals.log_signal.connect(self.log)
        self.signals.done_signal.connect(self.merge_done)

    def init_ui(self):
        layout = QVBoxLayout()

        row = QHBoxLayout()

        self.md_edit = QLineEdit()

        btn_md = QPushButton("Папка с md")
        btn_md.clicked.connect(self.select_md_folder)

        self.json_list = QListWidget()

        btn_json = QPushButton("Добавить папку json")

        btn_json.clicked.connect(self.add_json_folder)

        self.run_btn = QPushButton("Объединить")

        self.run_btn.clicked.connect(self.start_merge)

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        row.addWidget(self.md_edit)
        row.addWidget(btn_md)

        layout.addLayout(row)

        layout.addWidget(QLabel("Папки с json"))

        layout.addWidget(self.json_list)

        layout.addWidget(btn_json)

        layout.addWidget(self.run_btn)

        layout.addWidget(self.logs)

        self.setLayout(layout)
    
    def select_md_folder(self):
        folder = self.select_folder()

        if folder:
            self.md_edit.setText(folder)

    def add_json_folder(self):
        folder = self.select_folder()

        if folder:
            self.json_dirs.append(folder)
            self.json_list.addItem(folder)

    def start_merge(self):
        if not self.md_edit.text():
            QMessageBox.critical(self, "Ошибка", "Выберите папку с md")
            return

        if not self.json_dirs:
            QMessageBox.critical(self, "Ошибка", "Добавьте хотя бы одну папку с json")
            return
        
        self.logs.clear()
        self.log("=== НАЧАЛО ОБЪЕДИНЕНИЯ ===")

        self.run_btn.setEnabled(False)
        
        self.thread = threading.Thread(
            target=self.merge_worker,
            daemon=True
        )

        self.thread.start()

    def merge_worker(self):

        merge_json_to_md(
            self.md_edit.text(),
            self.json_dirs,
            self.signals.log_signal.emit,
            lambda x, y: None
        )

        self.signals.done_signal.emit()

    def merge_done(self):

        self.run_btn.setEnabled(True)

        self.log(
            "=== ОБЪЕДИНЕНИЕ ЗАВЕРШЕНО ==="
        )
