""" Main file of GRASP (greedy randomized adaptive search procedure) """
#imports
import random, time
import numpy as np
import matplotlib.pyplot as plt
from problem_dependent.construct import construct
import Utils.Checks as Check
#configuration parameters
from configuration import conf  #configuration parameters

#problem dependent
from Instances_OPL.py_instance2 import data as sourcedata
from Utils.DataClass import DataClass
from problem_dependent.local_search import local_search
from problem_dependent.greedy import get_solution_elements, compute_obj

#configuration
SEED = int(conf['seed'])
MAXITER = int(conf['maxiter'])
ALPHA = float(conf['alpha'])
random.seed(SEED)
seeds = [random.randint(10**3, 10**4) for x in range(MAXITER)]

#initializations
sol_best = None
obj_best = 10**8
obj_hist = [0]*MAXITER   #records objective function value of the best so far

data = DataClass(sourcedata)

E = get_solution_elements(data)

t_begin = time.time()
for i in range(MAXITER):
    print('Iteration: ' + str(i))
    sol, valid = construct(E, ALPHA, data, seeds[i])
    if valid: 
        sol = local_search(sol, data)
        obj = compute_obj(sol)
        #Check all constrains
        valid = Check.CheckAllConstrains(sol,data,True)
        if valid == False: 
            obj = 10000
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$-- Some errors ----- " +  str(obj))
        if obj < obj_best:
            sol_best = sol
            obj_best = obj
        print("----- Feasible solution obtained ----- with obj func: " +  str(obj))
    elif sol == None:
        print('Not feasible: solution could not be corrected')
        #the error of why could not be corrected is displayed by correc_resting_hours function
    else:
        print("Not feasible: solution was corrected but it did not fulfil the constaints either")
    obj_hist[i] = obj_best

t_end = time.time()
#plot evolution of the best solution
plt.plot(obj_hist)
plt.xlabel('number of iterations')
plt.ylabel('cost of best solution')
plt.axis([0, MAXITER, 0, data.nNurses*1.1])
plt.show()

#print solution obtained
print('---------- SOLUTION -----------')
print('Total time: {:.2f}s'.format(t_end - t_begin))
if not sol_best:
    print('Could not find any feasible solution')
else:
    print('Best objective function value: ' + str(obj_best))
    print('Solution:')
    #print(sorted(sol_best))
