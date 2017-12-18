# imports
import math
import matplotlib.pyplot as plt
import time
import datetime
import BRKGA as brkga # BRKGA framework (problem independent)
import Decoders.DECODER_2_1 as decoder # Dgcoder algorithm (problem-dependent)
from Python_Instances.factible_instance2 import data # Input data (problem-dependent and instance-dependent)
from CONFIGURATION import config # Configuration parameters (problem-dependent and execution-dependent)
from pandas import *

print(config)
# initializations
numIndividuals=int(config['numIndividuals'])
numElite=int(math.ceil(numIndividuals*config['eliteProp']))
numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
numCrossover=max(numIndividuals-numElite-numMutants,0)
maxNumGen=int(config['maxNumGen'])
ro=float(config['inheritanceProb'])
evol=[]

chrLength=decoder.getChromosomeLength(data)

# Main body

population=brkga.initializePopulation(numIndividuals,chrLength)
t_ini = time.time()
i=0
while (i<maxNumGen):
    population = decoder.decode(population,data)
    evol.append(brkga.getBestFitness(population)['fitness'])
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
    print(i)
t_end = time.time()

t_int = t_end - t_ini
print(t_int)


population = decoder.decode(population, data)
bestIndividual = brkga.getBestFitness(population)
plt.plot(evol)
plt.xlabel('number of generations')
plt.ylabel('Fitness of best individual')
plt.axis([0, len(evol), 0, 1+int(data['nNurses'])])
plt.show()
print("nNurses : " + str(bestIndividual['fitness']))
print(DataFrame(bestIndividual['solution']))