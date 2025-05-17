from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QSplitter)
from PyQt6.QtCore import Qt
from .organism_view import OrganismView
from .control_panel import ControlPanel
from .event_log import EventLog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.setWindowTitle("Модель отравления синильной кислотой")
        self.setGeometry(100, 100, 1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        self.organism_view = OrganismView()
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        
        self.control_panel = ControlPanel()
        self.event_log = EventLog()
        
        right_layout.addWidget(self.control_panel)
        right_layout.addWidget(QLabel("Ход процесса:"))
        right_layout.addWidget(self.event_log, 1)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.organism_view)
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 300])
        
        main_layout.addWidget(splitter)

    def connect_signals(self):
        self.control_panel.simulation_started.connect(
            self.organism_view.start_simulation)
        self.control_panel.simulation_stopped.connect(
            self.organism_view.stop_simulation)
        self.control_panel.clear_requested.connect(
            self.clear_all)
        self.organism_view.event_occurred.connect(
            self.event_log.add_event)

    def clear_all(self):
        if self.organism_view.is_running:
            self.event_log.add_error("Нельзя очистить во время визуализации процесса!")
            return
            
        self.event_log.clear_events()
        self.organism_view.reset()
        self.control_panel.reset_controls()