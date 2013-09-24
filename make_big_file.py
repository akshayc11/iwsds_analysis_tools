#!/usr/bin/python

import sys
import re
import argparse

if __name__ == '__main__':
    
    parser = argparse.argument_parser(description='''
    This is used to parse all the files and then convert 
    it into a tab separated value ''')
    
    parser.add_argument('data',
                        metavar='<data directory>',
                        help=': input data directory')
    
    parser.add_argument('list',
                        metavar='<runs list>',
                        help=': list of runs for file generation')
    
    parser.add_argument('output',
                        metavar='<output file>',
                        help=': output file')
    
    parser.add_argument('-d',
                        '--delimiter'
                        type=str,
                        default='\t',
                        help=': delimiter for output file, default="\\t"')
    
    args = vars(parser.parse_args())
    
    dataDir      = args['data']
    listFileId   = args['list']
    outputFileId = args['output']
    delimiter    = args['delimiter']
    
    
