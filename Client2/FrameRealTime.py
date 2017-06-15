from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Converter.Converter import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import paho.mqtt.client as mqtt
from DataTraining.Clustering import *
from DataTraining.HMMGesto import *
from RealTime.EngineContinuous import *

IP = "127.0.0.1"
PORTA = "1883"
TOPIC = "home"

soglia = -1150

class FrameRealTime(QFrame):
    def __init__(self, parent):
        super(FrameRealTime, self).__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()
        hbox_1 = QHBoxLayout()

        self.labelIP = QLabel("Indirizzo IP")
        self.editIP = QLineEdit()
        self.editIP.setText(IP)

        self.labelPorta = QLabel("Port")
        self.editPorta = QLineEdit()
        self.editPorta.setText(PORTA)

        self.labelTopic = QLabel("Topic")
        self.editTopic = QLineEdit()
        self.editTopic.setText(TOPIC)

        self.buttonConnect = QPushButton("Start Recognition")
        self.buttonConnect.clicked.connect(self.eventConnect)

        self.buttonDisconnect = QPushButton("Stop Recognition")
        self.buttonDisconnect.clicked.connect(self.eventDisconnect)

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
        # start(self.client)

    def eventDisconnect(self):
        # self.connectionMQTT.disconnect()
        self.connectionMQTT.stopConn()
        # disconnect(self.client)

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
        self.listaPoints = []
        self.maxValueBefore = 0
        self.gestoBefore = ""
        self.discesa = False
        # Carica i centroidi dal file
        self.centroids = loadCentroids("./DataTraining/Centroids/centroids.csv")

        # Carica i modelli dai file
        self.model1 = HMMGesto()
        self.model1.loadModel("./DataTraining/Models/model1.xml")

        self.model2 = HMMGesto()
        self.model2.loadModel("./DataTraining/Models/model2.xml")

        self.model3 = HMMGesto()
        self.model3.loadModel("./DataTraining/Models/model3.xml")

    def run(self):
        self.startConn()

    def startConn(self):
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        # print "connected"
        # self.client.subscribe("home")
        self.client.on_message = self.on_message

        self.client.connect(IP, PORTA, 60)

        self.received.emit("Sottoscrizione effettuata al topic: " + TOPIC)
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()
    '''
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # self.areaText.setText(msg.topic + " " + str(msg.payload))
        #data = msg.payload.encode('hex')
        data = msg.payload
        # codice per la conversione in floating point
        pay = ",".join(c.encode("hex") for c in data)  #DA RIMETTERE!!!!!!!!!!!!!!!!!!
        # with open("test1.txt", 'bw') as openfileobject:
        #    openfileobject(data)

        #pay = pay.rstrip('\n') + ","
        #print pay
        sensors = hexToFloatForLine(pay)
        self.listaPoints.append(sensors)

        if len(self.listaPoints) > 700:
            result, maxValue = computeLikelihood4(self.listaPoints, self.model1, self.model2, self.model3, self.centroids)
            #self.received.emit(result)
            del self.listaPoints[0:50]

            if self.maxValueBefore == 0:
                self.maxValueBefore = maxValue
                self.gestoBefore = result
            else:
                if self.maxValueBefore < maxValue and self.gestoBefore == result:
                    string = "-----------Nessun Gesto--------- MAX BEFORE: "+str(self.maxValueBefore)
                    self.received.emit(string)
                    self.maxValueBefore = maxValue
                    self.discesa = False
                elif self.maxValueBefore >= maxValue and self.gestoBefore == result:
                    if not self.discesa:
                        string = result +" MAX BEFORE: " +str(self.maxValueBefore)
                    else:
                        string = "-----------Nessun Gesto--------- MAX BEFORE: " + str(self.maxValueBefore)
                    self.received.emit(string)
                    self.maxValueBefore = maxValue
                    self.discesa = True
                elif self.gestoBefore != result:
                    string = "Last..."+self.gestoBefore
                    self.received.emit(string)
                    self.maxValueBefore = maxValue
                    self.gestoBefore = result
                    self.discesa = False

        #with open("test1.txt", 'a') as openfileobject:
            #openfileobject.writelines(pay.upper())
        #    openfileobject.write(pay.upper() + ",")

        # print(pay.upper())

            # The callback for when a PUBLISH message is received from the server.
    '''
    def on_message(self, client, userdata, msg):
        # self.areaText.setText(msg.topic + " " + str(msg.payload))
        # data = msg.payload.encode('hex')
        data = msg.payload
        # codice per la conversione in floating point
        pay = ",".join(c.encode("hex") for c in data)  #DA RIMETTERE!!!!!!!!!!!!!!!!!!
        # with open("test1.txt", 'bw') as openfileobject:
        #    openfileobject(data)

        # pay = pay.rstrip('\n') + ","
        # print pay
        sensors = hexToFloatForLine(pay)
        self.listaPoints.append(sensors)

        if len(self.listaPoints) > 300:
            result, maxValue = computeLikelihood4(self.listaPoints, self.model1, self.model2, self.model3,
                                                  self.centroids)
            string = result +"MAX VERO: " +str(maxValue)
            self.received.emit(string)
            '''
            if maxValue < soglia:
                self.received.emit(string +"------------NESSUN GESTO-----------")
            '''
            del self.listaPoints[0:50]
            '''
            if maxValue < soglia:
                self.received.emit(string +"------------NESSUN GESTO-----------")

            del self.listaPoints[0:50]
            # with open("test1.txt", 'a') as openfileobject:
            # openfileobject.writelines(pay.upper())
            #    openfileobject.write(pay.upper() + ",")

            # print(pay.upper())
            '''
    def stopConn(self):
        self.client.disconnect()
        print("Disconnected")
        self.received.emit("Disconnessione effettuata")