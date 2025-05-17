from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QTimer


class LoadingSplash(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap(400, 200))
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        
        self.message_font = QFont('Arial', 14)
        self.progress = 0
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50) 
        
    def update_progress(self):
        self.progress += 1
        if self.progress >= 100:
            self.timer.stop()
            self.close()
        self.redraw()
        
    def redraw(self):
        pixmap = QPixmap(400, 200)
        pixmap.fill(QColor(33, 150, 243))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.message_font)
        
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, 
                        "Модель отравления\nсинильной кислотой\n\nЗагрузка...")
        
        painter.setBrush(QColor(255, 255, 255, 100))
        painter.drawRect(50, 150, 300, 20)
        
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(50, 150, 3 * self.progress, 20)
        
        painter.end()
        self.setPixmap(pixmap)
