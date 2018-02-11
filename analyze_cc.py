import extract_component as Plot
import glob
import matplotlib.pyplot as plt
"""
This file compute the average connected component for input cc output.
For temporal files, plot the avg cc size vs. time.
"""

if __name__ == '__main__':
    inputtype = '/data/Data/Gcc_Temp/*.int_new.txt.cc'
    inputfiles = glob.glob(inputtype)
    outputfolder = '/data/Data/'
    maxTimeIdx = 0
    for inputfile in inputfiles:
        timeIdx = int(inputfile.split('subedges')[1].split('.')[0])
        maxTimeIdx = max(timeIdx, maxTimeIdx)
    avgSizes = [0] * (maxTimeIdx + 1)
    maxSizes = [0] * (maxTimeIdx + 1)
    for inputfile in inputfiles:
        timeIdx = int(inputfile.split('subedges')[1].split('.')[0])
        inputfile = inputfile.split('.int')[0]
        #print timeIdx
        avgSizes[timeIdx] = Plot.plotSize(inputfile, False)[1]
        maxSizes[timeIdx] = Plot.plotSize(inputfile, False)[2]
    print avgSizes
    time = range(maxTimeIdx + 1)
    fig = plt.figure()
    plt.scatter(time, avgSizes)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Average Size', fontsize=16)
    #fig.savefig('../Data/' + inputfile + '.num_size_cc.jpg')
    fig.savefig(outputfolder + 'avgsize_time_cc.jpg')

    # plot max size vs. time
    fig = plt.figure()
    plt.scatter(time, maxSizes)
    #plt.xscale('log')
    #plt.yscale('log')
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Max Size', fontsize=16)
    #fig.savefig('../Data/' + inputfile + '.num_size_cc.jpg')
    fig.savefig(outputfolder + 'maxsize_time_cc.jpg')
