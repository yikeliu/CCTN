import sys
import re
import collections
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import generate_graphs as Graph
import json
import config
import fileinput
import numpy as np
"""
This file plot the size distribution of connected component and extracts the
largest component and generate its edge list.

input:
    name of edge list file, size of time bins (in day), size of time stamps (in
    day), raw datafile(s)
"""

def plotSize(inputedgefile, optPlot):
    # plot number vs. size of connected components
    ccfile = inputedgefile + '.int_new.txt.cc'
    fcc = open(ccfile, 'r')
    cc = {}
    maxId = -1
    maxSize = 0
    for line in fcc.readlines():
        #print line
        ccId = int(re.split(' |\t', line)[1])
        if not cc.get(ccId):
            cc[ccId] = 1
        else:
            cc[ccId] += 1
        if cc[ccId] > maxSize:
            maxId = ccId
            maxSize = cc[ccId]
    sizes = cc.values()
    avgSize = np.mean(sizes)
    # check max size too
    maxSize = max(sizes)
    sizeDistr = collections.Counter(sizes)
    siz = []
    num = []
    for s in sizeDistr:
        siz.append(s)
        num.append(sizeDistr[s])
    if optPlot:
        fig = plt.figure()
        plt.scatter(siz, num)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Size', fontsize=16)
        plt.ylabel('Count', fontsize=16)
        #fig.savefig('../Data/' + inputfile + '.num_size_cc.jpg')
        fig.savefig(inputedgefile + '.num_size_cc.eps')
    fcc.close()
    return maxId, avgSize, maxSize

def extractComp(maxId, inputedgefile):
    # extract the edge list of largest connected component
    #print maxId
    ccfile = inputedgefile + '.int_new.txt.cc'
    fcc = open(ccfile, 'r')
    subNodes = []
    for line in fcc.readlines():
        ccId = int(re.split(' |\t', line)[1])
        nodeId = int(re.split(' |\t', line)[0])
        if ccId == maxId:
            subNodes.append(nodeId)
    #print subNodes, len(subNodes)
    edgefile = inputedgefile + '.int'
    subEdgefile = edgefile + '.subedges'
    fi = open(edgefile, 'r')
    fo = open(subEdgefile, 'w')
    fi.next()
    for line in fi:
        node1 = int(line.split(' ')[0])
        node2 = int(line.split(' ')[1])
        if node1 in subNodes and node2 in subNodes:
            fo.write(line)
    fcc.close()
    fi.close()
    fo.close()
    return subNodes

def convertToString(subNodes, inputedgefile):
    f = open(inputedgefile + '.int_rev-dict')
    intDict = json.load(f)
    return [intDict[str(x)] for x in subNodes]

def generateSubgraphs(data, stamps, subNodes, outputfilePWP):
    # generate subgraphs containing only nodes in the gcc with each time stamp
    n = len(stamps)
    phones = defaultdict(list)
    phoneConcurrences = {}
    for post in data:
        page = post['uri'].split('/')[-1]
        if post.get('mentions'):
            infos = post['mentions']
            time = post['dateCreated'].split('T')[0]
            year = time.split('-')[0]
            month = time.split('-')[1]
            day = time.split('-')[2]
            if len(infos) >= 2:
                numPhones = 0
                phoneNums = []
                for info in infos:
                    info = info.split('/')[5:]
                    #print info
                    if 'phone' in info:
                        phoneNum = info[-1]
                        if phoneNums and phoneNum in subNodes:
                            for number in phoneNums:
                                #foPWP.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                                if not phoneConcurrences.get((number, phoneNum)) and not phoneConcurrences.get((phoneNum, number)):
                                    phoneConcurrences[(number, phoneNum)] = 1
                                    if config.optTemporal:
                                        #print year, month, day
                                        for i in range(1, n): # data not sorted by date
                                            if int(year) < stamps[i][0] or (int(year) == stamps[i][0] and int(month) < stamps[i][1]) or (int(year) == stamps[i][0] and int(month) == stamps[i][1] and int(day) <= stamps[i][2]):
                                                #print 'writing to stamp file...' + str(i - 1)
                                                outputfile = outputfilePWP + '.subedges' +  str(i - 1)
                                                fo = open(outputfile, 'a')
                                                fo.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                                                fo.close()
                                                # aggregate graph for this analysis
                                                #break
                                elif phoneConcurrences.get((number, phoneNum)):
                                    phoneConcurrences[(number, phoneNum)] += 1
                                else: phoneConcurrences[(phoneNumber, number)] += 1
                        phoneNums.append(phoneNum)
    return

if __name__ == '__main__':
    inputedgefile = sys.argv[1]
    maxId, avgSize, maxSize = plotSize(inputedgefile, True)
    """
    subNodes = extractComp(maxId, inputedgefile)
    subNodes = convertToString(subNodes, inputedgefile)
    if config.optMultiple:
        inputfile = sys.argv[4:]
    else:
        inputfile = sys.argv[4]
    binSize = int(sys.argv[2])
    stampSize = int(sys.argv[3])
    data = []
    if config.optMultiple:
        fi = fileinput.input(files=tuple(inputfile))
        #print 'Multiple files loaded'
        for line in fi:
            #print 'loading line: ' + line
            line = json.loads(line)
            data.append(line)
    else:
        fi = open(inputfile, 'r')
        for line in fi.readlines():
            line = json.loads(line)
            data.append(line)
            #print data

    print 'Data loaded.'

    # output edge lists
    if config.optMultiple:
        #inputfile = '/data/Data/all'
        inputfile = '../Data/all'
    outputfilePWP = inputfile + '.phone-page-phone.edges'

    minYear, minMonth, minDay, maxYear, maxMonth, maxDay = Graph.findMinMaxTime(data)
    if config.optTemporal:
        stamps, outputfilePPPStamps, outputfilePWPStamps = Graph.createStamps(minYear, minMonth,minDay, maxYear, maxMonth, maxDay, stampSize, inputfile)
    generateSubgraphs(data, stamps, subNodes, outputfilePWP)
    """
