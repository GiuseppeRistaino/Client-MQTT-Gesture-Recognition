from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Converter.Converter import *

class FrameConverter(QFrame):
    def __init__(self, parent):
        super(FrameConverter, self).__init__(parent)
        self.parent = parent

        self.buttonConverter = QPushButton("Convert")
        self.buttonConverter.clicked.connect(self.eventButtonConverter)

        self.areaText = QTextEdit()
        self.areaText.setReadOnly(True)

        self.buttonSave = QPushButton("Save")
        self.buttonSave.clicked.connect(self.eventButtonSave)

        vbox = QVBoxLayout()
        vbox.addWidget(self.buttonConverter)
        vbox.addWidget(self.areaText)
        vbox.addWidget(self.buttonSave)
        self.setLayout(vbox)


    def eventButtonConverter(self):
        fileDialog = QFileDialog()
        fname = fileDialog.getOpenFileName(self, 'Open file', '//home')
        sensors = hexToFloat(fname)
        self.writeAreaText(sensors)
        #self.writeAreaTextFromFile(fname)

    def eventButtonSave(self):
        fileDialog = QFileDialog()
        fname = fileDialog.getSaveFileName(self, 'Save file', '//home','csv files (*.csv)')
        self.saveFile(fname)

    def saveFile(self, file):
        with open(file, 'a') as openfileobject:
            openfileobject.writelines(self.areaText.toPlainText())

    def writeAreaText(self, sensors):
        for elem in sensors:
            self.areaText.append(str(elem['x_acc']) + ',' +str(elem['y_acc']) + ','
                                 +str(elem['z_acc']) + ',' +str(elem['x_gir']) + ','
                                 +str(elem['y_gir']) + ',' +str(elem['z_gir']) + ',')




