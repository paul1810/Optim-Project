import pandas as pd
import numpy as np
import gurobipy as gp
from gurobipy import GRB

"""
The time is computed in integer way with 12:00 being 1200 and 14:45 being 1475
"""


# Compute the flights matrix
df = pd.read_excel('flights_1.xlsx')

flights_matrix = df.values

print(flights_matrix)


# Compute the gates matrix
df = pd.read_excel('gates_1.xlsx')

gates_matrix = df.values

print(gates_matrix)


# Compute the costs matrix, columns = gates and rows = flights
df = pd.read_excel('costs_1.xlsx')

c = df.iloc[:, 1:].values

print(c)

# n = number of flights
n = len(flights_matrix[:, 1])
# m = number of gates
m = len(gates_matrix[:, 1])
print(n)

#classes flights and gates

class Gate:
    def __init__(self,gNum,opeT,cloT,catG):
        self.gNum=gNum
        self.opeT=opeT
        self.cloT=cloT
        self.catG=catG
    
    def __repr__(self):
        text= "{0.gNum} - {0.opeT} - {0.cloT} - {0.catG}\n".format(self)
        return text

gate=[]
for info in gates_matrix:
    gate.append(Gate(info[0],info[1],info[2],info[3]))

class Flight:
    def __init__(self,fNum,arrT,depT,catA,wigS):
        self.fNum=fNum
        self.arrT=arrT
        self.depT=depT
        self.catA=catA
        self.wigS=wigS
    
    def __repr__(self):
        text = "{0.fNum} - {0.arrT} - {0.depT} - {0.catA} - {0.wigS}\n".format(self)
        return text

flight=[]
for i in range(n):
    flight[i] = Flight(flights_matrix[0][i],flights_matrix[1][i],flights_matrix[2][i],0.0,flights_matrix[3][i])
    
    '''flight[i].fNum = flights_matrix[0][i]
    flight[i].arrT = flights_matrix[1][i]
    flight[i].depT = flights_matrix[2][i]
    flight[i].catA = 0.0
    flight[i].wigS = flights_matrix[3][i]'''

for i in range(n):
    if flight[i].wigS < 30:
        flight[i].catA = 1
    elif flight[i].wigS < 45 and flight[i].wigS >= 30:
        flight[i].catA = 2
    elif flight[i].wigS < 70 and flight[i].wigS >= 45:
        flight[i].catA = 3
    else:
        flight[i].catA = 4



model = gp.Model()

x = model.addVars(n+1, n+1,m, vtype=GRB.BINARY, name="x")


model.setObjective(gp.quicksum(x[i, j, k] * c[i][k] for i in range(1, n) for j in range(1, n+1) for k in range(m)) + gp.quicksum(x[0, j, k] * c[j][k] for j in range(0, n) for k in range(m)), GRB.MINIMIZE)


model.addConstrs((gp.quicksum(x[i, j, k] for i in range(0, n) for k in range(m)) == 1 for j in range(1, n+1)), name="C1")
model.addConstrs((gp.quicksum(x[0, j, k] for j in range(1, n+1)) == 1 for k in range(m)), name="C1*")
#model.addConstrs((gp.quicksum(x[i, n, k] for i in range(0, n)) == 1 for k in range(m)), name="C1**")
#model.addConstrs((gp.quicksum(x[i, j, k] for i in range(0, n)) == gp.quicksum(x[j, i, k] for i in range(1, n+1)) for j in range(n+1) for k in range(m)), name="C2")
model.addConstrs((gp.quicksum(x[0, j, k] for j in range(1, n+1)) == 1 for k in range(m) ), name="C1*")

for i in range(n):
    for k in range(m):
        if flight[i].catA > gate[k].catG:
            model.addConstrs((x[i, j, k] == 0 for j in range(n+1)))


for i in range(n):
    for j in range(n):
        if flight[j].arrT < flight[i].depT:
            model.addConstrs((x[i, j, k] == 0 for k in range(m)))
        


"""
model.addConstrs((w[i, j] <= q_not_ordered[i][j]*g[i]*g[j] for j in range(33) for i in range(33)), name="C1*")
model.addConstrs((x[i, j] + gp.quicksum(w[i, n] for n in range(33))*(1-g[j]) + gp.quicksum(w[n, j] for n in range(33))*(1-g[i]) <= LF*gp.quicksum(z[i, j, k]*s[k] for k in range(3)) for j in range(33) for i in range(33)), name="C2")
model.addConstrs((gp.quicksum(z[i, j, k] for j in range(33)) == gp.quicksum(z[j, i, k] for j in range(33)) for i in range(33) for k in range(3)), name="C3")
model.addConstrs((gp.quicksum((d[i][j]/V[k] + LTO[k]*(1.5-0.5*g[j]))*z[i, j, k] for i in range(33) for j in range(33)) <= 7*10*AC[k] for k in range(3)), name="C4")
model.addConstrs((z[i, j, k] <= 0 for i in range(33) for j in range(33) for k in range(3) if d[i][j] > R[k]), name="C5")
"""
model.setParam('TimeLimit', 60)

model.update()

model.optimize()  