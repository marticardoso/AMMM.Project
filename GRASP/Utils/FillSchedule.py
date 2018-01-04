################################################################
## Functions to fill the schedule of a nurse (final solution) ##
################################################################

def FillAllSchedules(solution, data):
    for nurse in solution:
        valid = FillSchedule(nurse, data)
        if(valid == False):
            return False
    return True

def FillSchedule(nurse, data):

    ini = nurse['ini']
    end = nurse['end']

    optionalRests = []

    pos = ini
    while pos <= end-data.maxConsec:
        # Window internval (length maxConsec +1)
        screenIni = pos
        screenEnd = pos+data.maxConsec
        
        # For that set the rests correctly
        i = screenEnd
        firstRestFound = False
        mostRightRest = None
        nearRest = None
        while i>=screenIni:
            if(nurse['schedule'][i]==0):
                if(firstRestFound==False):
                    mostRightRest = i
                    nearRest = i
                    firstRestFound = True
                    SetWorkingHour(i-1, nurse, data)
                    SetWorkingHour(i+1, nurse, data)
                else:
                    optionalRests = optionalRests +[i]
                    nearRest = i
                    SetWorkingHour(i-1, nurse, data)
            i -= 1
        #If there is no rest in the interval -> maxConsec error
        if mostRightRest == None:
            return False
        pos = mostRightRest +1

    # Last window
    i = pos
    while i < end:
        if(nurse['schedule'][i]==0):
            optionalRests = optionalRests +[i]
            SetWorkingHour(i+1, nurse, data)
        i += 1


    i = 0
    while i < len(optionalRests) and nurse['workingHours']<data.minHours:
        SetWorkingHour(optionalRests[i], nurse, data)
        i +=1
    # If needed, it add hours to the left and right
    if nurse['workingHours']<data.minHours:
        AddRightHours(nurse, data)
    if nurse['workingHours']<data.minHours:
        AddLeftHours(nurse, data)

    return True


def SetWorkingHour(hour,nurse,data):
    if hour >= data.nHours:
        return
    if(nurse['schedule'][hour]==1):
        return

    nurse['schedule'][hour] = 1
    nurse['workingHours'] +=1
    nurse['ini'] = min(nurse['ini'],hour)
    nurse['end'] = max(nurse['end'],hour)


# It add hours to the right of the schedule until it reach the minHours
def AddRightHours(nurse, data):
    consec = 0
    i = nurse['end']
    while i>=0 and nurse['schedule'][i]==1:
        consec +=1
        i -=1
    i = nurse['end']+1
    # If maxConsec, then rest 1 hour
    if(consec == data.maxConsec):
        i +=1
        consec = 0

    while(i< data.nHours and  nurse['workingHours']< data.minHours):
        SetWorkingHour(i, nurse, data)
        consec +=1
        i += 1
        # If maxConsec, then rest 1 hour
        if(consec == data.maxConsec):
            i += 1
            consec = 0

# It add hours to the left of the schedule until it reach the minHours
def AddLeftHours(nurse, data):
    consec = 0
    i = nurse['ini']
    while i < data.nHours and nurse['schedule'][i]==1:
        consec +=1
        i +=1
    
    i = nurse['ini']-1
    # If maxConsec, then rest 1 hour
    if(consec == data.maxConsec):
        i -=1
        consec = 0

    while(i>=0 and  nurse['workingHours']< data.minHours):
        SetWorkingHour(i, nurse, data)
        consec +=1
        i -= 1
        # If max consec, then rest 1 hour
        if(consec == data.maxConsec):
            i -= 1
            consec = 0
