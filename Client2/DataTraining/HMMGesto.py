#coding: utf-8
from ghmm import *
from Clustering import *
from Wrapper import *

class HMMGesto:
    def __init__(self):

        '''
        Definiamo l'alfabeto del nostro modello come il numero dei centroidi (5 Centroidi)
        '''
        self.sigma = IntegerRange(0, 5)

        '''
        Definiamo il numero degli stati N
        '''
        self.N = 5

        '''
        Definiamo la matrice di transizione A
        '''
        self.A = [[0.2] * 5,
                 [0.2] * 5,
                 [0.2] * 5,
                 [0.2] * 5,
                 [0.2] * 5]

        '''
        Probabilità delle emissioni dei centroidi nei diversi stati.
        In questo caso le probabilità sono equiprobabili
        '''
        self.emissions = [1.0 / 5] * 5

        '''
        Matrice B delle probabilità per ogni gesto a seconda dei centroidi
        '''
        self.B = [self.emissions] * 5

        '''
        Probabilità di iniziare da un gesto (50 e 50)
        '''
        self.pi = [0.2] * 5

        '''
        Modello di Markov Iniziale
        '''
        self.model = HMMFromMatrices(self.sigma, DiscreteDistribution(self.sigma), self.A, self.B, self.pi)

    '''
    Allena il modello con il metodo BaumWelch attraverso le osservazioni di centroidi.
        - pathDataTrain: path dove si trovano i dati sui quali si intende allenare il modello
        - centroids: lista dei centroidi delle osservazioni presenti nel dataSet
    '''
    def train(self, pathDataTrain, centroids):
        # BAUM-WELCH
        points = np.vstack(getLista(pathDataTrain))
        baum_centroids = closest_centroid(points, centroids).tolist()
        train_set = EmissionSequence(self.sigma, baum_centroids)
        self.model.baumWelch(train_set)

    '''
    Salva il modello HMM in un file
        - file: nome dle file dove salvare il modello (formato xml)
    '''
    def saveModel(self, file):
        self.model.write(file)

    '''
    Verifica la verosomiglianza di una serie di osservazioni con il modello.
        - pathDataTest: path dove si trovano le osservazioni delel quali si vuole conoscere la verosomiglianza
        - centroids: lista dei centroidi delle osservazioni presenti nel dataSet
    '''
    def getLikelihood(self, pathDataTest, centroids):
        points = np.vstack(getLista(pathDataTest))
        testCentroid = closest_centroid(points, centroids).tolist()

        test_seq = EmissionSequence(self.sigma, testCentroid)
        c = self.model.loglikelihood(test_seq)
        return c

    def getLikelihoodForFile(self, file, centroids):
        lista = []
        # print files
        with open(file) as openfileobject:
            # openfileobject.readline()
            for line in openfileobject:
                vector = line.split(",")
                xa = float(vector[0])
                ya = float(vector[1])
                za = float(vector[2])
                xg = float(vector[3])
                yg = float(vector[4])
                zg = float(vector[5])
                lista.append([xa, ya, za, xg, yg, zg])
                # print lista.__len__()
            points = np.vstack(lista)
            testCentroid = closest_centroid(points, centroids).tolist()

            test_seq = EmissionSequence(self.sigma, testCentroid)
            c = self.model.loglikelihood(test_seq)
        return c

    '''
    Verifica la verosomiglianza di una serie di osservazioni con il modello.
        - points: le osservazioni delle quali si vuole conoscere la verosomiglianza
        - centroids: lista dei centroidi delle osservazioni presenti nel dataSet
    '''

    def getLikelihoodFromPoints(self, points, centroids):
        testCentroid = closest_centroid(points, centroids).tolist()

        test_seq = EmissionSequence(self.sigma, testCentroid)
        c = self.model.loglikelihood(test_seq)
        return c

    '''
    Carica il modello da un file xml
        - file: nome del file dove caricazr eil modello (formato xml)
    '''
    def loadModel(self, file):
        self.model = HMMOpen(file)


    def help(self):
        help('ghmmH')
