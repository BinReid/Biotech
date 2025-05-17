from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QDoubleSpinBox, 
    QComboBox, QPushButton, QHBoxLayout,
    QLabel, QGroupBox
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont


class ControlPanel(QWidget):
    simulation_started = pyqtSignal(float, float, str)
    simulation_stopped = pyqtSignal()
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("controlPanel")
        self.setup_ui()
        self.is_running = False

    def setup_ui(self):
        # Основной layout
        layout = QFormLayout(self)
        layout.setContentsMargins(5, 15, 5, 5)
        layout.setVerticalSpacing(10)
        
        # Группа параметров
        params_group = QGroupBox("Параметры модели")
        params_group.setObjectName("paramsGroup")
        params_layout = QFormLayout(params_group)
        params_layout.setContentsMargins(10, 15, 10, 10)
        
        # Поле ввода дозы
        self.dose_input = QDoubleSpinBox()
        self.dose_input.setObjectName("doseInput")
        self.dose_input.setRange(0.1, 10.0)
        self.dose_input.setValue(1.0)
        self.dose_input.setSingleStep(0.1)
        
        # Поле ввода массы
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setObjectName("weightInput")
        self.weight_input.setRange(10, 150)
        self.weight_input.setValue(70)
        self.weight_input.setSingleStep(1)
        
        # Выбор состояния косточки
        self.seed_combo = QComboBox()
        self.seed_combo.setObjectName("seedCombo")
        self.seed_combo.addItems(["Разжёвана", "Целая"])
        
        # Добавляем элементы в группу
        params_layout.addRow("Концентрация амигдалина (мг):", self.dose_input)
        params_layout.addRow("Масса тела (кг):", self.weight_input)
        params_layout.addRow("Состояние косточки:", self.seed_combo)
        
        # Группа управления
        control_group = QGroupBox("Управление")
        control_group.setObjectName("controlGroup")
        control_layout = QHBoxLayout(control_group)
        control_layout.setContentsMargins(10, 10, 10, 10)
        
        # Кнопки управления
        self.start_stop_btn = QPushButton("Начать визуализацию")
        self.start_stop_btn.setObjectName("startButton")
        self.start_stop_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.cancel_btn = QPushButton("Сброс")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.setEnabled(False)
        
        control_layout.addWidget(self.start_stop_btn)
        control_layout.addWidget(self.cancel_btn)
        
        # Добавляем группы в основной layout
        layout.addRow(params_group)
        layout.addRow(control_group)
        
        # Подключаем сигналы
        self.start_stop_btn.clicked.connect(self.toggle_simulation)
        self.cancel_btn.clicked.connect(self.request_clear)

    def toggle_simulation(self):
        if not self.is_running:
            self.start_simulation()
        else:
            self.stop_simulation()

    def start_simulation(self):
        self.is_running = True
        self.start_stop_btn.setText("Остановить")
        self.start_stop_btn.setObjectName("stopButton")
        self.start_stop_btn.style().polish(self.start_stop_btn)
        self.cancel_btn.setEnabled(False)
        
        self.simulation_started.emit(
            self.dose_input.value(),
            self.weight_input.value(),
            self.seed_combo.currentText()
        )

    def stop_simulation(self):
        self.is_running = False
        self.start_stop_btn.setText("Начать визуализацию")
        self.start_stop_btn.setObjectName("startButton")
        self.start_stop_btn.style().polish(self.start_stop_btn)
        self.cancel_btn.setEnabled(True)
        
        self.simulation_stopped.emit()

    def request_clear(self):
        self.clear_requested.emit()

    def reset_controls(self):
        self.is_running = False
        self.start_stop_btn.setText("Начать визуализацию")
        self.start_stop_btn.setObjectName("startButton")
        self.start_stop_btn.style().polish(self.start_stop_btn)
        self.cancel_btn.setEnabled(False)