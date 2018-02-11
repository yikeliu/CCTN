import sys
"""
This file add weight 1 to a 2 column edge list: 3 column, with
edge weight as the last column.

input:
edgelist file name
"""

inputfile = sys.argv[1]
fi = open(inputfile, 'r')
outputfile = inputfile + '.weight'
fo = open(outputfile, 'w')

fi.next()
for line in fi:
    node1 = int(line.split('\t')[0])
    node2 = int(line.split('\t')[1])
    fo.write(str(node1) + '\t' + str(node2) + '\t' + '1' + '\n')

fi.close()
fo.close()
