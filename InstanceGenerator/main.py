# Imports
import math
import random
import os
import errno

# Configuration parameters
from CONFIGURATION import config 
print config

# initializations
numInstances = int(config['numInstances'])
nNurses = config['nNurses']
minHours = config['minHours']
maxHours = config['maxHours']
maxConsec = config['maxConsec']
maxPresence = config['maxPresence']
nHours = config['nHours']
demand = config['demand']
demandInc = config['demandInc']

# Function definitions. 
# If data is a list of two elements (min,max) return a random value inside the interval
# if data is a simple value returns the value.
def generateValue(data, minBound=None, maxBound=None):
    if isinstance(data, list):
        minValue = int(data[0])
        maxValue = int(data[1])
        #Allowing bounds
        if isinstance(minBound, int):
            minValue = max(minValue, minBound)
        if isinstance(maxBound, int):
            minValue = min(minValue, maxBound)
            maxValue = min(maxValue, maxBound)

        return random.randint(minValue,maxValue)
    else:
        return int(data)

# Generate the intance demand.
# If demand is integer -> returns a list with all same demand
# If demand is a list (min, max), then:
#### If demandInc is valid: generates the first demand random (min,max)
####    and then the other demands are a random number between (previous-inc, previous+inc)
#### Else: generate a list of random number between min and max
def generateDemand(demand, demandInc, length, nNurses, rho):
    if isinstance(demand, list):
        minDemand = min(int(demand[0]), int(math.ceil(nNurses*rho)))
        maxDemand = min(int(demand[1]), int(math.ceil(nNurses*rho)))
        instance_demand=[]
        lastDemand = None
        for i in range(instance_nHours):
            if isinstance(lastDemand, int) and isinstance(demandInc, int) and demandInc>=0:
                localMinDemand = max(lastDemand - demandInc, minDemand)
                localMaxDemand = min(lastDemand + demandInc, maxDemand)
                newDemand = random.randint(localMinDemand,localMaxDemand)
            else:
                newDemand = random.randint(minDemand,maxDemand)
            instance_demand.append(newDemand)
            lastDemand = newDemand
        return instance_demand
    else:
        return [min(int(demand),nNurses)]*length

# Creates the CPLEX folder if not exists
cplexfolder = "./InstanceGenerator/CPLEX_Instances/"
if not os.path.exists(os.path.dirname(cplexfolder)):
    try:
        os.makedirs(os.path.dirname(cplexfolder))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

# Creates the Python folder if not exists
phytonfolder = "./InstanceGenerator/Python_Instances/"
if not os.path.exists(os.path.dirname(phytonfolder)):
    try:
        os.makedirs(os.path.dirname(phytonfolder))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

# Main body
for i in range(numInstances):
    # Nurses
    instance_nNurses = generateValue(nNurses)
    # Hours
    instance_nHours = generateValue(nHours)
    # Min Hours
    instance_minHours = generateValue(minHours, maxBound = instance_nHours)
    # Max Hours
    instance_maxHours = generateValue(maxHours, minBound = instance_minHours, maxBound = instance_nHours)
    # Max consecutive
    instance_maxConsec = generateValue(maxConsec, maxBound = instance_maxHours)
    # Max presence
    instance_maxPresence = generateValue(maxPresence, maxBound = instance_nHours)
    # Demand
    rho =float(instance_maxHours)/float(instance_nHours)
    instance_demand=generateDemand(demand, demandInc, length = instance_nHours, nNurses = instance_nNurses, rho = rho)
    
    # CPLEX
    file = open(cplexfolder +'cplex_instance' + str(i) + '.dat','w')
    file.write('nNurses = ' + str(instance_nNurses) + ';\n')
    file.write('nHours = ' + str(instance_nHours) + ';\n')
    file.write('minHours = ' + str(instance_minHours) + ';\n')
    file.write('maxHours = ' + str(instance_maxHours) + ';\n')
    file.write('maxConsec = ' + str(instance_maxConsec) + ';\n')
    file.write('maxPresence = ' + str(instance_maxPresence) + ';\n')
    file.write('demand = ' + str(instance_demand) + ';\n')
    file.close() 

    # Python
    file = open(phytonfolder +'py_instance' + str(i) + '.py','w')
    file.writelines('data = { \n')
    file.write('   "nNurses": ' + str(instance_nNurses) + ', \n')
    file.writelines('   "nHours": ' + str(instance_nHours) + ',  \n')
    file.writelines('   "minHours": ' + str(instance_minHours) + ',  \n')
    file.writelines('   "maxHours": ' + str(instance_maxHours) + ',  \n')
    file.writelines('   "maxConsec": ' + str(instance_maxConsec) + ',  \n')
    file.write('   "maxPresence": ' + str(instance_maxPresence) + ',  \n')
    file.write('   "demand": ' + str(instance_demand) + ' \n')
    file.write('}')
    file.close()