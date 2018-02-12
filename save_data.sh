#!/bin/bash #
# This file download the jason files of phone-post, email-post mapping of
# humantrafficking dataset with time.
#
# input:
# size of file: 10, 100, 1000...
#
cat query
curl -s -XPOST http://memex:digdig@52.38.229.251:8080/dig-latest/webpage/_search --data-binary  "@query" > ../Data/page_phone_email10000.json


