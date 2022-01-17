import sys
import time
# import modules.thread

__version__ = "0.0.1"

try:
    from PyQt5 import QtWidgets,QtGui,QtCore
    import loguru
except ModuleNotFoundError:
    try:
        import pip
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Plz install pip and re-run script")
        exit(2)
    if "--no-install" in sys.argv:
        raise ModuleNotFoundError("Plz install pip and re-run script")
        exit(2)
    old_argv = sys.argv
    sys.argv = ["pip", "install", "pyqt5", "loguru"]
    pip.main()
    sys.argv = old_argv
    del pip, old_argv
    try:
        loguru
    except:
        import loguru

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
    def __init__(self, root, x, y, text):
        self.root = root
        self.x = x
        self.y = y
        self.text = text
        self.label = QtWidgets.QLabel(self.root)
        self.label.setText(self.text)
        self.label.move(self.x, self.y)

    def show(self):
        self.label.show()

    def hide(self):
        self.label.hide()

class MainWindow(QtWidgets.QWidget):
    def __init__(self, x, y, title):
        super(MainWindow, self).__init__()
        self.x = x
        self.y = y
        self.windowTitle = title
        
        self.setStyleSheet("background-color: #323232;");

        # self.setWindowIcon(QtGui.QIcon("icon.png"))

        self.video_rect = QtCore.QRect(self.x // 4, self.y // 4, self.x // 2, self.y // 2)

        self.button = Button(self, 0, 0, "reee", do_nothing)
        self.button.show()

        self.label = Label(self, 100, 100, "reee?")
        self.label.show()

        self.initUI()

    def initUI(self):

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
        # print(dir(QtGui.QPainter))
        self.painter = QtGui.QPainter(self)
        self.painter.fillRect(self.video_rect, QtGui.QColor("green"))
        self.painter.end()
        # draw video rectangle
        # self.painter = QtGui.QPainter(self)
        # self.brush = QtGui.QBrush(QtGui.QColor("green"))
        # self.painter.setBrush(self.brush)
        # self.painter.drawRect(self.video_rect)


def main():
    logger.info("Starting Homebase version " + __version__)
    app = QtWidgets.QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()

    logger.info("screen width/height: " + str(width) + "," + str(height))
    if sys.platform == "darwin":
        height -= 53
    mainWindow = MainWindow(width, height, "Homebase")
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
