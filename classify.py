import sys
import os.path
import xml.dom.minidom
import csv

def main():
    num_args = len(sys.argv)

    # Make sure the right number of input files are specified
    if  num_args < 2 or num_args > 3:
        print 'Expected input format: python classify.py <csvFile> <XMLFile>'
        return
    # If they are read them in
    else: 
        decision_file = open(sys.argv[2], "r")

        tree = xml.dom.minidom.parse(decision_file)
        iterate(tree)

def iterate(node):
    if node:
        if len(node.childNodes) == 0:
            return
        #elif str(node.firstChild.tagName) == str("decision"):
        #    print node.firstChild.data
        else:
            for child in node.childNodes:
                print child.toxml()
                iterate(child)
            
        

if __name__ == '__main__':
    main()
