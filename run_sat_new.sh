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

# Get absolute paths to check for directory names
abs_path1=$(realpath "$file_1_path")
abs_path2=$(realpath "$file_2_path")

# Determine output directory based on path
if [[ "$abs_path1" == *"variable_dcj_ops"* ]] || [[ "$abs_path2" == *"variable_dcj_ops"* ]]; then
    output_dir="results_multiple/variable_dcj_ops"
elif [[ "$abs_path1" == *"variable_gene_families"* ]] || [[ "$abs_path2" == *"variable_gene_families"* ]]; then
    output_dir="results_multiple/variable_gene_families"
else
    echo "Error: Input paths must contain either 'variable_dcj_ops' or 'variable_gene_families' directory"
    exit 1
fi

# Run dcj
cd gredu-dcj/src/
./dcj "$file_1_path" "$file_2_path"
cd ../..

# Run python with the concatenated folder path and redirect to appropriate output file
/usr/bin/time -v python -u main.py "gredu-dcj/src/simp_parameters/${folder_name}" > "${output_dir}/${folder_name}.out" 2>&1 &