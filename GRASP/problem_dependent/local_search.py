from problem_dependent.greedy import compute_obj
import numpy as np
from Utils.ValidAddingHour import CanAddHour
from Utils.FillSchedule import SetWorkingHour, FillAllSchedules
from Utils.Checks import CheckAllConstrains
import copy

def CanRealocateHour(hour, nurseOrigin, sol, data):
    for nurse in range(len(sol)):
        if nurse!=nurseOrigin and sol[nurse]['workingHours']>0:
            valid = CanAddHour(hour,sol[nurse],data)
            if valid:
                return True, nurse
    return False, -1

def local_search_main(sol, data):
    demand = np.array(np.array(data.demand), copy=True) 
    for nurse in sol:
        for hour in range(0,data.nHours):
            demand[hour] -= nurse['schedule'][hour]
    
    for n in range(len(sol)):
        if(sol[n]['workingHours']>0):
            sol2 = copy.deepcopy(sol)
            validRemoveNurse = True
            sheduleToDelete = sol[n]['schedule']
            hour = 0
            while validRemoveNurse and hour < data.nHours:
                if sheduleToDelete[hour] == 1 and demand[hour]==0:
                    canRemoveHour, n2 = CanRealocateHour(hour, n, sol2, data)
                    if(canRemoveHour):
                        SetWorkingHour(hour, sol2[n2],data)
                    else:
                        validRemoveNurse = False
                hour +=1
            
            if(validRemoveNurse):
                sol2 = sol2[0:n] + sol2[n+1:data.nNurses]
                return sol2, True

    return sol, False

def local_search(solution, data):
    firstSolution = solution
    improvement = True
    while improvement:
        solution, improvement = local_search_main(solution, data)
        #if improvement:
        #    print('********** local serach does something **********')
    
    valid = FillAllSchedules(solution,data)
    if(valid==True):
        valid = CheckAllConstrains(solution,data, True)

    if(valid == False):
        return firstSolution
    return solution