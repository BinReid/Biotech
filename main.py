import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui.main_window import MainWindow
from gui.splash_screen import LoadingSplash


def main():
    app = QApplication(sys.argv)
    
    with open('gui/styles.css', 'r') as f:
        app.setStyleSheet(f.read())
    
    splash = LoadingSplash()
    splash.show()
    
    window = MainWindow()
    
    QTimer.singleShot(3000, lambda: [
        splash.finish(window),
        window.show()
    ])
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
