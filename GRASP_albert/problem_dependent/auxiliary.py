def can_work(n, h, solution, data):
    hours = []
    for e in solution:
        if e[0] == n:
            hours.append(e[1])
    
    if not hours:   #is empty
        return True
    
    hours = sorted(hours) 

    #already works that hour
    if h in hours:
        return False
    #works maximum number of hours
    if len(hours) >= data.maxHours:
            return False
    #maxPresence
    if h - hours[0] + 1 >= data.maxPresence or hours[-1]-h + 1 >= data.maxPresence:
        return False

    #maxConsec
    hours.append(h)
    hours = sorted(hours)
    consec = 0
    for indx, value in enumerate(hours):
        if value == hours[max(0,indx-1)] + 1:
            consec += 1
            if consec > data.maxConsec:
                return False
        else:   
            consec = 1
    #rests
    #the distance between two consecutive working hours cannot be greater that 2
    for indx, value in enumerate(hours):
        if value - hours[max(0,indx-1)] > 2:
            return False
    return True

def can_work_relaxed(n, h, solution, data):
    """The same than before but without checking the resting hours"""    
    hours = []
    for e in solution:
        if e[0] == n:
            hours.append(e[1])
    
    if not hours:   #is empty
        return True
    
    hours = sorted(hours) 

    #already works that hour
    if h in hours:
        return False
    #works maximum number of hours
    if len(hours) >= data.maxHours:
            return False
    #maxPresence
    if h - hours[0] + 1 >= data.maxPresence or hours[-1]-h + 1 >= data.maxPresence:
        return False

    #maxConsec
    hours.append(h)
    hours = sorted(hours)
    consec = 0
    for indx, value in enumerate(hours):
        if value == hours[max(0,indx-1)] + 1:
            consec += 1
            if consec > data.maxConsec:
                return False
        else:   
            consec = 1
    
    return True

def check_constraints(solution, data):
    workers = [0]*data.nHours
    d = {}
    for n in range(data.nNurses):
        d[n] = []
    for e in solution:
        d[e[0]].append(e[1])
        workers[e[1]] += 1
    
    if not all(w >= d for w,d in zip(workers, data.demand)):
        print('demand could not be satisfied')
        return False

    for n in range(data.nNurses):
        hours = d[n]

        if hours:
            #works maximum number of hours
            if len(hours) > data.maxHours:
                print("Error: nurse " + str(n) + " works too much.")
                return False

            hours = sorted(hours)

            #maxPresence
            if hours[-1] - hours[0] + 1 >= data.maxPresence:
                print("Error: nurse " + str(n) + " is present too many hours")
                return False
            #maxConsec
            consec = 0
            for indx, value in enumerate(hours):
                if value == hours[max(0,indx-1)] + 1:
                    consec += 1
                    if consec > data.maxConsec:
                        print("Error: nurse " + str(n) + " works too many consecutive hours")
                        return False
                else:   
                    consec = 1
            #rests
            #the distance between two consecutive working hours cannot be greater that 2
            for indx, value in enumerate(hours):
                if value - hours[max(0,indx-1)] > 2:
                    print("1st error: nurse " + str(n) + " rests too much.")
                    return False
    return True
                
def avoids_consecutive_rest(h, hours):
    for hour in hours:
        if abs(hour - h) <= 2:
            return True
    return False