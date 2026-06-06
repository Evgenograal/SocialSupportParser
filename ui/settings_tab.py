from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QListWidget,
    QTabWidget,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QMessageBox,
    QInputDialog,
    QFileDialog
)

import json
import shutil

from data.settings_manager import load_settings, save_settings

from core.settings import reload_settings
from core.api_checker import check_api_key

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

        self.settings = load_settings()

        self.load_settings_to_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        self.create_ai_tab()
        self.create_api_tab()
        self.create_reference_tab()
        self.create_prompt_tab()
        self.create_service_tab()

        layout.addWidget(self.tabs)

        save_btn = QPushButton("Сохранить настройки")
        save_btn.clicked.connect(self.save_all_settings)

        layout.addWidget(save_btn)

        self.setLayout(layout)

    # AI

    def create_ai_tab(self):

        tab = QWidget()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Модель"))

        self.model_combo = QComboBox()

        self.model_combo.addItems([
            "openai/gpt-oss-120b",
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ])

        layout.addWidget(self.model_combo)

        layout.addWidget(QLabel("Base URL"))

        self.base_url_edit = QLineEdit()

        layout.addWidget(self.base_url_edit)

        layout.addWidget(QLabel("Max Retries"))

        self.retries_spin = QSpinBox()

        self.retries_spin.setRange(1, 100)

        layout.addWidget(self.retries_spin)

        layout.addWidget(QLabel("Max Workers"))

        self.workers_spin = QSpinBox()

        self.workers_spin.setRange(1, 100)

        layout.addWidget(self.workers_spin)

        layout.addWidget(QLabel("Request Delay"))

        self.delay_spin = QDoubleSpinBox()

        self.delay_spin.setDecimals(2)

        self.delay_spin.setRange(0, 60)

        layout.addWidget(self.delay_spin)

        layout.addStretch()

        tab.setLayout(layout)

        self.tabs.addTab(tab, "Нейросеть")








    # API

    def create_api_tab(self):
        tab = QWidget()

        layout = QVBoxLayout()

        self.api_list = QListWidget()
        layout.addWidget(self.api_list)

        row = QHBoxLayout()

        btn_add = QPushButton("Добавить")
        btn_remove = QPushButton("Удалить")

        btn_add.clicked.connect(self.add_api_key)
        btn_remove.clicked.connect(self.remove_api_key)

        row.addWidget(btn_add)
        row.addWidget(btn_remove)

        layout.addLayout(row)

        tab.setLayout(layout)

        self.tabs.addTab(tab, "API ключи")

    def add_api_key(self):
        text, ok = QInputDialog.getText(self, "API ключ", "Введите ключ")

        if ok and text:
            self.api_list.addItem(text)

    def remove_api_key(self):
        item = self.api_list.currentRow()

        if item >= 0:
            self.api_list.takeItem(item)








    # References

    def create_reference_tab(self):
        tab = QWidget()

        layout = QVBoxLayout()

        self.reference_tab = QTabWidget()

        self.categories_list = QListWidget()
        self.life_list = QListWidget()
        self.family_list = QListWidget()
        self.territories_list = QListWidget()

        self.reference_tab.addTab(self.categories_list, "Категории")
        self.reference_tab.addTab(self.life_list, "Жизненные ситуации")
        self.reference_tab.addTab(self.family_list, "Семейные статусы")
        self.reference_tab.addTab(self.territories_list, "Территории")

        layout.addWidget(self.reference_tab)

        row = QHBoxLayout()

        btn_add = QPushButton("Добавить")
        btn_remove = QPushButton("Удалить")

        btn_add.clicked.connect(self.add_reference)
        btn_remove.clicked.connect(self.remove_reference)

        row.addWidget(btn_add)
        row.addWidget(btn_remove)

        layout.addLayout(row)

        tab.setLayout(layout)

        self.tabs.addTab(tab, "Справочники")

    def current_reference_widget(self):
        return self.reference_tab.currentWidget()

    def add_reference(self):
        text, ok = QInputDialog.getText(self, "Добавить", "Введите значение")

        if ok and text:
            self.current_reference_widget().addItem(text)

    def remove_reference(self):
        widget = self.current_reference_widget()

        row = widget.currentRow()

        if row >= 0:
            widget.takeItem(row)







        
    # Prompt

    def create_prompt_tab(self):
        tab = QWidget()

        layout = QVBoxLayout()

        self.prompt_edit = QTextEdit()

        layout.addWidget(self.prompt_edit)

        tab.setLayout(layout)

        self.tabs.addTab(tab, "Промпт")


    # Load
    def load_settings_to_ui(self):
        self.model_combo.setCurrentText(self.settings["model"])

        self.base_url_edit.setText(self.settings["base_url"])

        self.retries_spin.setValue(self.settings["max_retries"])

        self.workers_spin.setValue(self.settings["max_workers"])

        self.delay_spin.setValue(self.settings["request_delay"])

        self.api_list.clear()

        for item in self.settings["api_keys"]:
            self.api_list.addItem(item)

        self.load_list(self.categories_list, self.settings["categories"])

        self.load_list(self.life_list, self.settings["life_situations"])

        self.load_list(self.family_list, self.settings["family_statuses"])

        self.load_list(self.territories_list, self.settings["territories"])

        self.prompt_edit.setPlainText(self.settings["prompt_template"])

    def load_list(self, widget, data):
        widget.clear()

        for item in data:
            widget.addItem(item)








    # Save

    def widget_to_list(self, widget):
        result = []

        for i in range (widget.count()):
            result.append(widget.item(i).text())

        return result

    def save_all_settings(self):
        self.settings["model"] = self.model_combo.currentText()

        self.settings["base_url"] = self.base_url_edit.text()

        self.settings["api_keys"] = self.widget_to_list(self.api_list)

        self.settings["max_retries"] = self.retries_spin.value()

        self.settings["max_workers"] = self.workers_spin.value()

        self.settings["request_delay"] = self.delay_spin.value()

        self.settings["categories"] = self.widget_to_list(self.categories_list)

        self.settings["life_situations"] = self.widget_to_list(self.life_list)

        self.settings["family_statuses"] = self.widget_to_list(self.family_list)

        self.settings["territories"] = self.widget_to_list(self.territories_list)

        self.settings["prompt_template"] = self.prompt_edit.toPlainText()

        save_settings(self.settings)

        reload_settings()

        QMessageBox.information(self, "Успех", "Настройки применены")








    # Сервисная вкладка

    def create_service_tab(self):
        tab = QWidget()

        layout = QVBoxLayout()

        btn_export = QPushButton("Экспорт настроек")
        btn_import = QPushButton("Импорт настроек")
        btn_reset = QPushButton("Сбросить настройки")
        btn_restore_prompt = QPushButton("Восстановить стандартный промпт")
        btn_check_api = QPushButton("Проверь API ключи")

        btn_export.clicked.connect(self.export_settings)
        btn_import.clicked.connect(self.import_settings)
        btn_reset.clicked.connect(self.reset_settings)
        btn_restore_prompt.clicked.connect(self.restore_default_prompt)
        btn_check_api.clicked.connect(self.check_api_keys)

        layout.addWidget(btn_export)
        layout.addWidget(btn_import)
        layout.addWidget(btn_reset)
        layout.addWidget(btn_restore_prompt)
        layout.addWidget(btn_check_api)

        layout.addStretch()

        tab.setLayout(layout)

        self.tabs.addTab(tab, "Сервис")

    def export_settings(self):
        path, _ = QFileDialog.getSaveFileName(self, "Экспорт настроек",
                                              "settings_backup.json", "JSON (*json)")

        if not path:
            return

        shutil.copy("data/settings.json", path)

        QMessageBox.information(self, "Успех", "Настройки экспортированы")

    def import_settings(self):
        path, _ = QFileDialog.getOpenFileName(self, "Импорт настроек",
                                              "", "JSON (*.json)")

        if not path:
            return

        try:
            with open(path, "r", encoding = "utf-8") as f:
                data = json.load(f)

            save_settings(data)
            self.settings = load_settings()
            self.load_settings_to_ui()
            reload_settings()

            QMessageBox.information(self, "Успех", "Настройки импортированы")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def reset_settings(self):
        result = QMessageBox.question(self, "Подтверждение", "Сбросить все настройки")

        if result != QMessageBox.Yes:
            result

        with open("data/default_settings.json", "r", encoding = "utf-8") as f:
            data = json.load(f)

        save_settings(data)
        self.settings = load_settings()
        self.load_settings_to_ui()
        reload_settings()

        QMessageBox.information(self, "Готово", "Настройки сброшены")

    def restore_default_prompt(self):
        with open("data/default_prompt.txt", "r", encoding = "utf-8") as f:
            self.prompt_edit.setPlainText(f.read())

        QMessageBox.information(self, "Успех", "Промпт восстановлен")

    def check_api_keys(self):
        good = 0
        bad = 0

        model = self.model_combo.currentText()
        base_url = self.base_url_edit.text()

        for i in range(self.api_list.count()):
            key = self.api_list.item(i).text()

            if check_api_key(key, base_url, model):
                good += 1

            else:
                bad += 1

        QMessageBox.information(self, "Проверка завершена", f"Действиющих ключей: {good}\nНерабочих: {bad}")