#coding: UTF-8

import sys
import os
import struct
import md5
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d","--dir",action="store",dest="path",default="",
                  help="")
(options,args) = parser.parse_args(sys.argv)
if not options.path.strip():
    parser.print_help()
    exit()

if not os.path.exists(options.path):
    print "Path is not exists,Pls input dir"
    parser.print_help()
    exit()

if not os.path.isabs(options.path):
    path = os.path.join(os.getcwd(),options.path)
else:
    path = options.path

passwd = raw_input("Pls input your passwd:")

def convert_passwd(passwd):
    m = md5.new()
    m.update(passwd)
    return m.hexdigest()
key = convert_passwd(passwd)

def encoding_file(file,key):
    buffer_size = 2 ** 10
    #read_buffer = bytearray(buffer_size)
    #print os.path.getsize(file)
    try:
        f = open(file,"r+b",buffering=buffer_size)
        i = 0
        kl = len(key)
        while True:
            ch = f.read(1)
            if not ch:
                break
            else:
                j = i%kl
                i=i+1
                ch1 = chr(ord(ch) ^ ord(key[j]))
                byte =struct.pack("c",ch1)
                k = f.tell()
                f.seek(k-1)
                f.write(byte)
    except:
        print "open file error", file
    finally:
        f.close()
    return

#encoding_file("/Users/zmhu/bin/sfile/a/胡志明.JPG",key)

def proccess_path (path,key):
    for d in os.listdir(path):
        absp = os.path.join(path,d)
        if os.path.isdir(absp):
            proccess_path(absp,key)
        else:
            print absp
            encoding_file(absp,key)

proccess_path(path,key)
