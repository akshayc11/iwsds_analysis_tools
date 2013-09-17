#!/usr/bin/python

import read_write_annotation_files as rw
import argparse
import annotation_schema
import sys

read_simple  = rw.read_simple_annotation_file
write_simple = rw.write_simple_annotation_file

if __name__ == '__main__':
    
    # Parse the command line
    parser = argparse.ArgumentParser(description='''
    Script to remove OOV from domain annotations
    ''')
    
    parser.add_argument('input',
                        metavar='<Input Domain Annotated File>',
                        help='Input Domain annotation xml file')
    
    parser.add_argument('output',
                        metavar='<Output Domain Annotated File>',
                        help='Output Domain annotationxml file')
    
    args = vars(parser.parse_args())
    
    inputFileId  = args['input']
    outputFileId = args['output']
    
    inWords, inAnnots, inNotes = read_simple(inputFileId)
    
    domainLabels = annotation_schema.domainLabels
    
    domainNames = [domain.name for domain in domainLabels]
    if len(inAnnots) > 0:
        if not (inAnnots[0].label in domainNames):
            print "Error: input file is not a domain annotated file. Aborting"
            sys.exit(1)
    remList = []
    for i in range(len(inAnnots)):
        if inAnnots[i].label == 'OOD':
            remList.append(i)
    
    remList.reverse()
    
    for rem in remList:
        inAnnots.pop(rem)
    
    write_simple(inWords, inAnnots, inNotes, outputFileId)
