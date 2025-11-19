import sys
import os

# Add the src directory to the python path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from qfluentwidgets import setTheme, Theme
from ui.main_window import MainWindow
from database.db_manager import DatabaseManager

def main():
    print("Creating QApplication...")
    app = QApplication(sys.argv)
    print("QApplication created.")
    
    setTheme(Theme.LIGHT)
    print("Theme set.")
    
    # Initialize Database
    db = DatabaseManager()
    print("Database initialized.")
    
    w = MainWindow()
    print("MainWindow created.")
    w.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
