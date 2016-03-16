#!/usr/bin/env python
#coding:utf-8
import time
import os
import sys
import getopt
import linecache

filename = ""
def usage():
    ""
    print "="*50
    print "Pytail manual:"
    print ""
    print "The toos tail for python"
    print "The parameter '-f' must first"
    print "python pytail.py -f [filename] -n [num]"
    print "python pytail.py -f [filename] -m"
    print "="*50
    sys.exit(0)

def tail(filename):
    filename = filename
    filename = open(filename,'r')
    filename.seek(0,2)
    fileseek = filename.tell()
    while True:
        try:
            filename.seek(0,2)
            tmpseek = filename.tell()
            change = fileseek - tmpseek
            if tmpseek > fileseek:
                filename.seek(change,1)
                for i in filename.readlines():
                    print i,
                fileseek = filename.tell()
            time.sleep(0.5)
        except KeyboardInterrupt:
            sys.exit(0)

def readlines(filename,linenum):
    ""
    f = open(filename)
    countlines = len(linecache.getlines(filename))
    readlines = countlines - linenum 
    for i in f.readlines()[readlines:]:
        print i,

def main():
        ""
        global filename
        if not len(sys.argv[1:]):
                usage()
                
        # read the commandline options
        try:
                opts, args = getopt.getopt(sys.argv[1:],"hf:mn:",["help","file","monit","num"])
        except getopt.GetoptError as err:
                print str(err)
                usage()
                
        for o,a in opts:
            if o in ("-h","--help"):
                usage()
            if o in ("-f","--file"):
                filename = a 
            if o in ("-n","--num"):
                readlines(filename,int(a))
            if o in ("-m","--monit"):
                readlines(filename,10)
                tail(filename)
                
if __name__ == "__main__":
    main()

