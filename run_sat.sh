#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <file_1_path> <file_2_path>"
    exit 1
fi

file_1_path=$1
file_2_path=$2

cd gredu-dcj/src/
./dcj ../../$file_1_path ../../$file_2_path
cd ../..
time python3 main.py gredu-dcj/src/simp_parameters