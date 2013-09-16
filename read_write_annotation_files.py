#read_write_annotation_files.py
#read and write annotation files to and from xml


from headers import *
from xml.dom import minidom
import ast

class item:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
    def dom_node(self, doc):
        n = doc.createElement(self.name)
        for a in sorted(self.attributes.keys()):
            n.setAttribute(str(a), str(self.attributes[a]))
        return n


def write_annotation_file(words, annotations, notes, filename):
    """Write annotation files for complex annotations"""
    #print dir(minidom)
    doc = minidom.getDOMImplementation().createDocument(None, "ANNOTATION_FILE", None)
    top_element = doc.documentElement
    
    #add words
    words_node = doc.createElement('WORDS')
    for w in sorted(words, key=lambda x: x.s_time):
        n = item('word', {'name':w.name, 'text':w.text, 's_time':w.s_time, 'e_time':w.e_time, 'speaker':w.speaker})
        words_node.appendChild(n.dom_node(doc))
    top_element.appendChild(words_node)

    #add annotations
    annotations_node = doc.createElement('ANNOTATIONS')
    for a in annotations:
        n = item('annotation', {'name':a.name, 'words':[w.name for w in a.words], 'label':a.label, 'object_parameter':a.object_parameter, 'text_parameter':a.text_parameter, 'number':a.number})
        annotations_node.appendChild(n.dom_node(doc))
    top_element.appendChild(annotations_node)

    #add notes
    notes_node = doc.createElement('NOTES')
    for note in notes:
        n = item('note', {'text':note.text, 'reference':note.reference})
        notes_node.appendChild(n.dom_node(doc))
    top_element.appendChild(notes_node)

    #write file
    doc.writexml(open(filename,'w'), addindent='    ', newl='\n')
        

def write_simple_annotation_file(words, annotations, notes, filename):
    """Write annotation file for simple annotation program

    These files contain a set of words, a set of annotations, and a set of notes
    """
    #print dir(minidom)
    doc = minidom.getDOMImplementation().createDocument(None, "ANNOTATION_FILE", None)
    top_element = doc.documentElement
    
    #add words
    words_node = doc.createElement('WORDS')
    for w in sorted(words, key=lambda x: x.s_time):
        n = item('word', {'name':w.name, 'text':w.text, 's_time':w.s_time, 'e_time':w.e_time, 'speaker':w.speaker})
        words_node.appendChild(n.dom_node(doc))
    top_element.appendChild(words_node)

    #add annotations
    annotations_node = doc.createElement('ANNOTATIONS')
    for a in annotations:
        n = item('annotation', {'name':a.name, 'words':[w.name for w in a.words], 'label':a.label, 'number':a.number})
        annotations_node.appendChild(n.dom_node(doc))
    top_element.appendChild(annotations_node)

    #add notes
    notes_node = doc.createElement('NOTES')
    for note in notes:
        n = item('note', {'text':note.text, 'reference':note.reference})
        notes_node.appendChild(n.dom_node(doc))
    top_element.appendChild(notes_node)

    #write file
    doc.writexml(open(filename,'w'), addindent='    ', newl='\n')


def read_annotation_file(filename):
    """Read annotation file for custom DA and object reference annotation program"""
    w_map = dict()
    words = []
    annotations = []
    notes = []
    doc = minidom.parse(open(filename, 'r'))
    top_element = doc.childNodes[0]
    words_node = [n for n in top_element.childNodes if n.nodeName == 'WORDS'][0]
    annotations_node = [n for n in top_element.childNodes if n.nodeName == 'ANNOTATIONS'][0]
    notes_node = [n for n in top_element.childNodes if n.nodeName == 'NOTES'][0]

    word_items = [n for n in words_node.childNodes if n.nodeName == 'word']
    for wi in word_items:
        w = word()
        w.name = wi.getAttribute('name')
        w.text = wi.getAttribute('text')
        w.s_time = float(wi.getAttribute('s_time'))
        w.e_time = float(wi.getAttribute('e_time'))
        w.speaker = wi.getAttribute('speaker')
        words.append(w)
        w_map[wi.getAttribute('name')] = w

    annotation_items = [n for n in annotations_node.childNodes if n.nodeName == 'annotation']
    for ai in annotation_items:
        a = complex_annotation()
        a.name = ai.getAttribute('name')
        a.number = int(ai.getAttribute('number'))
        #ast.literal_eval should be safer than eval()ing an untrusted string
        a.words = [w_map[x] for x in ast.literal_eval(ai.getAttribute('words'))]
        a.label = ai.getAttribute('label')
        a.object_parameter = ai.getAttribute('object_parameter')
        a.text_parameter = ai.getAttribute('text_parameter')
        annotations.append(a)


    return words, annotations, notes



def read_simple_annotation_file(filename):
    """Read annotation file for simple annotation program"""
    w_map = dict()
    words = []
    annotations = []
    notes = []
    doc = minidom.parse(open(filename, 'r'))
    top_element = doc.childNodes[0]
    words_node = [n for n in top_element.childNodes if n.nodeName == 'WORDS'][0]
    annotations_node = [n for n in top_element.childNodes if n.nodeName == 'ANNOTATIONS'][0]
    notes_node = [n for n in top_element.childNodes if n.nodeName == 'NOTES'][0]

    word_items = [n for n in words_node.childNodes if n.nodeName == 'word']
    for wi in word_items:
        w = word()
        w.name = wi.getAttribute('name')
        w.text = wi.getAttribute('text')
        w.s_time = float(wi.getAttribute('s_time'))
        w.e_time = float(wi.getAttribute('e_time'))
        w.speaker = wi.getAttribute('speaker')
        words.append(w)
        w_map[wi.getAttribute('name')] = w

    annotation_items = [n for n in annotations_node.childNodes if n.nodeName == 'annotation']
    for ai in annotation_items:
        a = simple_annotation()
        a.name = ai.getAttribute('name')
        a.number = int(ai.getAttribute('number'))
        #ast.literal_eval should be safer than eval()ing an untrusted string
        a.words = [w_map[x] for x in ast.literal_eval(ai.getAttribute('words'))]
        a.label = ai.getAttribute('label')
        annotations.append(a)


    return words, annotations, notes


def read_transcript(f, spk, starting_number=0):
    """Read a .trs transcript file created in Transcriber

    From a .trs file with words separated, only one episode, section, turn.
    only 1 speaker
    """
    words = set()
    doc = minidom.parse(f)
    trans = doc.childNodes[1]
    episode = [n for n in trans.childNodes if n.nodeName == 'Episode'][0]
    section = [n for n in episode.childNodes if n.nodeName == 'Section'][0]
    turn = [n for n in section.childNodes if n.nodeName == 'Turn'][0]
    
    words = []
    t = 0
    w = None
    for n in turn.childNodes:
        if n.nodeName == 'Sync':
            t = float(n.getAttribute('time'))
            if not w is None:
                w.e_time = t
                words.append(w)
                w = None
        else:
            text = n.wholeText.strip()
            if text == '':
                w = None
            else:
                w = word()
                w.name = 'word_'+str(len(words)+starting_number)
                w.text = text
                w.speaker = spk
                w.s_time = t

    #for multi-word words, split them by white space, divide the time slot
    w_new = []
    for w in words:
        sub_words = w.text.split(' ')
        for i in range(len(sub_words)):
            tmp = word()
            tmp.text = sub_words[i]
            tmp.s_time = w.s_time + 1.0*(i)/len(sub_words)*(w.e_time - w.s_time)
            tmp.e_time = w.s_time + 1.0*(i+1)/len(sub_words)*(w.e_time - w.s_time)
            tmp.speaker = w.speaker
            #words have to have unique name!
            tmp.name = w.name+'_'+str(i)
            w_new.append(tmp)
    words = w_new
    return words

def utterances(words, spk):
    utt_threshold = .5
    #utt_threshold = 1.0
    utts = []
    utt = None
    w_prev = None
    for w in words:
        if w_prev is None:
            utt = utterance()
            utt.speaker = spk
            utt.add_word(w)
        else:
            if w.s_time - w_prev.e_time <= utt_threshold:
                utt.add_word(w)
            else:
                utts.append(utt)
                utt = utterance()
                utt.speaker = spk
                utt.add_word(w)
        w_prev = w
    if len(words) > 0:
        utts.append(utt)

    return utts


def process_transcript_pair(f_driver='/home/cohend/E_DRIVE/DATA/processed_for_annotation/AudioOnly/CESAR_May-Fri-11-11-00-50-2012-audio-driver.trs', f_copilot='/home/cohend/E_DRIVE/DATA/processed_for_annotation/AudioOnly/CESAR_May-Fri-11-11-00-50-2012-audio-copilot.trs', filename = 'annotation.xml'):
    words = read_transcript(f_driver, 'driver')
    words = words + read_transcript(f_copilot, 'copilot', len(words))
    #utterances = set(read_transcript(f_driver, 'driver') + read_transcript(f_copilot, 'copilot'))
    #words = reduce(lambda x,y: x+y, [u.words for u in utterances])
    annotations = []
    notes = []
    write_annotation_file(words, annotations, notes, filename)

def process_ctm_trans(input_file, output_file):
    words = set()
    annotations = []
    notes = []
    
    f = open(input_file)
    i = 0
    for line in f:
        items = line.split('\t')
        w = word()
        w.name = 'word_'+str(i)
        w.s_time = float(items[0])
        w.e_time = float(items[1])
        w.speaker = items[2]
        w.text = items[3].strip()
        words.add(w)
        i += 1
    write_annotation_file(words, annotations, notes, output_file)

#process_ctm_trans("/home/cohend/v0.2/annotation/CESAR_Jun-Sun-3-13-01-47-2012/CESAR_Jun-Sun-3-13-01-47-2012-headset.txt", "/home/cohend/v0.2/annotation/CESAR_Jun-Sun-3-13-01-47-2012/domain_annotation.xml")

def list_object_names(kml_world_objects_file):
    """Collect a list of the names of every object in the kml file"""
    doc = minidom.parse(kml_world_objects_file)
    root = doc.documentElement
    dirs = [c for c in root.childNodes[1].childNodes if c.localName=='Folder']
    ans = []
    while len(dirs) > 0:
        d = dirs.pop(0)
        plc = [c for c in d.childNodes if c.localName=='Placemark']
        dirs.extend([c for c in d.childNodes if c.localName=='Folder'])
        for p in plc:
            ans.append([c.childNodes[0].nodeValue for c in p.childNodes if c.localName=='name'][0])
    return ans


def get_objects(kml_world_objects_file):
    """returns obj objects (see headers), which contain category information"""
    doc = minidom.parse(kml_world_objects_file)
    root = doc.documentElement
    dirname = [c.childNodes[0].nodeValue for c in root.childNodes[1].childNodes if c.localName=='name'][0]
    dirs = [[c, [dirname]] for c in root.childNodes[1].childNodes if c.localName=='Folder']
    ans = []
    while len(dirs) > 0:
        d = dirs.pop(0)
        dirnames = d[1]
        d = d[0]
        dirnames = dirnames + [c.childNodes[0].nodeValue for c in d.childNodes if c.localName=='name']
        plc = [c for c in d.childNodes if c.localName=='Placemark']
        dirs.extend([[c, dirnames] for c in d.childNodes if c.localName=='Folder'])
        for p in plc:
            ans.append(obj([c.childNodes[0].nodeValue for c in p.childNodes if c.localName=='name'][0], dirnames))
    return ans

def write_kml_as_js(kml_filename, js_filename):
    """Get the names, category, and polygon info for all the objects in the kml file."""
    f = open(js_filename, 'w')
    f.write('var places = new Object()\n\n')
    doc = minidom.parse(kml_filename)
    root = doc.documentElement
    dirname = [c.childNodes[0].nodeValue for c in root.childNodes[1].childNodes if c.localName=='name'][0]
    dirs = [[c, [dirname]] for c in root.childNodes[1].childNodes if c.localName=='Folder']
    ans = []
    while len(dirs) > 0:
        d = dirs.pop(0)
        dirnames = d[1]
        d = d[0]
        dirnames = dirnames + [c.childNodes[0].nodeValue for c in d.childNodes if c.localName=='name']
        plc = [c for c in d.childNodes if c.localName=='Placemark']
        dirs.extend([[c, dirnames] for c in d.childNodes if c.localName=='Folder'])
        for p in plc:
            name = [c.childNodes[0].nodeValue for c in p.childNodes if c.localName=='name'][0]
            poly = [c.childNodes for c in p.childNodes if c.localName=='Polygon'][0]
            outer_boundary = [c.childNodes for c in poly if c.localName=='outerBoundaryIs'][0]
            lin_ring = [c.childNodes for c in outer_boundary if c.localName=='LinearRing'][0]
            coords = [c for c in lin_ring if c.localName=='coordinates'][0]
            coords = coords.toxml().replace('<coordinates>','').replace('</coordinates>','').strip().replace(',0 ','\n').replace(',0','\n')


            new_coords = []
            for line in coords.split('\n'):
                tmp = line.split(',')
                if len(tmp) == 1:
                    break
                (lat, lon) = (float(tmp[0]), float(tmp[1]))
                new_coords.append('['+str(lat)+','+str(lon)+']')


            f.write('places["'+name+'"] = ['+','.join(new_coords)+']\n')




if __name__ == '__main__':
    write_kml_as_js('My Places.kml', 'My Places.js')

