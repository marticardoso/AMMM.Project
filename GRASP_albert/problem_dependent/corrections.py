def correct_resting_hours(solution, data):
    d = {}
    for n in range(data.nNurses):
        d[n] = []
    for e in solution:
            d[e[0]].append(e[1])
    for n in range(data.nNurses):
        hours = d[n]
        if hours:
            hours = sorted(hours)
            #rests
            for indx, value in enumerate(hours):
                if value - hours[max(0, indx-1)] > 2:
                    #tries to solve the problem by adding working hours
                    add_hours = correct_gap(hours[indx-1], hours[indx], consec_left(hours, indx-1), 
                                consec_right(hours, indx), len(hours), data)
                    if not add_hours:
                        print('Nurse ' + str(n) + ' could not be corrected')
                        return []
                    else: 
                        for h in add_hours:
                            solution.append((n,h))   
    return solution

def correct_gap(left, right, cons_l, cons_r, working_hours, data):
    dist = right - left
    if dist % 2 == 0:
        return correct_even_gap(left, right, working_hours, data, [])
    else:
        return correct_odd_gap(left, right, cons_l, cons_r, working_hours, data, [])
    #return the hours to be inserted to the solution. If empty the problem cannot be solved

def correct_odd_gap(left, right, cons_l, cons_r, working_hours, data, new_hours):
    dist = right - left
    if dist == 3:
        return correct_gap_3(left, right, cons_l, cons_r, working_hours, data, new_hours)
    else: 
        if cons_l < data.maxConsec:
            return correct_even_gap(left+1, right, working_hours + 1, data, [left+1] + new_hours)
        elif cons_r < data.maxConsec:
            return correct_even_gap(left, right-1, working_hours + 1, data, [right-1] + new_hours)
        else:
            return correct_odd_gap(left + 2, right, 1, cons_r, 
                                   working_hours + 1, data, [left +2] + new_hours)

def correct_gap_3(left, right, cons_l, cons_r, working_hours, data, new_hours):
    dist = right - left
    if dist != 3:
        raise ValueError('Not distance 3 given to correct_gap_3')
    if working_hours + 1 > data.maxHours:
        return []
    if cons_l < data.maxConsec:
        new_hours.append(left + 1)
    elif cons_r < data.maxConsec:
        new_hours.append(right - 1)
    else:
        return []
    return new_hours

def correct_even_gap(left, right, working_hours, data, new_hours):
    dist = right - left
    if dist % 2 != 0:
        raise ValueError('An odd gap has been given to the function correct_even_gap')
    added_hours = dist/2 - 1
    if working_hours + added_hours <= data.maxHours:
        for k in range(int(added_hours)):
            new_hours.append(left + 2*(k+1))
        return new_hours
    else:
        return []

def consec_left(v, indx):
    if indx == 0:
        return 1
    else:
        consec = 1
        for i in range(1,indx+1):
            if v[indx-i] + 1 == v[indx-i+1]:
                consec += 1
            else:
                return consec
        return consec

def consec_right(v, indx):
    if indx == len(v)-1:
        return 1
    else:
        consec = 1
        for i in range(indx, len(v)-1):
            if v[i] + 1 == v[i+1]:
                consec += 1
            else:
                return consec
        return consec