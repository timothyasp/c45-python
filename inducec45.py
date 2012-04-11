import sys
import os.path
import xml.dom.minidom
import csv
from collections import Counter
from database import ElectionDatabase
from data_types import CSVData, ClassificationData

class Trainer:
    def __init__(self, domain, class_data, db):
        self.load_domain(domain)
        self.db = db

        self.converter = {'Id':'id', 'Political Party':'party', 'Ideology':'ideology', 
                          'Race':'race', 'Gender':'gender', 'Religion':'religion', 
                          'Family Income':'income', 'Education':'education', 'Age':'age',
                          'Region':'region', 'Bush Approval':'bush_approval', 'Vote':'vote'}

        #by the time we are at this point we have the following things available. 
        #1) class_data a ClassificationData object containing the headers of the csvdata file stored
        #2) a database of the tuples 
             #--for some reason I was having a hard time getting it to work with the numbers insert we should check that out
        self.class_data  = class_data
        self.attributes  = class_data.names
        self.category    = class_data.category[0]
        self.column_size = class_data.domain_size
        self.data        = self.db.load_data()

        print self.attributes
        print self.column_size
        print self.category[0]
        print self.data
        #db.data_slice(attribute, data_range)
        #db.is_homogeneous(class_data.category)

    def load_domain(self, domain):
        # Load the domain into a parseable document object
        self.dom = xml.dom.minidom.parse(domain).documentElement

        # values can be accesses by : self.category['values'] or if you want the
        # first element, it'd be self.category['values'][0]
        self.category = {'name': self.dom.getElementsByTagName('Category')[0].getAttribute('name'), 'values': self.get_choice()}
        self.cols = self.get_columns()
        self.attributes = self.cols.keys()

    def get_columns(self):
        cols = {}

        for node in self.dom.getElementsByTagName('variable'):
            col_name = node.getAttribute('name')
            cols[col_name] = self.get_group(node)

        return cols

    def get_group(self, node):
        vals = []

        for el in node.getElementsByTagName('group'):
            name = el.getAttribute('name')
            p    = el.getAttribute('p')
            vals.append({'name': name, 'p': float(p)})

        return vals

    def get_choice(self):
        vals = []

        for c in self.dom.getElementsByTagName('choice'):
           c_name = c.getAttribute('name') 
           c_type = c.getAttribute('type') 
           vals.append((c_name, c_type))

        return vals

    def find_most_frequent_label(self, D):
        return Counter(D).most_common(1)
    
    # D : Dataset
    # A : Attributes
    # T : Tree we're building
    def c45(self, D, A, doc, threshold):
        print "Attributes: ", A
        if self.db.is_homogenous(D):
            node = doc.createElementNS(None, 'node')
            node.setAttribute('var', D[0])
        # No more attributes to consider
        elif len(A) == 0:
            most_freq_label = self.find_most_frequent_label(D)
            node = doc.createElementNS(None, 'node')
            print "Most Freq label: ", most_freq_label
            node.setAttribute('var', most_freq_label)
        else:
            # Step 2: select splitting attribute
            Ag = A[1]#select_splitting_attr(A, D, threshold)

            # no attribute is good for a split
            if (Ag == None):
                most_freq_label = sorted(self.find_most_frequent_label(D))[0]
                print "NONE Most Freq label: ", most_freq_label
                node = doc.createElementNS(None, 'node')
                node.setAttribute('var', most_freq_label)
                doc.appendChild(node)

        # Step 3: Tree Construction
            else:
                node = doc.createElementNS(None, 'node')

                print "Step 3"
                for attr in A:
                    Dv = self.data_slice(Ag)
                    if len(Dv) != 0:
                        self.c45(Dv, A.remove(Ag), doc, threshold)
                        edge = node.createElementNS(None, 'edge')
                        edge.setAttribute('var', Ag)
                        node.appendChild(edge)
                        doc.appendChild(node)

                        print Ag

    def data_slice(self, attr):
        key = self.attributes.index(attr)
        lists = {}
        for i in range(int(self.column_size[key])):
            val = i+1
            lists[val] = self.db.slice_by(self.converter[attr], val)
            #print "Slice " + str(val) + ": " + str(self.db.slice_by(self.converter[attr], val))

        return lists

    #return -1 when no attribute selected!!
    def select_splitting_attr(A, D, threshold):
        p0 = enthropyD(D)
        p = {}
        gain = {}
        for v in A: 
            p[Ai] = enthropyAi(D);
            gain[Ai] = p0 - p[Ai]; 
        best = max(gain)
        if best > threshold: 
            return gain.index(best)
        else:
             return -1;

    def entropyD(D):
        for i in range(len(D)):
            return
            
    #def entropyAi(D):

def main():
    num_args = len(sys.argv)
    domain = training = restriction = ''

    # Make sure the right number of input files are specified
    if  num_args <= 2 or num_args > 4:
        print 'Expected input format: python inducec45.py <domainFile.xml> <TrainingSetFile.csv> [<restrictionsFile>]'
        return
    # If they are read them in
    else: 
        if check_file(sys.argv[1]) == -1 or check_file(sys.argv[2]) == -1:
            return -1
    
        domain = open(sys.argv[1], "r")
 
        #connect to our elections db, stored on my mediatemple  
        db = ElectionDatabase()
        db.connect()
 
        db.clean_up_nums()       
 
        #parse the rows directly to the db
        class_data = ClassificationData(sys.argv[2]);
        class_data.parse_tuples_to_db(db);

        if num_args == 4:
            restriction = open(check_file(sys.argv[3]), "r") 
    
    d = Trainer(domain, class_data, db)

    print d.data

    doc = xml.dom.minidom.parseString("<Tree></Tree>")
    print doc.toxml()
    d.c45(d.data, d.attributes, doc, 0)

def check_file(filename):
    if not os.path.exists(filename) or not os.path.isfile(filename): 
        print 'Error can not find the specified file: ', filename
        return -1
    else:
        return filename


# def find_most_frequent_label(D):

# def create_label():

# def enthropy(D):

# D : Training Dataset
# A : List of Attributes
# T : Constructed Decision tree

#def parse_domain():

if __name__ == '__main__':
    main()
