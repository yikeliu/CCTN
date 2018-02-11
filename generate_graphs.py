import json
import sys
from collections import defaultdict
import config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fileinput
import pdb
"""
This file loads in the .json data files and generate projection graphs, plot #
nodes vs. time stamp.

input:
    size of time bins (in day), size of time stamps (in day), datafile(s)
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
        #print post
        page = post['uri'].split('/')[-1]
        if post.get('mentions'):
            time = post['dateCreated'].split('T')[0]
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

def createStamps(minYear, minMonth, minDay, maxYear, maxMonth, maxDay, stampSize, inputfile):
    year = minYear
    month = minMonth
    day = minDay
    stamps = []
    if config.optTemporal:
        while year < maxYear or (year == maxYear and month < maxMonth) or (year == maxYear and month == maxMonth and day < maxDay):
            stamps.append((year, month, day))
            if (month in [1, 3, 5, 7, 8, 10, 12] and day + stampSize > 31) or (month in [4, 6, 9, 11] and day + stampSize > 30) or (month == 2 and day + stampSize > 28):
                if month == 12:
                    year += 1
                    month = 1
                    day = stampSize - (31 - day)
                else:
                    if month == 2:
                        if year % 4 == 0:
                            day = stampSize - (29 - day)
                        else:
                            day = stampSize - (28 - day)
                        #print 'Feb full, new day: ' + str(day)
                    elif month in [1, 3, 5, 7, 8, 10]:
                        day = stampSize - (31 - day)
                    else: day = stampSize - (30 - day)
                    month += 1
            else:
                day += stampSize
        stamps.append((maxYear, maxMonth, maxDay))
        print stamps
        n = len(stamps) - 1
        outputfilePPPStamps = []
        outputfilePWPStamps = []
        for i in range(n):
            outputfilePPPStamps.append(inputfile + '.page-phone-page' + str(i))
            outputfilePWPStamps.append(inputfile + '.phone-page-phone' + str(i))
        return stamps, outputfilePPPStamps, outputfilePWPStamps
"""
def checkRange(minYear, minMonth, minDay, maxYear, maxMonth, maxDay, year, month, day):
    # check if the given date is within the time range
    if year > minYear and year < maxYear: return True
    lowCheck, upCheck = False, False
    if year == minYear:
        if month == minMonth:
            if day >= minDay: lowCheck = True
            else: lowCheck = False
        elif month > minMonth: lowCheck = True
        else: lowCheck = False
    if year == maxYear:
        if month == maxMonth:
            if day <= maxDay: upCheck = True
            else: upCheck = False
        elif month < maxMonth: upCheck = True
        else: upCheck = False
    return upCheck and lowCheck
"""
def checkRange(minYear, minMonth, minDay, maxYear, maxMonth, maxDay, year, month, day):
    # check if the given date is within the time range
    if year > minYear and year < maxYear: return True
    lowCheck, upCheck = False, False
    if year == minYear:
        if month == minMonth:
            if day >= minDay: lowCheck, upCheck = True, True
            else: lowCheck = False
        elif month > minMonth: lowCheck, upCheck = True, True
        else: lowCheck = False
    if year == maxYear:
        if month == maxMonth:
            if day <= maxDay: upCheck, lowCheck = True, True
            else: upCheck = False
        elif month < maxMonth: upCheck, lowCheck = True, True
        else: upCheck = False
    return upCheck and lowCheck

def generatePageGraphs(data, stamps, foPPP, foPEP, foPWP, outputfilePPPStamps, outputfilePWPStamps):
    # project on webpages, connected if two pages have same phone / email
    # project on phones, connected if two phones appear on same webpage
    # edge weight = frequency of cocurrence + 1
    n = len(stamps)
    phones = defaultdict(list)
    emails = defaultdict(list)
    phoneConcurrences = {}
    phoneConcurrencesStamps = [None] * (n - 1)
    minYear, minMonth, minDay, maxYear, maxMonth, maxDay = 2015, 10, 1, 2015, 11, 30
    if config.optTemporal:
        tempNodes = [set() for i in range(n)]
        tempPhones = [set() for i in range(n)]
        tempPhoneNums = [set() for i in range(n)]
    for post in data:
        page = post['uri'].split('/')[-1]
        if post.get('mentions'):
            infos = post['mentions']
            time = post['dateCreated'].split('T')[0]
            year = time.split('-')[0]
            month = time.split('-')[1]
            day = time.split('-')[2]
            if not checkRange(minYear, minMonth, minDay, maxYear, maxMonth, maxDay, int(year), int(month), int(day)):
                #print year, month, day
                continue
            #for info in infos:
            #    info = info.split('/')[5:]
            #    #print info
            #    if 'phone' in info:
            #        phoneNum = info[-1]
            #        newId = page
            #        foPP.write(phoneNum + '\t' + newId + '\n')
            #        if phones[phoneNum]:
            #            for pageTime in phones[phoneNum]:
            #                edgeWeight = 1
            #                #if pageTime[1] == time:
            #                oldTime = pageTime[1]
            #                oldYear = oldTime.split('-')[0]
            #                oldMonth = oldTime.split('-')[1]
            #                oldDay = oldTime.split('-')[2]
            #                if oldYear == year and oldMonth == month and abs(int(oldDay) - int(day)) <= binSize / 2 :
            #                    edgeWeight += 1
            #                #if edgeWeight > 1:
            #                #    print 'phone conccurence: ' + str(edgeWeight)
            #                foPPP.write(pageTime[0] + ',' + newId + ',' + str(edgeWeight) + '\n')
            #                if config.optTemporal:
            #                    #print year, month, day
            #                    for i in range(1, n): # data not sorted by date
            #                        if int(year) < stamps[i][0] or (int(year) == stamps[i][0] and int(month) < stamps[i][1]) or (int(year) == stamps[i][0] and int(month) == stamps[i][1] and int(day) < stamps[i][2]):
            #                            #print 'writing to stamp file...' + str(i - 1)
            #                            foPPPStamp = open(outputfilePPPStamps[i - 1], 'a')
            #                            foPPPStamp.write(pageTime[0] + ',' + newId + ',' + str(edgeWeight) + '\n')
            #                            tempNodes[i - 1].add(pageTime[0])
            #                            tempNodes[i - 1].add(newId)
            #                            tempPhones[i - 1].add(phoneNum)
            #                            foPPPStamp.close()
            #        phones[phoneNum].append((newId, time))
            #    if 'email' in info:
            #        emailAdd = info[-1]
            #        newId = page
            #        if emails[emailAdd]:
            #            for pageTime in emails[emailAdd]:
            #                edgeWeight = 1
            #                oldTime = pageTime[1]
            #                oldYear = oldTime.split('-')[0]
            #                oldMonth = oldTime.split('-')[1]
            #                oldDay = oldTime.split('-')[2]
            #                if oldYear == year and oldMonth == month and abs(int(oldDay) - int(day)) <= binSize / 2 :
            #                    edgeWeight += 1
            #                #if edgeWeight > 1:
            #                #    print 'email conccurence: ' + str(edgeWeight)
            #                foPEP.write(pageTime[0] + ',' + newId + ',' + str(edgeWeight) + '\n')
            #        emails[emailAdd].append((newId, time))
            if len(infos) >= 2:
                numPhones = 0
                phoneNums = []
                for info in infos:
                    info = info.split('/')[5:]
                    #print info
                    if 'phone' in info:
                        phoneNum = info[-1]
                        if phoneNums:
                            for number in phoneNums:
                                #edgeWeight = 1
                                ##if pageTime[1] == time:
                                #oldTime = pageTime[1]
                                #oldYear = oldTime.split('-')[0]
                                #oldMonth = oldTime.split('-')[1]
                                #oldDay = oldTime.split('-')[2]
                                #if oldYear == year and oldMonth == month and abs(int(oldDay) - int(day)) <= binSize / 2 :
                                #    edgeWeight += 1
                                ##if edgeWeight > 1:
                                ##    print 'phone conccurence: ' + str(edgeWeight)
                                if not phoneConcurrences.get((number, phoneNum)) and not phoneConcurrences.get((phoneNum, number)):
                                    phoneConcurrences[(number, phoneNum)] = 1
                                    #foPWP.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                                elif phoneConcurrences.get((number, phoneNum)):
                                    phoneConcurrences[(number, phoneNum)] += 1
                                else: phoneConcurrences[(phoneNum, number)] += 1
                                if config.optTemporal:
                                    if (number, phoneNum) == ('x-24704508813', 'x-450881331') or (phoneNum, number) == ('x-24704508813', 'x-450881331'): 
                                        print 'checking ' + number + ', ' + phoneNum
                                        print year, month, day
                                    for i in range(1, n): # data not sorted by date
                                        if int(year) < stamps[i][0] or (int(year) == stamps[i][0] and int(month) < stamps[i][1]) or (int(year) == stamps[i][0] and int(month) == stamps[i][1] and int(day) <= stamps[i][2]):
                                            #print 'adding ' + number + ', ' + phoneNum + ' to stamp file...' + str(i - 1)
                                            #pdb.set_trace()
                                            if (number, phoneNum) == ('x-24704508813', 'x-450881331') or (phoneNum, number) == ('x-24704508813', 'x-450881331'): print 'adding ' + number + ', ' + phoneNum
                                            if not phoneConcurrencesStamps[i - 1]:
                                                tempDict = {(number, phoneNum): 1}
                                                #phoneConcurrencesStamps[i - 1][(number, phoneNum)] = 1
                                                phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                                #print 'addng to stamp file...' + str(i - 1)
                                                #foPWPStamp = open(outputfilePWPStamps[i - 1], 'a')
                                                #foPWPStamp.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                                                tempPhoneNums[i - 1].add(number)
                                                tempPhoneNums[i - 1].add(phoneNum)
                                                #foPWPStamp.close()
                                            elif not phoneConcurrencesStamps[i - 1].get((number, phoneNum)) and not phoneConcurrencesStamps[i - 1].get((phoneNum, number)):
                                                #tempDict = phoneConcurrencesStamps[i - 1]
                                                #tempDict[(number, phoneNum)] = 1
                                                #phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                                phoneConcurrencesStamps[i - 1][(number, phoneNum)] = 1
                                                #print 'addng to stamp file...' + str(i - 1)
                                                #foPWPStamp = open(outputfilePWPStamps[i - 1], 'a')
                                                #foPWPStamp.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                                                tempPhoneNums[i - 1].add(number)
                                                tempPhoneNums[i - 1].add(phoneNum)
                                            elif phoneConcurrencesStamps[i - 1].get((number, phoneNum)):
                                                #tempDict = phoneConcurrencesStamps[i - 1]
                                                #tempDict[(number, phoneNum)] += 1
                                                #phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                                phoneConcurrencesStamps[i - 1][(number, phoneNum)] += 1
                                            else: phoneConcurrencesStamps[i - 1][(phoneNum, number)] += 1
                                                #tempDict = phoneConcurrencesStamps[i - 1]
                                                #tempDict[(phoneNum, number)] += 1
                                                #phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                            # get aggregated graphs
                                            #break
                                        #else: print 'skipped stamp ' + str(i)
                        phoneNums.append(phoneNum)
        
    # print graphs
    for phoneNums in phoneConcurrences:
        phoneNum1 = phoneNums[0]
        phoneNum2 = phoneNums[1]
        weight = phoneConcurrences[phoneNums]
        #if weight > 1: print weight
        foPWP.write(phoneNum1 + '\t' + phoneNum2 + '\t' + str(weight) + '\n')
    if config.optTemporal:
        for i in range(n - 1): # data not sorted by date
            #print len(phoneConcurrencesStamps[i])
            if not phoneConcurrencesStamps[i]:
                continue
            foPWPStamp = open(outputfilePWPStamps[i], 'w')
            for phoneNums in phoneConcurrencesStamps[i]:
                phoneNum1 = phoneNums[0]
                phoneNum2 = phoneNums[1]
                weight = phoneConcurrencesStamps[i][phoneNums]
                foPWPStamp.write(phoneNum1 + '\t' + phoneNum2 + '\t' + str(weight) + '\n')
            foPWPStamp.close()

    return tempNodes, tempPhones, tempPhoneNums

def generatePageGraphsNew(data, foPPP, foPEP, foPWPNew):
    # project on webpages, connected if two pages have same phone (new extractor)
    # project on phones, connected if two phones appear on same webpage
    # edge weight = frequency of cocurrence + 1
    #n = len(stamps)
    phones = defaultdict(list)
    phoneConcurrences = {}
    pageToPhones = defaultdict(list)
    #phoneConcurrencesStamps = [None] * (n - 1)
    #minYear, minMonth, minDay, maxYear, maxMonth, maxDay = 2015, 10, 1, 2015, 11, 30
    for post in data:
        page = post.split('\t')[0]
        phoneNum = post.split('\t')[1]
        #if post.get('mentions'):
        #    infos = post['mentions']
        #    time = post['dateCreated'].split('T')[0]
        #    year = time.split('-')[0]
        #    month = time.split('-')[1]
        #    day = time.split('-')[2]
        #    #if not checkRange(minYear, minMonth, minDay, maxYear, maxMonth, maxDay, int(year), int(month), int(day)):
        #    #    #print year, month, day
        #    #    continue
        #    if len(infos) >= 2:
        #        numPhones = 0
        #        phoneNums = []
        #        for info in infos:
        #            info = info.split('/')[5:]
        #            #print info
        #            if 'phone' in info:
        #                phoneNum = info[-1]
        #                if phoneNums:
        if pageToPhones.get(page):
            phoneNums = pageToPhones[page]
            for number in phoneNums:
                if not phoneConcurrences.get((number, phoneNum)) and not phoneConcurrences.get((phoneNum, number)):
                    phoneConcurrences[(number, phoneNum)] = 1
                    #foPWP.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                elif phoneConcurrences.get((number, phoneNum)):
                    phoneConcurrences[(number, phoneNum)] += 1
                else: phoneConcurrences[(phoneNum, number)] += 1
                                #if config.optTemporal:
                                #    if (number, phoneNum) == ('x-24704508813', 'x-450881331') or (phoneNum, number) == ('x-24704508813', 'x-450881331'): 
                                #        print 'checking ' + number + ', ' + phoneNum
                                #        print year, month, day
                                #    for i in range(1, n): # data not sorted by date
                                #        if int(year) < stamps[i][0] or (int(year) == stamps[i][0] and int(month) < stamps[i][1]) or (int(year) == stamps[i][0] and int(month) == stamps[i][1] and int(day) <= stamps[i][2]):
                                #            #print 'adding ' + number + ', ' + phoneNum + ' to stamp file...' + str(i - 1)
                                #            #pdb.set_trace()
                                #            if (number, phoneNum) == ('x-24704508813', 'x-450881331') or (phoneNum, number) == ('x-24704508813', 'x-450881331'): print 'adding ' + number + ', ' + phoneNum
                                #            if not phoneConcurrencesStamps[i - 1]:
                                #                tempDict = {(number, phoneNum): 1}
                                #                #phoneConcurrencesStamps[i - 1][(number, phoneNum)] = 1
                                #                phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                #                #print 'addng to stamp file...' + str(i - 1)
                                #                #foPWPStamp = open(outputfilePWPStamps[i - 1], 'a')
                                #                #foPWPStamp.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                                #                tempPhoneNums[i - 1].add(number)
                                #                tempPhoneNums[i - 1].add(phoneNum)
                                #                #foPWPStamp.close()
                                #            elif not phoneConcurrencesStamps[i - 1].get((number, phoneNum)) and not phoneConcurrencesStamps[i - 1].get((phoneNum, number)):
                                #                #tempDict = phoneConcurrencesStamps[i - 1]
                                #                #tempDict[(number, phoneNum)] = 1
                                #                #phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                #                phoneConcurrencesStamps[i - 1][(number, phoneNum)] = 1
                                #                #print 'addng to stamp file...' + str(i - 1)
                                #                #foPWPStamp = open(outputfilePWPStamps[i - 1], 'a')
                                #                #foPWPStamp.write(number + '\t' + phoneNum + '\n')# + ',' + str(edgeWeight) + '\n')
                                #                tempPhoneNums[i - 1].add(number)
                                #                tempPhoneNums[i - 1].add(phoneNum)
                                #            elif phoneConcurrencesStamps[i - 1].get((number, phoneNum)):
                                #                #tempDict = phoneConcurrencesStamps[i - 1]
                                #                #tempDict[(number, phoneNum)] += 1
                                #                #phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                #                phoneConcurrencesStamps[i - 1][(number, phoneNum)] += 1
                                #            else: phoneConcurrencesStamps[i - 1][(phoneNum, number)] += 1
                                #                #tempDict = phoneConcurrencesStamps[i - 1]
                                #                #tempDict[(phoneNum, number)] += 1
                                #                #phoneConcurrencesStamps[i - 1] = tempDict.copy()
                                #            # get aggregated graphs
                                #            #break
                                #        #else: print 'skipped stamp ' + str(i)
            pageToPhones[page].append(phoneNum)
        else:
            pageToPhones[page].append(phoneNum)

    print pageToPhones
    print phoneConcurrences    
    # print graphs
    for phoneNums in phoneConcurrences:
        phoneNum1 = phoneNums[0]
        phoneNum2 = phoneNums[1]
        weight = phoneConcurrences[phoneNums]
        #if weight > 1: print weight
        foPWPNew.write(phoneNum1 + '\t' + phoneNum2 + '\t' + str(weight) + '\n')
    #if config.optTemporal:
    #    for i in range(n - 1): # data not sorted by date
    #        #print len(phoneConcurrencesStamps[i])
    #        if not phoneConcurrencesStamps[i]:
    #            continue
    #        foPWPStamp = open(outputfilePWPStamps[i], 'w')
    #        for phoneNums in phoneConcurrencesStamps[i]:
    #            phoneNum1 = phoneNums[0]
    #            phoneNum2 = phoneNums[1]
    #            weight = phoneConcurrencesStamps[i][phoneNums]
    #            foPWPStamp.write(phoneNum1 + '\t' + phoneNum2 + '\t' + str(weight) + '\n')
    #        foPWPStamp.close()

    return #tempNodes, tempPhones, tempPhoneNums

def groupPages(data, stamps, inputfile):
    # group webpages by phone numbers and time, write page content to separate files
    n = len(stamps)
    phonePages = defaultdict(list)
    minYear, minMonth, minDay, maxYear, maxMonth, maxDay = 2015, 10, 1, 2015, 11, 30
    #if config.optTemporal:
    #    tempNodes = [set() for i in range(n)]
    #    tempPhones = [set() for i in range(n)]
    #    tempPhoneNums = [set() for i in range(n)]
    for post in data:
        page = post['uri'].split('/')[-1]
        if post.get('mentions') and post.get('description'):
            infos = post['mentions']
            desc = post['description']
            time = post['dateCreated'].split('T')[0]
            year = time.split('-')[0]
            month = time.split('-')[1]
            day = time.split('-')[2]
            if not checkRange(minYear, minMonth, minDay, maxYear, maxMonth, maxDay, int(year), int(month), int(day)):
                continue
            for info in infos:
                info = info.split('/')[5:]
                #print info
                if 'phone' in info:
                    phoneNum = info[-1]
                    newId = page
                    if phonePages[phoneNum]:
                        outputfile = inputfile + '.' + phoneNum
                        if config.optTemporal:
                            #print year, month, day
                            for i in range(1, n): # data not sorted by date
                                if int(year) < stamps[i][0] or (int(year) == stamps[i][0] and int(month) < stamps[i][1]) or (int(year) == stamps[i][0] and int(month) == stamps[i][1] and int(day) <= stamps[i][2]):
                                    #print 'writing to stamp file...' + str(i - 1)
                                    outputfile += '.' + str(i - 1)
                                    fo = open(outputfile, 'a')
                                    #fo.write(desc.encode('utf-8') + '\n')
                                    fo.write(desc.encode('unicode-escape') + '\n')
                                    #tempNodes[i - 1].add(pageTime[0])
                                    #tempNodes[i - 1].add(newId)
                                    #tempPhones[i - 1].add(phoneNum)
                                    fo.close()
                                    break
                    phonePages[phoneNum].append(desc)
            #    if 'email' in info:
            #        emailAdd = info[-1]
            #        newId = page
            #        if emails[emailAdd]:
            #            for pageTime in emails[emailAdd]:
            #                edgeWeight = 1
            #                oldTime = pageTime[1]
            #                oldYear = oldTime.split('-')[0]
            #                oldMonth = oldTime.split('-')[1]
            #                oldDay = oldTime.split('-')[2]
            #                if oldYear == year and oldMonth == month and abs(int(oldDay) - int(day)) <= binSize / 2 :
            #                    edgeWeight += 1
            #                #if edgeWeight > 1:
            #                #    print 'email conccurence: ' + str(edgeWeight)
            #                foPEP.write(pageTime[0] + ',' + newId + ',' + str(edgeWeight) + '\n')
            #        emails[emailAdd].append((newId, time))
    return #tempNodes, tempPhones, tempPhoneNums

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
    fig.savefig(inputfile + '.nodes_time.jpg')
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
    fig.savefig(inputfile + '.unique_phones_time.jpg')
    return

def plotPhonesTime(inputfile, tempPhoneNums, n):
    # plot # pages vs. time
    numPhones = []
    for temp in tempPhoneNums:
        numPhones.append(len(temp))
    time = range(n)
    fig = plt.figure()
    plt.scatter(time, numPhones)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('# Phones', fontsize=16)
    fig.savefig(inputfile + '.phones_time.jpg')
    return

if __name__ == "__main__":
    # load data files
    if config.optMultiple:
        inputfile = sys.argv[3:]
    else:
        inputfile = sys.argv[3]
    binSize = int(sys.argv[1])
    stampSize = int(sys.argv[2])
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
            """
    inputfile = sys.argv[1]
    fi = open(inputfile, 'r')
    data = fi.read().splitlines()
    """

    print 'Data loaded.'

    # output edge lists
    if config.optMultiple:
        inputfile = '../Data/all'
    outputfilePPP = inputfile + '.page-phone-page.edges'
    outputfilePWP = inputfile + '.phone-page-phone.edges'
    #outputfilePWPNew = inputfile + '.phone-page-phone-new.edges'
    outputfilePEP = inputfile + '.page-email-page.edges'
    outputfilePP = inputfile + '.page-phone.edges'
    foPPP = open(outputfilePPP, 'w')
    foPWP = open(outputfilePWP, 'w')
    #foPWPNew = open(outputfilePWPNew, 'w')
    foPEP = open(outputfilePEP, 'w')
    foPP = open(outputfilePP, 'w')

    #minYear, minMonth, minDay, maxYear, maxMonth, maxDay = findMinMaxTime(data)
    minYear, minMonth, minDay, maxYear, maxMonth, maxDay = 2015, 10, 1, 2015, 11, 30
    if config.optTemporal:
        stamps, outputfilePPPStamps, outputfilePWPStamps = createStamps(minYear, minMonth, minDay, maxYear, maxMonth, maxDay, stampSize, inputfile)
    #tempNodes, tempPhones, tempPhoneNums = generatePageGraphs(data, stamps, foPPP, foPEP, foPWP, outputfilePPPStamps, outputfilePWPStamps)
    #generatePageGraphsNew(data, foPPP, foPEP, foPWPNew)
    inputfile = '../Data/Description_All/all'
    groupPages(data, stamps, inputfile)
    n = len(stamps)
    #plotNodesTime(inputfile, tempNodes, n)
    #plotNumPhones(inputfile, tempPhones, n)
    #plotPhonesTime(inputfile, tempPhoneNums, n)

    fi.close()
    foPPP.close()
    foPEP.close()
    foPWP.close()
    foPP.close()
