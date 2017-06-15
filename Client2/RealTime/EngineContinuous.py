import os
import numpy as np

MAX_LIKE = {"gesto1": -259, "gesto2":-259, "gesto3":-259}



def computeLikelihood3(numElem, shift, pathTestSet, model1, model2, model3, centroids):
    # creiamo il vettore che contiene tutte le osservazioni
    lista = []
    files = os.listdir(pathTestSet)
    for file in files:
        with open(pathTestSet + file) as openfileobject:
            for line in openfileobject:
                vector = line.split(",")
                xa = float(vector[0])
                ya = float(vector[1])
                za = float(vector[2])
                xg = float(vector[3])
                yg = float(vector[4])
                zg = float(vector[5])
                lista.append([xa, ya, za, xg, yg, zg])

    listaGesti = []

    # prendiamo "numElem" dal vettore e confrontiamo la verosomiglianza con i 3 gesti
    while len(lista) > numElem:
        points = lista[0:numElem]
        points = np.vstack(points)

        l1 = model1.getLikelihoodFromPoints(points, centroids)
        l2 = model2.getLikelihoodFromPoints(points, centroids)
        l3 = model3.getLikelihoodFromPoints(points, centroids)

        listaLike = [l1, l2, l3]
        print "verosimiglianza gesto 1 = " + str(listaLike[0])
        print "verosimiglianza gesto 2 = " + str(listaLike[1])
        print "verosimiglianza gesto 3 = " + str(listaLike[2])
        # print "verosimiglianza gesto 4 = " + str(lista[3])
        maxValue = l1
        gesto = "--GESTO 1--"
        i = 0
        while i < len(listaLike):
            if (listaLike[i] > maxValue):
                maxValue = listaLike[i]
                if i == 1:
                    gesto = "--GESTO 2--"
                elif i == 2:
                    gesto = "--GESTO 3--"
                    # elif i == 3:
                    # gesto = "gesto4"

            i += 1

        print "Stai effettuando il " + gesto
        before = gesto
        listaGesti.append([gesto, maxValue, before])
        # cancelliamo gli elementi dalla lista
        del lista[0:shift]
    print listaGesti
    gesto = listaGesti[0]
    resultGesti = []
    for elem in listaGesti[1::]:
        try:
            if elem[2] == gesto[2] and elem[1] > gesto[1]:
                gesto[0] = "--NULLA--"
            elif elem[2] == gesto[2] and elem[1] <= gesto[1]:
                elem[0] = "--NULLA--"
            gesto = elem
        except IndexError:
            print "index out of bound"

    print listaGesti
    return listaGesti

def printListaGesti(listaGesti):
    for elem in listaGesti:
        if elem[0] != "--NULLA--":
            print elem[0] + str(elem[1])



def computeLikelihood4(listaPoints, model1, model2, model3, centroids):
    # creiamo il vettore che contiene tutte le osservazioni
    #print len(listaPoints)
    #print listaPoints
    lista = []
    for elem in listaPoints:
        for subElem in elem:
            xa = float(subElem["x_acc"])
            ya = float(subElem["y_acc"])
            za = float(subElem["z_acc"])
            xg = float(subElem["x_gir"])
            yg = float(subElem["y_gir"])
            zg = float(subElem["z_gir"])
            lista.append([xa, ya, za, xg, yg, zg])

    listaGesti = []

    points = np.vstack(lista)

    l1 = model1.getLikelihoodFromPoints(points, centroids)
    l2 = model2.getLikelihoodFromPoints(points, centroids)
    l3 = model3.getLikelihoodFromPoints(points, centroids)

    listaLike = [l1, l2, l3]
    #print "verosimiglianza gesto 1 = " + str(listaLike[0])
    #print "verosimiglianza gesto 2 = " + str(listaLike[1])
    #print "verosimiglianza gesto 3 = " + str(listaLike[2])
    # print "verosimiglianza gesto 4 = " + str(lista[3])
    maxValue = l1
    gesto = "--GESTO 1--"
    i = 0
    while i < len(listaLike):
        if (listaLike[i] > maxValue):
            maxValue = listaLike[i]
            if i == 1:
                gesto = "--GESTO 2--"
            elif i == 2:
                gesto = "--GESTO 3--"
                # elif i == 3:
                # gesto = "gesto4"

        i += 1

    string = "Stai effettuando il " + gesto

    '''
        before = gesto
        listaGesti.append([gesto, maxValue, before])
        print listaGesti
        gesto = listaGesti[0]
        resultGesti = []
        for elem in listaGesti[1::]:
            try:
                if elem[2] == gesto[2] and elem[1] > gesto[1]:
                    gesto[0] = "--NULLA--"
                elif elem[2] == gesto[2] and elem[1] <= gesto[1]:
                    elem[0] = "--NULLA--"
                gesto = elem
            except IndexError:
                print "index out of bound"

        print listaGesti
        return listaGesti
        '''

    #print string
    return string, maxValue

