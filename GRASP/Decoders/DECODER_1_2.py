import numpy as np
import DataClass as dataClass
data={"nNurses": 25, "nHours": 20, "minHours": 3, "maxHours": 6, "maxConsec": 6, "maxPresence": 10, "demand": [15, 17, 14, 17, 20, 20, 18, 20, 17, 14, 11, 8, 6, 9, 9, 6, 8, 7, 5, 6]}

def getRange(value, range):
    interval = range[1]-range[0]
    return int(range[0]+ int(interval*value))


def GetConsecutiveHours(hour,schedule):
    beforeNoWorking = afterNoWorking = hour
    schedule[hour] = 1
    before = np.argwhere(schedule[:hour] == 0)
    if(before.size>0):
        beforeNoWorking = before[-1][0]

    after = np.argwhere(schedule[hour+1:] == 0)
    if(after.size>0):
        afterNoWorking = after[0][0] + hour+1

    consecutive = afterNoWorking-beforeNoWorking-1
    schedule[hour] = 0
    return(consecutive)

def CheckMaxConsecutive(schedule, maxConsec):
    consec = 0
    for i in range(len(schedule)):
        if(schedule[i]==1):
            consec +=1
            if(consec > maxConsec):
                return False
        else:
            consec = 0
    return(True)

def CheckRestAndMaxPresence(schedule, maxPresence):
    prov = np.argwhere(schedule ==1)
    ini = prov[0][0]
    end = prov[-1][0]
    presence = end-ini+1
    #Presense
    if(presence>maxPresence): 
        return(False)
    #Rest
    for i in range(ini+1,end):
        if(schedule[i]==0 and (schedule[i-1]==0 or schedule[i+1]==0)):
            return(False)
    return(True)

def CheckPresence(schedule, maxPresence):
    prov = np.argwhere(schedule ==1)
    ini = prov[0][0]
    end = prov[-1][0]
    presence = end-ini+1
    return(presence>maxPresence)


def isValidNurse(schedule, data):
    schedule = np.array(schedule)
    # Max hours
    workingHours = np.sum(schedule)
    if(workingHours > data.maxHours):
        return False
    
    # Min hours
    if(workingHours < data.minHours):
        return False

    # Max Presence and rest
    if(CheckRestAndMaxPresence(schedule, data.maxPresence) == False):
        return False

    # Max Consec
    if(CheckMaxConsecutive(schedule, data.maxConsec) == False):
        return False

    return True

def SettingRest(gens, working, initHour, endHour, maxConsec):
    if len(working[initHour: endHour+1])<= maxConsec: 
        return

    # Cannot rest the first or the last hour
    gensInterval = gens[initHour+1:endHour]

    restIndex = initHour + 1 + gensInterval.index(max(gensInterval))

    working[restIndex] = 0
    SettingRest(gens, working, initHour,    restIndex-1, maxConsec)
    SettingRest(gens, working, restIndex+1, endHour,     maxConsec)

def SettingMaxHours(working, initHour, endHour, data):

    while sum(working) > data.maxHours:
        if data.demand[initHour]> data.demand[endHour]:
            working[initHour] = 0
            initHour +=1
            #If next rest
            if working[initHour] == 0:
                initHour +=1
        else:
            working[endHour] = 0
            endHour -=1
            #If next rest
            if working[endHour] == 0:
                endHour -=1


def SetNewNurse(chromosomeNurse, data):
   
    initHourRange = [0, data.nHours- data.minHours]
    initHour = getRange(chromosomeNurse[0], initHourRange)

    endHourRange = [initHour + data.minHours - 1, data.nHours]
    endHour = getRange(chromosomeNurse[1], endHourRange)
    
    workingHours = [0]*data.nHours
    for i in range(initHour, endHour+1):
        workingHours[i] = 1

    restGens = [0] + chromosomeNurse[2 : ] + [0]

    SettingRest(restGens,workingHours, initHour, endHour,data.maxConsec)

    SettingMaxHours(workingHours, initHour, endHour,data)
    return(workingHours)


def decodeOneChromosome(chromosome, sourceData):
    data = dataClass.DataClass(sourceData)
    solution = []
    nurse = 0
    while nurse < data.nNurses and max(data.demand)>0:
        nurseChr = chromosome[nurse*data.nHours : (nurse+1)*data.nHours]
        workingH = SetNewNurse(nurseChr, data)
        for h in range(len(workingH)):
            if workingH[h] == 1:
                data.demand[h] -=1
        if(isValidNurse(workingH,data) == False):
            return {'solution': [], 'fitness': data.nNurses*100}
        nurse+=1
        solution = solution + [workingH]

    if max(data.demand)>0:
        fitness = data.nNurses +2
    else:
        fitness = nurse #Last nurse
    
    result = {'solution': solution, 'fitness': fitness}
    return(result)

def decode(population, sourceData ):
    for ind in population:
        result = decodeOneChromosome(list(ind['chr']),sourceData)
        ind['solution']=result['solution']
        ind['fitness']=result['fitness']
    return(population)
    

def getChromosomeLength(sourceData):
    data = dataClass.DataClass(sourceData)
    chrLen = data.nNurses*(data.nHours)
    return(chrLen)