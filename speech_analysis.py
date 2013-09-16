#!/usr/bin/python

'''
This is a set of tools that perform analysis on the 
ctm files to provide various statistics on the speech data
for each run in CESAR

Author: Akshay Chandrashekaran

version 0.1: 2013/09/16 : 15:00:00
Initial Implementation

'''

import argparse
import headers


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''
    This is a tool to perform speech analysis on the CESAR 
    data. For all the runs specified
    ''')
    
    parser.add_argument('data',
                        metavar='<data-directory>',
                        help='''
                        directory where all the data is located
                        ''')
    
    parser.add_argument('list',
                        metavar='<run-list>',
                        help='''
                        List of runs to be used for analysis
                        ''')
    
    
    args = vars(parser.parse_args())
    
    dataDir   = args['data']
    runListId = args['list']
    
    runListP  = open(runListId,'r')
    
    runList = []
    
    speechAnalysisCount = {}
    for line in runListP:
        line = line.strip()
        runList.append(line)
        speechAnalysisCount[line] = dict()
        speechAnalysisCount[line]['driver']    = 0.0
        speechAnalysisCount[line]['copilot']   = 0.0
        speechAnalysisCount[line]['total']     = 0.0
        speechAnalysisCount[line]['maxLength'] = 0.0
    for run in runList:
        runPath    = dataDir + '/' + run
        # metadataId = runPath + '/' + 'metadata.xml'
        ctmFileId  = runPath + '/' + 'data.fixed.origwords.ctm'
        
        ctmFile = open(ctmFileId,'r')
        
        for line in ctmFile:
            line = line.strip()
            components = line.split()
            s_time  = float(components[0])
            e_time  = float(components[1])
            dur     = e_time - s_time
            speaker = components[2]
            
            speechAnalysisCount[run][speaker] += dur
            speechAnalysisCount[run]['total'] += dur
            speechAnalysisCount[run]['maxLength'] = max(speechAnalysisCount[run]['maxLength'],e_time)
    
    totAnalysis = {}
    totAnalysis['driver'] = 0.0
    totAnalysis['copilot'] = 0.0
    totAnalysis['total']   = 0.0
    totAnalysis['maxLength'] = 0.0
    
    for run in runList:
        line = '\t'.join([run,
                          str(speechAnalysisCount[run]['driver']),
                          str(speechAnalysisCount[run]['copilot']),
                          str(speechAnalysisCount[run]['total']),
                          str(speechAnalysisCount[run]['maxLength'])])
        print line
                         
        for key in (speechAnalysisCount[run]).keys():
            totAnalysis[key] += speechAnalysisCount[run][key]
        
    
    print ''
    line = '\t'.join(['Overall:',
                      str(totAnalysis['driver']),
                      str(totAnalysis['copilot']),
                      str(totAnalysis['total']),
                      str(totAnalysis['maxLength'])])
        
    print line
