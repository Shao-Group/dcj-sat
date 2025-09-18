#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

def extract_filename(file_path):
    return Path(file_path).stem

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path1> <file_path2>")
        sys.exit(1)
    
    file_path1 = sys.argv[1]
    file_path2 = sys.argv[2]
    
    # Extract filenames without directories or extensions
    filename1 = extract_filename(file_path1)
    filename2 = extract_filename(file_path2)
    
    # Create folder path
    folder_path = f"simp_parameters/{filename1}_{filename2}/"
    
    print(f"Processing files: {file_path1}, {file_path2}")
    print(f"Extracted filenames: {filename1}, {filename2}")
    print(f"Folder path: {folder_path}")
    
    try:
        print("Running: ./src/dcj {} {}".format(file_path1, file_path2))
        result1 = subprocess.run(["./src/dcj", file_path1, file_path2], 
                               check=True, capture_output=True, text=True)
        print("dcj command completed successfully")
        if result1.stdout:
            print("Output:", result1.stdout)
        
        print("Running: python main.py {}".format(folder_path))
        result2 = subprocess.run(["python", "main.py", folder_path], 
                               check=True, capture_output=True, text=True)
        print("main.py command completed successfully")
        if result2.stdout:
            print("Output:", result2.stdout)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Command failed with return code: {e.returncode}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Command not found: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()