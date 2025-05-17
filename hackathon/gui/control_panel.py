from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QDoubleSpinBox, 
    QComboBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor


class ControlPanel(QWidget):
    simulation_started = pyqtSignal(float, float, str)
    simulation_stopped = pyqtSignal()
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QFormLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.dose_input = QDoubleSpinBox()
        self.dose_input.setRange(0.1, 10.0)
        self.dose_input.setValue(1.0)

        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(10, 150)
        self.weight_input.setValue(70)

        self.seed_combo = QComboBox()
        self.seed_combo.addItems(["Разжёвана", "Целая"])

        buttons_layout = QHBoxLayout()
        
        self.start_stop_btn = QPushButton("Начать визуализацию")
        self.start_stop_btn.setStyleSheet("padding: 5px; background: #ddffdd;")
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setStyleSheet("padding: 5px; background: #ffdddd;")
        self.cancel_btn.setEnabled(False)

        buttons_layout.addWidget(self.start_stop_btn)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addRow("Амигдалин (мг):", self.dose_input)
        layout.addRow("Масса тела (кг):", self.weight_input)
        layout.addRow("Состояние:", self.seed_combo)
        layout.addRow(buttons_layout)

        self.start_stop_btn.clicked.connect(self.toggle_simulation)
        self.cancel_btn.clicked.connect(self.cancel_simulation)

        self.is_running = False

    def toggle_simulation(self):
        if not self.is_running:
            self.start_simulation()
        else:
            self.stop_simulation()

    def start_simulation(self):
        self.is_running = True
        self.start_stop_btn.setText("Стоп")
        self.start_stop_btn.setStyleSheet("padding: 5px; background: #ffdddd;")
        self.cancel_btn.setEnabled(False)
        self.simulation_started.emit(
            self.dose_input.value(),
            self.weight_input.value(),
            self.seed_combo.currentText()
        )

    def stop_simulation(self):
        self.is_running = False
        self.start_stop_btn.setText("Начать визуализацию")
        self.start_stop_btn.setStyleSheet("padding: 5px; background: #ddffdd;")
        self.cancel_btn.setEnabled(True)
        self.simulation_stopped.emit()

    def cancel_simulation(self):
        self.clear_requested.emit()
        self.reset_controls()

    def reset_controls(self):
        self.is_running = False
        self.start_stop_btn.setText("Начать визуализацию")
        self.start_stop_btn.setStyleSheet("padding: 5px; background: #ddffdd;")
        self.cancel_btn.setEnabled(False)
