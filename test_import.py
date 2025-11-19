import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

print("Starting imports without App")

try:
    from ui.main_window import MainWindow
    print("MainWindow imported")
except Exception as e:
    print(f"Error importing main_window: {e}")

