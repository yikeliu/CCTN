#!/bin/bash
# This file runs clustering and evaluates clustering results.
# input: dataset (h3, m), astruc, acont, lambda, mu, # features, 
# clustering method (k - kmeans, x - xmeans)

astruc=$1
acont=$2
lambda=$3
numf=$4
clusmethod=$5

# run clustering
matlab -r "compute_cluster_smooth($1, $2, $3, $4)"

# run new evaluation
#matlab -r evaluate_cluster_smooth\(\'$1\'\)
LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libstdc++.so.6" matlab -r "evaluate_cluster_smooth('$5')"
#matlab -r "evaluate_cluster_smooth('$1', $6, '$7')"
