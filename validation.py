import sys
import os.path
import xml.dom.minidom
import csv

def main():
    num_args = len(sys.argv)

    # Make sure the right number of input files are specified
    if  num_args < 3 or num_args > 4:
        print 'Expected input format: python classify.py <csvFile> <XMLFile>'
        return
    # If they are read them in
    else: 
        if num_args == 4:
            restrictions = open(sys.argv[3], 'r')
            print restrictions
        csv_reader = csv.reader(open(sys.argv[1], 'r'))
        n_fold = int(sys.argv[2])

        print "N Folds: ", n_fold
        for row in csv_reader:
            print row


        

if __name__ == '__main__':
    main()
