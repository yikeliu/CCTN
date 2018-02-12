#!/bin/bash #
# This file process unweighted edge list and run centrality code
# iteratively for the temporal files.

for edgelist in /data/Data/Temporal/*
do
    # input
    intedges=$edgelist.int
    input=$edgelist.txt
    cenoutput=$edgelist.tab
    
    # convert str to int
    python str_to_int.py $edgelist $intedges
    
    # remove first line
    sed '1d' $intedges > tmpfile; mv tmpfile $intedges
    
    # run centrality
    snap/examples/centrality/centrality -i:$intedges -o:$cenoutput
done
