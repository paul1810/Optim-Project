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

#classes flights and gates

class Flight:
    def __init__(self,fNum,arrT,depT,wingS):
        self.fNum=fNum
        self.arrT=arrT
        self.depT=depT
        self.wingS=wingS
    
    def __repr__(self):
        text = "{0.fNum} - {0.arrT} - {0.depT} - {0.wingS}\n".format(self)
        return text

class Gate:
    def __init__(self,gNum,opT,cloT,caT):
        self.gNum=gNum
        self.opT=opT
        self.cloT=cloT
        self.caT=caT
    
    def __repr__(self):
        text= "{0.ICAO} - {0.RunwayL}\n".format(self)
        return text

aircraft=[]
for info in dataaircraft:
    aircraft.append(Aircraft(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9]))

airports=[]
uselesscount=0
for info in dataairport:
        uselesscount+=1
        if uselesscount%2==0:
            airports.append(Airport(info[1],info[4]))

airportlist=[airports[i].ICAO for i in range(len(airports))]

# n = number of flights
n = len(flights_matrix[:, 1])
# m = number of gates
m = len(gates_matrix[:, 1])


gates_category = gates_matrix[:, 3]

flights_arrival_time = flights_matrix[:, 1]
flights_departing_time = flights_matrix[:, 2]
flights_wingspan = flights_matrix[:, 3]
flights_category = np.zeros(len(flights_wingspan))


for i in range (n):
    if flights_wingspan[i] < 30:
        flights_category[i] = 1
    elif flights_wingspan[i] < 45 and flights_wingspan[i] >= 30 :
        flights_category[i] = 2
    elif flights_wingspan[i] < 70 and flights_wingspan[i] >= 45 :
        flights_category[i] = 3
    else :
        flights_category[i] = 4
    
        
print(flights_arrival_time,flights_departing_time, flights_wingspan, flights_category)


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
        if flights_category[i] > gates_category[k]:
            model.addConstrs((x[i, j, k] == 0 for j in range(n+1)))


for i in range(n):
    for j in range(n):
        if flights_arrival_time[j] < flights_departing_time[i]:
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