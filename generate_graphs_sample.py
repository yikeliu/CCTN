import json
import sys
from collections import defaultdict
import config
import matplotlib.pyplot as plt
"""
This file loads in the .json data files and generate projection graphs, plot #
nodes vs. time stamp.

input:
    datafile, size of time bins (in day), size of time stamps (in day)
"""
# TODO: fix the binSize issue

def findMinMaxTime(data):
    # check time range, set up time stamps
    minYear = 9999
    minMonth = 99
    minDay = 99
    maxYear = 0000
    maxMonth = 00
    maxDay = 00
    bins = []
    for post in data:
        page = post['_source']
        if page.get('mentions'):
            infos = page['mentions']
            time = page['dateCreated'].split('T')[0]
            year = int(time.split('-')[0])
            month = int(time.split('-')[1])
            day = int(time.split('-')[2])
            if year < minYear:
                minYear = year
                minMonth = month
                minDay = day
            elif year == minYear:
                if month < minMonth:
                    minMonth = month
                    minDay = day
                elif month == minMonth:
                    if day < minDay:
                        minDay = day
            if year > maxYear:
                maxYear = year
                maxMonth = month
                maxDay = day
            elif year == maxYear:
                if month > maxMonth:
                    maxMonth = month
                    maxDay = day
                elif month == maxMonth:
                    if day > maxDay:
                        maxDay = day
    #print minYear, maxYear
    #print minMonth, maxMonth
    #print minDay, maxDay
    return minYear, minMonth, minDay, maxYear, maxMonth, maxDay

def createStamps(minYear, minMonth, maxYear, maxMonth, maxDay):
    year = minYear
    month = minMonth
    day = 1
    stamps = []
    if config.optTemporal:
        while year <= maxYear and month <= maxMonth and day <= maxDay:
            stamps.append((year, month, day))
            if day + stampSize > 31:
                if month == 12:
                    year += 1
                else:
                    month += 1
            else:
                day += stampSize
        stamps.append((maxYear, maxMonth, maxDay))
        print stamps
        n = len(stamps) - 1
        outputfilePPPStamps = []
        for i in range(n):
            outputfilePPPStamps.append('../Data/page-phone-page' + str(i) + '.edges')
        return stamps, outputfilePPPStamps

def generatePageGraphs(data, stamps, foPPP, foPEP, outputfilePPPStamps):
    # project on webpages, connected if two pages have same phone / email
    # edge weight = frequency of cocurrence + 1
    n = len(stamps)
    phones = defaultdict(list)
    emails = defaultdict(list)
    if config.optTemporal:
        tempNodes = [set() for i in range(n)]
        tempPhones = [set() for i in range(n)]
    for post in data:
        page = post['_source']
        if page.get('mentions'):
            infos = page['mentions']
            time = page['dateCreated'].split('T')[0]
            year = time.split('-')[0]
            month = time.split('-')[1]
            day = time.split('-')[2]
            for info in infos:
                if 'phone' in info:
                    phoneNum = info.split('/')[-1]
                    newId = post['_id'].split('/')[-1]
                    foPP.write(phoneNum + '\t' + newId + '\n')
                    if phones[phoneNum]:
                        for pageTime in phones[phoneNum]:
                            edgeWeight = 1
                            #if pageTime[1] == time:
                            oldTime = pageTime[1]
                            oldYear = oldTime.split('-')[0]
                            oldMonth = oldTime.split('-')[1]
                            oldDay = oldTime.split('-')[2]
                            if oldYear == year and oldMonth == month and abs(int(oldDay) - int(day)) <= binSize / 2 :
                                edgeWeight += 1
                            #if edgeWeight > 1:
                            #    print 'phone conccurence: ' + str(edgeWeight)
                            foPPP.write(pageTime[0] + ',' + newId + ',' + str(edgeWeight) + '\n')
                            if config.optTemporal:
                                #print year, month, day
                                for i in range(1, n): # data not sorted by date
                                    if int(year) < stamps[i][0] or (int(year) == stamps[i][0] and int(month) < stamps[i][1]) or (int(year) == stamps[i][0] and int(month) == stamps[i][1] and int(day) < stamps[i][2]):
                                        #print 'writing to stamp file...' + str(i - 1)
                                        foPPPStamp = open(outputfilePPPStamps[i - 1], 'a')
                                        foPPPStamp.write(pageTime[0] + ',' + newId + ',' + str(edgeWeight) + '\n')
                                        tempNodes[i - 1].add(pageTime[0])
                                        tempNodes[i - 1].add(newId)
                                        tempPhones[i - 1].add(phoneNum)
                                        foPPPStamp.close()
                    phones[phoneNum].append((newId, time))
                if 'email' in info:
                    emailAdd = info.split('/')[-1]
                    newId = post['_id'].split('/')[-1]
                    if emails[emailAdd]:
                        for pageTime in emails[emailAdd]:
                            edgeWeight = 1
                            oldTime = pageTime[1]
                            oldYear = oldTime.split('-')[0]
                            oldMonth = oldTime.split('-')[1]
                            oldDay = oldTime.split('-')[2]
                            if oldYear == year and oldMonth == month and abs(int(oldDay) - int(day)) <= binSize / 2 :
                                edgeWeight += 1
                            #if edgeWeight > 1:
                            #    print 'email conccurence: ' + str(edgeWeight)
                            foPEP.write(pageTime[0] + ',' + newId + ',' + str(edgeWeight) + '\n')
                    emails[emailAdd].append((newId, time))
    return tempNodes, tempPhones

def plotNodesTime(inputfile, tempNodes, n):
    # plot # nodes vs. time
    #print tempNodes
    numNodes = []
    for temp in tempNodes:
        numNodes.append(len(temp))
    time = range(n)
    fig = plt.figure()
    plt.scatter(time, numNodes)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('# Nodes', fontsize=16)
    fig.savefig('../Data/' + inputfile + '.nodes_time.jpg')
    return

def plotNumPhones(inputfile, tempPhones, n):
    # plot # unique phone numbers in each time stamp
    #print tempPhones
    numPhones = [len(tempPhones[0])]
    for i in range(1, n):
        phoneOverlap = tempPhones[i - 1].intersection(tempPhones[i])
        #print phoneOverlap
        numPhones.append(len(phoneOverlap))
    time = range(n)
    fig = plt.figure()
    plt.scatter(time, numPhones)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('# Phones', fontsize=16)
    fig.savefig('../Data/' + inputfile + '.unique_phones_time.jpg')
    return

if __name__ == "__main__":
    # load data files
    inputfile = sys.argv[1]
    binSize = int(sys.argv[2])
    stampSize = int(sys.argv[3])
    fi = open(inputfile, 'r')
    data = json.load(fi)
    data = data['hits']['hits']
    #print data

    # output edge lists
    outputfilePPP = '../Data/page-phone-page.edges'
    outputfilePEP = '../Data/page-email-page.edges'
    outputfilePP = '../Data/page-phone.edges'
    foPPP = open(outputfilePPP, 'w')
    foPEP = open(outputfilePEP, 'w')
    foPP = open(outputfilePP, 'w')

    minYear, minMonth, minDay, maxYear, maxMonth, maxDay = findMinMaxTime(data)
    if config.optTemporal:
        stamps, outputfilePPPStamps = createStamps(minYear, minMonth, maxYear, maxMonth, maxDay)
    tempNodes, tempPhones = generatePageGraphs(data, stamps, foPPP, foPEP, outputfilePPPStamps)
    n = len(stamps)
    plotNodesTime(inputfile, tempNodes, n)
    plotNumPhones(inputfile, tempPhones, n)

    fi.close()
    foPPP.close()
    foPEP.close()
    foPP.close()
