"""
Extract first n time stamps of data.

input:
    n
output:
    extracted matrix files, adjacency matrix file
"""
import sys
import subprocess

def cutMatrix(inputfile, ns):
    # extract the first ns stamps of each phone number, output the submatrix
    outputfile = inputfile + '.short'
    fi = open(inputfile, 'r')
    fo = open(outputfile, 'w')
    for line in fi.readlines():
        line = line.split('\t')[:(ns + 1)]
        fo.write('\t'.join(line) + '\n')
    fi.close()
    fo.close()
    return

if __name__ == '__main__':
    n = int(sys.argv[1])
    matrixfiles = ['../Data/structural_matrix.txt', '../Data/lsh_matrix.txt']
    for matrix in matrixfiles:
        cutMatrix(matrix, n)
    # copy the short adjacency matrix
    afile = '../Data/Temporal/all.phone-page-phone' + str(n - 1)
    newafile = '../Data/Temporal/all.phone-page-phone.edges.short'
    subprocess.call(['cp', afile, newafile])
