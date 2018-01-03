from problem_dependent.auxiliary import can_work
from problem_dependent.greedy import compute_obj

def remove_nurse(n, sol):
    new_sol = []
    for e in sol:
        if e[0] != n:
            new_sol.append(e)
    return new_sol

def local_search_main(sol, nurses_working, data):
    demand = data.demand

    for i in range(data.nNurses):
        if nurses_working[i]:
            sol2 = sol
            workers = [0]*data.nHours
            for e in sol:
                nurse, hour = e
                if (nurse != i):
                    workers[hour] += 1

            #try to make work more already working nurses
            for h in range(data.nHours):
                if workers[h] < demand[h]:
                    satisfied = False
                    for n in range(data.nNurses):
                        if (not satisfied) and n != i and nurses_working[n] and can_work(n, h, sol2, data):
                            sol2.append((n,h))
                            workers[h] += 1 #not necessary, at most one nurse more is needed
                            satisfied = True
            
            if all([w >= d for w,d in zip(workers, demand)]):
                nurses_working[i] = False
                return remove_nurse(i, sol2), nurses_working, True
    
    return sol, nurses_working, False

def local_search(x, data):
    #get working nurses
    nurses_working = [False]*data.nNurses
    for e in x:
        nurses_working[e[0]] = True
    
    solution = x
    improvement = True
    while improvement:
        solution, nurses_working, improvement = local_search_main(solution, nurses_working, data)
        #if improvement:
        #    print('********** local serach does something **********')

    return solution