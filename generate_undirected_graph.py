"""
Generate undirected graph given input graph in form of: source target weight.

input:
    input graph
ouput:
    undirecred graph with edge list doubled.
"""
import sys

def revertEdges(inputfile):
    fi = open(inputfile, 'r')
    outputfile = inputfile + '.undirected'
    fo = open(outputfile, 'w')
    for line in fi.readlines():
        line = line.split('\t')
        node1 = line[0]
        node2 = line[1]
        weight = line[2]
        fo.write(node1 + '\t' + node2 + '\t' + weight + '\n')
        fo.write(node2 + '\t' + node1 + '\t' + weight + '\n')
    fi.close()
    fo.close()
    return

if __name__ == '__main__':
    inputfile = sys.argv[1]
    revertEdges(inputfile)
