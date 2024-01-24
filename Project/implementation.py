import pulp
from create_graph import create_graph
from setup import *
from os import chdir
import time
#import sys

if __name__ == "__main__":
    start_time = time.time()
    param_list = [60, "test.txt"]
    tmlim = param_list[0]
    file_path = param_list[1]

    G, F, T0, TM, ids, a, d, gates =read(file_path)
    A = [T0]+a+[TM]
    D = [T0]+d+[TM]
    GATES = [[i for i in range(G)]]+gates+[[i for i in range(G)]]
    graph = create_graph(F, A, D)
        
    prob = pulp.LpProblem("GAP", pulp.LpMinimize)

    # We define the set of indices for which we can have a non-zero variable xij (the ij corresponding to an arc of the graph) :
    indicesijk = [(i,j, k) for i in range(len(graph)) for j in range (len(graph)) for k in range(G) if i!=j and graph[i][j] != -1 and k in GATES[i] and k in GATES[j]]
    # print ("arcs of the graph : {}".format(indicesijk))

    # We define the binary decision variable x
    x = pulp.LpVariable.dicts("x", indicesijk, cat="Binary")

    # Objective function
    prob += pulp.lpSum(graph[i][j]*x[i,j, k] for (i ,j, k) in indicesijk), "sum of the cost of the selected arcs"
        
    # Constraints 
    # start from the edge with indice 0
    for k in range(G):
        prob+= pulp.lpSum(x[0, j, k] for j in range(1,len(graph)) if (0 ,j, k) in indicesijk)==1,'Start from edge 0 from gate {}'.format(k)

    # end at the edge with indice N+1 (the last edge)
    for k in range(G):
        prob+= pulp.lpSum(x[i,len(graph)-1, k] for i in range(len(graph)-1) if (i, len(graph)-1, k) in indicesijk)==1,'End at the last edge of gate {}'.format(k)
        
    # Flow conservation at each edge
    for k in range(G):
        for s in range (1, len(graph)-1):
            prob+= pulp.lpSum(x[i,s, k] for i in range(len(graph))  if (i, s, k) in indicesijk) - pulp.lpSum(x[s,j, k] for j in range(len(graph)) if (s, j, k) in indicesijk) ==0,'flow_{} of gate {}'.format(s, k)

    # Constraint assuring that one aircraft has one gate and only one 
    for j in range(1, len(graph)-1):
        prob+= pulp.lpSum(x[i, j, k] for i in range(0,len(graph)-2) for k in range(G) if (i ,j, k) in indicesijk)==1,'Making sure that the flight {} has exactly one gate'.format(j)
        
    # Writing of the model in a file
    prob.writeLP("modele_GAP.lp")
        
    ####
    # Solving of the model with GUROBI
    ####

    prob.solve(pulp.GUROBI_CMD(msg=1, timeLimit=tmlim))
        
    ####
    # Recovering the model solution
    ####

    # Solution display and recovery in verification format
    solution_list=[]
    for k in range(G):
        gate_k_list = []
        next_flight= int(sum(j*x[0,j, k].varValue for j in range (len(graph)) if (0,j, k) in indicesijk))
        iter=0
        while next_flight != len(graph)-1 and iter<=len(graph):
            gate_k_list.append(ids[next_flight-1])
            next_flight= int(sum(j*x[next_flight,j, k].varValue for j in range (len(graph)) if (next_flight,j, k) in indicesijk))
            iter+=1
        if next_flight != F+1:
            gate_k_list.append(ids[next_flight-1])
        solution_list.append(gate_k_list)
    print (solution_list)

    solution_cost = pulp.value(prob.objective)
    print ("Cost of the shortest path = ", solution_cost)

    # Write instance solution to file
    chdir('solutions')
    output = "solution_{}_{}.txt".format(G, F)
    with open(output, "w") as out:
        out.write (("{} {}\n".format(G,F)))
        out.write(("{}".format(solution_cost)))
        for l in solution_list:
            text= "\n"
            for i in l:
                text+= ("{} ".format(i))
            out.write((text))
    
    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time} seconds")
