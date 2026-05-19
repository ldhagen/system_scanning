#!/usr/bin/env python3
import os
import hashlib
import pickle
import argparse
import pandas as pd

def calculate_md5(file_path, chunk_size=4096):
    """Calculate the MD5 hash of a file in chunks to be memory-efficient."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def get_scan(passed_start):
    """
    Walk through the directory tree and gather file metadata.
    Returns a list of tuples containing file info.
    """
    scan_data = []
    for root, _, files in os.walk(passed_start):
        for file in files:
            full_path = os.path.join(root, file)
            print(f"Scanning: {full_path}")
            
            md5_hash = calculate_md5(full_path)
            if md5_hash is None:
                continue

            try:
                file_stat = os.stat(full_path)
                scan_data.append({
                    'filename_full_path': full_path,
                    'md5_hash': md5_hash,
                    'size': file_stat.st_size,
                    'mtime': file_stat.st_mtime,
                    'ctime': file_stat.st_ctime,
                    'mode': file_stat.st_mode
                })
            except (PermissionError, FileNotFoundError):
                continue
                
    return scan_data

def create_dataframe(passed_list):
    """Convert the list of dictionaries into a Pandas DataFrame."""
    return pd.DataFrame(passed_list)

def main():
    parser = argparse.ArgumentParser(description="System file scanner to generate file metadata and hashes.")
    parser.add_argument('Beginning_Search_Path', help='The root directory to start the search', 
                        nargs='?', default='/var/tmp/ldh/working/')
    parser.add_argument('Output_Filename', help='The name of the output pickle file', 
                        nargs='?', default='ldh_1_out')
    args = parser.parse_args()

    if not os.path.exists(args.Beginning_Search_Path):
        print(f"Error: The path '{args.Beginning_Search_Path}' does not exist.")
        return

    print(f"Starting scan at: {args.Beginning_Search_Path}")
    data = get_scan(args.Beginning_Search_Path)
    df = create_dataframe(data)
    
    with open(args.Output_Filename, 'wb') as outw:
        pickle.dump(df, outw)
    
    print(f"Scan complete. Data saved to: {args.Output_Filename}")
    print(f"Total files scanned: {len(df)}")

if __name__ == '__main__':
     main()
