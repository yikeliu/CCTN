import os
from lsh import LSHCache
"""
This file finds the LSH duplicates for each phone-stamp webpage descriptions.
Input files located at Description/.
"""

cache = LSHCache()

def findLSHDup(docs, fo, optWrite):
    cache = LSHCache()
    dups = {}
    for i, doc in enumerate(docs):
        dups[i] = cache.insert(doc.split(), i)
    #print dups

    if optWrite:
        for i, duplist in dups.items():
            if i == 0 and len(duplist) == 1:
                fo.write('no dups found for doc [%d] : %s\n' % (i, docs[i]))
            elif duplist:
                #print 'orig [%d]: %s' % (i, docs[i])
                fo.write('orig [%d]: %s\n' % (i, docs[i]))
                for dup in duplist:
                    #print'\tdup : [%d] %s' % (dup, docs[dup])
                    fo.write('\tdup : [%d] %s\n' % (dup, docs[dup]))
            else:
                #print 'no dups found for doc [%d] : %s' % (i, docs[i])
                fo.write('no dups found for doc [%d] : %s\n' % (i, docs[i]))
    return dups

if __name__ == "__main__":
    inputfolder = '/data/Data/Description/'
    outputfolder = '/data/Data/Description_Out/'
    files = os.listdir(inputfolder)
    for inputfile in files:
        fi = open(inputfolder + inputfile, 'r')
        docs = fi.read().splitlines()
        outputfile = inputfile + '.out'
        fo = open(outputfolder + outputfile, 'w')
        findLSHDup(docs, fo, False)
