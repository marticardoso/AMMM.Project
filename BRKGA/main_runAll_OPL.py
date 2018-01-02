#Allows multiprocessing
from multiprocessing import freeze_support
if __name__ == '__main__':
    freeze_support()

    # imports
    import math
    import time
    import datetime
    import importlib
    import BRKGA as brkga # BRKGA framework (problem independent)
    import Utils.Checks as Check
    import Decoder as decoder # Dgcoder algorithm (problem-dependent)
    from CONFIGURATION import config # Configuration parameters (problem-dependent and execution-dependent)
    from pandas import *

    def import_instance(num):
        name = "Instances_OPL.py_instance" + str(num)
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

    for i in range(1,20+1):
        print('##############################################')
        print('###### Instances_OPL.py_instance' + str(i)+ ' #########')
        print('##############################################')
        data = import_instance(i)
        print('Data: ' +str(data))
        chrLength=decoder.getChromosomeLength(data)

        # Main body
        population=brkga.initializePopulation(numIndividuals,chrLength)
        t_ini = time.time()
        i=0
        while (i<maxNumGen):
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
            i+=1
            print str(i) +"("+str(bestFit)+")",
        
        t_end = time.time()

        t_int = t_end - t_ini

        ## Get the best
        population = decoder.decode(population, data)
        bestIndividual = brkga.getBestFitness(population)

        #Print some results
        print('Fitness: ' + str(bestIndividual['fitness']) + ' nNurses: ' + str(len(bestIndividual['solution'])))
        print('Time solving: ' + str(t_int) + ' sec')

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
                print('//////////////########################## ERROR REST ########################')

            #print('N:' +str(i)+' ' + str(nurse['schedule']) + ' Hours:' + str(nurse['workingHours'])+ ' (' + str(nurse['ini']) +' to '+str(nurse['end'])+')')
            i+=1

