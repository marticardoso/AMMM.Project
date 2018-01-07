# File that run all 100 instances used to do the Heuristic analyisis

#Allows multiprocessing
from multiprocessing import freeze_support
if __name__ == '__main__':
    freeze_support()

    # imports
    import math
    import time
    import importlib
    import numpy as np
    import BRKGA as brkga # BRKGA framework (problem independent)
    import Utils.Checks as Check
    import Decoder as decoder # Dgcoder algorithm (problem-dependent)
    from CONFIGURATION import config # Configuration parameters (problem-dependent and execution-dependent)

    def import_instance(num):
        name = "Instances_Heur.py_instance" + str(num)
        m = importlib.import_module(name)
        return m.data


    print('Config: ' + str(config))

    # initializations
    numIndividuals=int(config['numIndividuals'])
    numElite=int(math.ceil(numIndividuals*config['eliteProp']))
    numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
    numCrossover=max(numIndividuals-numElite-numMutants,0)
    maxNumGen=int(config['maxNumGen'])
    ro=float(config['inheritanceProb'])

   
    maxTime = 120
    fitnessTime = [0]*maxTime


    t_init_global = time.time()

        
    fitnessSum = 0
    timeSum = 0
    for fileNum in range(0,100):
        print ""
        print('############################################')
        print('###### Instances_Heur.py_instance' + str(fileNum))
        data = import_instance(fileNum)
        chrLength=decoder.getChromosomeLength(data)

        # Main body
        population=brkga.initializePopulation(numIndividuals,chrLength)
        t_ini = time.time()
        lastTime = 0
        lastFitness = data['nNurses']+1
        timeEnd = False
        i = 1
        while (timeEnd == False):
            population = decoder.decode(population,data)
            bestFit = brkga.getBestFitness(population)['fitness']
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
            t_end = time.time()

            timeLapse = int(math.ceil(t_end - t_ini))

            for t in range(lastTime,min(timeLapse, maxTime)):
                fitnessTime[t] += lastFitness
            
            lastFitness = bestFit
            lastTime = timeLapse
            if(timeLapse >= maxTime):
                timeEnd = True
            
            
            print str(i) + "-"+ str(lastTime)+"("+str(bestFit)+")",
            i+=1

        t_end = time.time()
        t_int = t_end - t_ini
        
        ## Get the best
        population = decoder.decode(population, data)
        bestIndividual = brkga.getBestFitness(population)

        #Print some results
        print('       -Fitness: ' + str(bestIndividual['fitness'])  +'       -Time solving: ' + str(t_int) + ' sec')


        timeSum += t_int
        fitnessSum += bestIndividual['fitness']



        print("Summary: ")
        print("   - Fitness: " + str(fitnessTime))
        print("   - Fitness: " + str(np.array(fitnessTime)/float(fileNum+1.0)))


        

    t_end_global = time.time()
    t_int_global = t_end_global - t_init_global
    print("Fitness: " + str(fitnessTime))
    print('Global time: ' + str(t_int_global) + ' sec')


        