#!/usr/bin/python

import argparse
import os
import read_write_annotation_files as rw
import annotation_schema
read_complex  =  rw.read_annotation_file
read_simple   =  rw.read_simple_annotation_file
write_complex =  rw.write_annotation_file
write_simple  =  rw.write_simple_annotation_file


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''
    Script to perform an analysis on the object references 
    vs DA annotations. 
    ''')
    
    parser.add_argument('data',
                        metavar='<data directory>',
                        description='''
                        directory where all the annotations 
                        are stored
                        ''')
    
    parser.add_argument('list',
                        metavar='<run list>',
                        description='''
                        list of all the runs for which 
                        analysis is to be performed
                        ''')
    
    parser.add_argument('--config',
                        type=str,
                        default=''
                        description='''
                        file where other optional configurations
                        are stored
                        ''');
    
    args = vars(parser.parse_args())
    
    dataDir    = args['data']
    runList    = args['list']
    configFile = args['config']
    
