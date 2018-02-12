#!/bin/bash
# move temporal files to Temporal/

nums='0 1 2 3 4 5 6 7 8 9'
datafolder=/data/Data
for i in $nums
do
    { # your 'try' block
        mv $datafolder/all.phone-page-phone$i* $datafolder/Temporal/ &&
        echo 'command failed'
    } || { # your 'catch' block
        continue
    }
done
