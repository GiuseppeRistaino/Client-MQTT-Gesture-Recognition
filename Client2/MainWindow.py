import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from MainFrame import *
from FrameTraining import *
from FrameAcquisition import *
from FrameConverter import *
from FrameRecognition import *
from FrameRealTime import *
from FramePlot import *

MENU_FILE = "File"
MENU_FILE_NEW = "New"
MENU_FILE_NEW_TRINING = "Training"
MENU_FILE_NEW_ACQUISITION = "Acquisition"
MENU_FILE_NEW_RECOGNITION = "Recognition"
MENU_FILE_NEW_REAL_TIME = "Real Time"
MENU_TOOLS = "Tools"
#MENU_TOOLS_CONVERTER = "Converter"
MENU_TOOLS_PLOT = "Plot"

WINDOW_TITLE = "PROGETTO MISURE"

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #MENU
        self.menu = self.menuBar()

        #MENU FILE
        self.menuFile = self.menu.addMenu(MENU_FILE)
        #MENU NEW
        self.menuNew = self.menuFile.addMenu(MENU_FILE_NEW)
        #MENU NEW TRAINING
        self.menuNew.addAction(MENU_FILE_NEW_TRINING)
        #MENU NEW ACQUISITION
        self.menuNew.addAction(MENU_FILE_NEW_ACQUISITION)
        #MENU NEW RECOGNITION
        self.menuNew.addAction(MENU_FILE_NEW_RECOGNITION)
        #MENU NEW REAL TIME
        self.menuNew.addAction(MENU_FILE_NEW_REAL_TIME)

        #MENU TOOLS
        self.menuTools = self.menu.addMenu(MENU_TOOLS)
        #MENU_TOOLS_CONVERTER
        #self.menuTools.addAction(MENU_TOOLS_CONVERTER)
        #MENU_TOOLS PLOT
        self.menuTools.addAction(MENU_TOOLS_PLOT)

        self.menu.triggered[QAction].connect(self.eventMenuBar)

        self.frameAcquisition = FrameAcquisition(self)
        self.setCentralWidget(self.frameAcquisition)

        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(self.size())


    def eventMenuBar(self, q):
        textMenuBar = q.text()
        if textMenuBar == MENU_FILE_NEW_TRINING:
            self.frameTraining = FrameTraining(self)
            self.setCentralWidget(self.frameTraining)
        elif textMenuBar == MENU_FILE_NEW_ACQUISITION:
            self.frameAcquisition = FrameAcquisition(self)
            self.setCentralWidget(self.frameAcquisition)
        elif textMenuBar == MENU_FILE_NEW_RECOGNITION:
            self.frameRecognition = FrameRecognition(self)
            self.setCentralWidget(self.frameRecognition)
        elif textMenuBar == MENU_FILE_NEW_REAL_TIME:
            self.frameRealTime = FrameRealTime(self)
            self.setCentralWidget(self.frameRealTime)
        #elif textMenuBar == MENU_TOOLS_CONVERTER:
        #    self.frameConverter = FrameConverter(self)
        #    self.setCentralWidget(self.frameConverter)
        elif textMenuBar == MENU_TOOLS_PLOT:
            self.framePlot = FramePlot(self)
            self.setCentralWidget(self.framePlot)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
