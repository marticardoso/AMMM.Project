import math
import numpy as np

# Return true if the schedule guarantee the maxConsec constrain
def CheckMaxConsecutiveHours(schedule, maxConsec):
    consec = 0
    for i in range(len(schedule)):
        if schedule[i] == 1:
            consec += 1
            if consec > maxConsec:
                return False
        else:
            consec = 0
    return True


def CheckMaxPresence(schedule, maxPresence):
    ini = len(schedule)
    end = 0
    for i in range(len(schedule)):
        if schedule[i] == 1:
            ini = min(ini, i)
            end = max(end, i)
    presence = end-ini +1
    return presence <= maxPresence

def CheckMinAndMaxHours(schedule, minHours, maxHours):
    workingHours = sum(schedule)
    if workingHours < minHours:
        return False
    if workingHours > maxHours:
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

def CheckDemand(solution, demand):
    for nurse in solution:
        demand = demand - nurse['schedule']
    return max(demand)<=0