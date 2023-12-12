#import pulp
#from create_graph import create_graph
from setup import *
#from os import chdir
#import sys
from implementation import *

if __name__ == "__main__":
    
    """
    # Verification for the GAP18_80
    G, F, T0, TM, ids, a, d, gates =read("GAP18_80.txt")
    instance_verif = Instance(G, F, T0, TM, ids, a, d, gates)
    
    solution_list = [['EZY18DT', 'ASL16W', 'BRU865', 'EZY82AR', 'EZY79DY', 'AUI129'], ['CSA3DZ', 'AUI3FU', 'EZY57NG', 'AFR17DP'], [], ['AFR12ZK', 'CSA2DZ', 'EZY68NG', 'ASL98F', 'EZY3798'], ['LZB431', 'EZY27YN', 'BTI3CE', 'CSA4CZ', 'EZY329C'], ['EZY81LX', 'AEA1011', 'EZY23YB', 'EZY14EZ', 'EZY657Y', 'EZY68HP'], ['AFR93XX', 'EZY696H', 'EZY48UH', 'EZY14ML', 'EZY36QF'], ['AUI130', 'AFR14CJ', 'EZY49QU', 'EZY64RH', 'EZY42NK', 'EZY81YK', 'EZY57QB'], ['EZY9004', 'AFR52EU', 'EZY7043', 'EZY56LP', 'CTN476'], [], ['EZY929H', 'AHY073', 'FIN6M', 'FIN2AP', 'EZY3672'], ['AFR132F', 'EZY35HL', 'AUA415C', 'AFR126N', 'EZY241B'], ['EZY43VJ', 'AUA411C', 'AUA413', 'EZY64UH', 'AFR15FX'], [], ['EZY41KM', 'FIN8PY', 'EZY86WT', 'EZY69KT', 'EZY13XV', 'EZY28KJ'], ['EZY31UP', 'AMC478', 'EZY59FD', 'EZY716N', 'AFR18PP'], ['EZY37FM', 'FIN4LF', 'EZY18NT', 'EZY92UE', 'AUA417C', 'EZY15NM'], ['EZY39CX', 'EZY48EP', 'CTN25F', 'EZY2439', 'EZY23PK']]
    instance_verif.solution = solution_list
    
    #print(instance_verif)
    
    print(instance_verif.check_sol())
    """