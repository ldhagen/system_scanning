#!/usr/bin/env python3
"""
This module is designed to walk a directory tree starting at the passed 
location and identify specifically formatted filenames which contain DTG.
These filenames are tested for specific length, prefix string, and suffix string
and then added to a dictionary by converted DTG. The result is persisted as a
pickle file with the name provided by the second argument passed.

Additional functions include copying the files from the dictionary sequentially
using str.zfill padding to ensure they stay sortable in their chronological
order.
"""

import os
import sys
import pickle
from datetime import datetime as dt
import shutil

# Constants
DEFAULT_START = '.'
DEFAULT_OUTPUT = './defaultDTGscan.pkl'
FILENAME_LENGTH_CONST = 29
FILENAME_PREFIX_CONST = 'ldh'
FILENAME_SUFFIX_CONST = '.jpg'
FILENAME_DTG_FORMAT_CONST = '%a_%d_%b_%y_%H_%M_%S' 

def walk_id(start_dir=DEFAULT_START, out_pickle_name=DEFAULT_OUTPUT):
    """
    Walks directory tree looking for constants above, confirms, 
    converts to DTG, populates dict, and persists as pickle file.
    """
    found_dict = {}
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith(FILENAME_SUFFIX_CONST):
                if len(file) == FILENAME_LENGTH_CONST:
                    if file.startswith(FILENAME_PREFIX_CONST):
                        try:
                            # Extract DTG part and parse it
                            dtg_str = file[len(FILENAME_PREFIX_CONST):-len(FILENAME_SUFFIX_CONST)]
                            dvalue = dt.strptime(dtg_str, FILENAME_DTG_FORMAT_CONST)
                            found_dict[dvalue] = os.path.join(root, file)
                        except ValueError:
                            # Skip files that don't match the DTG format
                            continue

    with open(out_pickle_name, 'wb') as ofile:
        pickle.dump(found_dict, ofile)
    print(f"Scan complete. Found {len(found_dict)} files. Saved to {out_pickle_name}")

def copy_files(pkl_dict_path, target_dir, spacing=3600):
    """
    Opens the passed pickled dictionary and copies the listed
    files in sequence spaced as passed.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(pkl_dict_path, 'rb') as ifile:
        passed_dict = pickle.load(ifile)

    if not passed_dict:
        print("No files found in the dictionary.")
        return

    sorted_keys = sorted(passed_dict.keys())
    current_time = sorted_keys[0]
    seq_count = 0

    for dt_key in sorted_keys:
        if (dt_key - current_time).total_seconds() >= spacing or seq_count == 0:
            print(f"Processing: {dt_key}")
            prefix = str(seq_count).zfill(8)
            source_path = passed_dict[dt_key]
            filename = os.path.basename(source_path)
            out_target = os.path.join(target_dir, f"{prefix}_{filename}")
            
            print(f"Copying to: {out_target}")
            shutil.copy2(source_path, out_target)
            
            current_time = dt_key 
            seq_count += 1

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: walk_id.py <start_dir> <output_pickle>")
    else:
        walk_id(sys.argv[1], sys.argv[2])
