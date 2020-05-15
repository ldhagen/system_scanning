#!/usr/bin/env python
import subprocess as sp
import pickle, os

def main():
    print('Hello')
    p1 = sp.Popen(['find', '/', '-type', 'f'], stdout = sp.PIPE)
    out1 = p1.communicate()[0]
    print(len(out1))
    print(type(out1))
    list1 = []
    for x in out1[:-1].split('/n'):
        list1.append(x)
    for y in list1:
        print(y)

if __name__ == '__main__':
     main()

