import numpy as np
import math
import DataClass as dataClass
data={"nNurses": 25, "nHours": 20, "minHours": 3, "maxHours": 6, "maxConsec": 6, "maxPresence": 10, "demand": [15, 17, 14, 17, 20, 20, 18, 20, 17, 14, 11, 8, 6, 9, 9, 6, 8, 7, 5, 6]}


def GetDemandOrder(chromosome,demand):
    
    # Convert [1,2,1](demand) -> [[0],[1,1],[2]] (indexes)
    demandMatrix = map(lambda (index, value): [index]*value, enumerate(demand))

    # Convert [[0],[1,1],[2]] -> [0,1,1,2] (flat matrix)
    #demandList = demandMatrix.flatten()
    demandList = np.array(reduce((lambda x, y: x + y), demandMatrix))

    # Get chromosome index sorted [1,2,0] -> [2,0,1]
    chromIndexSorted = chromosome.argsort()
    
    # Chromosome length = demandList length
    # sort Demand List using the chormosome order
    demandOrdered = demandList[chromIndexSorted]

    return(demandOrdered)


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

def PresenceAddingHour(hour,nurse):

    ini = min(hour, nurse['ini'])
    end = max(hour, nurse['end'])
    presence = end-ini+1
    
    return(presence)

def RestAddingHour(init, end, schedule, data, optLeft, oblLeft, minRest,maxRest):
    #Precondition: schedule guarantee maxConsec
    #Init 
    screenIni = init
    screenEnd = min(end,init+data.maxConsec+1)

    restsIntervals = []
    consecutiveRest = 0
    for i in range(init+1, screenEnd+1):
        if(schedule[i]==0):
            consecutiveRest +=1
        else:
            if(consecutiveRest>0):
                restsIntervals.append({'length':consecutiveRest,'end':i-1})
            consecutiveRest = 0
    
    if(consecutiveRest>0):
        restsIntervals.append({'length':consecutiveRest,'end':screenEnd})
    
    # Compute optional rest (except the last consecutive rest)
    obligatoryRest = 0
    optionalRest = 0
    for i in range(len(restsIntervals)-1):
        restLength = restsIntervals[i]['length']
        optionalRest += math.ceil(restLength/2.0)


    # Compute last consecutive rest
    
    if(len(restsIntervals)>0 and screenEnd < end):
        lastRest = restsIntervals[-1] #Last
        #Need more screens
        if(lastRest['end']==screenEnd and lastRest['length'] > 1 and schedule[screenEnd+1]==0):
            option1_opt = optLeft + optionalRest + math.ceil((lastRest['length'])/2)-1
            option1_obl = oblLeft + 1
            valid = RestAddingHour(lastRest['end'], end, schedule, data, option1_opt, option1_obl, minRest, maxRest)
            if(valid):
                return True

            option2_opt = optLeft + optionalRest + math.ceil((lastRest['length']-1)/2)-1
            option2_obl = oblLeft + 1
            valid = RestAddingHour(lastRest['end']-1, end, schedule, data, option2_opt, option2_obl, minRest, maxRest)
            return valid
        else:
            opt = optLeft + optionalRest + math.ceil((lastRest['length'])/2)-1
            obl = oblLeft + 1
            valid = RestAddingHour(lastRest['end'], end, schedule, data, opt, obl, minRest, maxRest)
            return valid
    else:
        opt = optLeft + optionalRest 
        obl = oblLeft
        if(len(restsIntervals)>0):
            lastRest = restsIntervals[-1] #Last
            opt += math.ceil((lastRest['length'])/2)
        return maxRest >= obl and minRest <= obl+opt 

def CanAddHour(hour, nurse, data):
    schedule = nurse['schedule']
    if(schedule[hour] == 1):
        return False
    
    if(data.maxHours < nurse['workingHours']+1):
        return False
    
    if(data.maxPresence < PresenceAddingHour(hour, nurse)):
        return False

    if(ValidConsecutiveHoursAddingHour(hour,schedule, data.maxConsec)==False):
        return False


    ini = min(hour, nurse['ini'])
    end = max(hour, nurse['end'])
    presence = end-ini+1

    maxRest = presence - data.minHours
    minRest = math.floor(presence / (data.maxConsec+1.0))
    minRest = max(minRest, presence - data.maxHours)
    if (RestAddingHour(ini, end, schedule, data, 0, 0, minRest,maxRest) == False):
        return False
    #restValid = (hour>0 and schedule[hour-1]==1) or (hour>1 and schedule[hour-2]==1) or (hour < data.nHours-2 and schedule[hour+2]==1)or (hour < data.nHours-1 and schedule[hour+1]==1)
    #if(restValid == False):
    #    return False

    return(True)

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

    if(usedNurses<=data.nNurses):
        result = {'solution': solution[:usedNurses], 'fitness': usedNurses}
    else:
        result = {'solution': [], 'fitness': data.nNurses*1000}
    return(result)

def decode(population, sourceData ):
    i = 0
    for ind in population:
        chromosome = np.array(ind['chr'])
        result = decodeOneChromosome(chromosome,sourceData)
        ind['solution']=result['solution']
        ind['fitness']=result['fitness']
        i += 1
        print(str(i)+ ',' + str(result['fitness']))
    return(population)
    
def getChromosomeLength(sourceData):
    data = dataClass.DataClass(sourceData)
    return(sum(data.demand))

