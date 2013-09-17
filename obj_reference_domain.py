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
    vs domain annotations. 
    ''')
    
    parser.add_argument('data',
                        metavar='<data directory>',
                        help='''
                        directory where all the annotations 
                        are stored
                        ''')
    
    parser.add_argument('list',
                        metavar='<run list>',
                        help='''
                        list of all the runs for which 
                        analysis is to be performed
                        ''')
    
    parser.add_argument('--config',
                        type=str,
                        default=''
                        help='''
                        file where other optional configurations
                        are stored
                        ''');
    
    args = vars(parser.parse_args())
    
    dataDir      = args['data']
    runListId    = args['list']
    configFileId = args['config']
    
    runListP = open(runListId, 'r')
    
    runList = []
    for line in runListP:
        line = line.strip()
        runList.append(line)
    
    analysisCount = dict()
        domainList = []
        for domainLabel in domainLabels:
            domainName = domainLabel.name
            domainList.append(domainName)
        
        domainList.sort()
        
        objSet = set()
        for objLabel in objectReferenceComplexLabels:
            objName = (objLabel.name).split(' (')
            objSet.add(objName)
        
        objList =list(objSet)
        objList.sort()
        
        gestureList = ['(Gesture)', '(No Gesture)']
    
    # Create the analysisCount structure
    for objName in objList:
        analysisCount[objName] = dict()
        
        for gesture in gestureList:
            analysisCount[objName][gesture] = dict()
            
            for domainName in domainList:
                analysisCount[objName][gesture][domainName] = 0
            
        
    # Update analysisCount from all the runs
    for runId in runList:
        run               = dataDir + '/' + runId
        objectReferenceId = run + '/' + 'object-reference.xml'
        domainId          = run + '/' + 'DA.xml'
        
        objWords, objAnnotations, objNotes = read_complex(objectReferenceId)
        domWords, domAnnotations, domNodes = read_simple(domainId)
        
        
        
        
