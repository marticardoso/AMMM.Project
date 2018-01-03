from Utils.ValidAddingHour import CanAddHour
import numpy as np
def compute_greedy_cost(E, sol, data):
    greedy_cost = [1.0]*len(E)
    demand = data.demand

    workers = np.array([0.0]*data.nHours)
    for nurse in sol:
        workers += nurse['schedule']

    remainingDemand = np.array(demand) - workers
    
    firstHourWithDemand = 0
    found = False
    while found == False:
        if remainingDemand[firstHourWithDemand]>0:
            found = True
        else:
            firstHourWithDemand+=1

    for indx, e in enumerate(E):
        
        nurse, hour = e
        #Factor1: if a nurse works
        factor1 = int(sol[nurse]['workingHours']>0)
        
        demandHour = remainingDemand[hour]
        if hour>0:
            demandLeft = max(remainingDemand[hour-1],0)
        else:
            demandLeft = 0
        if hour< data.nHours-1:
            demandRight = max(remainingDemand[hour+1],0)
        else:
            demandRight = 0

        #Factor2: remaining demand at hour hour
        factor2 = demandHour

        #Factor4: difference of demand between (hour-1 and hour) and (hour+1 and hour)
        factor4 = min(demandHour -demandLeft, demandHour - demandRight)

        #Factor3: Has an hour near
        factor3 = 0
        if hour > 0 and sol[nurse]['schedule'][hour-1]:
            factor3=1
        if hour<data.nHours-1 and sol[nurse]['schedule'][hour+1]:
            factor3=1

        #Factor5: First hour with remaining demand
        factor5 = firstHourWithDemand == hour
        greedy_cost[indx] = 10*data.nNurses*factor1 + 10*factor4 + 10*factor2 + factor3 + factor5
    return greedy_cost

def compute_obj(sol):
    """Computes objective function given a solution"""
    objFunc = 0
    for nurse in sol:
        if nurse['workingHours']>0:
            objFunc+=1
    return objFunc

def update(E, sol, lastNurse, data):
    """Updates the vector of elements. In doing so also checks if the demand
    is already fulfilled, in which case the elements available have to be 0 or
    the algorithm will continue to add elements to the solution."""
    workers = np.array([0.0]*data.nHours)
    for nurse in sol:
        workers += nurse['schedule']
    
    E_updated = []
    for e in E:
        if workers[e[1]] < data.demand[e[1]]:
            if lastNurse != e[0]:
                E_updated.append(e)
            elif CanAddHour(e[1],sol[e[0]], data):
                E_updated.append(e)
    return E_updated

def get_solution_elements(data):
    """Creates the vector containing the elements that can be in the solution"""
    elements = []
    for i in range(data.nNurses):
        for j in range(data.nHours):
            elements.append((i, j)) #from 0 to the number-1,
    return elements
