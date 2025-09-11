#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <file_1_path> <file_2_path>"
    exit 1
fi

file_1_path=$1
file_2_path=$2

# Extract base names without path and extension
base1=$(basename "$file_1_path" | sed 's/\.[^.]*$//')
base2=$(basename "$file_2_path" | sed 's/\.[^.]*$//')

# Concatenate with underscore
folder_name="${base1}_${base2}"

# Run dcj
cd gredu-dcj/src/
./dcj "$file_1_path" "$file_2_path"
cd ../..

python main.py "gredu-dcj/src/simp_parameters/${folder_name}" 