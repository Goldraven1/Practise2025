from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon as FIF, SplashScreen
from .views import DashboardInterface

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        # Create sub interfaces
        self.dashboardInterface = DashboardInterface(self)

        # Add items to navigation interface
        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(self.dashboardInterface, FIF.HOME, 'Главная')

        self.navigationInterface.addSeparator()

    def initWindow(self):
        self.resize(1100, 750)
        self.setMinimumWidth(760)
        self.setWindowTitle('Finance Tracker')
        
        # Center on screen
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
