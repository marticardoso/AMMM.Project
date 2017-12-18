import numpy as np
import DataClass as dataClass
data={"nNurses": 25, "nHours": 20, "minHours": 3, "maxHours": 6, "maxConsec": 6, "maxPresence": 10, "demand": [15, 17, 14, 17, 20, 20, 18, 20, 17, 14, 11, 8, 6, 9, 9, 6, 8, 7, 5, 6]}


def GetDemandOrder(chromosome,demand):
    # Convert [1,2,1](demand) -> [[0],[1,1],[2]] (indexes)
    demandMatrix = map(lambda (index, value): [index]* value, enumerate(demand))
    # Convert [[0],[1,1],[2]] -> [0,1,1,2] (flat matrix)
    demandList = reduce((lambda x, y: x + y), demandMatrix)

    # Chromosome length = demandList length
    # sort Demand List using the chormosome order
    demandOrder = [x for _,x in sorted(zip(chromosome,demandList))]
    return(demandOrder)


def ConsecutiveHoursAddingHour(hour,schedule):
    consecutive = 1

    i = hour-1
    while i>=0 and schedule[i] == 1:
        consecutive +=1
        i-=1
    
    i = hour + 1
    while i < schedule.size and schedule[i] == 1:
        consecutive +=1
        i+=1

    return(consecutive)

def PresenceAddingHour(hour,schedule):
    
    prov = np.argwhere(schedule ==1)
    ini = prov[0][0]
    end = prov[-1][0]
    
    ini = min(ini,hour)
    end = max(end,hour)
    presence = end-ini+1
    return(presence)


def CanAddHour(hour, schedule, data):
    schedule = schedule
    if(schedule[hour] == 1):
        return False
    
    if(data.maxHours <= sum(schedule)):
        return False

    if(data.maxConsec <= ConsecutiveHoursAddingHour(hour,schedule)):
        return False

    if(data.maxPresence <= PresenceAddingHour(hour,schedule)):
        return False

    return(True)

def decodeOneChromosome(chromosome, sourceData):
    data = dataClass.DataClass(sourceData)
    chrLength = getChromosomeLength(sourceData)

    solution = []
    
    usedNurses = 0
    
    demandOrder = GetDemandOrder(chromosome,data.demand)
    i = 0
    while i < chrLength and usedNurses < data.nNurses:
        hourToDemand = demandOrder[i]
        j = 0
        added = False
        
        while j < usedNurses and added == False:
            added = CanAddHour(hourToDemand, solution[j],data)
            if(added == True):
                solution[j][hourToDemand] = 1
            j+=1
            
        # Not added
        if(added == False):
            newNurse = np.array([0]*data.nHours)
            newNurse[hourToDemand] = 1
            solution = solution + [newNurse]
            usedNurses +=1

        i +=1

    if(usedNurses<data.nNurses):
        result = {'solution': solution, 'fitness': usedNurses}
    else:
        result = {'solution': [], 'fitness': data.nNurses*1000}
    return(result)

def decode(population, sourceData ):
    for ind in population:
        result = decodeOneChromosome(list(ind['chr']),sourceData)
        ind['solution']=result['solution']
        ind['fitness']=result['fitness']
    return(population)
    
def getChromosomeLength(sourceData):
    data = dataClass.DataClass(sourceData)
    return(sum(data.demand))

