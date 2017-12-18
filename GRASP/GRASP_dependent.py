import math
import numpy as np

def createCandidateAssignments(data):
    assigments=[]
    for i in range(data.nNurses):
        for j in range(data.nHours):
            assigments.append({'nurse':i,'hour': j, 'cost': None})
    return(assigments)

def initializeSolution(data):
    return([None]*data.nNurses)

def filterCandidatesAndComputeGreedyCost(assigments, solution, data):
    filtered = []
    for assigment in assigments:

        if(isValidCandidate(assigment['nurse'], assigment['hour'],solution, data)):
            assigment['cost'] = computeGreedyCost()
            filtered.append(assigment)
    return filtered

def isValidCandidate(nurse, hour, solution, data):
    schedule = np.copy(solution[nurse])
    if(schedule == None):
        return True
    
    if(schedule[hour]==1):
        return False

    if(data.maxHours <= np.sum(schedule)):
        return False

    if(data.maxConsec < ConsecutiveHoursAddingHour(hour,schedule)):
        return False

    if(data.maxPresence < PresenceAddingHour(hour,schedule)):
        return False

    return True

 
def ConsecutiveHoursAddingHour(hour,schedule):
    before = np.argwhere(schedule[:hour] == 0)
    if(before.size>0):
        beforeNoWorking = before[-1][0]
    else:
        beforeNoWorking = 0

    after = np.argwhere(schedule[hour+1:] == 0)
    if(after.size>0):
        afterNoWorking = after[0][0] + hour+1
    else:
        afterNoWorking = len(schedule)-1

    consecutive = afterNoWorking-beforeNoWorking-1
    return(consecutive)

def PresenceAddingHour(hour,schedule):
    schedule[hour] = 1
    prov = np.argwhere(schedule ==1)
    ini = prov[0][0]
    end = prov[-1][0]
    
    ini = min(ini,hour)
    end = max(end,hour)
    presence = end-ini+1
    schedule[hour] = 0
    return(presence)

def PresenceAddingHour(hour,schedule):
    schedule[hour] = 1
    prov = np.argwhere(schedule ==1)
    ini = prov[0][0]
    end = prov[-1][0]
    
    ini = min(ini,hour)
    end = max(end,hour)
    presence = end-ini+1
    schedule[hour] = 0
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
        optionalRest += math.ceil(restLength/2)


    # Compute last consecutive rest
    lastRest = restsIntervals[-1] #Last
    if(screenEnd < end):
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
        return optionalRest, obligatoryRest
    









def doCrossover(elite,nonelite,ro,numCrossover):
    crossover=[]
    for i in range(numCrossover):
        indexElite=int(math.floor(np.random.rand()*len(elite)))
        indexNonElite=int(math.floor(np.random.rand()*len(nonelite)))
        chrElite=elite[indexElite]['chr']
        chrNonElite=nonelite[indexNonElite]['chr']
        rnd=list(np.random.rand(len(chrElite)))
        chrCross=[chrElite[i] if rnd[i]<= ro else chrNonElite[i] for i in range(len(chrElite))]
        crossover.append({'chr':chrCross, 'solution':{},'fitness':None})
    return crossover
    
def getBestFitness(population):
    fitness=np.array([e['fitness'] for e in population])
    order=sorted(range(len(fitness)), key=lambda k: fitness[k])
    return population[order[0]]
