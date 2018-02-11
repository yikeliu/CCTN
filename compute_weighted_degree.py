"""
Compute weighted degree of input edge list.

input:
    weighted edge list
output:
    list file where each number indicates the weighted degree of the
    corresponding node
"""
import sys

def computeDegree(inputfile):
    f = open(inputfile, 'r')
    degDict = {}
    for line in f.readlines():
        line = line.split(' ')
        node1 = line[0]
        node2 = line[1]
        weight = line[2]
        if '.' in weight:
            weight = float(weight)
        else: weight = int(weight)
        if degDict.get(node1):
            degDict[node1] += weight
        else:
            degDict[node1] = weight
        if degDict.get(node2):
            degDict[node2] += weight
        else:
            degDict[node2] = weight
    f.close()
    return degDict

def printDegree(outputfile, degDict):
    f = open(outputfile, 'w')
    for node in degDict:
        f.write(node + '\t' + str(degDict[node] / 2) + '\n')
    return

if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = inputfile + '.degree'
    degrees = computeDegree(inputfile)
    printDegree(outputfile, degrees)
