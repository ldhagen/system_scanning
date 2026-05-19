#!/usr/bin/env python3
import os
import hashlib
import pickle
import argparse
import pandas as pd
from datetime import datetime
import stat

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
    Returns a list of dictionaries containing file info.
    """
    scan_data = []
    dir_count = 0
    file_count = 0

    # Optional: Add directories you want to skip entirely to speed things up
    exclude_dirs = {'.cache', '.local', '.rustup', '.nvm', 'node_modules', '.virtualenvs'}

    for root, dirs, files in os.walk(passed_start):
        dir_count += 1
        
        # Modify the 'dirs' list in-place to prevent os.walk from entering excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_count += 1
            full_path = os.path.join(root, file)
            
            try:
                # Get file stats BEFORE trying to read/hash it (use lstat to not follow symlinks)
                file_stat = os.lstat(full_path)
                
                # Check if it's a regular file. If it's a socket, pipe, or symlink, skip it.
                if not stat.S_ISREG(file_stat.st_mode):
                    continue
                
                # If the file is larger than 100MB, print a warning so you know it's not frozen
                file_size_mb = file_stat.st_size / (1024 * 1024)
                if file_size_mb > 100:
                    print(f"\n[!] Notice: Hashing large file ({file_size_mb:.2f} MB): {full_path}")
                    
            except (PermissionError, FileNotFoundError):
                continue

            # Update the progress indicator less frequently to reduce I/O overhead
            if file_count % 50 == 0:
                print(f"Scanned: {dir_count} directories, {file_count} files. Data points: {len(scan_data)}", end='\r')
            
            md5_hash = calculate_md5(full_path)
            if md5_hash is None:
                continue

            scan_data.append({
                'filename_full_path': full_path,
                'md5_hash': md5_hash,
                'size': file_stat.st_size,
                'mtime': file_stat.st_mtime,
                'ctime': file_stat.st_ctime,
                'mode': file_stat.st_mode
            })
                
    print(f"\nScan complete. Processed {file_count} files across {dir_count} directories.")
    return scan_data

def create_dataframe(passed_list):
    """Convert the list of dictionaries into a Pandas DataFrame."""
    return pd.DataFrame(passed_list)

def main():
    dtg = datetime.now().strftime('%Y%m%d_%H%M%S')
    default_output = f'ldh_scan_{dtg}.pkl'

    parser = argparse.ArgumentParser(description="System file scanner to generate file metadata and hashes.")
    parser.add_argument('Beginning_Search_Path', help='The root directory to start the search', 
                        nargs='?', default='/var/tmp/ldh/working/')
    parser.add_argument('Output_Filename', help=f'The name of the output pickle file (default: {default_output})', 
                        nargs='?', default=default_output)
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
