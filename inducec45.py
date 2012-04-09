import sys
import os.path
import xml.dom.minidom
import csv

def main():
    num_args = len(sys.argv)
    domain = training = restriction = ''

    # Make sure the right number of input files are specified
    if  num_args <= 2 or num_args > 4:
        print 'Expected input format: python inducec45.py <domainFile.xml> <TrainingSetFile.csv> [<restrictionsFile>]'
        return
    # If they are read them in
    else: 
        domain = open(check_file(sys.argv[1]), "r")
        training = open(check_file(sys.argv[2]), "r")
        if num_args == 4:
            restriction = open(check_file(sys.argv[3]), "r") 
    
    t_reader = csv.reader(training)
    d_reader = xml.dom.minidom.parse(domain)
    
def check_file(filename):
    if not os.path.exists(filename) or not os.path.isfile(filename): 
        print 'Error can not find the specified file: ', filename
        return
    else:
        return filename

# D : Training Dataset
# A : List of Attributes
# T : Constructed Decision tree

#def c45(D, A, T, threshold):
# Step 1: check termination conditions
# D contains records with the same class label c
# if for all d is in D: class(d) = ci then
#if :
#     create leaf node r;
#     label(r) := ci;
#     T := r;
# No more attributes to consider
# else if A = NONE LEFT then
#elif :
#     c := find most frequent label(D);
#     create leaf node r;
#     label(r) := c;
# else 
#else:
# Step 2: select splitting attribute
#     Ag := selectSplittingAttribute(A,D, threshold);
#    Ag = select_splitting_attr(A, D, threshold)
#     if Ag = NULL then //no attribute is good for a split
#    if (Ag == NULL):
#         create leaf node r;
#         label(r) := find most frequent label(D);
#         T := r;
#    else:
#     else // Step 3: Tree Construction
#         create tree node r;
#         label(r) := Ag;
#         foreach v is in dom(Ag) do
#             Dv := {t belongs in D|t[Ag] = v};
#             if Dv =6 NONE LEFT then
#                 C45(Dv, A - {Ag}, Tv); //recursive call
#                 append Tv to r with an edge labeled v;
#             endif
#         endfor
#     endif
# endif

#uses information gain
# D : Training Dataset
# A : List of Attributes
#def select_splitting_attr(A, D, threshold):
# p0 := enthropy(D);
# for each Ai in A do
#     p[Ai] := enthropyAi (D);
#     Gain[Ai] = p0 - p[Ai]; //compute info gain
# endfor
# best := arg(findMax(Gain[]));
# if Gain[best] >threshold then return best
# else return NULL;

#uses information gain ratio
# D : Training Dataset
# A : List of Attributes
#def select_splitting_attr_ratio(A, D, threshold);
# p0 := enthropy(D);
# for each Ai in A do
#     p[Ai] := enthropyAi (D);
#     Gain[Ai] := p0 - p[Ai]; //compute info gain
#     gainRatio[Ai] := Gain[Ai]/enthropy(Ai); //compute info gain ratio
# endfor
# best := arg(findMax(gainRatio[]));
# if Gain[best] >threshold then return best
# else return NULL;

#def parse_domain():
    

if __name__ == '__main__':
    main()
