"""
Conver data in json format to txt separated by tab.

input:
    json file to be parsed
output:
    txt file
"""
import sys
import json

def convertFormat(inputfile):
    fi = open(inputfile, 'r')
    outputfile = inputfile + '.txt'
    fo = open(outputfile, 'w')
    matrix = json.load(fi)
    for node in matrix:
        values = matrix[node]
        fo.write(node)
        if len(values) > 1:
            for value in values:
                fo.write('\t' + str(value))
        else:
            fo.write('\t' + str(values))
        fo.write('\n')
    fi.close()
    fo.close()
    return

if __name__ == '__main__':
    filename = sys.argv[1]
    convertFormat(filename)
