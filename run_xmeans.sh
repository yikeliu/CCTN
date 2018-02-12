# Run xmeans.
#
# input:
#     .mat file that contains C
# output:
#     .clus file that contains cluster assignment

#!/bin/bash

mFile=$1
cFile=$2

extension="${mFile##*.}"
filename="${mFile%.*}"
outfile=$filename.xmeans

# run xmeans
python run_xmeans.py $mFile $cFile
xmeans/membership $cFile > $outfile

