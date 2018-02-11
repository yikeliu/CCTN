"""
Compute the Euclidean distance and Dynamic Time Warping distance for sequence
pairs.

input:
    .json file of matrix, chosen distance measure(E for Euclidean, D for DTW)

output:
    square matrix of distances
"""

import numpy as np
from dtw.dtw import dtw
import json
import sys

def computeEuclidean(sequences):
    # compute Euclidean distance of two sequences
    n = len(sequences)
    D = [[None] * n for i in range(n)]
    for i in range(n):
        D[i][i] = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(np.array(sequences[i]) - np.array(sequences[j]))
            D[i][j] = D[j][i] = d
    return D

def computeDTW(sequences):
    n = len(sequences)
    D = [[None] * n for i in range(n)]
    for i in range(n):
        x = y = np.array(sequences[i]).reshape(-1, 1)
        d, cost, acc, path = dtw(x, y, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
        D[i][i] = d
    for i in range(n):
        for j in range(i + 1, n):
            x = np.array(sequences[i]).reshape(-1, 1)
            y = np.array(sequences[j]).reshape(-1, 1)
            d, cost, acc, path = dtw(x, y, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
            D[i][j] = D[j][i] = d
    return D

if __name__ == '__main__':
    inputfile = sys.argv[1]
    method = sys.argv[2]
    fi = open(inputfile, 'r')
    matrix = json.load(fi)
    data = ['1-4157382305', '1-4157382314', '1-4089070127', '1-2064073519', '1-2064186542']
    sequences = []
    keys = []
    for key in data:
        keys.append(key)
        sequences.append(matrix[key])
    print keys
    if method == 'E':
        print computeEuclidean(sequences)
    if method == 'D':
        print computeDTW(sequences)
