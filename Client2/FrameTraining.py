from PyQt4.QtCore import *
from PyQt4.QtGui import *
from DataTraining.Clustering import *
from DataTraining.Wrapper import *
from DataTraining.HMMGesto import *
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
import threading
from matplotlib.figure import Figure

PATH_DATA_SET = "./DataTraining/dataSet/"
PATH_SAVE_CENTROIDS = "./DataTraining/Centroids/centroids.csv"

class FrameTraining(QFrame):
    def __init__(self, parent=None):
        super(FrameTraining, self).__init__(parent)
        self.parent = parent

        self.buttonClustering = QPushButton("Start Clustering")
        self.buttonClustering.clicked.connect(self.eventButtonClustering)
        self.progressBar = MyProgressBar()
        self.progressBar.setText("")

        self.figure = Clustering(self)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)

        self.buttonTraining = QPushButton("Training")
        self.buttonTraining.clicked.connect(self.eventButtonTraining)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.buttonClustering)
        hbox1.addWidget(self.progressBar)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.buttonTraining)
        self.setLayout(vbox)

    def eventButtonTraining(self):
        # Inizializiamo i modelli HMM e dopo averli addestrati li salviamo su file

        self.centroids = loadCentroids("./DataTraining/Centroids/centroids.csv")
        model1 = HMMGesto()
        model1.train("./DataTraining/gesto1/", self.centroids)
        model1.saveModel("./DataTraining/Models/model1.xml")

        model2 = HMMGesto()
        model2.train("./DataTraining/gesto2/", self.centroids)
        model2.saveModel("./DataTraining/Models/model2.xml")

        model3 = HMMGesto()
        model3.train("./DataTraining/gesto3/", self.centroids)
        model3.saveModel("./DataTraining/Models/model3.xml")

        msg = QMessageBox()
        msg.setText("Training HMM successful!")
        msg.exec_()

    def eventButtonClustering(self):
        self.progressBar.setText("Clustering...")
        self.progressBar.setRange(0, 0)
        self.draw_plots()

    def draw_plots(self):
        """ Plot Plots """
        self.figure.start_plotting_thread(on_finish=self.finish_drawing_plots)

    def finish_drawing_plots(self):
        """ Finish drawing plots """
        self.canvas.draw()
        self.show()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(100)
        self.progressBar.setText("Done")


class Clustering(Figure, QThread):
    def __init__(self, parent, *args, **kwargs):
        QThread.__init__(self, parent)
        Figure.__init__(self, *args, **kwargs)


    def start_plotting_thread(self, on_finish=None):
        """ Start plotting """

        if on_finish is not None:
            self.finished.connect(on_finish)

        self.start()

    def run(self):
        """ Run as a thread """
        # Figure out rows and columns
        points = np.vstack(getLista(PATH_DATA_SET))
        self.centroids, closestCentroid = computeValues(points)
        saveCentroids(PATH_SAVE_CENTROIDS, self.centroids)
        ax = Axes3D(self)
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=closestCentroid)

class MyProgressBar(QProgressBar):

    def __init__(self, parent=None):
        super(MyProgressBar, self).__init__(parent)
        self.parent = parent
        #self.setRange(0, 0)
        self.setAlignment(Qt.AlignCenter)
        self._text = None

    def setText(self, text):
        self._text = text

    def text(self):
        return self._text