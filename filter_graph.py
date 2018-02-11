import sys
"""
Filter the edge list and remove the wrong phone numbers with its incident edges.

input:
    edge list file
output:
    filtered edge list (.fitered)
"""

def filterEdges(inputfile, nodeExcluded):
    # nodeExcluded is a list of node to be removed
    outputfile = inputfile + '.filtered'
    fi = open(inputfile, 'r')
    fo = open(outputfile, 'w')
    for line in fi.readlines():
        node1 = line.split('\t')[0]
        node2 = line.split('\t')[1].split('\n')[0]
        if node1 in nodeExcluded or node2 in nodeExcluded:
            continue
        else:
            fo.write(line)
    fi.close()
    fo.close()
    return

if __name__ == "__main__":
    inputfile = sys.argv[1]
    nodeExcluded = ['1-1001001001', '1-1001001002', '1-1000000000', '1-1001502002', '1-1001502003', '1-1001502004', '1-1001502005', '1-1001502008', '1-1001307173', '1-1000587712', '1-1402676424', '1-2469250810', '1-1003063812', '1-1003137405', '1-1002482542', '1-1004049400', '1-6080120200', 'x-200916758', 'x-250702910', 'x-250469516', 'x-954549335', 'x-954589469', 'x-954560346', '1-2214997603', '1-2702980618', '1-9544651983']#, '1-1001502505', '1-1004154992', '1-1004155212', '1-1001502005', '1-1003608306', '1-1004259050', '1-1004156299']
    filterEdges(inputfile, nodeExcluded)
