import numpy as np
import math
import DataClass as dataClass

def getChromosomeLength(sourceData):
    data = dataClass.DataClass(sourceData)
    return(sum(data.demand))

# Decoder

def decode(population, sourceData ):
    i = 0
    for ind in population:
        chromosome = np.array(ind['chr'])
        result = decodeOneChromosome(chromosome,sourceData)
        ind['solution']=result['solution']
        ind['fitness']=result['fitness']
        i += 1
    return(population)


def decodeOneChromosome(chromosome, sourceData):
    data = dataClass.DataClass(sourceData)
    chrLength = getChromosomeLength(sourceData)

    solution = [None]*data.nNurses
    usedNurses = 0
    
    demandOrder =  GetDemandOrder(chromosome,data.demand)
    i = 0
    
    while i < chrLength and usedNurses <= data.nNurses:
        hourToDemand = demandOrder[i]
        
        added = False
        
        j = 0
        while j < usedNurses and added == False:
            added = CanAddHour(hourToDemand, solution[j],data)
            if(added == True):
                solution[j]['schedule'][hourToDemand] = 1
                solution[j]['workingHours'] +=1
                solution[j]['ini'] = min(solution[j]['ini'], hourToDemand)
                solution[j]['end'] = max(solution[j]['end'], hourToDemand)
            j+=1
            
        # Not added
        if(added == False):
            if(usedNurses < data.nNurses):
                solution[usedNurses] = {'schedule': np.zeros(data.nHours), 'workingHours':1, 'ini': hourToDemand, 'end': hourToDemand }
                solution[usedNurses]['schedule'] = solution[usedNurses]['schedule'].astype(int)
                solution[usedNurses]['schedule'][hourToDemand] = 1
            usedNurses +=1

        i +=1
    
    
    valid = (usedNurses <= data.nNurses)
    if(valid == True):
        valid = CheckValidSolution(solution[:usedNurses], data)

    if(valid == True):
        result = {'solution': solution[:usedNurses], 'fitness': usedNurses}
    else:
        result = {'solution': [], 'fitness': data.nNurses*1000}
    return(result)


def GetDemandOrder(chromosome,demand):
    
    # Convert [1,2,1](demand) -> [[0],[1,1],[2]] (indexes)
    demandMatrix = map(lambda (index, value): [index]*value, enumerate(demand))

    # Convert [[0],[1,1],[2]] -> [0,1,1,2] (flat matrix)
    demandList = np.array(reduce((lambda x, y: x + y), demandMatrix))

    # Get chromosome index sorted [1,2,0] -> [2,0,1]
    chromIndexSorted = chromosome.argsort()
    
    # Chromosome length = demandList length
    # sort Demand List using the chormosome order
    demandOrdered = demandList[chromIndexSorted]

    return(demandOrdered)

################################################
## Functions to check if an hour can be added ##
################################################

def CanAddHour(hour, nurse, data):
    schedule = nurse['schedule']
    if schedule[hour] == 1:
        return False
    
    if data.maxHours < nurse['workingHours']+1:
        return False
    
    if data.maxPresence < PresenceAddingHour(hour, nurse):
        return False

    if ValidConsecutiveHoursAddingHour(hour,schedule, data.maxConsec)==False:
        return False

    if ValidRestAddingHour(hour, nurse, data) == False:
        return False

    return(True)


# Check if the hour can be added without breaking the maxConsec constrain
def ValidConsecutiveHoursAddingHour(hour,schedule, maxConsec):

    maxConsec -=1 #Selected hour

    #Left side
    i = hour-1
    while i>=0 and schedule[i] == 1:
        maxConsec -=1
        if(maxConsec<0):
            return False
        i-=1

    #Right side
    i = hour + 1
    while i < schedule.size and schedule[i] == 1:
        maxConsec -=1
        if(maxConsec<0):
            return False
        i+=1

    return (maxConsec>=0)

# Return the presence adding hour
def PresenceAddingHour(hour,nurse):

    ini = min(hour, nurse['ini'])
    end = max(hour, nurse['end'])
    presence = end-ini+1
    return(presence)

# Check if the hour can be added without breaking the rest constrain
def ValidRestAddingHour(hour, nurse, data):
    # Compute new ini and end
    ini = min(hour, nurse['ini'])
    end = max(hour,nurse['end'])
    presence = end - ini + 1

    # Compute min and max rest 
    maxRest = presence - data.minHours
    minRest = math.floor(presence / (data.maxConsec+1.0))
    minRest = max(minRest, presence - data.maxHours)
    

    optionalRests = 0
    obligatoryRest = 0

    pos = ini
    while pos <= end-data.maxConsec:
        # Window internval (length maxConsec +1)
        # It has to rest at least one time (obligatory) and a few more (optional)
        # Compute this values
        windowIni = pos
        windowEnd = pos+data.maxConsec
        
        mostRightRest = None #Most right rest in the window
        
        i = windowEnd # Right to left for
        while i>windowIni:
            # If nurse is not working in i hour
            if(hour != i and nurse['schedule'][i]==0):
                # If first, add one obligatory rest
                if(mostRightRest==None):
                    mostRightRest = i
                    obligatoryRest +=1
                    i -= 1 # Decrease 1 hour because a nurse can not rest two consec hours
               
                # If more rests, add one optional rest 
                else:
                    optionalRests +=1
                    i -= 1 # Decrease 1 hour because a nurse can not rest two consec hours
            i -= 1
        #If there is no rest in the interval -> maxConsec error
        if mostRightRest == None:
            return False
        pos = mostRightRest +1

    # Last window (no obligatory rest)
    i = pos+1
    while i < end:
        if(hour!=i and nurse['schedule'][i]==0):
            optionalRests += 1
            i +=1
        i += 1
    
    # Check if the rests can be possible
    if obligatoryRest > maxRest:
        return False
    if obligatoryRest + optionalRests < minRest:
        return False
    return True
    




###########################################
## Functions to check the final solution ##
###########################################

# Fill and check if the solution is valid
def CheckValidSolution(solution, data):
    for nurse in solution:
        schedule = nurse['schedule']

        # Try to fill all schedule
        valid = FillSchedule(nurse, data)
        if(valid == False):
            return False

        #Max presence
        presence =  nurse['end'] - nurse['ini'] + 1  
        if(presence> data.maxPresence): 
            return False
        
        #Max hours
        if(nurse['workingHours']> data.maxHours):
            return False
        
        #Min hours
        if(nurse['workingHours']< data.minHours):
            return False

        #Max consec
        if(CheckMaxConsecutive(nurse['schedule'], data.maxConsec) == False):
            return False
        
        #Check rest
        if(CheckRest(nurse['schedule']) == False):
            return False
    return True


# Return true if the schedule guarantee the maxConsec constrain
def CheckMaxConsecutive(schedule,maxConsec):
    consec = 0
    for i in range(len(schedule)):
        if(schedule[i]==1):
            consec +=1
        else:
            consec = 0

        if(consec > maxConsec):
            return False
    return True

# Return true if the schedule guarantee the rest constrain
def CheckRest(schedule):
    isWorking = False
    restConsec = 0
    for i in range(len(schedule)):
        if(schedule[i]==1):
            if(restConsec>1 and isWorking):
                return False
            restConsec = 0
            isWorking = True
        else:
            restConsec +=1
    return True



################################################################
## Functions to fill the schedule of a nurse (final solution) ##
################################################################

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
        i += 1
        # If maxConsec, then rest 1 hour
        if(consec == data.maxConsec):
            i -= 1
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

