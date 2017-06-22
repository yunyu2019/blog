#! /usr/bin/env python 
#encoding=utf-8
import mylib
import argparse

if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='Get InnoDB Page Info')
   parser.add_argument('-f','--file',required=True,type=str,help='the tablespace file path')
   parser.add_argument('-o','--output',default='result.txt',help='output put the result to file')
   parser.add_argument('-t',default=1,type=int,help='number thread to anayle the tablespace file')
   parser.add_argument('-v',action='store_true',help='verbose mode')
   args=parser.parse_args()
   myargv={"v":args.v,"tablespace":args.file,"output":args.output}
   mylib.get_innodb_page_type(**myargv)
