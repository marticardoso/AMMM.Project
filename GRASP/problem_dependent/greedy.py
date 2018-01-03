from Utils.ValidAddingHour import CanAddHour

def compute_greedy_cost(E, sol, data):
    greedy_cost = [1.0]*len(E)
    demand = data.demand

    workers = [0]*data.nHours
    nurses_used = [0]*data.nNurses
    hours = {}
    for idx, nurse in enumerate(sol):
        for hour in range(0,data.nHours):
            workers[hour]+=nurse['schedule'][hour]
        nurses_used[idx] = nurse['workingHours']>0

    firstHourWithDemand = 0
    found = False
    while found == False:
        if demand[firstHourWithDemand]- workers[firstHourWithDemand]>0:
            found = True
        else:
            firstHourWithDemand+=1

    lastHourWithDemand = 0
    found = False
    while found == False:
        if demand[lastHourWithDemand]- workers[lastHourWithDemand]>0:
            found = True
        else:
            lastHourWithDemand-=1
    #for key in hours:
    #    hours[key] = sorted(hours[key])
    for indx, e in enumerate(E):
        
        nurse, hour = e
        factor1 = int(nurses_used[nurse])
        
        demandHour = demand[hour]-workers[hour]
        if hour>0:
            demandLeft = max(demand[hour-1]-workers[hour-1],0)
        else:
            demandLeft = 0
        if hour< data.nHours-1:
            demandRight = max(demand[hour+1]-workers[hour+1],0)
        else:
            demandRight = 0

        factor2 = demandHour
        factor4 = min(demandHour -demandLeft, demandHour - demandRight)
        factor3 = 0
        if hour > 0 and sol[nurse]['schedule'][hour-1]:
            factor3=1
        if hour<data.nHours-1 and sol[nurse]['schedule'][hour+1]:
            factor3=1

        factor5 = firstHourWithDemand == hour + lastHourWithDemand == hour
        greedy_cost[indx] = data.nNurses*factor1 + factor4 + factor2
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
    workers = [0]*data.nHours
    for nurse in sol:
        for hour in range(0,data.nHours):
            workers[hour] += nurse['schedule'][hour]
                

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
