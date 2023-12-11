

#********** DATA LECTURE FUNCTION **********
def read(filename):
  ''' function for reading GAP instance files - returns file elements'''
  ids, a, d, gates  = [], [], [], []
  with open(filename, 'r') as f:
    for i, line in enumerate(f):
      w = line.strip().split()
      if len(w)==0:
          continue      
      if w[0] == 'Gates:':
        G = int(w[1])
        F = int(w[3])
        continue
      if w[0] == 'Opening':
        T0 = int(w[2])
        TM = int(w[5])
        continue
      ids.append(w[0])
      a.append(int(w[1]))
      d.append(int(w[2]))
      g=[]
      for j in range (3, len(w)):
          g.append(int(w[j]))
      gates.append(g)
    return G, F, T0, TM, ids, a, d, gates
#G = number of gates of this given problem
#F = number of flights of this given problem
#T0 = starting time of the problem
#TM = ending time of the problem
# ids = list of flights ids
# a = list of flights arrival dates
# d = list of flights departures dates
# gates = list of all the lists with the available gates for each flight


#********** SETUP FOR CLASSES AND METHODS **********
class Flight(object):
    ''' flight object '''
    def __init__(self, i, a, d, gates):
        self.id = i  # id of the flight (string)
        self.a = a   # arrival time (int)
        self.d = d   # departure time (int)
        self.gates = gates
        

    def __repr__(self):
        text = "{0.id} - {0.a} {0.d} -".format(self)
        text += " gates: {}\n".format(self.gates)
        return text

class Instance(object):
    ''' Object describing a GAP problem instance '''
    def __init__(self, G, F, T0, TM, ids, a, d, gates):
        self.nb_flights = F              # number of flights (int)
        self.nb_gates = G           # number of gates (int)
        self.ot =T0                 # opening time (int)
        self.ct =TM                # closing time (int)
        self.flights = []  # flight list
        for i in range (len(ids)):
            flight=Flight(ids[i], a[i], d[i], gates[i])
            self.flights.append(flight)
        self.solution =[] #the solution is an empty list or a list of ordered lists of flight IDs assigned to the various positions.
            
    def search_flight(self, Id):
        ''' returns the flight of the instance whose identifier is Id '''
        for item in self.flights:
            if item.id == Id:
                return item
        return None
    
    def __repr__(self):
        text = "Instance with {} flights and {} gates\n".format(self.nb_flights, self.nb_gates)
        text += "Time window : [{} , {}]\n".format(self.ot,self.ct)
        for i in range (len(self.flights)):
            text += repr(self.flights[i])
        if len(self.solution) !=0: #if the instance's solution is empty, it's not printed 
            text += "Feasible solution founded :\n"
            for i in range (len(self.solution)):
                text += "p{} : ".format(i)
                text += repr(self.solution[i])
                text += "\n"
        return text
        
    def check_sol(self):
        ''' Checks the consistency of the solution found for the instance and returns its robustness cost if calculable'''
        # Checking of the constraint's respect
        possible_cost=1
        sol_ok=1
        if len(self.solution) ==0:
            print ("Warning, the solution is empty")
            possible_cost=0
            sol_ok=0 
        if len(self.solution) != self.nb_gates:
            print ("Error on the number of gates")
            possible_cost=0
            sol_ok=0
        flights_list=[]
        for i in range (len(self.solution)):
            for j in range (len(self.solution[i])):
                flights_list.append(self.solution[i][j])
        for i in range (self.nb_flights):
            c = flights_list.count(self.flights[i].id)
            if c == 0:
                print ("flight {} has no gate".format(self.flights[i].id))
                sol_ok=0
            elif c>1 :
                print ("flight {} has {} gates".format(self.flights[i].id,c))
                sol_ok=0
        for i in range (len(self.solution)):
            for j in self.solution[i]:
                if self.search_flight(j)==None:
                    print ("{} isn't a flight of this instance".format(j))
                    possible_cost = 0
                    sol_ok=0
        if possible_cost:        
            for i in range (len(self.solution)):
                if len(self.solution[i]) > 1:    
                    for j in range (len(self.solution[i])-1):
                        first_one = self.solution[i][j]
                        next_one = self.solution[i][j+1]
                        if self.search_flight(first_one).d > self.search_flight(next_one).a :
                            print("flight {} (departing {}) and {} (arriving {}) can't be one after the other on the same gate".format(first_one,self.search_flight(first_one).d , next_one,self.search_flight(next_one).a))
                            sol_ok=0
 
        # Computation of the solution cost
            cost = 0
            for i in range (len(self.solution)):
                if len(self.solution[i]) == 0:
                    cost += (self.ct-self.ot)**2
                else:    
                    cost+= (self.search_flight(self.solution[i][0]).a -self.ot)**2
                    next_one = self.solution[i][0]
                    for j in range (len(self.solution[i])-1):
                        first_one = self.solution[i][j]
                        next_one = self.solution[i][j+1]
                        cost += (self.search_flight(next_one).a - self.search_flight(first_one).d)**2
                    cost += (self.ct - self.search_flight(next_one).d)**2
            #print ("cost of the solution : {}\n".format(cost))
            if sol_ok:
                print("No error has been detected in the solution!") 
            return(cost)
        else: 
            return (None)             

#**********

if __name__ == "__main__":
    print('This module include : \n - the read function, for reading the files GAPi_j.txt \n - the code of the classes Flight and Instance allowing us to more easily manipulate the data and solutions of the instances \n - the solution-checking function (method from Instance) check_sol\n')  