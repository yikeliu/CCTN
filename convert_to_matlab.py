import sys
"""
This file convert a 2 column edge list to matlab input format: 3 column, with
edge weight as the last column.

input:
edgelist file name
"""

inputfile = sys.argv[1]
fi = open(inputfile, 'r')
outputfile = inputfile + '.minput'
fo = open(outputfile, 'w')

fi.next()
for line in fi:
    node1 = int(line.split(' ')[0])
    node2 = int(line.split(' ')[1])
    fo.write(str(node1 + 1) + ' ' + str(node2 + 1) + ' ' + '1' + '\n')

fi.close()
fo.close()
