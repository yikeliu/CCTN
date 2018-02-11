"""
Parse txt file of matrix. Generate 2 files: phone numbers indicating
representation of each line, matrix of data.

input:
    txt file to be parsed
output:
    phone number list
    data matrix
"""
import sys

def parse_matrix(inputfile):
    fi = open(inputfile, 'r')
    fphones = open(inputfile + '.phones', 'w')
    fdata = open(inputfile + '.data', 'w')
    for line in fi.readlines():
        line = line.split('\t')
        phone = line[0]
        data = line[1:]
        fphones.write(phone + '\n')
        for i in range(len(data) - 1):
            fdata.write(data[i] + '\t')
        fdata.write(data[i + 1])
    fi.close()
    fphones.close()
    fdata.close()
    return

if __name__ == '__main__':
    inputfile = sys.argv[1]
    parse_matrix(inputfile)

