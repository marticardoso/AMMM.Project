# imports
import math
import matplotlib.pyplot as plt
import time
import datetime
import BRKGA as brkga
import Utils.Checks as Check
import Decoder as decoder 
from Instances_Heur.py_instance86 import data 
from CONFIGURATION import config 
from pandas import *

print(config)
print(data)
# initializations
numIndividuals=int(config['numIndividuals'])
numElite=int(math.ceil(numIndividuals*config['eliteProp']))
numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
numCrossover=max(numIndividuals-numElite-numMutants,0)
maxNumGen=int(config['maxNumGen'])
ro=float(config['inheritanceProb'])
evol=[]

# Main body
chrLength=decoder.getChromosomeLength(data)
population=brkga.initializePopulation(numIndividuals,chrLength)
t_ini = time.time()
i=0
while (i<maxNumGen):
    population = decoder.decodeNoMultiprocessing(population,data)
    bestFit = brkga.getBestFitness(population)['fitness']
    evol.append(bestFit)
    if numElite>0:
        elite, nonelite = brkga.classifyIndividuals(population,numElite)
    else:
        elite = []
        nonelite = population
    if numMutants>0: mutants = brkga.generateMutantIndividuals(numMutants,chrLength)
    else: mutants = []
    if numCrossover>0: crossover = brkga.doCrossover(elite,nonelite,ro,numCrossover)
    else: crossover=[]
    population=elite + crossover + mutants
    i+=1
    print("Round: " + str(i)+ " - fit: "+ str(bestFit))
    
t_end = time.time()
t_exec = t_end - t_ini

population = decoder.decodeNoMultiprocessing(population, data)
bestIndividual = brkga.getBestFitness(population)

 #Print some results
print('Fitness: ' + str(bestIndividual['fitness']) + ' nNurses: ' + str(len(bestIndividual['solution'])))
print('Time solving: ' + str(t_exec) + ' sec')

plt.plot(evol)
plt.xlabel('number of generations')
plt.ylabel('Fitness of best individual')
plt.axis([0, len(evol), 0, 1+int(data['nNurses'])])
plt.show()
print("nNurses : " + str(bestIndividual['fitness']))

#Check all constrains
if Check.CheckDemand(bestIndividual['solution'],data['demand'])==False:
    print('//////////////########################## ERROR DEMAND ########################')
    
i = 1
for nurse in bestIndividual['solution']:
    if Check.CheckMaxConsecutiveHours(nurse['schedule'], data['maxConsec']) == False:
        print('//////////////########################## ERROR MAXCONSEC ########################')

    if Check.CheckMaxPresence(nurse['schedule'], data['maxPresence']) == False:
        print('//////////////########################## ERROR MAXPRESENCE ########################')

    if Check.CheckMinAndMaxHours(nurse['schedule'], data['minHours'], data['maxHours']) == False:
        print('//////////////########################## ERROR MINMAXHOURS ########################')

    if Check.CheckRest(nurse['schedule']) == False:
        print('//////////////######################### ERROR REST ########################')

    print('N' +str(i)+' ' + str(nurse['schedule']) + ' Hours:' + str(nurse['workingHours'])+ ' (' + str(nurse['ini']) +' to '+str(nurse['end'])+')')
    i+=1

