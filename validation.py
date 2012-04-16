import sys
import os.path
import xml.dom.minidom
import csv
import math
import random
import itertools
from data_types import ClassificationData
from inducec45 import Trainer
from classify import Classifier
from copy import deepcopy

def main():
    num_args = len(sys.argv)

    # Make sure the right number of input files are specified
    if  num_args < 3 or num_args > 4:
        print 'Expected input format: python classify.py <csvFile> <XMLFile>'
        return
    # If they are read them in
    else:
        if num_args == 5:
            restrictions = ClassificationData(sys.argv[4])
            restrictions.parse_restr_tuples();
 
        class_data = ClassificationData(sys.argv[2])
        class_data.parse_tuples()

        num_folds = int(sys.argv[3])

        validator = Validator([])
        data_folds = validator.split_data_rand(num_folds, class_data)
        full_attributes = deepcopy(class_data.attributes)

        class_data.attributes.remove("Id")
        class_data.attributes.remove("Vote")
      
        for i in range(num_folds):
            holdout_set = data_folds[i]
            training_set = []
            for j in range(num_folds):
                if j != i:
                    for row in data_folds[j]:
                        training_set.append(row)
            root = validator.train(sys.argv[1], class_data)
            validator.classify(root, holdout_set, full_attributes)

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

    def split_data_rand(self, n, class_data):
        rand_groups = []
        rand_data = deepcopy(class_data.tuples)
        random.shuffle(rand_data)
        incr_val = math.ceil(len(rand_data) / float(n))
        print "INCR: " + str(incr_val)
 
        group_index = 0
        ctr = 0       
        for row in rand_data:
            if ctr == incr_val: 
                ctr = 0
                group_index += 1
            if ctr == 0:
                rand_groups.append([])
            rand_groups[group_index].append(row)
            ctr += 1
        return rand_groups

    def train(self, domain, class_data):
        document = xml.dom.minidom.Document()
        node = document.createElement('Tree')
        document.appendChild(node)
        
        d = Trainer(domain, class_data, document)
      
        if len(self.restr) > 0:
            d.rem_restrictions(self.restr)

        d.c45(d.data, d.attributes, node, 0)

        return document.documentElement

    def classify(self, root, data, attributes):
        classifier = Classifier()
        classifier.has_category = True 
        for row in data:
            classifier.classify(root, row, attributes)
      
        print classifier.get_eval_stats()

        

if __name__ == '__main__':
    main()
