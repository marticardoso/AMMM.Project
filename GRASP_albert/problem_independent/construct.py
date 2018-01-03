"""Builds the solution. This is problem independent"""
import random
from problem_dependent.greedy import compute_greedy_cost, update
import time

def construct(E, alpha, params, data, seed):
    random.seed(seed)
    x = []
    while E:
        #t_start = time.time()
        #print '-- step -- ' + str(len(E))
        greedy_cost = compute_greedy_cost(E, x, data)
        #t_greedy = time.time()
        #print 'Greedy time: ' + str(t_greedy-t_start)
        max_cost = max(greedy_cost)
        min_cost = min(greedy_cost)
        threshold = min_cost + alpha*(max_cost - min_cost)
        RCL = []
        for indx, e in enumerate(E):
            if greedy_cost[indx] <= threshold:
                RCL.append(e)
        pick = random.randint(0, len(RCL)-1)
        x.append(RCL[pick])
        #t_rcl = time.time()
        #print 'RCL time: ' + str(t_rcl - t_greedy)
        E = update(E, x, params, data)
        #t_update = time.time()
        #print 'Update time: ' + str(t_update - t_rcl)

        #we should check if the solution is feasible or not

    return x
