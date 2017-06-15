import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import threading
import paho.mqtt.client as mqtt
from Converter.Converter import *

IP = "127.0.0.1"
PORTA = "1883"
TOPIC = "home"
sensorsCopy = []

class FrameAcquisition(QFrame):
    def __init__(self, parent):
        super(FrameAcquisition, self).__init__(parent)

        layout = QVBoxLayout()
        hbox_1 = QHBoxLayout()

        self.labelIP = QLabel("Indirizzo IP")
        self.editIP = QLineEdit()
        self.editIP.setText(IP)

        self.labelPorta = QLabel("Porta")
        self.editPorta = QLineEdit()
        self.editPorta.setText(PORTA)

        self.labelTopic = QLabel("Topic")
        self.editTopic = QLineEdit()
        self.editTopic.setText(TOPIC)

        self.buttonConnect = QPushButton("Connect")
        self.buttonConnect.clicked.connect(self.eventConnect)

        self.buttonDisconnect = QPushButton("Disconnect")
        self.buttonDisconnect.clicked.connect(self.eventDisconnect)

        self.buttonSave = QPushButton("Save")
        self.buttonSave.clicked.connect(self.eventSave)

        hbox_1.addWidget(self.labelIP)
        hbox_1.addWidget(self.editIP)
        hbox_1.addWidget(self.labelPorta)
        hbox_1.addWidget(self.editPorta)
        hbox_1.addWidget(self.labelTopic)
        hbox_1.addWidget(self.editTopic)
        hbox_1.addWidget(self.buttonConnect)
        hbox_1.addWidget(self.buttonDisconnect)

        self.areaText = QTextEdit()
        self.areaText.setReadOnly(True)

        layout.addLayout(hbox_1)
        layout.addWidget(self.areaText)
        layout.addWidget(self.buttonSave)
        self.setLayout(layout)


    def eventConnect(self):
        '''
        ip = str(self.editIP.text())
        topic = str(self.editTopic.text())
        self.connectionMQTT.start(ip, 1883, topic)
        '''
        self.areaText.clear()
        global IP, PORTA, TOPIC
        IP = str(self.editIP.text())
        PORTA = str(self.editPorta.text())
        TOPIC = str(self.editTopic.text())
        self.connectionMQTT = ConnectionMQTT()
        self.connectionMQTT.received.connect(self.areaText.append)
        self.connectionMQTT.start()
        #start(self.client)

    '''
    def eventSave(self):
        fileDialog = QFileDialog()
        fname = fileDialog.getSaveFileName(self, 'Save file', '//home','txt files (*.txt)')
        self.saveFile(fname)
    '''

    def eventSave(self):
        fileDialog = QFileDialog()
        fname = fileDialog.getSaveFileName(self, 'Save file', '//home', 'csv files (*.csv)')
        self.saveFile(fname)

    '''
    def saveFile(self, file):
        try:
            with open(file, 'a') as openfileobject:
                openfileobject.write(self.areaText.toPlainText())
        except IOError:
            pass
    '''

    def saveFile(self, file):
        try:
            with open(file, 'a') as openfileobject:
                for elem in sensorsCopy:
                    openfileobject.write(str(elem['x_acc']) + ',' +str(elem['y_acc']) + ','
                                 +str(elem['z_acc']) + ',' +str(elem['x_gir']) + ','
                                 +str(elem['y_gir']) + ',' +str(elem['z_gir']) + '\n')
        except IOError:
            pass

    def eventDisconnect(self):
        #self.connectionMQTT.disconnect()
        self.connectionMQTT.stopConn()
        #disconnect(self.client)









# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)


class ConnectionMQTT(QThread):

    received = pyqtSignal([str], [unicode])

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.startConn()
        sensorsCopy = []

    def startConn(self):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        #print "connected"
        #self.client.subscribe("home")
        self.client.on_message = self.on_message

        self.client.connect(IP, PORTA, 60)

        self.received.emit("Sottoscrizione effettuata al topic: " +TOPIC)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        #self.areaText.setText(msg.topic + " " + str(msg.payload))
        # data = msg.payload.encode('hex')
        data = msg.payload
        #codice per la conversione in floating point
        pay = ",".join(c.encode("hex") for c in data) # DA RIMETTERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # with open("test1.txt", 'bw') as openfileobject:
        #    openfileobject(data)
        '''
        with open("test1.txt", 'a') as openfileobject:
            # openfileobject.writelines(pay.upper())
            openfileobject.write(pay.upper() +",")
        self.received.emit(pay.upper()+",")
        #print(pay.upper())
        '''
        sensors = hexToFloatForLine(pay)
        for elem in sensors:
            sensorsCopy.append(elem)
        self.received.emit(pay)
        #self.received.emit(pay.upper()+",")  #DA RIMETTEREEE!!!!!!!!!!!!!!!!

    def stopConn(self):
        self.client.disconnect()
        print("Disconnected")
        self.received.emit("Disconnessione effettuata")