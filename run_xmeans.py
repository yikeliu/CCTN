"""
Generate .ds file as input of xmeans and run xmeans.

input:
    .mat file that contains C
output:
    .clus file that contains cluster assignment
"""
import sys
import scipy.io as sio
import subprocess
import os

def genXmeansInput(C, inFile):
    # generate input files for xmeans
    (n, f) = C.shape
    fin = open(inFile, 'w')
    for i in range(f):
        fin.write('x' + str(i) + ' ')
    fin.write('\n')
    for values in C:
        for v in values:
            fin.write(str(v) + ' ')
        fin.write('\n')
    fin.close()
    return

def runXmeans(inFile, clFile):
    # run xmeans given the .ds file
    # generate .universe file
    subprocess.call(['xmeans/kmeans_fast', 'makeuni', 'in', inFile])
    # run xmeans
    subprocess.call(['xmeans/kmeans_fast', 'kmeans', '-k', '1', '-method', 'blacklist', '-max_leaf_size', '40', '-min_box_width', '0.03', '-cutoff_factor', '0.5', '-max_iter', '200', '-num_splits', '6', '-max_ctrs', '15', '-in', inFile, '-printclusters', clFile])
    return

if __name__ == '__main__':
    mFile, cFile = sys.argv[1], sys.argv[2]
    mDict = sio.loadmat(mFile)
    C = mDict['C']
    path, fname = os.path.split(mFile)
    inFile = path + '/' + fname.split('.')[0] + '.ds'
    genXmeansInput(C, inFile)
    clFile = path + '/' + fname.split('.')[0] + '.clus'
    runXmeans(inFile, clFile)
