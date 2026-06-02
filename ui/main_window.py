from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon

from ui.process_tab import ProcessTab
from ui.retry_tab import RetryTab
from ui.merge_tab import MergeTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Социальный парсер")

        self.setWindowIcon(QIcon("images/logo.svg"))

        self.resize(1000, 800)

        tabs = QTabWidget()

        tabs.addTab(ProcessTab(), "Обработка")

        tabs.addTab(RetryTab(), "Повторная обработка")

        tabs.addTab(MergeTab(), "Объединение JSON с MD")

        self.setCentralWidget(tabs)