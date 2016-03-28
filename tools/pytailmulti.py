#!/usr/bin/env python
#coding:utf-8
import time
import os
import sys
import getopt
import linecache
import threading

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
    readlines(filename,10)
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
            filename.close()
            sys.exit(0)

def readlines(filename,linenum):
    ""
    f = open(filename)
    countlines = len(linecache.getlines(filename))
    readlines = countlines - linenum 
    for i in f.readlines()[readlines:]:
        print i,

def optparser_f(opts):
    ""
    opts = opts.split(",")
    return opts

def multirun(opts):
    for o in opts:
        client_thread = threading.Thread(target=tail,args=(o,))
        client_thread.start()

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
                opts = optparser_f(a)
            if o in ("-n","--num"):
                readlines(filename,int(a))
            if o in ("-m","--monit"):
                multirun(opts)
                
if __name__ == "__main__":
    main()

