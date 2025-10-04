import sys
import psutil
import time
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
    QPushButton, QTextEdit, QLabel, QStyleFactory, QTabWidget, QGridLayout,
    QScrollArea, QMenuBar, QMenu, QFileDialog, QMessageBox, QLineEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont, QPainter, QPen, QBrush
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.data = []
        self.max_points = 60

    def update_graph(self, value, label):
        self.data.append(value)
        if len(self.data) > self.max_points:
            self.data.pop(0)
        self.ax.clear()
        self.ax.plot(self.data, color='#005A9E', linewidth=2)
        self.ax.set_ylim(0, 100)
        self.ax.set_title(label, fontsize=12, color='#000000')
        self.ax.set_xlabel('Time (s)', fontsize=10, color='#000000')
        self.ax.set_ylabel('Usage (%)', fontsize=10, color='#000000')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.canvas.draw()

class SystemMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('icon.ico'))

        self.current_lang = 'en'
        self.current_theme = 'Windows11'
        self.history = []
        self.cpu_data = []
        self.ram_data = []
        self.disk_data = []
        self.max_data_points = 60
        self.warning_threshold = 80
        self.load_history()

        self.texts = {
            'en': {
                'title': 'System Monitor',
                'cpu_label': 'CPU Usage:',
                'ram_label': 'RAM Usage:',
                'disk_label': 'Disk Usage:',
                'refresh_label': 'Refresh Rate (ms):',
                'theme_label': 'Theme:',
                'language_label': 'Language:',
                'history_tab': 'History',
                'monitor_tab': 'System Monitor',
                'settings_tab': 'Settings',
                'clear_history': 'Clear History',
                'save_history': 'Save History to File',
                'status_idle': 'Monitoring system resources...',
                'status_updated': 'Updated: {time}',
                'status_warning': 'High {resource} usage: {value}% at {time}',
                'history_time': 'Time',
                'history_cpu': 'CPU (%)',
                'history_ram': 'RAM (%)',
                'history_disk': 'Disk (%)',
                'apply': 'Apply',
                'file_menu': 'File',
                'exit_action': 'Exit',
                'about': 'About',
                'about_text': 'System Monitor\nVersion 1.0\nDeveloped by Hamid Yarali\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'cpu_details': 'CPU Details:',
                'ram_details': 'RAM Details:',
                'disk_details': 'Disk Details:',
                'total': 'Total:',
                'used': 'Used:',
                'free': 'Free:',
                'percent': 'Percent:',
                'warning_threshold': 'Warning Threshold (%):'
            },
            'fa': {
                'title': 'مانیتور سیستم',
                'cpu_label': 'استفاده از CPU:',
                'ram_label': 'استفاده از RAM:',
                'disk_label': 'استفاده از دیسک:',
                'refresh_label': 'نرخ به‌روزرسانی (میلی‌ثانیه):',
                'theme_label': 'تم:',
                'language_label': 'زبان:',
                'history_tab': 'تاریخچه',
                'monitor_tab': 'مانیتور سیستم',
                'settings_tab': 'تنظیمات',
                'clear_history': 'پاک کردن تاریخچه',
                'save_history': 'ذخیره تاریخچه در فایل',
                'status_idle': 'نظارت بر منابع سیستم...',
                'status_updated': 'به‌روزرسانی شد: {time}',
                'status_warning': 'استفاده بالای {resource}: {value}% در {time}',
                'history_time': 'زمان',
                'history_cpu': 'CPU (%)',
                'history_ram': 'RAM (%)',
                'history_disk': 'دیسک (%)',
                'apply': 'اعمال',
                'file_menu': 'فایل',
                'exit_action': 'خروج',
                'about': 'درباره',
                'about_text': 'مانیتور سیستم\nنسخه ۱.۰\nتوسعه‌یافته توسط حمید یارعلی\nگیت‌هاب: https://github.com/HamidYaraliOfficial\nاینستاگرام: https://www.instagram.com/hamidyaraliofficial\nتلگرام: @Hamid_Yarali',
                'cpu_details': 'جزئیات CPU:',
                'ram_details': 'جزئیات RAM:',
                'disk_details': 'جزئیات دیسک:',
                'total': 'کل:',
                'used': 'استفاده‌شده:',
                'free': 'آزاد:',
                'percent': 'درصد:',
                'warning_threshold': 'آستانه هشدار (%):'
            },
            'zh': {
                'title': '系统监控器',
                'cpu_label': 'CPU使用率：',
                'ram_label': '内存使用率：',
                'disk_label': '磁盘使用率：',
                'refresh_label': '刷新率（毫秒）：',
                'theme_label': '主题：',
                'language_label': '语言：',
                'history_tab': '历史记录',
                'monitor_tab': '系统监控',
                'settings_tab': '设置',
                'clear_history': '清除历史记录',
                'save_history': '将历史记录保存到文件',
                'status_idle': '正在监控系统资源...',
                'status_updated': '已更新：{time}',
                'status_warning': '高{resource}使用率：{value}% 在 {time}',
                'history_time': '时间',
                'history_cpu': 'CPU (%)',
                'history_ram': '内存 (%)',
                'history_disk': '磁盘 (%)',
                'apply': '应用',
                'file_menu': '文件',
                'exit_action': '退出',
                'about': '关于',
                'about_text': '系统监控器\n版本 1.0\n由 Hamid Yarali 开发\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'cpu_details': 'CPU详情：',
                'ram_details': '内存详情：',
                'disk_details': '磁盘详情：',
                'total': '总量：',
                'used': '已使用：',
                'free': '可用：',
                'percent': '百分比：',
                'warning_threshold': '警告阈值 (%):'
            },
            'ru': {
                'title': 'Системный монитор',
                'cpu_label': 'Использование ЦП:',
                'ram_label': 'Использование ОЗУ:',
                'disk_label': 'Использование диска:',
                'refresh_label': 'Частота обновления (мс):',
                'theme_label': 'Тема:',
                'language_label': 'Язык:',
                'history_tab': 'История',
                'monitor_tab': 'Системный монитор',
                'settings_tab': 'Настройки',
                'clear_history': 'Очистить историю',
                'save_history': 'Сохранить историю в файл',
                'status_idle': 'Мониторинг системных ресурсов...',
                'status_updated': 'Обновлено: {time}',
                'status_warning': 'Высокое использование {resource}: {value}% в {time}',
                'history_time': 'Время',
                'history_cpu': 'ЦП (%)',
                'history_ram': 'ОЗУ (%)',
                'history_disk': 'Диск (%)',
                'apply': 'Применить',
                'file_menu': 'Файл',
                'exit_action': 'Выход',
                'about': 'О программе',
                'about_text': 'Системный монитор\nВерсия 1.0\nРазработано Hamid Yarali\nGitHub: https://github.com/HamidYaraliOfficial\nInstagram: https://www.instagram.com/hamidyaraliofficial\nTelegram: @Hamid_Yarali',
                'cpu_details': 'Подробности ЦП:',
                'ram_details': 'Подробности ОЗУ:',
                'disk_details': 'Подробности диска:',
                'total': 'Всего:',
                'used': 'Использовано:',
                'free': 'Свободно:',
                'percent': 'Процент:',
                'warning_threshold': 'Порог предупреждения (%):'
            }
        }

        self.themes = {
            'Windows11': {
                'background': QColor(243, 243, 243),
                'text': QColor(0, 0, 0),
                'button': QColor(225, 225, 225),
                'button_text': QColor(0, 0, 0),
                'button_hover': QColor(200, 200, 200),
                'accent': QColor(0, 90, 158),
                'border': QColor(180, 180, 180),
                'header': QColor(230, 230, 230),
                'progress': QColor(0, 90, 158),
                'warning': QColor(255, 204, 204)
            },
            'Dark': {
                'background': QColor(32, 32, 32),
                'text': QColor(230, 230, 230),
                'button': QColor(50, 50, 50),
                'button_text': QColor(230, 230, 230),
                'button_hover': QColor(70, 70, 70),
                'accent': QColor(0, 120, 212),
                'border': QColor(80, 80, 80),
                'header': QColor(40, 40, 40),
                'progress': QColor(0, 120, 212),
                'warning': QColor(100, 50, 50)
            },
            'Light': {
                'background': QColor(255, 255, 255),
                'text': QColor(0, 0, 0),
                'button': QColor(240, 240, 240),
                'button_text': QColor(0, 0, 0),
                'button_hover': QColor(220, 220, 220),
                'accent': QColor(0, 120, 212),
                'border': QColor(200, 200, 200),
                'header': QColor(245, 245, 245),
                'progress': QColor(0, 120, 212),
                'warning': QColor(255, 204, 204)
            },
            'Red': {
                'background': QColor(255, 235, 235),
                'text': QColor(80, 0, 0),
                'button': QColor(255, 200, 200),
                'button_text': QColor(80, 0, 0),
                'button_hover': QColor(255, 180, 180),
                'accent': QColor(200, 0, 0),
                'border': QColor(220, 150, 150),
                'header': QColor(255, 220, 220),
                'progress': QColor(200, 0, 0),
                'warning': QColor(255, 150, 150)
            },
            'Blue': {
                'background': QColor(235, 245, 255),
                'text': QColor(0, 0, 80),
                'button': QColor(200, 220, 255),
                'button_text': QColor(0, 0, 80),
                'button_hover': QColor(180, 200, 255),
                'accent': QColor(0, 0, 200),
                'border': QColor(150, 180, 220),
                'header': QColor(220, 235, 255),
                'progress': QColor(0, 0, 200),
                'warning': QColor(150, 200, 255)
            }
        }

        self.init_ui()
        self.apply_theme(self.current_theme)
        self.update_texts()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_monitor)
        self.timer.start(1000)

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.menu_bar = QMenuBar()
        self.file_menu = QMenu(self.texts['en']['file_menu'])
        self.exit_action = self.file_menu.addAction(self.texts['en']['exit_action'])
        self.exit_action.triggered.connect(self.close)
        self.about_action = self.file_menu.addAction(self.texts['en']['about'])
        self.about_action.triggered.connect(self.show_about)
        self.menu_bar.addMenu(self.file_menu)
        self.main_layout.addWidget(self.menu_bar)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.95);
            }
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                background: rgba(0, 0, 0, 0.05);
                color: black;
            }
            QTabBar::tab:selected {
                background: rgba(0, 90, 158, 0.3);
                font-weight: bold;
                color: black;
            }
        """)
        self.main_layout.addWidget(self.tabs)

        self.monitor_tab = QWidget()
        self.monitor_layout = QVBoxLayout(self.monitor_tab)
        self.monitor_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.monitor_layout.setSpacing(10)

        self.cpu_label = QLabel()
        self.cpu_label.setFont(QFont("Segoe UI", 12))
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setFixedHeight(40)
        self.cpu_progress.setStyleSheet("""
            QProgressBar {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QProgressBar::chunk {
                background-color: #005A9E;
                border-radius: 6px;
            }
        """)
        self.cpu_graph = GraphWidget()
        self.cpu_details = QTextEdit()
        self.cpu_details.setReadOnly(True)
        self.cpu_details.setFixedHeight(100)
        self.cpu_details.setStyleSheet("""
            QTextEdit {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)

        self.ram_label = QLabel()
        self.ram_label.setFont(QFont("Segoe UI", 12))
        self.ram_progress = QProgressBar()
        self.ram_progress.setFixedHeight(40)
        self.ram_progress.setStyleSheet("""
            QProgressBar {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QProgressBar::chunk {
                background-color: #005A9E;
                border-radius: 6px;
            }
        """)
        self.ram_graph = GraphWidget()
        self.ram_details = QTextEdit()
        self.ram_details.setReadOnly(True)
        self.ram_details.setFixedHeight(100)
        self.ram_details.setStyleSheet("""
            QTextEdit {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)

        self.disk_label = QLabel()
        self.disk_label.setFont(QFont("Segoe UI", 12))
        self.disk_progress = QProgressBar()
        self.disk_progress.setFixedHeight(40)
        self.disk_progress.setStyleSheet("""
            QProgressBar {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QProgressBar::chunk {
                background-color: #005A9E;
                border-radius: 6px;
            }
        """)
        self.disk_graph = GraphWidget()
        self.disk_details = QTextEdit()
        self.disk_details.setReadOnly(True)
        self.disk_details.setFixedHeight(100)
        self.disk_details.setStyleSheet("""
            QTextEdit {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setFixedHeight(100)
        self.status_text.setStyleSheet("""
            QTextEdit {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)

        self.monitor_layout.addWidget(self.cpu_label)
        self.monitor_layout.addWidget(self.cpu_progress)
        self.monitor_layout.addWidget(self.cpu_graph)
        self.monitor_layout.addWidget(self.cpu_details)
        self.monitor_layout.addWidget(self.ram_label)
        self.monitor_layout.addWidget(self.ram_progress)
        self.monitor_layout.addWidget(self.ram_graph)
        self.monitor_layout.addWidget(self.ram_details)
        self.monitor_layout.addWidget(self.disk_label)
        self.monitor_layout.addWidget(self.disk_progress)
        self.monitor_layout.addWidget(self.disk_graph)
        self.monitor_layout.addWidget(self.disk_details)
        self.monitor_layout.addWidget(self.status_text)

        self.history_tab = QWidget()
        self.history_layout = QVBoxLayout(self.history_tab)
        self.history_scroll = QScrollArea()
        self.history_scroll.setWidgetResizable(True)
        self.history_content = QWidget()
        self.history_grid = QGridLayout(self.history_content)
        self.history_grid.setSpacing(10)
        self.history_scroll.setWidget(self.history_content)
        self.history_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.95);
            }
        """)
        self.clear_history_btn = QPushButton()
        self.clear_history_btn.setFixedHeight(40)
        self.clear_history_btn.setFont(QFont("Segoe UI", 12))
        self.clear_history_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(200, 0, 0, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(200, 0, 0, 1.0);
            }
        """)
        self.clear_history_btn.clicked.connect(self.clear_history)
        self.save_history_btn = QPushButton()
        self.save_history_btn.setFixedHeight(40)
        self.save_history_btn.setFont(QFont("Segoe UI", 12))
        self.save_history_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.save_history_btn.clicked.connect(self.save_history_to_file)
        self.history_layout.addWidget(self.history_scroll)
        self.history_layout.addWidget(self.clear_history_btn)
        self.history_layout.addWidget(self.save_history_btn)

        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.settings_layout.setSpacing(10)

        self.language_label = QLabel()
        self.language_label.setFont(QFont("Segoe UI", 12))
        self.language_combo = QComboBox()
        self.language_combo.addItems(['English', 'فارسی', '中文', 'Русский'])
        self.language_combo.setFixedHeight(40)
        self.language_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.theme_label = QLabel()
        self.theme_label.setFont(QFont("Segoe UI", 12))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Windows11', 'Dark', 'Light', 'Red', 'Blue'])
        self.theme_combo.setFixedHeight(40)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        self.refresh_label = QLabel()
        self.refresh_label.setFont(QFont("Segoe UI", 12))
        self.refresh_input = QLineEdit("1000")
        self.refresh_input.setFixedHeight(40)
        self.refresh_input.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)

        self.warning_label = QLabel()
        self.warning_label.setFont(QFont("Segoe UI", 12))
        self.warning_input = QLineEdit(str(self.warning_threshold))
        self.warning_input.setFixedHeight(40)
        self.warning_input.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }
        """)

        self.apply_btn = QPushButton()
        self.apply_btn.setFixedHeight(40)
        self.apply_btn.setFont(QFont("Segoe UI", 12))
        self.apply_btn.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(0, 90, 158, 0.8);
                color: white;
            }
            QPushButton:hover {
                background: rgba(0, 90, 158, 1.0);
            }
        """)
        self.apply_btn.clicked.connect(self.apply_settings)

        self.settings_layout.addWidget(self.language_label)
        self.settings_layout.addWidget(self.language_combo)
        self.settings_layout.addWidget(self.theme_label)
        self.settings_layout.addWidget(self.theme_combo)
        self.settings_layout.addWidget(self.refresh_label)
        self.settings_layout.addWidget(self.refresh_input)
        self.settings_layout.addWidget(self.warning_label)
        self.settings_layout.addWidget(self.warning_input)
        self.settings_layout.addWidget(self.apply_btn)
        self.settings_layout.addStretch()

        self.tabs.addTab(self.monitor_tab, self.texts['en']['monitor_tab'])
        self.tabs.addTab(self.history_tab, self.texts['en']['history_tab'])
        self.tabs.addTab(self.settings_tab, self.texts['en']['settings_tab'])

        self.update_monitor()
        self.update_history_ui()

    def apply_theme(self, theme_name):
        palette = QPalette()
        theme = self.themes.get(theme_name, self.themes['Windows11'])
        palette.setColor(QPalette.ColorRole.Window, theme['background'])
        palette.setColor(QPalette.ColorRole.WindowText, theme['text'])
        palette.setColor(QPalette.ColorRole.Button, theme['button'])
        palette.setColor(QPalette.ColorRole.ButtonText, theme['button_text'])
        palette.setColor(QPalette.ColorRole.Highlight, theme['accent'])
        palette.setColor(QPalette.ColorRole.Base, theme['background'])
        palette.setColor(QPalette.ColorRole.AlternateBase, theme['header'])
        palette.setColor(QPalette.ColorRole.Text, theme['text'])
        self.setPalette(palette)
        self.setStyle(QStyleFactory.create('WindowsVista' if theme_name == 'Windows11' else 'Fusion'))
        self.cpu_progress.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }}
            QProgressBar::chunk {{
                background-color: {theme['progress'].name()};
                border-radius: 6px;
            }}
        """)
        self.ram_progress.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }}
            QProgressBar::chunk {{
                background-color: {theme['progress'].name()};
                border-radius: 6px;
            }}
        """)
        self.disk_progress.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid rgba(0, 0, 0, 0.2);
                background: rgba(255, 255, 255, 0.95);
                color: black;
            }}
            QProgressBar::chunk {{
                background-color: {theme['progress'].name()};
                border-radius: 6px;
            }}
        """)
        self.cpu_details.setStyleSheet(f"""
            QTextEdit {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)
        self.ram_details.setStyleSheet(f"""
            QTextEdit {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)
        self.disk_details.setStyleSheet(f"""
            QTextEdit {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)
        self.status_text.setStyleSheet(f"""
            QTextEdit {{
                border-radius: 8px;
                font-size: 14px;
                border: 1px solid {theme['border'].name()};
                background: {theme['background'].name()};
                color: {theme['text'].name()};
            }}
        """)

    def update_texts(self):
        lang = self.current_lang
        self.setWindowTitle(self.texts[lang]['title'])
        self.cpu_label.setText(self.texts[lang]['cpu_label'])
        self.ram_label.setText(self.texts[lang]['ram_label'])
        self.disk_label.setText(self.texts[lang]['disk_label'])
        self.refresh_label.setText(self.texts[lang]['refresh_label'])
        self.theme_label.setText(self.texts[lang]['theme_label'])
        self.language_label.setText(self.texts[lang]['language_label'])
        self.clear_history_btn.setText(self.texts[lang]['clear_history'])
        self.save_history_btn.setText(self.texts[lang]['save_history'])
        self.apply_btn.setText(self.texts[lang]['apply'])
        self.status_text.setText(self.texts[lang]['status_idle'])
        self.warning_label.setText(self.texts[lang]['warning_threshold'])
        self.file_menu.setTitle(self.texts[lang]['file_menu'])
        self.exit_action.setText(self.texts[lang]['exit_action'])
        self.about_action.setText(self.texts[lang]['about'])

        self.tabs.setTabText(0, self.texts[lang]['monitor_tab'])
        self.tabs.setTabText(1, self.texts[lang]['history_tab'])
        self.tabs.setTabText(2, self.texts[lang]['settings_tab'])

        alignment = Qt.AlignmentFlag.AlignRight if lang == 'fa' else Qt.AlignmentFlag.AlignLeft
        self.cpu_label.setAlignment(alignment)
        self.ram_label.setAlignment(alignment)
        self.disk_label.setAlignment(alignment)
        self.refresh_label.setAlignment(alignment)
        self.theme_label.setAlignment(alignment)
        self.language_label.setAlignment(alignment)
        self.warning_label.setAlignment(alignment)
        self.cpu_details.setAlignment(alignment)
        self.ram_details.setAlignment(alignment)
        self.disk_details.setAlignment(alignment)
        self.status_text.setAlignment(alignment)

        self.update_monitor()
        self.update_history_ui()

    def change_language(self, index):
        langs = ['en', 'fa', 'zh', 'ru']
        self.current_lang = langs[index]
        self.update_texts()

    def change_theme(self, index):
        themes = ['Windows11', 'Dark', 'Light', 'Red', 'Blue']
        self.current_theme = themes[index]
        self.apply_theme(self.current_theme)

    def apply_settings(self):
        try:
            refresh_rate = int(self.refresh_input.text())
            self.timer.setInterval(max(100, refresh_rate))
        except ValueError:
            self.refresh_input.setText("1000")
            self.timer.setInterval(1000)
        try:
            self.warning_threshold = int(self.warning_input.text())
        except ValueError:
            self.warning_threshold = 80
            self.warning_input.setText("80")
        self.update_texts()
        self.apply_theme(self.current_theme)
        self.update_monitor()

    def show_about(self):
        QMessageBox.information(self, self.texts[self.current_lang]['about'], 
                               self.texts[self.current_lang]['about_text'])

    def update_monitor(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        self.cpu_progress.setValue(int(cpu_usage))
        self.ram_progress.setValue(int(ram.percent))
        self.disk_progress.setValue(int(disk.percent))

        self.cpu_graph.update_graph(cpu_usage, self.texts[self.current_lang]['cpu_label'])
        self.ram_graph.update_graph(ram.percent, self.texts[self.current_lang]['ram_label'])
        self.disk_graph.update_graph(disk.percent, self.texts[self.current_lang]['disk_label'])

        cpu_details = (
            f"{self.texts[self.current_lang]['cpu_details']}\n"
            f"{self.texts[self.current_lang]['percent']} {cpu_usage:.1f}%\n"
            f"Logical CPUs: {psutil.cpu_count(logical=True)}\n"
            f"Physical CPUs: {psutil.cpu_count(logical=False)}"
        )
        ram_details = (
            f"{self.texts[self.current_lang]['ram_details']}\n"
            f"{self.texts[self.current_lang]['total']} {ram.total / (1024**3):.2f} GB\n"
            f"{self.texts[self.current_lang]['used']} {ram.used / (1024**3):.2f} GB\n"
            f"{self.texts[self.current_lang]['free']} {ram.free / (1024**3):.2f} GB\n"
            f"{self.texts[self.current_lang]['percent']} {ram.percent:.1f}%"
        )
        disk_details = (
            f"{self.texts[self.current_lang]['disk_details']}\n"
            f"{self.texts[self.current_lang]['total']} {disk.total / (1024**3):.2f} GB\n"
            f"{self.texts[self.current_lang]['used']} {disk.used / (1024**3):.2f} GB\n"
            f"{self.texts[self.current_lang]['free']} {disk.free / (1024**3):.2f} GB\n"
            f"{self.texts[self.current_lang]['percent']} {disk.percent:.1f}%"
        )

        self.cpu_details.setText(cpu_details)
        self.ram_details.setText(ram_details)
        self.disk_details.setText(disk_details)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_text.setText(self.texts[self.current_lang]['status_updated'].format(time=timestamp))

        if cpu_usage > self.warning_threshold:
            self.status_text.setText(self.texts[self.current_lang]['status_warning'].format(
                resource='CPU', value=cpu_usage, time=timestamp))
            self.cpu_progress.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    font-size: 14px;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.95);
                    color: black;
                }}
                QProgressBar::chunk {{
                    background-color: {self.themes[self.current_theme]['warning'].name()};
                    border-radius: 6px;
                }}
            """)
        else:
            self.cpu_progress.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    font-size: 14px;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.95);
                    color: black;
                }}
                QProgressBar::chunk {{
                    background-color: {self.themes[self.current_theme]['progress'].name()};
                    border-radius: 6px;
                }}
            """)

        if ram.percent > self.warning_threshold:
            self.status_text.setText(self.texts[self.current_lang]['status_warning'].format(
                resource='RAM', value=ram.percent, time=timestamp))
            self.ram_progress.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    font-size: 14px;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.95);
                    color: black;
                }}
                QProgressBar::chunk {{
                    background-color: {self.themes[self.current_theme]['warning'].name()};
                    border-radius: 6px;
                }}
            """)
        else:
            self.ram_progress.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    font-size: 14px;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.95);
                    color: black;
                }}
                QProgressBar::chunk {{
                    background-color: {self.themes[self.current_theme]['progress'].name()};
                    border-radius: 6px;
                }}
            """)

        if disk.percent > self.warning_threshold:
            self.status_text.setText(self.texts[self.current_lang]['status_warning'].format(
                resource='Disk', value=disk.percent, time=timestamp))
            self.disk_progress.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    font-size: 14px;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.95);
                    color: black;
                }}
                QProgressBar::chunk {{
                    background-color: {self.themes[self.current_theme]['warning'].name()};
                    border-radius: 6px;
                }}
            """)
        else:
            self.disk_progress.setStyleSheet(f"""
                QProgressBar {{
                    border-radius: 8px;
                    font-size: 14px;
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background: rgba(255, 255, 255, 0.95);
                    color: black;
                }}
                QProgressBar::chunk {{
                    background-color: {self.themes[self.current_theme]['progress'].name()};
                    border-radius: 6px;
                }}
            """)

        self.history.append({
            'time': timestamp,
            'cpu': cpu_usage,
            'ram': ram.percent,
            'disk': disk.percent
        })
        if len(self.history) > 1000:
            self.history.pop(0)
        self.save_history()
        self.update_history_ui()

    def save_history(self):
        with open('system_monitor_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        try:
            with open('system_monitor_history.json', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save_history_to_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, self.texts[self.current_lang]['save_history'], "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
            self.status_text.setText(self.texts[self.current_lang]['status_updated'].format(time="History saved to file"))

    def update_history_ui(self):
        for i in reversed(range(self.history_grid.count())):
            self.history_grid.itemAt(i).widget().setParent(None)

        headers = [
            self.texts[self.current_lang]['history_time'],
            self.texts[self.current_lang]['history_cpu'],
            self.texts[self.current_lang]['history_ram'],
            self.texts[self.current_lang]['history_disk']
        ]
        for col, header in enumerate(headers):
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; color: black;")
            label.setAlignment(Qt.AlignmentFlag.AlignRight if self.current_lang == 'fa' else Qt.AlignmentFlag.AlignLeft)
            self.history_grid.addWidget(label, 0, col)

        for row, item in enumerate(self.history[-50:], 1):
            time_label = QLabel(item['time'])
            cpu_label = QLabel(f"{item['cpu']:.1f}%")
            ram_label = QLabel(f"{item['ram']:.1f}%")
            disk_label = QLabel(f"{item['disk']:.1f}%")
            
            for label in [time_label, cpu_label, ram_label, disk_label]:
                label.setStyleSheet("font-size: 12px; padding: 5px; border-bottom: 1px solid rgba(0, 0, 0, 0.1); color: black;")
                label.setWordWrap(True)
                label.setAlignment(Qt.AlignmentFlag.AlignRight if self.current_lang == 'fa' else Qt.AlignmentFlag.AlignLeft)
            
            self.history_grid.addWidget(time_label, row, 0)
            self.history_grid.addWidget(cpu_label, row, 1)
            self.history_grid.addWidget(ram_label, row, 2)
            self.history_grid.addWidget(disk_label, row, 3)

    def clear_history(self):
        self.history = []
        self.save_history()
        self.update_history_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    window = SystemMonitorApp()
    window.show()
    sys.exit(app.exec())