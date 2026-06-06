from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import Qt

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Запуск приложения")
        self.setWindowIcon(QIcon("images/logo.svg"))
        self.setFixedSize(600, 250)

        layout = QVBoxLayout()

        self.title = QLabel("Загрузка социального парсера")
        self.title.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Запуск")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()

        layout.addStretch()

        layout.addWidget(self.title)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress)

        layout.addStretch()

        self.setLayout(layout)

    def update_status(self, percent, text):
        self.progress.setValue(percent)

        self.status_label.setText(f"[{percent}%] {text}")