from PyQt5.QtWidgets import QApplication
from ui.loading_screen import LoadingScreen
import sys
import qdarktheme

def progress_events(app):
    app.processEvents()

def main():
    app = QApplication(sys.argv)
    stylesheet = qdarktheme.load_stylesheet(theme="dark")
    app.setStyleSheet(stylesheet)

    splash = LoadingScreen()
    splash.show()

    app.processEvents()

    splash.update_status(10, "Загрузка настроек")
    progress_events(app)
    from data.settings_manager import load_settings
    settings = load_settings()

    splash.update_status(20, "Проверка конфигурации")
    progress_events(app)
    required = [
        "model",
        "api_keys",
        "base_url"
    ]
    for key in required:
        if key not in settings:
            print(f"{key} - не работает")

    splash.update_status(35, "Инициализация обработчиков")
    progress_events(app)
    from core.settings import reload_settings
    reload_settings()

    splash.update_status(50, "Загрузка основной обработки")
    progress_events(app)
    from ui.process_tab import ProcessTab

    splash.update_status(65, "Загрузка повторной обработки")
    progress_events(app)
    from ui.retry_tab import RetryTab

    splash.update_status(75, "Загрузка объединения файлов")
    progress_events(app)
    from ui.merge_tab import MergeTab

    splash.update_status(85, "Загрузка визуализатора json")
    progress_events(app)
    from ui.json_viewer_tab import LoadJsonTab

    splash.update_status(90, "Загрузка настроек")
    progress_events(app)
    from ui.settings_tab import SettingsTab

    splash.update_status(95, "Загрузка интерфейса")
    progress_events(app)
    from ui.main_window import MainWindow
    window = MainWindow()

    splash.update_status(100, "Запуск приложения")
    progress_events(app)
    splash.close()

    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()