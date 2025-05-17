from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import (QPainter, QPen, QColor, QFont)
from PyQt6.QtCore import (Qt, pyqtSignal, QTimer)

class OrganismView(QWidget):
    event_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 650)
        self.organs = self._setup_organs()
        self.current_stage = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_stage)
        self.stages = [
            #флэш уведомление: Постепенно всасывается через слизистую ЖКТ
            ("ЖКТ", "Косточка абрикоса попадает в ЖКТ", QColor(139, 69, 19)),
            ("Желудок", "Если косточка разжёвана, амигдалин высвобождается, и взаимодействует с ферментами", QColor(210, 105, 30)),
            ("Кишечник", "β-глюкозидаза расщепляет амигдалин и происходит синтез HCN", QColor(205, 133, 63)),
        
            ("Печень", "Часть HCN детоксифицируется роданазой", QColor(50, 205, 50)),
            ("Кровь", "HCN связывается с гемоглобином, что нарушает транспорт кислорода", QColor(220, 20, 60)),
            ("Сердце", "Нарушение синтеза АТФ → аритмия → остановка сердца", QColor(178, 34, 34)),
            ("Мозг", "Гипоксия → судороги → кома", QColor(70, 130, 180))
        ]
        self.is_running = False
        
    def _setup_organs(self):
        return {
            "ЖКТ": {"pos": (100, 100), "radius": 40, "color": QColor(240, 230, 140)},
            "Желудок": {"pos": (150, 180), "radius": 35, "color": QColor(255, 165, 0)},
            "Кишечник": {"pos": (250, 200), "radius": 50, "color": QColor(210, 180, 140)},
            "Кровь": {"pos": (200, 300), "radius": 30, "color": QColor(220, 20, 60, 150)},
            "Печень": {"pos": (350, 180), "radius": 45, "color": QColor(144, 238, 144)},
            "Сердце": {"pos": (300, 100), "radius": 40, "color": QColor(255, 99, 71)},
            "Мозг": {"pos": (200, 50), "radius": 35, "color": QColor(135, 206, 250)}
        }
        
    def next_stage(self):
        if self.current_stage < len(self.stages) - 1:
            self.current_stage += 1
            stage, desc, _ = self.stages[self.current_stage]
            
            if stage == "Кишечник" and self.seed_condition == "Целая":
                desc = "Косточка не повреждена - HCN не высвобождается"
                self.event_occurred.emit(desc)
                self.timer.stop()
                return
                
            if stage == "Сердце":
                toxicity = self.dose / self.weight
                if toxicity > 1.0:
                    desc += " → ОСТАНОВКА СЕРДЦА"
                elif toxicity > 0.5:
                    desc += " → Тяжелая аритмия"
                    
            self.event_occurred.emit(f"{stage}: {desc}")
            self.update()
        else:
            self.timer.stop()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for name, organ in self.organs.items():
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.setBrush(organ["color"])
            painter.drawEllipse(
                organ["pos"][0] - organ["radius"],
                organ["pos"][1] - organ["radius"],
                organ["radius"] * 2,
                organ["radius"] * 2
            )
            
            painter.setFont(QFont("Arial", 8))
            painter.drawText(
                organ["pos"][0] - organ["radius"],
                organ["pos"][1] - organ["radius"] - 5,
                name
            )
        
        if self.current_stage < len(self.stages):
            current_organ, _, stage_color = self.stages[self.current_stage]
            organ = self.organs[current_organ]
            
            painter.setPen(QPen(stage_color, 3))
            painter.drawEllipse(
                organ["pos"][0] - organ["radius"] - 5,
                organ["pos"][1] - organ["radius"] - 5,
                (organ["radius"] + 5) * 2,
                (organ["radius"] + 5) * 2
            )
            
            painter.setBrush(stage_color)
            painter.drawEllipse(
                organ["pos"][0] - 10,
                organ["pos"][1] - 10,
                20, 20
            )

    def start_simulation(self, dose, weight, seed_condition):
        self.is_running = True
        self.dose = dose
        self.weight = weight
        self.seed_condition = seed_condition
        self.current_stage = 0
        self.event_occurred.emit(f"Начало: проглочена косточка ({seed_condition} состояние)")
        self.timer.start(1500)
        self.update()
        
    def stop_simulation(self):
        self.is_running = False
        self.timer.stop()
        self.event_occurred.emit("Визуализация приостановлена")
        
    def reset(self):
        self.is_running = False
        self.current_stage = 0
        self.timer.stop()
        self.update()
        self.event_occurred.emit("Состояние сброшено")