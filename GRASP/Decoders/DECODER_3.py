import numpy as np
import math
import DataClass as dataClass
data={"nNurses": 25, "nHours": 20, "minHours": 3, "maxHours": 6, "maxConsec": 6, "maxPresence": 10, "demand": [15, 17, 14, 17, 20, 20, 18, 20, 17, 14, 11, 8, 6, 9, 9, 6, 8, 7, 5, 6]}

def getRange(value, range):
    interval = range[1]-range[0]
    return int(range[0]+ int(interval*value))




def GetDemandOrder(chromosome,demand):
    # Get chromosome index sorted [1,2,0] -> [2,0,1]
    chromIndexSorted = chromosome.argsort()
    
    return(chromIndexSorted)


def ConsecutiveHoursAddingHour(hour,schedule):
    beforeNoWorking = afterNoWorking = hour

    before = np.argwhere(schedule[:hour] == 0)
    if(before.size>0):
        beforeNoWorking = before[-1][0]

    after = np.argwhere(schedule[hour+1:] == 0)
    if(after.size>0):
        afterNoWorking = after[0][0] + hour+1

    consecutive = afterNoWorking-beforeNoWorking-1

    return(consecutive)

def PresenceAddingHour(hour,schedule):
    
    prov = np.argwhere(schedule ==1)
    ini = prov[0][0]
    end = prov[-1][0]
    
    ini = min(ini,hour)
    end = max(end,hour)
    presence = end-ini+1
    return(presence)

def ExistsAValidSolutionAddingHour(hour,schedule, data):
    if(schedule[hour] == 1):
        return False
    
    #Clone schedule
    schedule = np.copy(schedule)
    schedule[hour] = 1

    # Max hours
    assignedHours = np.sum(schedule)
    if(assignedHours >= data.maxHours):
        return False

    # Max Presence
    prov = np.argwhere(schedule ==1)
    ini = prov[0][0]
    end = prov[-1][0]
    presence = end-ini+1
    if(data.maxPresence <= presence):
        return False

    # Max Consec
    minHoursToAdd = data.minHours - assignedHours 
    maxHoursToAdd = data.maxHours - assignedHours 
    blanksHours = presence - assignedHours
    if(blanksHours < minHoursToAdd):
        return False

    minHoursToRest = math.floor((presence+1)/data.MaxConsec)

    i = ini
    consec = 0
    while(i<=end):
        if(schedule[i]==1):
            consec += 1
        else:
            consec = 0
        


    return(True)

def CanAddHour(hour, schedule, data):
    if(schedule[hour] == 1):
        return False
    
    if(data.maxHours <= np.sum(schedule)):
        return False

    if(data.maxConsec <= ConsecutiveHoursAddingHour(hour,schedule)):
        return False

    if(data.maxPresence <= PresenceAddingHour(hour,schedule)):
        return False

    return(True)

def decodeOneChromosome(chromosome, sourceData):
    data = dataClass.DataClass(sourceData)
    chrLength = getChromosomeLength(sourceData)

    solution = np.zeros((data.nNurses, data.nHours))
    solution = solution.astype(int)
    usedNurses = 0
    
    demandOrder =  GetDemandOrder(chromosome,data.demand)
    i = 0
    
    while i < chrLength and usedNurses < data.nNurses:
        hourToDemand = demandOrder[i]
        
        added = data.demand[hourToDemand]
        
        j = 0
        while j < usedNurses and added > 0:
            valid = CanAddHour(hourToDemand, solution[j],data)
            if(valid == True):
                solution[j][hourToDemand] = 1
                added -=1
            j+=1
            
        # Not added
        while added > 0 and usedNurses < data.nNurses:
            solution[usedNurses][hourToDemand] = 1
            usedNurses +=1
            added -= 1

        i +=1

    if(usedNurses<data.nNurses):
        result = {'solution': solution[:usedNurses], 'fitness': usedNurses}
    else:
        result = {'solution': [], 'fitness': data.nNurses*1000}
    return(result)

def decode(population, sourceData ):
    for ind in population:
        chromosome = np.array(ind['chr'])
        result = decodeOneChromosome(chromosome,sourceData)
        ind['solution']=result['solution']
        ind['fitness']=result['fitness']
    return(population)
    
def getChromosomeLength(sourceData):
    data = dataClass.DataClass(sourceData)
    return(len(data.demand))

