import os
import threading

from PyQt5.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QTextEdit,
    QLabel,
    QProgressBar,
    QLineEdit,
    QMessageBox
    )

from core.process_processing import process_folder

from ui.base_tab import BaseTab

class ProcessTab(BaseTab):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.signals.log_signal.connect(self.log)
        self.signals.progress_signal.connect(self.update_progress)
        self.signals.done_signal.connect(self.processing_done)

    def init_ui(self):
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

        self.progress = QProgressBar()
        self.progress_label = QLabel("0%")

        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        
        layout.addLayout(row1)
        layout.addLayout(row2)

        layout.addWidget(self.run_btn)

        layout.addWidget(self.progress)
        layout.addWidget(self.progress_label)

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

    def update_progress(self, current, total):
        super().update_progress(current, total)

        if total == 0:
            percent = 0
        else:
            percent = int((current/total) * 100)

        self.progress_label.setText(f"{current}/{total} ({percent}%)")

    def start_processing(self):
        input_dir = self.input_edit.text()
        output_dir = self.output_edit.text()

        if not input_dir:
            QMessageBox.critical(self, "Ошибка", "Выберите исходную папку")

            return
        
        if not output_dir:
            output_dir = os.path.join(input_dir, "json_output")

            os.makedirs(output_dir, exist_ok = True)

            self.output_edit.setText(output_dir)
        
        self.run_btn.setEnabled(False)
        self.logs.clear()

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
        
        except Exception as e:
            import traceback
            self.signals.log_signal.emit(traceback.format_exc())

        finally:
            self.signals.done_signal.emit()

    def processing_done(self):
        self.run_btn.setEnabled(True)