import numpy as np
import math
import Utils.DataClass as dataClass
import Utils.FillSchedule as fillScheduleFunctions
import Utils.Checks as checkFunctions
from multiprocessing import Pool
from functools import partial

def getChromosomeLength(sourceData):
    return(sum(sourceData['demand']))


def decode(population, sourceData ):
    #Multithread
    nprocs = 4
    chunksize = 5
    p = Pool(nprocs)
    populationResult= p.map(partial(decodeIndividual, sourceData=sourceData), population, chunksize=chunksize)
    p.terminate()
    return populationResult

def decodeIndividual(ind, sourceData):
    chromosome = np.array(ind['chr'])
    result = decodeOneChromosome(chromosome,sourceData)
    ind['solution']=result['solution']
    ind['fitness']=result['fitness']
    return ind


def decodeNoMultiprocessing(population, sourceData ):
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

    solution = list([None]*data.nNurses)
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
        result = {'solution': [], 'fitness': data.nNurses*100}
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
    minRest = math.floor(presence / (data.maxConsec+1.0))
    minRest = max(minRest, presence - data.maxHours)
    maxRest = max(minRest, presence - data.minHours)
    

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
        valid = fillScheduleFunctions.FillSchedule(nurse, data)
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
        if(checkFunctions.CheckMaxConsecutiveHours(nurse['schedule'], data.maxConsec) == False):
            return False
        
        #Check rest
        if(checkFunctions.CheckRest(nurse['schedule']) == False):
            return False
    return True









