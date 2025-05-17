from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QDateTime
from PyQt6.QtGui import QFont, QTextCharFormat, QColor


class EventLog(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 9))
        self.setStyleSheet("""
            background: #f8f8f8;
            border: 1px solid #ddd;
            padding: 5px;
        """)
        
    def add_event(self, message):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        
        # Форматирование формул
        if "Токсичность = " in message:
            message = f"<font color='blue'>{message}</font>"
        elif "Доза амигдалина:" in message or "Масса тела:" in message:
            message = f"<i>{message}</i>"
        
        self.append(f"<b>[{timestamp}]</b> {message}")
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

        
    def add_error(self, message):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        error_format = QTextCharFormat()
        error_format.setForeground(QColor(255, 0, 0))
        
        self.append(f"<b><font color='red'>[{timestamp}] {message}</font></b>")
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        
    def clear_events(self):
        self.clear()