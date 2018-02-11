"""
Find phone numbers matrices have in common, reprint matrices.

input:
    txt files of matrices
output:
    filtered matrices
"""
import sys
import json

def findCommSet(keysets):
    # find maximum common set of keys
    n = len(keysets)
    commkeys = set(keysets[0])
    for i in range(1, n):
        commkeys = commkeys & set(keysets[i])
    return list(commkeys)

def getkeys(inputfile):
    f = open(inputfile, 'r')
    keys = []
    for line in f.readlines():
        key = line.split('\t')[0]
        keys.append(key)
    f.close()
    return keys

def printMatrix(inputfile, keys):
    outputfile = inputfile + '.filtered'
    fi = open(inputfile, 'r')
    fo = open(outputfile, 'w')
    for line in fi.readlines():
        key = line.split('\t')[0]
        if key in keys:
            fo.write(line)
    fi.close()
    fo.close()
    return

def printIdx(keys):
    outputfile = '../Data/filtered_index.json'
    f = open(outputfile, 'w')
    keyDict = {}
    i = 0
    for key in keys:
        i += 1
        keyDict[key] = i
    json.dump(keyDict, f, indent=4)
    f.close()
    return keyDict

def printAdjacency(inputfile, keys, keyDict):
    fi = open(inputfile, 'r')
    outputfile = inputfile + '.filtered'
    fo = open(outputfile, 'w')
    for line in fi.readlines():
        line = line.split('\t')
        node1 = line[0]
        node2 = line[1]
        weight = line[2]
        if node1 in keys and node2 in keys:
            fo.write(str(keyDict[node1]) + '\t' + str(keyDict[node2]) + '\t' + weight)
    fi.close()
    fo.close()
    return

if __name__ == '__main__': 
    inputfiles = sys.argv[1:]
    keysets = []
    for inputfile in inputfiles:
        keys = getkeys(inputfile)
        keysets.append(keys)
    commkeys = findCommSet(keysets)
    for inputfile in inputfiles:
        printMatrix(inputfile, commkeys)
    keyDict = printIdx(commkeys)
    printAdjacency('../Data/all.phone-page-phone.edges', commkeys, keyDict)

