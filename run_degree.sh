#!/bin/bash #
# This file process weighted edge list and run weighted degree code
# iteratively for the temporal files.

for edgelist in ../Data/Temporal/*int
do
    # run weighted degree
    python compute_weighted_degree.py $edgelist
done
