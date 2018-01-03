from problem_dependent.auxiliary import can_work_relaxed, avoids_consecutive_rest

def compute_greedy_cost(E, x, data):
    greedy_cost = [1.0]*len(E)
    demand = data.demand

    workers = [0]*data.nHours
    nurses_used = [False]*data.nNurses
    hours = {}
    for e in x:
        nurse, hour = e
        workers[hour] += 1
        if not nurses_used[nurse]:
            hours[nurse] = [hour]
            nurses_used[nurse] = True
        else:
            hours[nurse].append(hour)

    #for key in hours:
    #    hours[key] = sorted(hours[key])

    for indx, e in enumerate(E):
        nurse, hour = e
        if workers[hour] < demand[hour]:
            greedy_cost[indx] -= 0.1
        if nurses_used[nurse]:
            greedy_cost[indx] -= 0.1
            if avoids_consecutive_rest(hour, hours[nurse]):
                greedy_cost[indx] -= 0.1
    return greedy_cost

def compute_obj(sol):
    """Computes objective function given a solution"""
    nurses = [n for n, _ in sol]
    different_nurses = set(nurses)
    return len(different_nurses)

def update(E, sol, params, data):
    """Updates the vector of elements. In doing so also checks if the demand
    is already fulfilled, in which case the elements available have to be 0 or
    the algorithm will continue to add elements to the solution."""
    workers = [0]*data.nHours
    for e in sol:
        nurse, hour = e
        workers[hour] += 1

    nurse, hour = sol[-1]    #last added element
    E_updated = []
    for e in E:
        if workers[e[1]] < data.demand[e[1]]*params:
            if nurse != e[0]:
                E_updated.append(e)
            elif can_work_relaxed(e[0], e[1], sol, data):
                E_updated.append(e)
    return E_updated

def get_solution_elements(data):
    """Creates the vector containing the elements that can be in the solution"""
    elements = []
    for i in range(data.nNurses):
        for j in range(data.nHours):
            elements.append((i, j)) #from 0 to the number-1,
    return elements
