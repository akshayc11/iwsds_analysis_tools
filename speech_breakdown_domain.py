#!/usr/bin/python

'''
This tool is used to find the amount of time spent by 
the driver and copilot in any of the domains

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
    
    domainLabels = annotation_schema.domainLabels
    
    analysisCount = dict()
    runAnalysisCount = dict()
    
    domNames =  [domainLabel.name for domainLabel in domainLabels]
    spkList  =  ['copilot', 'driver']
    
    # Create the analysisCount structure
    for domName in domNames:
        analysisCount[domName] = dict()
        runAnalysisCount[domName] = dict()
        for spk in spkList:
            analysisCount[domName][spk] = 0
            runAnalysisCount[domName][spk] = 0
                
    
    # Update analysisCount from all the runs
    totalCount = 0
    errCount   = 0
    print '\t'.join(domNames)
    for runId in runList:
        for domName in domNames:
            for spk in spkList:
                runAnalysisCount[domName][spk] = 0
        runCount = 0
        run               = dataDir + '/' + runId
        domainId = run + '/' + 'domain-annotated.xml'
        
        domWords, domAnnotations, domNotes = read_simple(domainId)
        
        
        for domAnnotation in domAnnotations:
            domLabel     = domAnnotation.label
            Words     = domAnnotation.words
            for word in Words:
                if word in domWords:
                    domWords.remove(word)
                spk = word.speaker
                s_time = float(word.s_time)
                e_time = float(word.e_time)
                try:
                    analysisCount[domLabel][spk] += (e_time - s_time)
                    runAnalysisCount[domLabel][spk] += (e_time - s_time)
                
                except:
                    errCount += 1
                    print "error for", word.name
        # All remaining words are a part of OOD
        for word in domWords:
            spk = word.speaker
            s_time = float(word.s_time)
            e_time = float(word.e_time)
            domLabel='OOD'
            try:
                analysisCount[domLabel][spk] += (e_time - s_time)
                runAnalysisCount[domLabel][spk] += (e_time - s_time)
                
            except:
                errCount += 1
                print "error for", word.name
        print runId
        for spk in spkList:
            line = ['\t' + spk]
            domVals = [str(runAnalysisCount[domName][spk]) for domName in domNames]
            line = line + domVals
            print '\t'.join(line)
        
    
    print '\nTotal:'
    
    for spk in spkList:
        line = ['\t' + spk]
        domVals = [str(analysisCount[domName][spk]) for domName in domNames]
        line = line + domVals
        print '\t'.join(line)
    
    
