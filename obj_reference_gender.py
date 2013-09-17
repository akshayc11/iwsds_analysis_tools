#!/usr/bin/python

import argparse
import os
import read_write_annotation_files as rw
import annotation_schema
import sys
read_complex  =  rw.read_annotation_file
read_simple   =  rw.read_simple_annotation_file
write_complex =  rw.write_annotation_file
write_simple  =  rw.write_simple_annotation_file


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''
    Script to perform an analysis on the object references 
    vs gender of the speakers. 
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
                        default='',
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
    
    domainLabels = annotation_schema.domainLabels
    objectReferenceComplexLabels = annotation_schema.objectReferenceComplexLabels
    
    analysisCount = dict()
    domainList = []
    for domainLabel in domainLabels:
        domainName = domainLabel.name
        domainList.append(domainName)
        
    domainList.sort()
    print domainList    
    objSet = set()
    for objLabel in objectReferenceComplexLabels:
        objName = (objLabel.name).split(' (')[0]
        objSet.add(objName)
        
    objList =list(objSet)
    objList.sort()
    print objList
    
    gestureList = ['(Gesture)', '(No Gesture)']
    
    # Create the analysisCount structure
    for objName in objList:
        analysisCount[objName] = dict()
        
        for gesture in gestureList:
            analysisCount[objName][gesture] = dict()
            
            for domainName in domainList:
                analysisCount[objName][gesture][domainName] = 0
            
    
    # Update analysisCount from all the runs
    totalCount = 0
    errCount   = 0
    for runId in runList:
        print runId
        run               = dataDir + '/' + runId
        objectReferenceId = run + '/' + 'object-reference.xml'
        domainId          = run + '/' + 'domain-annotated.xml'
        
        objWords, objAnnotations, objNotes = read_complex(objectReferenceId)
        domWords, domAnnotations, domNodes = read_simple(domainId)
        
        
        for objAnnotation in objAnnotations:
            objLabel     = objAnnotation.label
            gesture      = ''.join(objLabel.partition('(')[1:])
            label        = objLabel.partition('(')[0].strip()
            objWords     = objAnnotation.words
            domSet = set()
            for word in objWords:
                for domAnnotation in domAnnotations:
                    wordNames = [wrd.name for wrd in domAnnotation.words]
                    if word.name in wordNames:
                        #print domAnnotation.label
                        domSet.add(domAnnotation.label)
                    
                
            
            domList = sorted(list(domSet))
            if len(domList) == 0:
                domList.append('OOD')
            #print gesture, label,domList 
            for dom in domList:
                try:
                    analysisCount[label][gesture][dom] += 1
                    totalCount += 1
                except:
                    errCount += 1
                    print runId,": error for:", objAnnotation.name
                    
    for objName in objList:
        for gesture in gestureList:
            for domainName in domainList:
                print '\t'.join([objName, gesture, domainName, str(analysisCount[objName][gesture][domainName])]) 
    
    print 'total\t', totalCount
    print 'errors\t', errCount
