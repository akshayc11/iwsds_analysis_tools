#!/usr/bin/python

import argparse
import metadata

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''
    This script uses the specified metadata.xml and gets the offset fom it. 
    It subtracts all the numbers in the input file with this offset and 
    then stores it in the output file specified
    ''')
    
    parser.add_argument('input',
                        metavar='<input file>',
                        help='path to input file')
    
    parser.add_argument('meta',
                        metavar='<metadata.xml>',
                        help='path to metadata file')
    
    parser.add_argument('output',
                        metavar='<output file>',
                        help='path to output file')
    
    
    args = vars(parser.parse_args())
    
    inputFileId  = args['input']
    metadataId   = args['meta']
    outputFileId = args['output']
    
    metadataObj = metadata.metadata()
    metadataObj.Read(metadataId)
    
    offset = metadataObj.get_offset()
    
    inputFile  = open(inputFileId,'r')
    outputFile = open(outputFileId,'w')
    for line in inputFile:
        line = line.strip()
        comps = [float(comp) for comp in line.split()]
        noOffComps = ['%0.3f'%(comp - offset) for comp in comps]
        outLine = '\t'.join(noOffComps)
        print line, ':', outLine
        outLine += '\n'
        outputFile.write(outLine)
        
    inputFile.close()
    outputFile.close()

