#!/usr/bin/env python
import subprocess as sp
import pickle, os, sys, argparse

def get_scan(passed_start):
    print('Hello')
#    p1 = sp.Popen(['find', '/var/tmp/ldh/working/system_scanning/', '-type', 'f'], stdout = sp.PIPE)
    p1 = sp.Popen(['find', passed_start, '-type', 'f'], stdout = sp.PIPE)
    out1 = p1.communicate()[0]
    print(len(out1))
    print(type(out1))
    out2 = str(out1)
    list1 = []
    for x in out2[2:-1].split(r'\n'):
        list1.append(x)
    for y in list1:
        print(y)
    return list1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(r'Beginning_Search_Path', help=r'Where search starts', nargs='?', default=r'/var/tmp/ldh/working/')
    parser.add_argument(r'Output_Filename', help=r'Out file name', nargs='?', default=r'ldh_1_out')
    args = parser.parse_args()
    x = get_scan(args.Beginning_Search_Path)
    print(x[0])
#    with open('output_test1', 'wb') as outw:
    with open(args.Output_Filename, 'wb') as outw:
        pickle.dump(x, outw)

if __name__ == '__main__':
     main()

