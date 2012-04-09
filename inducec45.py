import sys
import os.path
import xml.dom.minidom
import csv

def main():


# D : Training Dataset
# A : List of Attributes
# T : Constructed Decision tree

def c45(D, A, T, threshold):
# Step 1: check termination conditions
# if for all d ∈ D: class(d) = ci then
#     create leaf node r;
#     label(r) := ci;
#     T := r;
# else if A = ∅ then
#     c := ﬁnd most frequent label(D);
#     create leaf node r;
#     label(r) := c;
# else 
# Step 2: select splitting attribute
#     Ag := selectSplittingAttribute(A,D, threshold);
#     if Ag = NULL then //no attribute is good for a split
#         create leaf node r;
#         label(r) := ﬁnd most frequent label(D);
#         T := r;
#     else // Step 3: Tree Construction
#         create tree node r;
#         label(r) := Ag;
#         foreach v ∈ dom(Ag) do
#             Dv := {t ∈ D|t[Ag] = v};
#             if Dv =6 ∅ then
#                 C45(Dv, A − {Ag}, Tv); //recursive call
#                 append Tv to r with an edge labeled v;
#             endif
#         endfor
#     endif
# endif

#uses information gain
# D : Training Dataset
# A : List of Attributes
def select_splitting_attr(A, D, threshold):
# p0 := enthropy(D);
# for each Ai ∈ A do
#     p[Ai] := enthropyAi (D);
#     Gain[Ai] = p0 − p[Ai]; //compute info gain
# endfor
# best := arg(findMax(Gain[]));
# if Gain[best] >threshold then return best
# else return NULL;

#uses information gain ratio
# D : Training Dataset
# A : List of Attributes
def select_splitting_attr_ratio(A, D, threshold);
# p0 := enthropy(D);
# for each Ai ∈ A do
#     p[Ai] := enthropyAi (D);
#     Gain[Ai] := p0 − p[Ai]; //compute info gain
#     gainRatio[Ai] := Gain[Ai]/enthropy(Ai); //compute info gain ratio
# endfor
# best := arg(findMax(gainRatio[]));
# if Gain[best] >threshold then return best
# else return NULL;

def parse_domain():
    

if __name__ == '__main__':
    main()
