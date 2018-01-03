import numpy as np
class DataClass:

    def __init__(self, sourcedata):
        self.nNurses = int(sourcedata["nNurses"])
        self.nHours = int(sourcedata["nHours"])
        self.minHours = int(sourcedata["minHours"])
        self.maxHours = int(sourcedata["maxHours"])
        self.maxConsec = int(sourcedata["maxConsec"])
        self.maxPresence = int(sourcedata["maxPresence"])
        self.demand = np.array(sourcedata["demand"])
        self.originalData = sourcedata
    
    def clone(self):
        return(DataClass(self.originalData))

    def AllDemand(self):
        return(max(self.demand)<=0)
        
