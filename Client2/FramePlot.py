from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from DataTraining.Wrapper import *
import numpy as np
import matplotlib.pyplot as plt

class FramePlot(QFrame):
    def __init__(self, parent=None):
        super(FramePlot, self).__init__(parent)
        self.parent = parent

        self.buttonFile = QPushButton("Open File")
        self.buttonFile.clicked.connect(self.eventButtonFile)

        self.figureAcc = plt.figure()
        self.figureGir = plt.figure()

        self.canvasAcc = FigureCanvas(self.figureAcc)
        self.canvasAcc.setParent(self)
        self.mpl_toolbar_acc = NavigationToolbar(self.canvasAcc, self)

        self.canvasGir = FigureCanvas(self.figureGir)
        self.canvasGir.setParent(self)
        self.mpl_toolbar_gir = NavigationToolbar(self.canvasGir, self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.buttonFile)
        hbox1 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.canvasAcc)
        vbox1.addWidget(self.mpl_toolbar_acc)
        hbox1.addLayout(vbox1)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.canvasGir)
        vbox2.addWidget(self.mpl_toolbar_gir)
        hbox1.addLayout(vbox2)
        vbox.addLayout(hbox1)
        self.setLayout(vbox)

    def eventButtonFile(self):
        fileDialog = QFileDialog()
        fname = fileDialog.getOpenFileName(self, 'Open file', '//home')
        listXacc, listYacc, listZacc = getListPointsForPlotAcc(fname)
        listXgir, listYgir, listZgir = getListPointsForPlotGir(fname)

        ax_acc = self.figureAcc.add_subplot(111)
        ax_acc.plot(listXacc)
        ax_acc.plot(listYacc)
        ax_acc.plot(listZacc)

        ax_gir = self.figureGir.add_subplot(111)
        ax_gir.plot(listXgir)
        ax_gir.plot(listYgir)
        ax_gir.plot(listZgir)

        self.canvasAcc.draw()
        self.canvasGir.draw()