#!/usr/bin/python

import sys
import re
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
                        '--delimiter',
                        type=str,
                        default='\t',
                        help=': delimiter for output file, default="\\t"')
    
    parser.add_argument('-n',
                        '--not-available',
                        type=str,
                        default='<NA>',
                        help=': replacement if a field is not available')
    args = vars(parser.parse_args())
    
    dataDir      = args['data']
    listFileId   = args['list']
    outputFileId = args['output']
    delimiter    = args['delimiter']
    print delimiter
    unavailable  = args['not_available']
    
    listFile = open(listFileId,'r')
    runList = []
    for line in listFile:
        line = line.strip()
        runList.append(line)
    
    outputFile = open(outputFileId,'w')
    
    # Aggregate data
    for run in runList: #
        runDir        = dataDir + '/' + run

        domFile      = runDir + '/domain-annotated.xml'
        objFile      = runDir + '/object-reference.xml'
        nduFile      = runDir + '/NDU.xml'
        daFile       = runDir + '/DA.xml'
        metadataDile = runDir + '/metadata.xml'
        

        domWords, domAnnots, domNotes = read_simple(domFile)
        objWords, objAnnots, objNotes = read_complex(objFile)
        nduWords, nduAnnots, nduNotes = read_complex(nduFile)
        daWords,  daAnnots,  daNotes  = read_simple(daFile)
        
        domLen  = len(domWords)
        objLen  = len(objWords)
        nduLen  = len(nduWords)
        daLen   = len(daWords)
        
        if (domLen!=objLen) or (objLen != nduLen) or \
           (nduLen != daLen) or (daLen != domLen):
            print "Error:",run,": the annotation files seem to have different number of words"
            print domLen, objLen, nduLen, daLen
            sys.exit(1)
        # continue
        for i in range(len(domWords)):
            domWord = domWords[i]
            objWord = objWords[i]
            nduWord = nduWords[i]
            daWord  = daWords[i]
            
            s_time  = domWord.s_time  #
            e_time  = domWord.e_time  #
            text    = domWord.text    #
            speaker = domWord.speaker #
            
            # Find the domains for this word
            domAnns = [domAnnot for domAnnot in domAnnots if domWord in domAnnot.words]
            
            domLabels = [domAnn.label for domAnn in domAnns]
            if len(domLabels) == 0:
                domLabels = ['OOD']
        
            domStr = ' '.join(domLabels)
            domains = '' + domStr + '' #
        
            # Find the object references in this word if any:
            objAnns = [objAnnot for objAnnot in objAnnots 
                       if objWord in objAnnot.words]
            
            objNames   = [objAnn.name for objAnn in objAnns]
            objObjects = [objAnn.object_parameter for objAnn in objAnns]
            # if len(objNames) == 0:
            #     objNames   = [unavailable]
            #     objObjects = [unavailable]
        
            objNameStr   = ' '.join(objNames) 
            objNames = '' + objNameStr + '' # 
            objectStr    = ' '.join(objObjects)
            objects      = '' + objectStr + '' # 
            
            
            nduAnns = [nduAnnot for nduAnnot in nduAnnots if nduWord in nduAnnot.words]
            
            nduNames     = [nduAnn.name for nduAnn in nduAnns]
            nduNameStr   = ' '.join(nduNames)
            nduNames     = '' + nduNameStr + '' #
            
            nduObjects   = [nduAnn.object_parameter for nduAnn in nduAnns]
            nduObjStr    = ' '.join(nduObjects)
            nduObjects   = '' + nduObjStr + '' #
            
            daAnns       = [daAnnot for daAnnot in daAnnots
                            if daWord in daAnnot.words]
            
            daNames      = [daAnn.name for daAnn in daAnns]
            daNameStr    = ' '.join(daNames)
            daNames      = '' + daNameStr + '' #
            
            dataList     = [run,
                            speaker,
                            str(s_time),
                            str(e_time),
                            text,
                            domains,
                            objNames,
                            nduNames,
                            daNames]
            dataString   = delimiter.join(dataList)
            dataString   = dataString + '\n'
            outputFile.write(dataString)
            
