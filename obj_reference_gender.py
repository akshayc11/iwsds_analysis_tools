#!/usr/bin/python

'''
This tool is used for analysis of object references 
with respect to gender of the diver and the copilot
'''


import argparse
import os
import read_write_annotation_files as rw
import annotation_schema
import sys
import metadata

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
    
    objectReferenceComplexLabels = annotation_schema.objectReferenceComplexLabels
    
    analysisCount = dict()
    runAnalysisCount = dict()
    
    genderList = ['female', 'male']
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
        runAnalysisCount[objName] = dict()
        for gesture in gestureList:
            analysisCount[objName][gesture] = dict()
            runAnalysisCount[objName][gesture] = dict()
            for gen in genderList:
                analysisCount[objName][gesture][gen] = 0
                runAnalysisCount[objName][gesture][gen] = 0
                
    
    # Update analysisCount from all the runs
    totalCount = 0
    errCount   = 0
    for runId in runList:
        for objName in objList:
            for gesture in gestureList:
                for gen in genderList:
                    runAnalysisCount[objName][gesture][gen] = 0
        runCount = 0
        run               = dataDir + '/' + runId
        objectReferenceId = run + '/' + 'object-reference.xml'
        metadataId        = run + '/' + 'metadata.xml'
        
        metadataObj = metadata.metadata()
        metadataObj.Read(metadataId)
        copilot_gender = metadataObj.get_copilot_gender()
        driver_gender  = metadataObj.get_driver_gender()
        gender = dict()
        gender['driver']  = driver_gender
        gender['copilot'] = copilot_gender
        print runId, 'driver:', driver_gender, 'copilot:', copilot_gender
        
        objWords, objAnnotations, objNotes = read_complex(objectReferenceId)
        
        
        for objAnnotation in objAnnotations:
            objLabel     = objAnnotation.label
            gesture      = ''.join(objLabel.partition('(')[1:])
            label        = objLabel.partition('(')[0].strip()
            objWords     = objAnnotation.words
            spkSet = set()
            for word in objWords:
                spkSet.add(word.speaker)
            
            spkList = sorted(list(spkSet))
            genList = [gender[spk] for spk in spkList]
            for gen in genList:
                try:
                    analysisCount[label][gesture][gen] += 1
                    runAnalysisCount[label][gesture][gen] += 1
                    
                    totalCount += 1
                except:
                    errCount += 1
                    print runId,": error for:", objAnnotation.name
        
        for gen in genderList:
            for objName in objList:
                for gesture in gestureList:
                    print '\t'.join(['',objName, gesture, gen, str(analysisCount[objName][gesture][gen])])
    
    print 'total\t', totalCount
    print 'errors\t', errCount
    for gen in genderList:
        for objName in objList:
            for gesture in gestureList:
                print '\t'.join([objName, gesture, gen, str(analysisCount[objName][gesture][gen])]) 
    
    
    
