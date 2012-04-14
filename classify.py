import sys
import os.path
import xml.dom.minidom
import csv
from data_types import CSVData, ClassificationData

class Classifier:
    def __init__(self):
        self.errors = 0
        self.successes = 0
        self.total = 0
        self.has_category = False
        
        self.classifications = {}
 
        self.true_pos = 0 
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0


    def classify(self, node, data, attributes):
        for child in node.childNodes:
            if child.localName == "edge":
                parent_var = child.parentNode.getAttribute('var')
                curr_edge = child.getAttribute('num')
                col_index = attributes.index(parent_var)
                if str(curr_edge) == str(data[col_index]):
                    self.classify(child, data, attributes)
            elif child.localName == "decision":
                self.classifications[data[0]] = child.getAttribute('end') 
                if self.has_category:
                    if int(child.getAttribute('end')) == int(data[11]):
                        if data[11] == 1:
                            self.true_pos += 1
                        if data[11] == 2:    
                            self.true_neg += 1
                        self.successes += 1
                        print "Success: Expected ", child.getAttribute('end'), " Got ", data[11]
                    else:
                        if int(data[11]) == 1:
                            self.false_pos += 1
                        if int(data[11]) == 2:
                            self.false_neg += 1
                        self.errors += 1
             
                        print "Error: Expected ", child.getAttribute('end'), " Got ", data[11]
                else:
                    print child.getAttribute('end')  +  str(data[11])
            elif child.localName == "node" or child.localName == "Tree":
                self.classify(child, data, attributes)
                
    def print_stats(self):

        print "Total processed: ", str(self.total)
        print "Errors: "         , str(self.errors)
        print "Successes: "      , str(self.successes)
        print "Accuracy: "       , str(float(self.successes / self.total))
        print "Error Rate: "     , str(1 - float(self.successes / self.total))
        print "TP" + str(self.true_pos)
        print "TN" + str(self.true_neg)
        print "FP" + str(self.false_pos)
        print "FN" + str(self.false_neg)
    def get_eval_stats():
        return (self.true_pos, self.true_neg, self.false_pos, self.false_neg)

def main():
    num_args = len(sys.argv)

    # Make sure the right number of input files are specified
    if  num_args < 2 or num_args > 3:
        print 'Expected input format: python classify.py <csvFile> <XMLFile>'
        return
    # If they are read them in
    else:
 
        decision_file = open(sys.argv[2], "r")

        csv_reader = ClassificationData(sys.argv[1])#csv.reader(open(sys.argv[1], 'r'))
        csv_reader.parse_tuples()

        classifier = Classifier()

        if len(csv_reader.category) > 0:
            classifier.has_category = True

        tree = xml.dom.minidom.parse(decision_file)
        root = tree.documentElement
        for row in csv_reader.tuples:
            classifier.total += 1
            result = classifier.classify(root, row, csv_reader.attributes)

        classifier.print_stats()

if __name__ == '__main__':
    main()
