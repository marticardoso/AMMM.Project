""" Main file of GRASP (greedy randomized adaptive search procedure) """
#imports
import random, time
import numpy as np
import math
from problem_dependent.construct import construct
import Utils.Checks as Check
#configuration parameters
from configuration import conf  #configuration parameters

#problem dependent
from Utils.DataClass import DataClass
from problem_dependent.local_search import local_search
from problem_dependent.greedy import get_solution_elements, compute_obj
import importlib


def import_instance(num):
    name = "Instances_Heur.py_instance" + str(num)
    m = importlib.import_module(name)
    return m.data

#configuration
SEED = int(conf['seed'])
MAXITER = int(conf['maxiter'])
ALPHA = float(conf['alpha'])
random.seed(SEED)
seeds = [random.randint(10**3, 10**4) for x in range(MAXITER)]

for i in range(1,20+1):
    print('##############################################')
    print('###### Instances_OPL.py_instance' + str(i)+ ' #########')
    print('##############################################')
    sourcedata = import_instance(i)
    print('Data: ' +str(sourcedata))
    #initializations
    sol_best = None
    obj_best = 10**8
    obj_hist = [0]*MAXITER   #records objective function value of the best so far

    data = DataClass(sourcedata)

    E = get_solution_elements(data)

    t_begin = time.time()
    for i in range(MAXITER):
        t_it_ini = time.time()
        sol, valid = construct(E, ALPHA, data, seeds[i])
        if valid: 
            sol = local_search(sol, data)
            obj = compute_obj(sol)
            #Check all constrains
            valid = Check.CheckAllConstrains(sol,data,True)

            if valid == True and obj < obj_best:
                sol_best = sol
                obj_best = obj
        obj_hist[i] = obj_best
        t_it_end = time.time()
        t_it_in = math.floor(t_it_end- t_it_ini)
        print "It"+str(i) + "-"+str(t_it_in)+"("+str(obj_best) + ")",
    print ""
    t_end = time.time()


    #print solution obtained
    #print('---------- SOLUTION -----------')
    print('    - Total time: {:.2f}s'.format(t_end - t_begin))
    if not sol_best:
        print('     - Nurses: Could not find any feasible solution')
    else:
        print('     - Nurses: ' + str(obj_best))
        #print('Solution:')
        #print(sorted(sol_best))
