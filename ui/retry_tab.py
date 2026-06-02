import threading

from PyQt5.QtWidgets import(
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QProgressBar,
    QMessageBox
)

from ui.base_tab import BaseTab

from core.reprocess import reprocess_failed_files

class RetryTab(BaseTab):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.signals.log_signal.connect(self.log)
        self.signals.progress_signal.connect(self.update_progress)
        self.signals.done_signal.connect(self.retry_done)

    def init_ui(self):
        layout = QVBoxLayout()

        self.input_edit = QLineEdit()

        btn_input = QPushButton("Исходная папка")
        btn_input.clicked.connect(self.browse_input)

        row1 = QHBoxLayout()
        row1.addWidget(self.input_edit)
        row1.addWidget(btn_input)

        self.output_edit = QLineEdit()

        btn_output = QPushButton("Выходная папка")
        btn_output.clicked.connect(self.browse_output)

        row2 = QHBoxLayout()
        row2.addWidget(self.output_edit)
        row2.addWidget(btn_output)

        self.log_edit = QLineEdit()

        btn_log = QPushButton("Выбрать лог")
        btn_log.clicked.connect(self.browse_log)

        row3 = QHBoxLayout()
        row3.addWidget(self.log_edit)
        row3.addWidget(btn_log)

        self.run_btn = QPushButton("Повторная обработка")
        self.run_btn.clicked.connect(self.start_retry)

        self.progress = QProgressBar()

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)

        layout.addWidget(self.run_btn)
        layout.addWidget(self.progress)
        layout.addWidget(self.logs)

        self.setLayout(layout)

    def browse_input(self):
        folder = self.select_folder()

        if folder:
            self.input_edit.setText(folder)

    def browse_output(self):
        folder = self.select_folder()

        if folder:
            self.output_edit.setText(folder)

    def browse_log(self):
        file_path = self.select_file("Текстовые файлы (*.txt)")

        if file_path:
            self.log_edit.setText(file_path)

    def start_retry(self):

        if not self.input_edit.text():
            QMessageBox.critical(self, "Ошибка", "Выберите исходную папку")
            return
        
        if not self.output_edit.text():
            QMessageBox.critical(self, "Ошибка", "Выберите выходную папку")
            return
        
        if not self.log_edit.text():
            QMessageBox.critical(self, "Ошибка", "Выберите лог-файл")
            return

        self.run_btn.setEnabled(False)
        self.logs.clear()

        self.thread = threading.Thread(
            target=self.retry_worker,
            args=(
                self.input_edit.text(),
                self.output_edit.text(),
                self.log_edit.text()
            ),
            daemon=True
        )

        self.thread.start()

    def retry_worker(
        self,
        input_dir,
        output_dir,
        log_file
    ):

        reprocess_failed_files(
            input_dir,
            output_dir,
            log_file,
            self.signals.log_signal.emit,
            self.signals.progress_signal.emit
        )

        self.signals.done_signal.emit()

    def retry_done(self):

        self.run_btn.setEnabled(True)

        self.log(
            "=== ПОВТОРНАЯ ОБРАБОТКА ГОТОВА ==="
        )