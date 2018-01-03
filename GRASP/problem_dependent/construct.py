"""Builds the solution"""
import random
import numpy as np
from problem_dependent.greedy import compute_greedy_cost, update
from Utils.FillSchedule import FillSchedule, SetWorkingHour, FillAllSchedules
import Utils.Checks as Check
import time

def construct(E, alpha, data, seed):
    random.seed(seed)
    # Initialize all schedules to no working
    solution = list(map(lambda x: {'schedule': np.zeros(data.nHours), 'workingHours': 0, 'ini':data.nHours,'end': 0}, [None]*data.nNurses))

    timegreedying = 0
    timeRCL = 0
    timeUpdate = 0
    while E:
        t_start = time.time()
        #Compute greedy cost
        greedy_cost = compute_greedy_cost(E, solution, data)
        t_greedy = time.time()

        #RCL
        max_cost = max(greedy_cost)
        min_cost = min(greedy_cost)
        threshold = min_cost + alpha*(max_cost - min_cost)
        RCL = [e for (e,cost) in zip(E,greedy_cost) if cost>=threshold]
        
        pick = random.randint(0, len(RCL)-1)
        pickNurse = RCL[pick][0]
        pickHour = RCL[pick][1]

        #Set nurse-hour to work
        SetWorkingHour(pickHour,solution[pickNurse],data)
        t_rcl = time.time()

        # Update candidates
        E = update(E, solution, pickNurse, data)
        t_update = time.time()

        timegreedying += t_greedy - t_start
        timeRCL += t_rcl - t_greedy
        timeUpdate += t_update - t_rcl

        


    # Remove unused nurses
    solution = [n for n in solution if n['workingHours']>0]

    #Fill schedules (to guarantee all constrains (minHours, rest,...))
    valid = FillAllSchedules(solution, data)
    
    #Check all constrains
    if valid == True:
        valid = Check.CheckAllConstrains(solution,data, False)

    if valid == False:
        return None, False

    return solution, True



