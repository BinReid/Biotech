from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QSplitter)
from PyQt6.QtCore import Qt
from .organism_view import OrganismView
from .control_panel import ControlPanel
from .event_log import EventLog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("mainWindow")
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.setWindowTitle("Модель отравления синильной кислотой")
        self.setGeometry(100, 100, 1000, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Левая часть - визуализация организма
        self.organism_view = OrganismView()
        
        # Правая часть - управление и лог
        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        right_layout.setSpacing(10)
        
        # Панель управления
        self.control_panel = ControlPanel()
        
        # Лог событий
        log_label = QLabel("Ход процесса:")
        log_label.setObjectName("logLabel")
        self.event_log = EventLog()
        
        # Добавляем компоненты
        right_layout.addWidget(self.control_panel)
        right_layout.addWidget(log_label)
        right_layout.addWidget(self.event_log, 1)
        
        # Разделитель
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.organism_view)
        splitter.addWidget(right_panel)
        splitter.setSizes([650, 350])
        splitter.setHandleWidth(5)
        
        main_layout.addWidget(splitter)

    def connect_signals(self):
        # Подключение сигналов управления
        self.control_panel.simulation_started.connect(
            self.organism_view.start_simulation)
        self.control_panel.simulation_stopped.connect(
            self.organism_view.stop_simulation)
        self.control_panel.clear_requested.connect(
            self.clear_all)
        
        # Подключение сигналов лога
        self.organism_view.event_occurred.connect(
            self.event_log.add_event)
        self.organism_view.error_occurred.connect(
            self.event_log.add_error)

    def clear_all(self):
        if self.organism_view.is_running:
            self.event_log.add_error("Нельзя очистить во время визуализации!")
            return
            
        self.event_log.clear_events()
        self.organism_view.reset()
        self.control_panel.reset_controls()
        self.event_log.add_event("Система сброшена в начальное состояние")