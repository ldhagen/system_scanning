#!/bin/env python
 
# This module is designed to walk a directory tree starting at the passed 
# location and identify specifically formatted filenames which contain DTG.
# These filenames are tested for specific lenght, prefix string, and suffix string
# and then added to a dictionary by converted DTG.  The result is persisted as a
# pickle file with the name provided by the second argument passed.
 
# Additional functions include copying the files from the dictionary sequentually
# using str.zfill padding to ensure they stary sortable in their chronological
# order.
 
import os, sys, pickle
from datetime import datetime as dt
import shutil
 
DefaultStart = r'.'
DefaultOutput = r'./defaultDTGscan.pkl'
FilenameLenghtConst = 29
FilenamePrefixConst = r'ldh'
FilenameSuffixConst = r'.jpg'
FilenameDTGFormatConst = r'%a_%d_%b_%y_%H_%M_%S' 
 
def walk_id(start_dir=DefaultStart, outpicklename=DefaultOutput):
    '''this function walks directory tree looking for constarts abovei
       confirms, converts to DGT, populates dict, and persists as pickle file'''
 
    found_dict = {}
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file[-4:] == (FilenameSuffixConst):
                if len(file) == FilenameLenghtConst:
                    if file[:3] == FilenamePrefixConst:
                        dvalue = dt.strptime(file[3:-4], FilenameDTGFormatConst)
                        found_dict[dvalue] = os.path.join(root,file)
 
    ofile = open(outpicklename, 'w')
    pickle.dump(found_dict, ofile)
    ofile.close()
 
def copy(pkl_dict, target_dir, spacing=3600):
    '''this function opens the passed  pickled dictionary and copies the listed
       files in sequence spaced as passed'''
 
    ifile = open(pkl_dict,'r')
    passed_dict = pickle.load(ifile)
    ifile.close()
    passed_dict_keys = passed_dict.keys()
    passed_dict_keys.sort()
    current_time = passed_dict_keys[0]
    seq_count = 0
    for x in passed_dict_keys:
        if (x - current_time).seconds > spacing:
            print x
            prefix = str(seq_count).zfill(8)
            out_tgt = target_dir + r'/' + prefix + os.path.basename(passed_dict[x])
            print out_tgt
            shutil.copy2(passed_dict[x],out_tgt)
            current_time = x 
            seq_count += 1
 
if __name__ == '__main__':
    walk_id(sys.argv[1], sys.argv[2])
