# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pylab
import csv
import random


np.random.seed(0)


def initialize_clusters(points, k):
    """Initializes clusters as k randomly selected points from points."""
    return points[np.random.randint(points.shape[0], size=k)]


# Function for calculating the distance between centroids
def get_distances(centroid, points):
    """Returns the distance the centroid is from each data point in points."""
    return np.linalg.norm(points - centroid, axis=1)

def closest_centroid(points, centroids):
    distances = np.sqrt(((points - centroids[:, np.newaxis])**2).sum(axis=2))
    return np.argmin(distances, axis=0)

def computeValues(points):

    k = 5
    maxiter = 50

    # Inizializziamo i centroidi in modo randomico
    centroids = initialize_clusters(points, k)

    classes = np.zeros(points.shape[0], dtype=np.float64)
    distances = np.zeros([points.shape[0], k], dtype=np.float64)

    # Loop per il massimo numero di iterazioni
    for i in range(maxiter):

        # Assegna tutti i punti (osservazioni) al centroide più vicino
        for i, c in enumerate(centroids):
            distances[:, i] = get_distances(c, points)

        # Determina la classe di appartenenza (Cluster) per ciascun punto mediante il centroide più vicino
        classes = np.argmin(distances, axis=1)

        # Aggiorna i centroidi spostandoli alla locazione migliore per ciascun cluster
        for c in range(k):
            centroids[c] = np.mean(points[classes == c], 0)

    listClosestCentroid = closest_centroid(points, centroids).tolist()
    #Rimuove la virgola nell'array
    closestCentroid = np.array(listClosestCentroid)

    return centroids, closestCentroid

def saveCentroids(fileName, centroids):
    with open(fileName, "wb") as f:
        wr = csv.writer(f)
        wr.writerows(centroids)

def loadCentroids(fileName):
    with open(fileName) as f:
        rows = csv.reader(f)
        floatRows = []
        for row in rows:
            floatRows.append([float(elem) for elem in row])
        centroids = np.array(list(floatRows))
    return centroids
