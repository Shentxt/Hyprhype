#!/bin/bash

#down=$(speedtest --no-download | awk '/Download/')
#up=$(speedtest --no-upload | awk '/Upload/')

down=$(speedtest --no-download | awk -F': ' '/Download:/{gsub(" Mbit/s", "", $2); printf $2}')
up=$(speedtest --no-upload | awk -F': ' '/Upload:/{gsub(" Mbit/s", "", $2); printf $2}')

echo "$up - $down"
