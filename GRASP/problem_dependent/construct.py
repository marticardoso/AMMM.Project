"""Builds the solution. This is problem independent"""
import random
import numpy as np
from problem_dependent.greedy import compute_greedy_cost, update
from Utils.FillSchedule import FillSchedule, SetWorkingHour, FillAllSchedules
import Utils.Checks as Check
import time

def construct(E, alpha, data, seed):
    random.seed(seed)
    solution = list(map(lambda x: {'schedule': np.zeros(data.nHours), 'workingHours': 0, 'ini':data.nHours,'end': 0}, [None]*data.nNurses))
    while E:
        #t_start = time.time()
        #print '-- step -- ' + str(len(E))
        greedy_cost = compute_greedy_cost(E, solution, data)
        #t_greedy = time.time()
        #print 'Greedy time: ' + str(t_greedy-t_start)
        max_cost = max(greedy_cost)
        min_cost = min(greedy_cost)
        threshold = min_cost + alpha*(max_cost - min_cost)
        RCL = []
        for indx, e in enumerate(E):
            if greedy_cost[indx] >= threshold:
                RCL.append(e)
        pick = random.randint(0, len(RCL)-1)
        pickNurse = RCL[pick][0]
        pickHour = RCL[pick][1]
        SetWorkingHour(pickHour,solution[pickNurse],data)
        #t_rcl = time.time()
        #print 'RCL time: ' + str(t_rcl - t_greedy)
        E = update(E, solution, pickNurse, data)
        #t_update = time.time()
        #print 'Update time: ' + str(t_update - t_rcl)

        #we should check if the solution is feasible or not
    
    #Fill schedules
    valid = FillAllSchedules(solution, data)
    #Check all constrains
    valid = Check.CheckAllConstrains(solution,data, True)

    if valid == False:
        return None, False
    return solution, True



