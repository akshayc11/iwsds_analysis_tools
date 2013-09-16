#headers.py

#cotains common classes for the annotation task
#word, utterance, annotation


class word:
    def __init__(self):
        self.name = ''
        self.text = ''
        self.s_time = None
        self.e_time = None
        self.speaker = None

class utterance:
    def __init__(self):
        self.words = []
        self.speaker = None
        self.s_time = None
        self.e_time = None
    def add_word(self, w):
        self.words.append(w)
        self.s_time = min([x.s_time for x in self.words])
        self.e_time = max([x.e_time for x in self.words])

#complex annotation class
class complex_annotation:
    def __init__(self):
        self.number = ''
        self.name = ''
        self.words =  []
        self.label = ''
        self.object_parameter = ''
        self.text_parameter = ''
    def text(self):
        return ' '.join([w.text for w in sorted(self.words, key=lambda x: x.s_time)])

#simple annotation class
class simple_annotation:
    def __init__(self):
        self.number = ''
        self.name = ''
        self.words = []
        self.label = ''
    def text(self):
        return ' '.join([w.text for w in sorted(self.words, key=lambda x: x.s_time)])

#for an annotator to leave a note
class note:
    def __init__(self):
        self.text = ''
        self.reference = ''

class simple_label:
    def __init__(self, name, doc_string):
        self.name = name
        self.doc_string = doc_string

# In addition to the label and doc string information,
# a complex label includes filtering information for parameters
class complex_label:
    def __init__(self, name, obj_allowed_types, parameter_restrictions, doc_string):
        self.name = name
        self.obj_allowed_types = obj_allowed_types
        #parameter_restrictions = 'obj only', 'text only', 'neither', or 'both' (no XOR enforcement)
        if not parameter_restrictions in ['obj only', 'text only', 'neither', 'both']:
            print 'error in DA', name, 'declaration'
            print 'invalid parameter restriction:', parameter_restrictions
            exit()
           
        self.parameter_restrictions = parameter_restrictions
        self.doc_string = doc_string
    def filter_allowable_object_params(self, objs):
        return [o for o in objs if len([t for t in o.types if t in self.obj_allowed_types+['generic']]) > 0]

# an obj to be a parameter for a complex annotation.
# it can have many types
class obj:
    def __init__(self, name, types):
        self.name = name
        self.types = types
