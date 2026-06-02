import os 
import threading

from core.reprocess import (reprocess_failed_files)

from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtWidgets import(
QWidget,
QLabel,
QPushButton,
QFileDialog,
QTextEdit,
QVBoxLayout,
QHBoxLayout,
QLineEdit,
QProgressBar
)

class Signals(QObject):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    done_signal = pyqtSignal()

class ReprogressWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.signals = Signals()
        self.init_ui()
        self.signals.log_signal.connect(self.log)
        self.signals.progress_signal.connect(self.update_progress)

        self.signals.done_signal.connect(self.retry_done)
    
    def init_ui(self):
        self.setWindowTitle("Повторная обработка")

        self.resize(700,600)

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

        self.run_btn = QPushButton("Запустить повторную обработку")
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
        folder = QFileDialog.getExistingDirectory()

        if folder:
            self.input_edit.setText(folder)

    def browse_output(self):
        folder = QFileDialog.getExistingDirectory()

        if folder:
            self.output_edit.setText(folder)
    def browse_log(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выберите файл лога")

        if file:
            self.log_edit.setText(file)

    def start_retry(self):
        input_dir = self.input_edit.text()
        output_dir = self.output_edit.text()
        log_file = self.log_edit.text()

        self.run_btn.setEnabled(False)

        self.thread = threading.Thread(
            target = self.retry_worker, args=(
                input_dir, output_dir, log_file
            ),
            daemon = True
        )

        self.thread.start()

    def log(self, text):
        self.logs.append(text)

    def update_progress(self, current, total):
        if total == 0:
            percent = 0
        
        else:
            percent = int((current/total) * 100)
        
        self.progress.setValue(percent)

    def retry_worker(self, input_dir, output_dir, log_file):
        reprocess_failed_files(input_dir, output_dir, log_file, self.signals.log_signal.emit, self.signals.progress_signal.emit)
        self.signals.done_signal.emit()

    def retry_done(self):
        self.run_btn.setEnabled(True)

        self.log("=== ПОВТОРНАЯ ПОДГОТОВКА ГОТОВА ===")