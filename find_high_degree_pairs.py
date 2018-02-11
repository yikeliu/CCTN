import sys
import collections
import subprocess
import config
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
"""
This file finds high degree nodes and their common neighbors, plot degree
distribution and generate plots on the clustering results.

input: input file name
"""

# degree of node to find
if config.optCommNeigh:
    minDeg = 10

# read input file
inputfile = sys.argv[1]
fi = open(inputfile, 'r')
#outputfolder = '../Data/static-seller-phone-seller/output/'
#outputfolder = '../Data/'
outputfolder = '/data/Data/'

# degree distribution
degrees = []


# preprocess input file
nodeDict = collections.defaultdict(list) # [nodeID map to number, neighbor nodeIDs]
numNodes = 0
for line in fi.readlines():
    #print line
    node1 = line.split('\t')[0]
    node2 = line.split('\t')[1].split('\n')[0]
    if not nodeDict.get(node1):
        numNodes += 1
        nodeDict[node1].append(numNodes - 1)
        nodeDict[node1].append(node2)
    else:
        nodeDict[node1].append(node2)
    if not nodeDict.get(node2):
        numNodes += 1
        nodeDict[node2].append(numNodes - 1)
        nodeDict[node2].append(node1)
    else:
        nodeDict[node2].append(node1)

# output for cpp code
#outputfile = outputfolder + inputfile.split('/')[-1] + '.input'
#fo = open(outputfile, 'w')
#fo.write(str(numNodes) + '\n')
if config.optCommNeigh:
    outputPair = outputfolder + inputfile.split('/')[-1] + '.pairs'
    outputneighor = outputfolder + inputfile.split('/')[-1] + '.neighbors'
    foPair = open(outputPair, 'w')
    foNeigh = open(outputneighor, 'w')
degreeDict = {}
for node in nodeDict:
    degree = len(nodeDict[node]) - 1
    degrees.append(degree)
    degreeDict[node] = degree
    #fo.write(str(nodeDict[node][0]) + ',' + str(degree))
    #neighbors = []
    #for neighbor in nodeDict[node][1:]:
    #    neighborID = nodeDict[neighbor][0]
    #    neighbors.append(neighborID)
    #neighbors = sorted(neighbors)
    #for neighbor in neighbors:
    #    fo.write(':' + str(neighbor))
    #fo.write('\n')
    # high degree node 1, high degree node 2, common neighbor
    if config.optCommNeigh:
        neighs = nodeDict[node][1:]
        n = len(neighs)
        i = j = 0
        for i in range(n):
            for j in range (i + 1, n):
                if len(nodeDict[neighs[i]]) - 1 >= minDeg and len(nodeDict[neighs[j]]) - 1 >= minDeg:
                    foPair.write(neighs[i] + '\t' + neighs[j] + '\t' + node +  '\n')

nodeSorted = sorted(degreeDict, key = degreeDict.__getitem__, reverse = True)
for node in nodeSorted:
        neighs = nodeDict[node][1:]
        foNeigh.write(node + ' : ')
        n = len(neighs)
        for i in range(n):
            foNeigh.write(neighs[i] + ' ')
        foNeigh.write('\n')

# print degrees
#print sorted(degrees, reverse = True)

fi.close()
#fo.close()
if config.optCommNeigh:
    foPair.close()
    foNeigh.close()

# plot degree distribution
degreeDistr = collections.Counter(degrees)
#print degreeDistr
deg = []
count = []
for d in degreeDistr:
    deg.append(d)
    count.append(degreeDistr[d])
fig = plt.figure()
plt.scatter(deg, count)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Degree', fontsize=16)
plt.ylabel('Count', fontsize=16)
#fig.savefig('../Data/' + inputfile + '.degree_distribution.jpg')
fig.savefig(inputfile + '.degree_distribution.jpg')
