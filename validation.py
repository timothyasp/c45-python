import sys
import os.path
import xml.dom.minidom
import csv
from data_types import ClassificationData
from inducec45 import Trainer
from classify import Classifier
def main():
    num_args = len(sys.argv)

    # Make sure the right number of input files are specified
    if  num_args < 3 or num_args > 4:
        print 'Expected input format: python classify.py <csvFile> <XMLFile>'
        return
    # If they are read them in
    else:
        if num_args == 4:
            restrictions = ClassificationData(sys.argv[3])
            restrictions.parse_restr_tuples();
 
        class_data = ClassificationData(sys.argv[1])
        class_data.parse_tuples()

        validator = Validator([])
        validator.train(sys.argv[2], class_data)
        #for row in class_data.tuples:
        #    print row

class Validator:
    def __init__(self, restrictions):
        self.attributes = [];
        self.true_pos = 0
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0
        
        if len(restrictions) > 0:
            self.restr = restrictions.restr
        else: 
            self.restr = restrictions

    def train(self, domain, class_data):
        document = xml.dom.minidom.Document()
        node = document.createElement('Tree')
        document.appendChild(node)
        d = Trainer(domain, class_data, document)
        partial_atts = d.attributes
        partial_atts.remove("Id")
        partial_atts.remove("Vote")
        print partial_atts
      
        if len(self.restr) > 0:
            d.rem_restrictions(self.restr)

        d.c45(d.data, d.attributes, node, 0)

        classifier = Classifier()

        if len(class_data.category) > 0:
            classifier.has_category = True

        for row in d.data:
            classifier.classify(document.documentElement, row, class_data.attributes)
            
        classifier.print_stats()

    #def print_stats(self):

    #def fmeasure(self):

    #def recall(self):

    #def precision(self):

    #def pf(self):

    #def confusion_matrix(self):

    #def accuracy(self):

if __name__ == '__main__':
    main()
