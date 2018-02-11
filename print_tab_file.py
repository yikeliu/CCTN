"""
Convert .json file to tab separated file.

input:
    .json file to be reprinted
output:
    .txt file separated by tab
"""

import json
import sys

def printTab(inputfile, outputfile):
    fi = open(inputfile, 'r')
    fo = open(outputfile, 'w')
    fileDict = json.load(fi)
    for key in fileDict:
        fo.write(key)
        values = fileDict[key]
        for value in values:
            fo.write('\t' + value)
        fo.write('\n')
    fi.close()
    fo.close()

if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = inputfile.split('json')[0] + 'txt'
