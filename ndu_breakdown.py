#!/usr/bin/python
# ndu_breakdown.py

"""
Analysis of NDU structure, breakdowns by driver gender, copilot
"""


import os
import read_write_annotation_files as rw
import annotation_schema
import sys
import metadata
import numpy as np
import matplotlib.pyplot as plt
import collections

read_complex  =  rw.read_annotation_file
read_simple   =  rw.read_simple_annotation_file
write_complex =  rw.write_annotation_file
write_simple  =  rw.write_simple_annotation_file

data_dir = "../data/"
run_ids = ['CESAR_Jun-Sun-3-09-09-17-2012', 'CESAR_Jun-Sun-3-11-10-36-2012', 'CESAR_Jun-Sun-3-13-01-47-2012', 'CESAR_Jun-Thu-21-09-08-54-2012', 'CESAR_Jun-Thu-21-11-04-52-2012', 'CESAR_Jun-Thu-21-13-30-23-2012', 'CESAR_Jun-Thu-21-17-12-36-2012', 'CESAR_May-Fri-25-14-55-42-2012', 'CESAR_May-Fri-25-17-05-43-2012', 'CESAR_May-Fri-25-19-15-14-2012', 'CESAR_May-Thu-17-11-36-14-2012', 'CESAR_May-Thu-31-09-17-54-2012', 'CESAR_May-Thu-31-11-21-35-2012', 'CESAR_May-Thu-31-15-06-55-2012', 'CESAR_May-Tue-29-13-06-47-2012']

ndu_da_map = dict()
male_driver_ndu_da_map = dict()
female_driver_ndu_da_map = dict()

run_driver_gender_map = dict()
total_number_of_das = 0



#### construct NDU/DA map
for r in run_ids:
    print r
    ndu_w, ndu_ann, ndu_notes = read_complex(data_dir+r+'/NDU.xml')
    da_w, da_ann, da_notes = read_complex(data_dir+r+'/DA.xml')
    total_number_of_das += len(da_ann)
    m = metadata.metadata()
    m.Read(data_dir+r+'/metadata.xml')
    run_driver_gender_map[r] = m.attribs['driver_gender']

    # figure out which DA's are contained by each NDU
    for n in ndu_ann:
        n_word_names = set([w.name for w in n.words])
        das_contained = set()
        for d in da_ann:
            for w in d.words:
                if w.name in n_word_names:
                    das_contained.add(d)
                    break
        ndu_da_map[n] = das_contained
        if m.attribs['driver_gender'] == 'male':
            male_driver_ndu_da_map[n] = das_contained
        else:
            female_driver_ndu_da_map[n] = das_contained
     

das_per_ndu = [len(x) for x in ndu_da_map.values()]
male_driver_das_per_ndu = [len(x) for x in male_driver_ndu_da_map.values()]
female_driver_das_per_ndu = [len(x) for x in female_driver_ndu_da_map.values()]
print
print "mean NDU length:", np.mean(das_per_ndu)
print "STD NDU length:", np.std(das_per_ndu)
print "n samples:", len(das_per_ndu)
print
print "male driver mean NDU length:", np.mean(male_driver_das_per_ndu)
print "male driver STD NDU length:", np.std(male_driver_das_per_ndu)
print "n samples:", len(male_driver_das_per_ndu)
print
print "female driver mean NDU length:", np.mean(female_driver_das_per_ndu)
print "female driver STD NDU length:", np.std(female_driver_das_per_ndu)
print "n samples:", len(female_driver_das_per_ndu)


# # plt.hist(das_per_ndu, normed=1, facecolor='b', alpha=.3, bins=range(11))
# plt.hist(male_driver_das_per_ndu, normed=1, facecolor='g', alpha=.3, bins=range(11))
# plt.hist(female_driver_das_per_ndu, normed=1, facecolor='r', alpha=.3, bins=range(11))
# plt.show()

# # compare the total number of DAs to the sum of DAs in each NDU
# # they should be the same (They're not)
# print 'These two numbers should be the same:'
# print sum(das_per_ndu)
# print total_number_of_das

#### get the overall DA breakdown
all_DAs = reduce(lambda x, y: x | y, ndu_da_map.values(), set())
print
print 'total'
print len(all_DAs)
print collections.Counter([x.label for x in all_DAs])
male_driver_DAs = reduce(lambda x, y: x | y, male_driver_ndu_da_map.values(), set())
print
print 'male driver'
print len(male_driver_DAs)
print collections.Counter([x.label for x in male_driver_DAs])
female_driver_DAs = reduce(lambda x, y: x | y, female_driver_ndu_da_map.values(), set())
print
print 'female driver'
print len(female_driver_DAs)
print collections.Counter([x.label for x in female_driver_DAs])

#### Get all the sequences of DAs, gesture-dependent
sequence_counter = collections.Counter()
for n in ndu_da_map.keys():
    da_sequence = sorted(ndu_da_map[n], key=lambda x: min([y.s_time for y in x.words])) # in-order DA sequence for n
    da_sequence = tuple([x.label for x in da_sequence])
    sequence_counter.update([da_sequence])
    
print
print len(sequence_counter), "different sequences of DA's showed up in the data"
common_sequences = sorted(sequence_counter.keys(), key = lambda k: sequence_counter[k], reverse=True)
for i in range(10):
    print sequence_counter[common_sequences[i]], common_sequences[i]







