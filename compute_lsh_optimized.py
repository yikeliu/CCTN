'''
Compute LSH score for each set of descriptions.
'''

from hashlib import sha1
import numpy as np
from datasketch.minhash import MinHash
from datasketch.weighted_minhash import WeightedMinHashGenerator
from datasketch.lsh import WeightedMinHashLSH, MinHashLSH
import find_lsh_dup as Group
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import json

data1 = ['minhash', 'is', 'a', 'probabilistic', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'datasets']
data2 = ['minhash', 'is', 'a', 'probability', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'documents']
data3 = ['minhash', 'is', 'probability', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'documents']
#data3 = ['test', 'data']

v1 = np.random.uniform(1, 10, 10)
v2 = np.random.uniform(1, 10, 10)
v3 = np.random.uniform(1, 10, 10)

def eg1():
    m1 = MinHash()
    m2 = MinHash()
    m3 = MinHash()
    for d in data1:
        m1.update(d.encode('utf8'))
    for d in data2:
        m2.update(d.encode('utf8'))
    for d in data3:
        m3.update(d.encode('utf8'))

    # Create LSH index
    lsh = MinHashLSH(threshold=0.5)
    lsh.insert("m2", m2)
    lsh.insert("m3", m3)
    print lsh
    result = lsh.query(m1)
    print m1.jaccard(m2)
    print("Approximate neighbours with Jaccard similarity > 0.5", result)

def eg2():
    mg = WeightedMinHashGenerator(10, 5)
    m1 = mg.minhash(v1)
    m2 = mg.minhash(v2)
    m3 = mg.minhash(v3)
    print m1, m2, m3
    print("Estimated Jaccard m1, m2", m1.jaccard(m2))
    print("Estimated Jaccard m1, m3", m1.jaccard(m3))
    # Create LSH index
    lsh = WeightedMinHashLSH(threshold=0.7, sample_size=5)
    lsh.insert("m2", m2)
    lsh.insert("m3", m3)
    result = lsh.query(m1)
    print("Approximate neighbours with weighted Jaccard similarity > 0.1", result)

def computeLSH(docs):
    # given the duplicates given by groups, compute lsh score for all pairs,
    # average out by # possible pairs
    n = len(docs)
    numPairs = n * (n - 1) / 2
    m = []
    for i in range(n):
        mEntry = MinHash()
        doc = docs[i].decode('utf-8').split()
        #print doc
        for word in doc:
            mEntry.update(word.encode('utf8'))
        #print i, m[i]
        m.append(mEntry)

    # Create LSH index
    lsh = MinHashLSH(threshold=0.7)

    for i in range(n):
        lsh.insert(i, m[i])
    result = {}
    # boolean array to track nodes
    lshCheck = [False] * n
    for i in range(n):
        #print m[i]
        if lshCheck[i]:
            continue
        else:
            group = lsh.query(m[i])
            #print group
            for idx in group:
                lshCheck[idx] = True
            gSize = len(group)
            for j in range(gSize):
                for k in range(j + 1, gSize):
                    #if result.get((m[group[j]], m[group[k]])):
                    #    continue
                    #elif result.get((m[group[k]], m[group[j]])):
                    #    continue
                    #else:
                    #    #print m[group[j]], m[group[k]]
                    score = m[group[j]].jaccard(m[group[k]])
                    result[(m[group[j]], m[group[k]])] = score
    result = result.values()
    if numPairs == 0:
        similarity = 0
    else:
        similarity = sum(result) / numPairs
    return similarity

def plotSampleTrend(data, matrix):
    stats = []
    n = len(data)
    for nodeId in data:
        stats.append(matrix[nodeId])

    fig = plt.figure()
    for i in range(n):
        plt.plot(range(len(stats[i])), stats[i], label=data[i])
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Avg Jaccard similarity', fontsize=16)
    pylab.legend(loc='upper right')
    #plt.xlim(1800, 1950)
    fig.savefig('/data/Data/sample_trend_lsh.jpg')
    return

if __name__ == '__main__':
    #outputfolder = '/data/Data/Description_Out/'
    outputfile = '/data/Data/lsh_matrix.json'
    fo = open(outputfile, 'w')
    inputfolder = '/data/Data/Description/'
    files = os.listdir(inputfolder)
    # find size of time stamps
    maxStamp = 0
    for inputfile in files:
        stamp = int(inputfile.split('.')[-1])
        maxStamp = max(stamp, maxStamp)
    size = maxStamp + 1
    print size
    matrix = {}
    #data = ['1-4157382305', '1-4157382314', '1-4089070127', '1-2064073519', '1-2064186542']
    data = ['1-2408416387', '1-4084163877', '1-4089077677', '1-2064073519', '1-2064186542']
    for inputfile in files:
        #print inputfile
        nodeId = inputfile.split('.')[1]
        #if not nodeId in data: continue
        stamp = int(inputfile.split('.')[2])
        fi = open(inputfolder + inputfile, 'r')
        docs = fi.read().splitlines()
        print inputfile
        score = computeLSH(docs)
        if not matrix.get(nodeId):
            matrix[nodeId] = [0.] * size
            matrix[nodeId][stamp] = score
        else:
            matrix[nodeId][stamp] = score
        #print matrix[nodeId]
    #print matrix[nodeId]
    json.dump(matrix, fo, indent=4)

    plotSampleTrend(data, matrix)
    # uncomment code below for debug purpose
    #inputfile = 'all.1-8186609498.6'
    #fi = open(inputfolder + inputfile, 'r')
    #docs = fi.read().splitlines()
    #outputfile = inputfile + '.out'
    #fo = open(outputfolder + outputfile, 'w')
    #computeLSH(docs)
    #inputfile = '/data/Data/Description/all.1-9292643965.2'
    #fi = open(inputfile, 'r')
    #docs = fi.read().splitlines()
    #print computeLSH(docs)

