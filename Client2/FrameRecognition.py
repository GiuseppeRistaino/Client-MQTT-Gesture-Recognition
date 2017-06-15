from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Converter.Converter import *
from DataTraining.Clustering import *
from DataTraining.HMMGesto import *

class FrameRecognition(QFrame):
    def __init__(self, parent):
        super(FrameRecognition, self).__init__(parent)
        self.parent = parent

        self.buttonStart = QPushButton("Start")
        self.buttonStart.clicked.connect(self.eventButtonStart)

        self.areaText = QTextEdit()
        self.areaText.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.buttonStart)
        vbox.addWidget(self.areaText)
        self.setLayout(vbox)


    def eventButtonStart(self):
        fileDialog = QFileDialog()
        fname = fileDialog.getOpenFileName(self, 'Open file', '//home')
        # Carica i centroidi dal file
        centroids = loadCentroids("./DataTraining/Centroids/centroids.csv")

        # Carica i modelli dai file
        model1 = HMMGesto()
        model1.loadModel("./DataTraining/Models/model1.xml")
        l1 = model1.getLikelihood("./testSet/", centroids)

        model2 = HMMGesto()
        model2.loadModel("./DataTraining/Models/model2.xml")
        l2 = model2.getLikelihood("./testSet/", centroids)

        model3 = HMMGesto()
        model3.loadModel("./DataTraining/Models/model3.xml")
        l3 = model3.getLikelihood("./testSet/", centroids)

        self.writeAreaTextFromFile(fname, model1, model2, model3, centroids)


    def writeAreaTextFromFile(self, file, model1, model2, model3, centroids):
        l1 = model1.getLikelihoodForFile(file, centroids)
        l2 = model2.getLikelihoodForFile(file, centroids)
        l3 = model3.getLikelihoodForFile(file, centroids)

        lista = [l1, l2, l3]
        # print "verosimiglianza gesto 1 = " + str(lista[0])
        self.areaText.append("verosimiglianza gesto 1 = " + str(lista[0]))
        # print "verosimiglianza gesto 2 = " + str(lista[1])
        self.areaText.append("verosimiglianza gesto 2 = " + str(lista[1]))
        # print "verosimiglianza gesto 3 = " + str(lista[2])
        self.areaText.append("verosimiglianza gesto 3 = " + str(lista[2]))
        # print "verosimiglianza gesto 4 = " + str(lista[3])
        maxValue = l1
        gesto = "gesto1"
        i = 0
        while i < len(lista):
            if (lista[i] > maxValue):
                maxValue = lista[i]
                if i == 1:
                    gesto = "gesto2"
                elif i == 2:
                    gesto = "gesto3"
                    # elif i == 3:
                    # gesto = "gesto4"
            i += 1

        # print "File: " + file + "Stai effettuando il " + gesto
        self.areaText.append("Stai effettuando il " + gesto)

    def writeAreaTextFormFolder(self, model1, model2, model3, centroids):
        files = os.listdir("./testSet/")

        for file in files:
            l1 = model1.getLikelihoodForFile("./testSet/" + file, centroids)
            l2 = model2.getLikelihoodForFile("./testSet/" + file, centroids)
            l3 = model3.getLikelihoodForFile("./testSet/" + file, centroids)

            lista = [l1, l2, l3]
            #print "verosimiglianza gesto 1 = " + str(lista[0])
            self.areaText.append("verosimiglianza gesto 1 = " + str(lista[0]))
            #print "verosimiglianza gesto 2 = " + str(lista[1])
            self.areaText.append("verosimiglianza gesto 2 = " + str(lista[1]))
            #print "verosimiglianza gesto 3 = " + str(lista[2])
            self.areaText.append("verosimiglianza gesto 3 = " + str(lista[2]))
            # print "verosimiglianza gesto 4 = " + str(lista[3])
            maxValue = l1
            gesto = "gesto1"
            i = 0
            while i < len(lista):
                if (lista[i] > maxValue):
                    maxValue = lista[i]
                    if i == 1:
                        gesto = "gesto2"
                    elif i == 2:
                        gesto = "gesto3"
                        # elif i == 3:
                        # gesto = "gesto4"
                i += 1

            #print "File: " + file + "Stai effettuando il " + gesto
            self.areaText.append("File: " + file + "Stai effettuando il " + gesto)
