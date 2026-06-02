from PyQt5.QtWidgets import (
    QWidget, 
    QFileDialog
    )

from PyQt5.QtCore import pyqtSignal, QObject

class BaseSignals(QObject):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    done_signal = pyqtSignal()

class BaseTab(QWidget):
    def __init__(self):
        super().__init__()

        self.signals = BaseSignals()
    
    def select_folder(self):
        return QFileDialog.getExistingDirectory(self, "Выберите папку")
    
    def select_file(self, file_filter = "Все файлы(*)"):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", file_filter)
        return file_path
    
    def log(self, text):
        if hasattr(self, "logs"):
            self.logs.append(text)

    def update_progress(self, current, total):
        if not hasattr(self, "progress"):
            return
        
        if total == 0:
            percent = 0
        else:
            percent = int((current/total) * 100)

        self.progress.setValue(percent)