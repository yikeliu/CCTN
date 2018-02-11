"""
Evaluate clustering results of coaction + xmeans.
"""
import json
import collections

def evalCls(clusters, numToPhone, n):
    # evaluate clusters
    # number of clusters
    numCls = len(set(clusters))
    print 'Number of clustsers: ' + str(numCls)
    # sizes of clusters
    cntCls = collections.Counter(clusters)
    print 'Sizes of clusters: ' + str(cntCls)
    # phones in the largest n cluster
    print 'Largest ' + str(n) ' clusters:'
    for cls, cnt in cntCls.most_common(n):
        nodes = [i for i, j in enumerate(clusters) if j == cls]
        nodes = [numToPhone[x + 1] for x in nodes]
        print str(cnt) + ' nodes: ' + str(nodes)

if __name__ == '__main__':
    datafolder = '../Data/'
    clsfile = datafolder + 'cluster_smooth.xmeans'
    mapfile = datafolder + 'filtered_index.json'
    fcls = open(clsfile, 'r')
    lines = fcls.read().split('\n')[:-2]
    clusters = [int(x) for x in lines]
    phoneToNum = json.loads(mapfile)
    numToPhone = {v: k for k, v in phoneToNum.iteritems()}
