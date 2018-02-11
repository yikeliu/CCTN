import glob
import json
from math import log
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import prettyplotlib as ppl
"""
Compute the pagerank / degree ratio for each phone number and time stamp.

output:
    p * t matrix, p: # phone numbers, t: # time stamps
"""

def findMax(inputfiles):
    # find size of time stamps
    maxStamp = 0
    for inputfile in inputfiles:
        stamp = int(inputfile.split('/')[-1].split('.')[1].split('phone')[-1])
        #stamp = inputfile.split('/')[-1].split('.')[1].split('phone')[-1]
        #print stamp
        maxStamp = max(stamp, maxStamp)
    return maxStamp + 1

def findDegree(inputfile):
    f = open(inputfile, 'r')
    dgDict = {}
    for line in f.readlines():
        line = line.split('\t')
        node = line[0]
        degree = int(line[1])
        if not dgDict.get(node):
            dgDict[node] = degree
    return dgDict


def computeMatrix(inputfiles, size, optPlot):
    # compute the pagerank / degree list for one phone number
    matrix = {}
    # add separate files for degree and pagerank
    matrixDg = {}
    matrixPr = {}
    if optPlot:
        pr = []
        dg = []
        minDg = 1000
        maxDg = 0
    for inputfile in inputfiles:
        stamp = int(inputfile.split('/')[-1].split('.')[1].split('phone')[-1])
        mapfile = inputfile.split('tab')[0] + 'int_rev-dict'
        fmap = open(mapfile, 'r')
        intDict = json.load(fmap)
        fi = open(inputfile, 'r')
        degreefile = inputfile.split('.tab')[0] + '.int.degree'
        dgDict = findDegree(degreefile)
        for i in range(3):
            fi.next()
        for line in fi:
            line = line.split('\t')
            nodeId = line[0]
            nodeId = intDict[nodeId]
            #degree = float(line[1])
            pagerank = float(line[7])
            degree = dgDict[line[0]]
            ratio = pagerank / degree
            if not matrix.get(nodeId):
                matrix[nodeId] = [0.] * size
                matrix[nodeId][stamp] = ratio
            else:
                matrix[nodeId][stamp] = ratio
            # add to degree and pagerank matrices
            if not matrixDg.get(nodeId):
                matrixDg[nodeId] = [0] * size
                matrixDg[nodeId][stamp] = ratio
            else:
                matrixDg[nodeId][stamp] = ratio
            if not matrixPr.get(nodeId):
                matrixPr[nodeId] = [0.] * size
                matrixPr[nodeId][stamp] = ratio
            else:
                matrixPr[nodeId][stamp] = ratio
            if optPlot:
                if stamp == size - 1:
                    pr.append(pagerank)
                    dg.append(degree)
                    maxDg = max(degree, maxDg)
                    minDg = min(degree, minDg)
    if optPlot:
        return minDg, maxDg, pr, dg
    return matrix, matrixDg, matrixPr

def plotPagerankDegree(minDg, maxDg, pr, dg, plotBin):
    # plot the pagerank vs. degree of last time stamp
    if plotBin:
        degrees = []
        #d = log(minDg, 2)
        d = minDg
        while d < maxDg:#log(maxDg, 2):
            #d += 1
            d += 40
            degrees.append(d)
        #degrees.append(log(maxDg, 2))
        print degrees
        pageranks = [[] for i in range(len(degrees))]
        n = len(pr)
        for i in range(n):
            j = 0
            for j in range(len(degrees)):
                #if log(dg[i], 2) <= degrees[j]:
                if dg[i] <= degrees[j]:
                    break
            pageranks[j].append(pr[i])
        #print pageranks
        medPr = []
        avgPr = []
        minPr = []
        maxPr = []
        for i in range(len(degrees)):
            medPr.append(np.median(pageranks[i]))
            avgPr.append(np.mean(pageranks[i]))
            minPr.append(np.mean(pageranks[i]) - min(pageranks[i]))
            maxPr.append(max(pageranks[i]) - np.mean(pageranks[i]))
        fig = plt.figure()
        plt.plot(degrees, medPr, label='Median pagerank')
        plt.errorbar(degrees, avgPr, yerr=[minPr, maxPr], fmt='o', label='Mean pagerank')
        #plt.xlabel('Log(degree)', fontsize=16)
        plt.xlabel('Degree', fontsize=16)
        plt.ylabel('Pagerank', fontsize=16)
        #pylab.xlim([0, 11])
        pylab.legend(loc='upper right')
        fig.savefig('../Data/pagerank_vs_degree.jpg')
    else:
        fig = plt.figure()
        #plt.scatter(dg, pr)
        ppl.scatter(dg, pr)
        #plt.xlabel('Log(degree)', fontsize=16)
        plt.xlabel('Degree', fontsize=16)
        plt.ylabel('Pagerank', fontsize=16)
        plt.xscale('log')
        plt.yscale('log')
        #heatmap, xedges, yedges = np.histogram2d(dg, pr, bins = 50)
        #extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #plt.clf()
        #plt.imshow(heatmap, extent = extent)
        #plt.show()
        #pylab.xlim([0, 11])
        pylab.ylim([1e-6, 1e-3])
        #pylab.legend(loc='upper right')
        fig.savefig('../Data/pagerank_vs_degree_scatter.jpg')

    return

def plotSampleTrend(data, matrix):
    stats = []
    n = len(data)
    for nodeId in data:
        stats.append(matrix[nodeId])

    fig = plt.figure()
    for i in range(n):
        plt.plot(range(len(stats[i])), stats[i], label=data[i])
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Pagerank/degree', fontsize=16)
    pylab.legend(loc='upper left')
    fig.savefig('../Data/sample_trend_ratio.jpg')
    return

def printMatrix(data, outputfile):
    f = open(outputfile, 'w')
    for phone in data:
        f.write(phone)
        for value in data[phone]:
            f.write('\t' + str(value))
        f.write('\n')
    f.close()
    return

if __name__ == '__main__':
    inputtype = '../Data/Temporal/*.tab'
    inputfiles = glob.glob(inputtype)
    #outputfile = '/data/Data/structural_matrix.json'
    outputfile = '../Data/structural_matrix.txt'
    outputfileDg = '../Data/degree_matrix.txt'
    outputfilePr = '../Data/pagerank_matrix.txt'
    #fo = open(outputfile, 'w')
    size = findMax(inputfiles)
    #minDg, maxDg, pr, dg = computeMatrix(inputfiles, size, True)
    #print pr, dg
    matrix, matrixDg, matrixPr = computeMatrix(inputfiles, size, False)
    #matrix = json.load('../Data/structural_matrix.json')
    #plotPagerankDegree(minDg, maxDg, pr, dg, False)
    #data = ['1-4157382305', '1-4157382314', '1-4089070127', '1-2064073519', '1-2064186542']
    #data = ['1-2408416387', '1-4084163877', '1-4089077677', '1-2064073519', '1-2064186542']
    #plotSampleTrend(data, matrix, False)
    #json.dump(matrix, fo, indent=4)
    #printMatrix(matrix, outputfile)
    printMatrix(matrixDg, outputfileDg)
    printMatrix(matrixPr, outputfilePr)
