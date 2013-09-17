#!/usr/bin/python

import read_write_annotation_files as rw
import sys
import argparse
import annotation_schema

read_complex  =  rw.read_annotation_file
read_simple   =  rw.read_simple_annotation_file
write_complex =  rw.write_annotation_file
write_simple  =  rw.write_simple_annotation_file

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''
    This function cleans up any annotation by removing 
    empty annotations from the input Annotation File
    ''')
    
    parser.add_argument('input',
                        metavar='<input annotation file>',
                        help='Input annotation file in XML format')
    
    # parser.add_argument('output',
    #                     metavar='<output annotation file>',
    #                     help='Output annotaiotn file in XML format')
    
    parser.add_argument('--complex',
                        action='store_true',
                        help='Indicate if annotations are complex or not')
    
    args = vars(parser.parse_args())
    
    Complex = args['complex']
    
    if Complex == True:
        read_annotation  = read_complex
        write_annotation = write_complex
    else:
        read_annotation  = read_simple
        write_annotation = write_simple
    
    
    inFileId  = args['input']
    #outFileId = args['output']
    
    inWords, inAnnots, inNotes = read_annotation(inFileId)
    
    remList = []
    for i in range(len(inAnnots)):
        inAnnot = inAnnots[i]
        words   = inAnnot.words
        if len(words) > 0:
            continue
        print inAnnot.name
        remList.append(i)
    
    # remList.reverse()
    
    # for rem in remList:
    #     inAnnots.pop(rem)
    
    # write_annotation(inWords, inAnnots, inNotes, outFileId)
    
