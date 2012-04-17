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

    if  num_args < 3 or num_args > 5:
        print 'Expected input format: python validation.py <domain> <csvdata>'
        return

    else:
        m_restrs = []
        if num_args == 5:
            restrictions = ClassificationData(sys.argv[4])
            restrictions.parse_restr_tuples();
            m_restrs = restrictions.restr
             
        class_data = ClassificationData(sys.argv[2])
        class_data.parse_tuples()

        num_folds = int(sys.argv[3])

        validator = Validator(m_restrs)
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
        
        print "\n\nValidator stats:"
        validator.confusion_matrix()
        print "PF-Measure: " + str(validator.pf())
        print "Recall: " + str(validator.recall()) 
        print "Precision: " + str(validator.precision())
        print "F-Measure: " + str(validator.fmeasure())
        print "Error Rate: " + str(validator.error_rate())
        print "Overall Accuracy: " + str(validator.overall_accuracy()) 

class Validator:
    def __init__(self, restrictions):
        self.attributes = [];
        self.true_pos = 0
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0
        self.classifier = Classifier()
        self.classifier.has_category = True
        self.restr_flag = False
 
        if len(restrictions) > 0:
            self.restr = restrictions
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
      
        if len(self.restr) > 0 and self.restr_flag == False:
            print "REMOVING RESTRS"
            d.rem_restrictions(self.restr)
            self.restr_flag = True

        d.c45(d.data, d.attributes, node, .1)

        return document.documentElement

    def classify(self, root, data, attributes):
        for row in data:
            self.classifier.classify(root, row, attributes)
      
        print self.classifier.get_eval_stats()

    def recall(self):
        TP = self.classifier.true_pos
        FN = self.classifier.false_neg
        if TP + FN == 0:
            return ""
        else:
            return float(TP) / float(TP + FN)

    def precision(self):
        TP = self.classifier.true_pos
        FP = self.classifier.false_pos
        if TP + FP == 0:
            return ""
        else:
            return float(TP) / float(TP + FP)

    def pf(self):
        TN = self.classifier.true_neg
        FP = self.classifier.false_pos
        if FP + TN == 0:
            return ""
        else:
            return float(FP) / float(FP + TN)

    def fmeasure(self):
        beta = 2 
        if self.precision() == "" or self.recall() == "":
            return ""
        else:
            return float(beta * self.precision() * self.recall()) / (self.precision() + self.recall())

    def confusion_matrix(self):
        print "###### CONFUSION MATRIX #######"
        print "                | Classified Positive | Classified Negative |"
        print "Actual Positive |          " + str(self.classifier.true_pos) + "           |          " + str(self.classifier.false_neg) + "           |"
        print "Actual Negative |          " + str(self.classifier.false_pos) + "           |           " + str(self.classifier.true_neg) + "          |"

    def error_rate(self):
        FN = self.classifier.false_neg
        FP = self.classifier.false_pos
        return (FN+FP) / float(self.classifier.total)
    
    def avg_accuracy(self):
        return 0

    def overall_accuracy(self):
        TN = self.classifier.true_neg
        TP = self.classifier.true_pos
        return (TN + TP) / float(self.classifier.total)


if __name__ == '__main__':
    main()
