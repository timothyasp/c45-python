import sys
import os.path
import xml.dom.minidom
import csv
from data_types import CSVData, ClassificationData

class Classifier:
    def __init__(self, decision, csv_f):
        self.errors = 0
        self.successes = 0
        self.total = 0
        self.has_category = False

        self.decision_file = open(decision, "r")
        self.csv_reader = csv.reader(open(csv_f, 'r'))


    def classify(self, node, data, attributes):
        for child in node.childNodes:
            if child.localName == "edge":
                parent_var = child.parentNode.getAttribute('var')
                curr_edge = child.getAttribute('num')
                col_index = attributes.index(parent_var)
                if str(curr_edge) == str(data[col_index]):
                    self.classify(child, data, attributes)
            elif child.localName == "decision":
                if self.has_category:
                    if child.getAttribute('end') == data[11]:
                        self.successes += 1
                        print "Success: Expected ", child.getAttribute('end'), " Got ", data[11]
                    else:
                        self.errors += 1
                        print "Error: Expected ", child.getAttribute('end'), " Got ", data[11]
                else:
                    print child.getAttribute('end')
            elif child.localName == "node" or child.localName == "Tree":
                self.classify(child, data, attributes)
                
    def print_stats(self):

        print "Total processed: ", str(self.total)
        print "Errors: "         , str(self.errors)
        print "Successes: "      , str(self.successes)
        print "Accuracy: "       , str(float(self.successes / self.total))
        print "Error Rate: "     , str(1 - float(self.successes / self.total))


def main():
    num_args = len(sys.argv)

    # Make sure the right number of input files are specified
    if  num_args < 2 or num_args > 3:
        print 'Expected input format: python classify.py <csvFile> <XMLFile>'
        return
    # If they are read them in
    else: 
        classifier = Classifier(sys.argv[2], sys.argv[1])

        data = []
        for i, row in enumerate(classifier.csv_reader):
            if i >= 3:
                data.append(row)
            else:
                if i == 0:
                    attributes = row
                elif i == 1:
                    column_size = row
                elif i == 2:
                    category = row
                    if len(category) == 1:
                        classifier.has_category = True

        print "Data: ", data
        print "Attributes: ", attributes
        print "Column Size: ", column_size
        print "Category", category
        tree = xml.dom.minidom.parse(classifier.decision_file)
        root = tree.documentElement
        for row in data:
            classifier.total += 1
            result = classifier.classify(root, row, attributes)

        classifier.print_stats()

if __name__ == '__main__':
    main()
