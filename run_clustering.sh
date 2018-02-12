#!/bin/bash
# This file process unweighted edge list and run the specified clustering
# method. (slashburn, louvain)
#
# input:
# name of edge list file

# input
edgelist=$1
clusmeth=$2
intedges=$edgelist.int
input=$intedges.minput

# convert str to int
python str_to_int.py $edgelist $intedges

# convert to formatted input
python convert_to_matlab.py $intedges

# run clustering
matlab -nodesktop -nosplash -r "run_clustering('$clusmeth', '$input')";
