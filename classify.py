import sys
import os.path
import xml.dom.minidom
import csv
from data_types import CSVData, ClassificationData

errors = 0
successes = 0
total = 0

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

        print "Data: ", data
        print "Attributes: ", attributes
        print "Column Size: ", column_size
        print "Category", category
        tree = xml.dom.minidom.parse(decision_file)
        for row in data:
            print "Data: ", row
            result = iterate(tree, row, attributes)
            global total
            total += 1
            print "\n"

        print_stats()

def iterate(node, data, attributes):
    end = {"2": "McCain",  "1": "Obama"}
    # decision
    for child in node.childNodes:
        if child.localName == "edge":
            parent_var = child.parentNode.getAttribute('var')
            curr_edge = child.getAttribute('var')
            col_index = attributes.index(parent_var)

            if curr_edge == data[col_index]:
                iterate(child, data, attributes)
        elif child.localName == "decision":
            if end[child.getAttribute('end')] == data[11]:
                global successes
                successes += 1
                print "Success: Expected ", end[child.getAttribute('end')], " Got ", data[11]
            else:
                global errors
                errors += 1
                print "Error: Expected ", end[child.getAttribute('end')], " Got ", data[11]
        elif child.localName == "node" or child.localName == "Tree":
            iterate(child, data, attributes)
    """elif str(node.localName) == str("edge"):
        print "edge"
    elif str(node.localName) == str("node"):
        print "node" """

def print_stats():
    global total, successes, errors

    print "Total processed: ", str(total)
    print "Errors: "         , str(errors)
    print "Successes: "      , str(successes)
    print "Accuracy: "       , str(float(successes / total))
    print "Error Rate: "     , str(1 - float(successes / total))

if __name__ == '__main__':
    main()
