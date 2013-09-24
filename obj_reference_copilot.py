#!/usr/bin/python

'''
This tool is used for analysis of object references 
with respect to the copilots
'''


import argparse
import os
import read_write_annotation_files as rw
import annotation_schema
import sys
import metadata
import time
import datetime

read_complex  =  rw.read_annotation_file
read_simple   =  rw.read_simple_annotation_file
write_complex =  rw.write_annotation_file
write_simple  =  rw.write_simple_annotation_file

monthDict = {}
monthDict['Jan'] = 1
monthDict['Feb'] = 2
monthDict['Mar'] = 3
monthDict['Apr'] = 4
monthDict['May'] = 5
monthDict['Jun'] = 6
monthDict['Jul'] = 7
monthDict['Aug'] = 8
monthDict['Sep'] = 9
monthDict['Oct'] = 10
monthDict['Nov'] = 11
monthDict['Dec'] = 12


def runID_hash(runId):
    datetime_str = runId.split('_')[1]
    components = datetime_str.split('-')
    year     = int(components[-1])
    month    = monthDict[components[0]]
    date     = int(components[2])
    hour     = int(components[3])
    minute   = int(components[4])
    second   = int(components[5])
    dateTime = datetime.datetime(year, month, date, hour, minute, second)
    copTime  = time.mktime(datetime.datetime.utctimetuple(dateTime))
    return copTime
    
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
                
    copilotNameSet = set()
    for runId in runList:
        run        = dataDir + '/' + runId
        metadataId = run     + '/' + 'metadata.xml'
        metadataObj = metadata.metadata()
        metadataObj.Read(metadataId)
        copilotNameSet.add(metadataObj.get_copilot_name())
    
    copilotNameList = list(copilotNameSet)
    copilotNameList.sort()
    analysisCount = dict()
    for copilotName in copilotNameList:
        analysisCount[copilotName] = dict()
        for objName in objList:
            analysisCount[copilotName][objName] = dict()
            for gesture in gestureList:
                analysisCount[copilotName][objName][gesture] = 0
            
        
    
    # Update analysisCount from all the runs
    totalCount = 0
    errCount   = 0
    for runId in runList:
        # Convert runID into datetime object
        copTime = runID_hash(runId)
        
        
        runCount = 0
        run               = dataDir + '/' + runId
        objectReferenceId = run     + '/' + 'object-reference.xml'
        metadataId        = run     + '/' + 'metadata.xml'
        
        metadataObj = metadata.metadata()
        metadataObj.Read(metadataId)
        copilot_name   = metadataObj.get_copilot_name()
        
        
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
            spk = spkList[0]
            if spk == 'copilot':
                #print spkList
                analysisCount[copilot_name][label][gesture] += 1
            
        
    
    for copName in copilotNameSet:
        print copName
        for gesture in gestureList:
            printList = [str(analysisCount[copName][objName][gesture]) for objName in objList]
            printStr  = '\t'.join(printList)
            print gesture,'\t',printStr

