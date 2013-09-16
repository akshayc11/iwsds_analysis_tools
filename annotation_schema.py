#Annotation_schema.py
from headers import *
import read_write_annotation_files as rw

##### Set the list of labels for simple_annotation
domainLabels = []
DALabels = []
# for domain annotation, uncomment this block:
domainLabels.append(simple_label('Navigation', """ """))
domainLabels.append(simple_label('Business Search / Local Guide', """ """))
domainLabels.append(simple_label('Alerts / Messaging', """ """))
domainLabels.append(simple_label('Scheduling', """ """))
domainLabels.append(simple_label('OOD', """ """))
domainLabels.append(simple_label('Experiment-OOD', """ """))

# DA annotation schema
DALabels.append(simple_label('Direct (Gesture)', """ """))
DALabels.append(simple_label('Direct (No Gesture)', """ """))
DALabels.append(simple_label('Offer (Gesture)', """ """))
DALabels.append(simple_label('Offer (No Gesture)', """ """))
DALabels.append(simple_label('Request Direction (Gesture)', """ """))
DALabels.append(simple_label('Request Direction (No Gesture)', """ """))
DALabels.append(simple_label('Ask Clarification (Gesture)', """ """))
DALabels.append(simple_label('Ask Clarification (No Gesture)', """ """))
DALabels.append(simple_label('Give Clarification (Gesture)', """ """))
DALabels.append(simple_label('Give Clarification (No Gesture)', """ """))
DALabels.append(simple_label('Acknowledge / Confirm (Gesture)', """ """))
DALabels.append(simple_label('Acknowledge / Confirm (No Gesture)', """ """))
DALabels.append(simple_label('Reject (Gesture)', """ """))
DALabels.append(simple_label('Reject (No Gesture)', """ """))
DALabels.append(simple_label('Other (Gesture)', """ """))
DALabels.append(simple_label('Other (No Gesture)', """ """))




##### For complex_annotation, 
objectReferenceComplexLabels = []
NDUComplexLabels = []
# Object reference annotation
objectReferenceComplexLabels.append(complex_label('Traffic Signal (Gesture)', ['traffic_signal', 'generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Traffic Signal (No Gesture)', ['traffic_signal', 'generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Road or Driveway (Gesture)', ['driveable', 'parking', 'generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Road or Driveway (No Gesture)', ['driveable', 'parking', 'generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Person or Vehicle (Gesture)', ['person','vehicle','landmark','generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Person or Vehicle (No Gesture)', ['person', 'vehicle','landmark','generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Building or Public Space (Gesture)', ['destination','parking_lot','landmark','generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Building or Public Space (No Gesture)', ['destination','parking_lot','landmark','generic'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Other (Gesture)', ['object'], 'obj only', """ """))
objectReferenceComplexLabels.append(complex_label('Other (No Gesture)', ['object'], 'obj only', """ """))

# NDU annotation schema
NDUComplexLabels.append(complex_label('Go To', ['driveable', 'parking'], 'obj only', """ """))
NDUComplexLabels.append(complex_label('Leave', ['driveable', 'parking'], 'obj only', """ """))
NDUComplexLabels.append(complex_label('Stop At', ['driveable', 'parking'], 'obj only', """ """))
NDUComplexLabels.append(complex_label('Set Destination', ['destination', 'landmark'], 'obj only', """ """))
NDUComplexLabels.append(complex_label('Other', [], 'neither', """ """))


##### Set filter function
domain_filter_label_list = []
DA_filter_label_list = ['Go To', 'Leave', 'Stop At']
NDU_filter_label_list = ['Navigation']
obj_ref_filter_label_list = []

#load objects from kml and elsewhere
kml_file = 'My Places.kml'
objects = []

for s in ['driver', 'copilot', 'sam_mckenna', 'phil_collison']:
    objects.append(obj(s, ['person', 'object']))
objects.append(obj('car', ['vehicle', 'object']))
objects.append(obj('moffett_field', ['object', 'destination']))

# these are abstract objects, we are only labeling physical object references
# for s in ['business_meeting@nanotech', 'business_meeting@crown_startup_funds', 'phils_business_meeting@barracks', 'social_meeting@sams', 'social_meeting@dinner']:
#     objects.append(obj(s, ['meeting', 'event']))

objs = rw.get_objects(kml_file)
for o in objs:
    o.types.extend(['object', 'situated'])
    objects.append(o)

for s in ['Other', 'Unknown', 'Set']:
    objects.append(obj(s, ['generic']))


