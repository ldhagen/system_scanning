#!/usr/bin/env python
import subprocess as sp
import pickle, os, sys, argparse
import pandas as pd

def get_scan(passed_start):
    p1 = sp.Popen(['find', passed_start, '-type', 'f'], stdout = sp.PIPE)
    out1 = str(p1.communicate()[0])
    list1 = []
    for x in out1[2:-1].split(r'\n'):
        list1.append(x)
        print(x)
    list2 = []
    for x in list1[0:-1]:
        p1 = sp.Popen(['md5sum', x], stdout = sp.PIPE)
        y = str(p1.communicate()[0])

        p1 = sp.Popen(['stat', x], stdout = sp.PIPE)
        z = str(p1.communicate()[0])

        list2.append((x,y[2:].split()[0],z))
    return list2

def create_dataframe(passed_list):
    df = pd.DataFrame(passed_list, columns = ['filename_full_path', 'md5_hash', 'stat'])
#    df = pd.DataFrame(passed_list)
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(r'Beginning_Search_Path', help=r'Where search starts', nargs='?', default=r'/var/tmp/ldh/working/')
    parser.add_argument(r'Output_Filename', help=r'Out file name', nargs='?', default=r'ldh_1_out')
    args = parser.parse_args()
    x = get_scan(args.Beginning_Search_Path)
    y = create_dataframe(x)
    with open(args.Output_Filename, 'wb') as outw:
        pickle.dump(y, outw)

if __name__ == '__main__':
     main()

