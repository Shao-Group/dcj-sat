#!/bin/bash

# Check if at least two arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <file_1_path> <file_2_path> [time_limit]"
    exit 1
fi

# Assign the compulsory arguments
file_1_path=$1
file_2_path=$2

# Check if the time limit argument is provided; if not, set it to 7200 seconds
time_limit=${3:-7200}

cd gredu-dcj/src/
./dcj ../../$file_1_path ../../$file_2_path
cd ../..
timeout $time_limit python3 main.py gredu-dcj/src/simp_parameters