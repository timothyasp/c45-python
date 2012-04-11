import sys
import os.path
import xml.dom.minidom
import csv
import math 

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
        self.data        = class_data.tuples 

        print self.attributes
        print self.column_size
        print self.category[0]
        #print self.data
        
        print "entropy d =: "
        print self.pr(self.data)
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

    def entropy(self, D):
        index = self.attributes.index(self.category)
        obama_ct = 0
        mccain_ct = 0
 
        for e in D:
            if e[index] == 1:
                obama_ct += 1
            elif e[index] == 2:
                mccain_ct += 1

        obama_ct = obama_ct / float(len(D))
        mccain_ct = mccain_ct / float(len(D))
 
        entropy = -obama_ct * math.log(obama_ct, 2) - mccain_ct * math.log(mccain_ct, 2)
        return entropy  

    def entropyAi(D, Ai):
       id_list = []
       slices = self.db.slice_by(D, Ai, id_list)
       entropies = []
       total_entropy = 0;

       for i, mslice in slices:
           entropies[i] = entropy(mslice)
       
       for i, entropy in entropies:
           total_entropy += len(slices[i])/len(D) * entropies[i]     

       return total_entropy
 
    # D : Dataset
    # A : Attributes
    # T : Tree we're building
    def c45(self, D, A, T, threshold):
        if self.db.is_homogenous(D):
            print "Is Homogenous"
            print D.keys()

        # No more attributes to consider
        elif len(A) == 0:
            print "None Left"

        else:
            # Step 2: select splitting attribute
            Ag = A[1]#select_splitting_attr(A, D, threshold)

            # no attribute is good for a split
            if (Ag == None):
                print "No attr good for split: "
                print D.keys()

        # Step 3: Tree Construction
            else:
                print "Step 3"
                index_list = []
                for var in A:
                    Dv = self.db.slice_by(Ag, var, index_list)
                    print Dv
                    if len(Dv) == 0:
                        self.c45(Dv, A.remove(Ag), T, threshold)
                        print Ag

    #return -1 when no attribute selected!!
    def select_splitting_attr(A, D, threshold):
        p0 = enthropy(D)
        p = {}
        gain = {}
        for attr in A: 
            p[attr] = enthropyAi(D, attr);
            gain[attr] = p0 - p[attr]; 
        best = max(gain)
        if best > threshold: 
            return gain.index(best)
        else:
             return -1;

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


    #d.c45(d.data, d.attributes, xml.dom.minidom.getDOMImplementation(), 0)

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
