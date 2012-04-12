import sys
import os.path
import xml.dom.minidom
import csv
from data_types import CSVData, ClassificationData

errors = 0
successes = 0
total = 0
has_category = False

def main():
    num_args = len(sys.argv)

    # Make sure the right number of input files are specified
    if  num_args < 2 or num_args > 3:
        print 'Expected input format: python classify.py <csvFile> <XMLFile>'
        return
    # If they are read them in
    else: 
        decision_file = open(sys.argv[2], "r")
        csv_reader = csv.reader(open(sys.argv[1], 'r'))

        data = []
        for i, row in enumerate(csv_reader):
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
                        global has_category
                        has_category = True

        print "Data: ", data
        print "Attributes: ", attributes
        print "Column Size: ", column_size
        print "Category", category
        tree = xml.dom.minidom.parse(decision_file)
        root = tree.documentElement
        global total
        for row in data:
            total += 1
            result = classify(root, row, attributes)

        print_stats()

def classify(node, data, attributes):
    global has_category, successes, errors
    for child in node.childNodes:
        if child.localName == "edge":
            parent_var = child.parentNode.getAttribute('var')
            curr_edge = child.getAttribute('num')
            col_index = attributes.index(parent_var)
            if str(curr_edge) == str(data[col_index]):
                classify(child, data, attributes)
        elif child.localName == "decision":
            if has_category:
                if child.getAttribute('end') == data[11]:
                    successes += 1
                    print "Success: Expected ", child.getAttribute('end'), " Got ", data[11]
                else:
                    errors += 1
                    print "Error: Expected ", child.getAttribute('end'), " Got ", data[11]
            else:
                print child.getAttribute('end')
        elif child.localName == "node" or child.localName == "Tree":
            classify(child, data, attributes)
            
def print_stats():
    global total, successes, errors

    print "Total processed: ", str(total)
    print "Errors: "         , str(errors)
    print "Successes: "      , str(successes)
    print "Accuracy: "       , str(float(successes / total))
    print "Error Rate: "     , str(1 - float(successes / total))

if __name__ == '__main__':
    main()
