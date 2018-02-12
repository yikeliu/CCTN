#!/bin/bash
# This file process unweighted edge list and run connected component code and
# clique code.
#
# input:
# name of edge list file

# input
edgelist=$1
intedges=$edgelist.int
input=$intedges\_new.txt
ccoutput=$input.cc

# convert str to int
python str_to_int.py $edgelist $intedges

# convert to formatted input
./edge2standard $intedges

# run connected component
ConnectedComponent/Connected_Comp/connected_component $input $ccoutput

# run clique
#MaximumClique/MCE_TODS/find_clique $input 4000 20 500 1

# analyze results

