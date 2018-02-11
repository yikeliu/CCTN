"""
Given the two feature matrices, compute cluster assignmen.
"""
import numpy as np
from numpy import linalg as LA
import scipy as sp

def computeLaplacian(G):
    # compute Laplcacian matrix of matrix G
    return sp.sparse.csgraph.laplacian(G)

def updateW(Wold, Xstruct, Xcontent, C, Iv, aStruct, aContent):
    # update weight matrix W
    # TODO: define Iv
    A = aStruct * np.transpose(Xstruct) * Xstruct + aContent * np.transpose(Xcontent) * Xcontent
    b = aStruct * np.transpose(Xstruct) * C + aContent * np.transpose(Xcontent) * C
    diff = 0
    for i in range(len(Wold)):
        diff += Iv[i] * (b[i] - A[i] * Wold) / ((LA.norm(A[i], 2)) ** 2) * np.transpose(A[i])
    return Wold + diff

def updateC(Cold, Xstruct, Xcontent, L, W, aStruct, aContent, lamb):
    # update cluster assignment C
    A = lamb * L + np.identity(len(L))
    b = aStruct * Xstruct * W + aContent * Xcontent * W
    diff = 0
    for i in range(len(C)):
        diff += Iv[i] * (b[i] - A[i] * Cold) / ((LA.norm(A[i], 2)) ** 2) * np.transpose(A[i])
    return Cold + diff

def runClustering(G, Xstruct, Xcontent):
    # run co-clustering on feature matrices, return cluster assignment
    # initialization
    C = np.array
    while delta >= 10^-3 and t <= 1000:


if __name__ == '__main__':

