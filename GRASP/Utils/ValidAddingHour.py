import numpy as np
import math
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
    maxRest = max(minRest,presence - data.minHours)
    

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
    