import os
import threading

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QProgressBar
)
from PyQt5.QtCore import (QObject, pyqtSignal)

from core.process_processing import (process_folder)

from ui.reprocess_window import ReprogressWindow

class Signals(QObject):
    log_signal = pyqtSignal(str)

    progress_signal = pyqtSignal(int, int)

    done_signal = pyqtSignal()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.signals = Signals()

        self.init_ui()

        self.signals.log_signal.connect(self.log)
        self.signals.progress_signal.connect(self.update_progress)
        self.signals.done_signal.connect(self.processing_done)

    def init_ui(self):
        
        self.setWindowTitle("Обработка мер поддержки")
        self.resize(800, 700)
        layout = QVBoxLayout()

        self.input_edit = QLineEdit()
        btn_input = QPushButton("Входная папка")
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

        self.run_btn = QPushButton("Запустить")
        self.run_btn.clicked.connect(self.start_processing)

        self.retry_btn = QPushButton("Повторная проверка")
        self.retry_btn.clicked.connect(self.open_retry_window)

        self.progress = QProgressBar()
        self.progress_label = QLabel("0%")

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addWidget(self.run_btn) 
        layout.addWidget(self.retry_btn)
        layout.addWidget(self.progress) 
        layout.addWidget(self.progress_label) 
        layout.addWidget(self.log_text)
        self.setLayout(layout)

    def browse_input(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")

        if folder:
            self.input_edit.setText(folder)

    def browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")

        if folder:
            self.output_edit.setText(folder)

    def log(self, text):
        self.log_text.append(text)

    def update_progress(self, current, total):
        if total == 0:
            percent = 0
        else:
            percent = int((current/total) * 100)

        self.progress_label.setText(f"{current}/{total} ({percent}%)")
        self.progress.setValue(percent)

    def start_processing(self):
        input_dir = self.input_edit.text()
        output_dir = self.output_edit.text()

        if not input_dir:
            QMessageBox.critical(self, "Ошибка", "Выберите папку")

            return
        
        if not output_dir:
            output_dir = os.path.join(input_dir, "json_output")

            os.makedirs(output_dir, exist_ok = True)

            self.output_edit.setText(output_dir)
        
        self.run_btn.setEnabled(False)
        self.log_text.clear()\
        
        self.log("=== НАЧАЛО ОБРАБОТКИ ===")

        self.thread = threading.Thread(
            target = self.process_worker,
            args = (input_dir, output_dir), 
            daemon = True
        )

        self.thread.start()

    def process_worker(self, input_dir, output_dir):
        try:
            process_folder(input_dir, output_dir,
                        self.signals.log_signal.emit,
                        self.signals.progress_signal.emit)
            self.signals.done_signal.emit()
        
        except Exception as e:
            import traceback
            self.signals.log_signal.emit(traceback.format_exc())

        finally:
            self.signals.done_signal.emit()

    def processing_done(self):
        self.run_btn.setEnabled(True)

    def open_retry_window(self):
        self.retry_window = ReprogressWindow()
        self.retry_window.show()