import sys
import time
# import modules.thread

import modules.gui as gui

__version__ = "0.0.1"

try:
    from PyQt5 import QtWidgets, QtGui, QtCore
    import pyqtgraph as pyg
    import loguru
except ImportError:
    try:
        import pip
    except ImportError:
        raise ImportError("Plz install pip and re-run script")
        exit(2)
    if "--no-install" in sys.argv:
        print("No u")
        exit(2)
    old_argv = sys.argv
    sys.argv = ["pip", "install", "pyqt5", "loguru", "pyqtgraph", "pyserial"]
    pip.main()
    sys.argv = old_argv
    del pip, old_argv
    print("Packages installed, please re-run")
    exit(0)

logger = loguru.logger

def do_nothing():
    pass

class Button:
    def __init__(self, root, x, y, text, func):
        self.root = root
        self.x = x
        self.y = y
        self.text = text
        self.func = func
        self.button = QtWidgets.QPushButton(self.root)
        self.button.setText(self.text)
        self.button.clicked.connect(self.func)
        self.button.move(self.x, self.y)

    def show(self):
        self.button.show()

    def hide(self):
        self.button.hide()

class Label:
    def __init__(self, root, x, y, text, centerx = True, centery = True, styleSheet = None):
        self.root = root
        self.label = QtWidgets.QLabel(self.root)
        self.label.setText(text)
        if centerx:
            self.x = x - (self.label.size().width() // 2)
        else:
            self.x = x
        if centery:
            self.y = y - (self.label.size().height() // 2)
        else:
            self.y = y
        self.text = text
        self.centerx = centerx
        self.centery = centery
        self.label.move(self.x, self.y)

        if styleSheet:
            self.label.setStyleSheet(styleSheet)
            self.styleSheet = styleSheet
        else:
            self.styleSheet = None
        
        self.x = x
        self.y = y

    def show(self):
        self.label.show()

    def hide(self):
        self.label.hide()

    def move(self, x, y):
        if self.centerx:
            self.x = x - (self.label.size().width() // 2)
        else:
            self.x = x
        if self.centery:
            self.y = y - (self.label.size().height() // 2)
        else:
            self.y = y
        self.label.move(self.x, self.y)
        self.root.update()
        
        self.x = x
        self.y = y

class MainWindow(QtWidgets.QWidget):
    def __init__(self, x, y, title):
        super(MainWindow, self).__init__()
        self.x = x
        self.y = y
        self.windowTitle = title
        
        self.setStyleSheet("background-color: #323232;")

        video_rect_aspect = 16/9
        video_rect_height = round(self.y * 2/3)
        video_rect_width  = round(video_rect_height * video_rect_aspect)

        # logger.info(video_rect_height)
        # logger.info(video_rect_width)

        # x, y, width, height
        self.video_rect = QtCore.QRect((self.x // 2) - (video_rect_width // 2), (self.y - video_rect_height), video_rect_width, video_rect_height)
        self.video_rect_text = Label(self, (self.x // 2), (self.y - video_rect_height), "Put Video Here!", centery = False,
                styleSheet = "color: white;")
        self.video_rect_text.show()

        self.initUI()

    def initUI(self):
        logger.info("Starting UI")
        # self.resize(self.x, self.y)
        self.setFixedSize(self.x, self.y)
        self.setWindowTitle(self.windowTitle)
        self.center()

        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def paintEvent(self, event):
        self.painter = QtGui.QPainter(self)
        self.painter.fillRect(self.video_rect, QtGui.QColor("#4d4d4d"))
        self.painter.end()

    # def closeEvent(self, event):
        

@logger.catch
def main():
    logger.info("Starting Homebase version " + __version__)

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.png"))
    app.setApplicationDisplayName("Homebase")

    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    logger.info("Screen width/height: " + str(width) + "," + str(height))
    
    if sys.platform == "darwin":
        height -= 53
    
    mainWindow = MainWindow(width, height, "Homebase")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
