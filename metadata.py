#!/usr/bin/python

'''
Module for importing in the CESAR corpus metadata
Data is stored in the metadata class

Primarily written for getting the attributes of a run for conversion
of the 
'''
import xml.etree.ElementTree as etree

class metadata(object):
    '''
    metadata class:
    Contains all the relevant information of a particular run 
    needed for kaldi data preparation.
    This includes: run_id, speakers, channels, some speaker related information
    '''
    
    inFileID       = ""
    channel_1      = "l"
    channel_2      = "r"
    speaker_1      = "driver"
    speaker_2      = "copilot"
    copilot_name   = ""
    copilot_gender = ""
    driver_gender  = ""
    run_id         = ""
    tree           = []
    attribs        = {}
    driver_id      = ""
    copilot_id     = ""
    channels       = {}
    offset         = 0.0
    verbosity      = 0
    
    def _getOffset(self,offset_str):
        offset_str = offset_str[1:-1]
        offset_tuple = [float(comp) for comp in offset_str.split(', ')]
        offset       = (offset_tuple[0]*60.0) + \
                       (offset_tuple[1]) + \
                       (offset_tuple[2]/30.0)
        
        return offset
    def __init__(self, verbosity=0):
        '''
        Initialize the metadata object
        '''
        self.verbosity      = verbosity
        self.inFileID       = ""
        self.channel_1      = "1"
        self.channel_2      = "2"
        self.speaker_1      = "driver"
        self.speaker_2      = "copilot"
        self.copilot_name   = ""
        self.copilot_gender = ""
        self.driver_gender  = ""
        self.run_id         = ""
        self.tree           = []
        self.attribs        = {}
        self.driver_id      = ""
        self.copilot_id     = ""
        self.channels       = {}
        self.offset         = 0.0
        return None
    
    def Clear(self):
        '''
        Clear the metadata object
        '''
        self.inFileID       = ""
        self.channel_1      = "l"
        self.channel_2      = "r"
        self.speaker_1      = "driver"
        self.speaker_2      = "copilot"
        self.copilot_name   = ""
        self.copilot_gender = ""
        self.driver_gender  = ""
        self.run_id         = ""
        self.tree           = []
        self.attribs        = {}
        self.driver_id      = ""
        self.copilot_id     = ""
        self.channels       = {}
        return True
    
    def Read(self, inFileID, flipChannel=False):
        
        self.inFileID = inFileID
        if inFileID == "":
            print "No xml File linked..."
            return False
        self.tree = etree.parse(inFileID)
        root = self.tree.getroot()
        self.attribs = root[0].attrib
        
        if flipChannel is False:
            self.channel_1 = "l"
            self.channel_2 = "r"
        
        else:
            self.channel_1 = "r"
            self.channel_2 = "l"
            
        if self.attribs.has_key('channel_1'):
            self.speaker_1 = self.attribs['channel_1']
            self.channels[self.speaker_1] = self.channel_1
            
        if self.attribs.has_key('channel_2'):
            self.speaker_2 = self.attribs['channel_2']
            self.channels[self.speaker_2] = self.channel_2
            
        
        
        
        if self.attribs.has_key('copilot_name'):
            self.copilot_name           = self.attribs['copilot_name']
        
        if self.attribs.has_key('driver_gender'):
            self.driver_gender         = self.attribs['driver_gender']
        
        if self.attribs.has_key('copilot_gender'):
            self.copilot_gender        = self.attribs['copilot_gender']
        
        if self.attribs.has_key('run_id'):
            self.run_id = self.attribs['run_id']
        
        self.offset = self._getOffset(self.attribs['audio_start_point'])
        
        return True
    
    def get_channels(self):
        '''
        Return a dictionary where the channels are stored by 
        key as speaker id and value as channel number
        '''
        return self.channels
    
    def get_copilot_gender(self):
        '''
        return copilot gender
        '''
        return self.copilot_gender
    
    def get_copilot_name(self):
        '''
        return copilot name
        '''
        return self.copilot_name
    
    def get_run_id(self):
        '''
        return run ID
        '''
        return self.run_id
    
    def get_driver_gender(self):
        '''
        return driver gender
        '''
        return self.driver_gender
    
    def get_driver_speaker_ID(self,
                              include_run_id=True,
                              include_driver_gender=False,
                              include_channel=False):
        '''
        Sets speakerID of the driver in the metadata class and returns it
        '''
        self.driver_id = ""
        
        if include_run_id is True:
            self.driver_id += self.run_id + "-"
        self.driver_id += "driver"
        
        if include_driver_gender is True:
            self.driver_id += "-" + self.driver_gender
        
        if include_channel is True:
            self.driver_id += "-" + self.channels['driver']
        
        return self.driver_id

    def get_copilot_speaker_ID(self,
                              include_run_id=True,
                              include_copilot_name=False, 
                              include_channel=False):
        '''
        Sets the speaker ID of the copilot in the metadata class and 
        returns the same
        '''
        
        self.copilot_id = ""
        
        if include_run_id is True:
            self.copilot_id += self.run_id + "-"
        self.copilot_id += "copilot"
        
        if include_copilot_name is True:
            self.copilot_id += "-" + self.copilot_name
        
        if include_channel is True:
            self.copilot_id += "-" + self.channels['copilot']
        
        return self.copilot_id
    
    
    def get_offset(self):
        '''
        Return the offset of the audio start point 
        '''
        return self.offset
