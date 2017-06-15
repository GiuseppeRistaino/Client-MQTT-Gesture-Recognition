import os


def getLista(path):
    lista = []
    files = os.listdir(path)
    #print files
    for file in files:
        with open(path+file) as openfileobject:
            #openfileobject.readline()
            for line in openfileobject:
                vector = line.split(",")
                xa = float(vector[0])
                ya = float(vector[1])
                za = float(vector[2])
                xg = float(vector[3])
                yg = float(vector[4])
                zg = float(vector[5])
                lista.append([xa, ya, za, xg, yg, zg])
            #print lista.__len__()
    #print lista
    return lista


def getListPointsForPlotAcc(file):
    listaX = []
    listaY = []
    listaZ = []
    with open(file) as openfileobject:
        openfileobject.readline()
        for line in openfileobject:
            vector = line.split(",")
            x = float(vector[0])
            y = float(vector[1])
            z = float(vector[2])
            listaX.append(x)
            listaY.append(y)
            listaZ.append(z)
        #print listaX.__len__()
    print listaX
    return listaX, listaY, listaZ


def getListPointsForPlotGir(file):
    listaX = []
    listaY = []
    listaZ = []
    with open(file) as openfileobject:
        openfileobject.readline()
        for line in openfileobject:
            vector = line.split(",")
            x = float(vector[3])
            y = float(vector[4])
            z = float(vector[5])
            listaX.append(x)
            listaY.append(y)
            listaZ.append(z)
        #print listaX.__len__()
    print listaX
    return listaX, listaY, listaZ