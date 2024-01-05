#import pulp
#from create_graph import create_graph
from setup import *
#from os import chdir
#import sys
from implementation import *

if __name__ == "__main__":
    
    
    # Verification for the GAP18_80
    G, F, T0, TM, ids, a, d, gates =read("GAP4_12.txt")
    instance_verif = Instance(G, F, T0, TM, ids, a, d, gates)
    
    solution_list = [['KL023', 'LH089', 'IB8776'], ['KL055', 'FR2105', 'KL6120'], ['CX403', 'LH218', 'LX1024'], ['LH479', 'ZI734', 'EZY4025']]
    instance_verif.solution = solution_list
    
    #print(instance_verif)
    
    print(instance_verif.check_sol())
    