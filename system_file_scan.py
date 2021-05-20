#!/usr/bin/env python
import subprocess as sp
import pickle, os

def get_scan():
    print('Hello')
    p1 = sp.Popen(['find', '/var/tmp/ldh/working/system_scanning/', '-type', 'f'], stdout = sp.PIPE)
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
    x = get_scan()
    print(x[0])
    with open('output_test1', 'wb') as outw:
        pickle.dump(x, outw)

if __name__ == '__main__':
     main()

