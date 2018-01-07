## AMMM Course Project ##
Project of AMMM (Algorithmic Methods for Mathematical Models)

Authors:
    -Martí Cardoso Sabé 
    -Albert Garriga Porqueras

January 2017

Content:
# ILM #
The folder CPLEX-AMMM/ is the main folder of the CPLEX project that contains the model that solves the problem. 
The project contains two exec config: 
    - RunOne: It runs only one instance.
    - RunAll: It runs the 20 instances used to do the report and it checks all constraints.

# BRKGA #
The folder BRKGA/ contains the python project that implements the BRKGA. 
You can run three different files:
    - main_runSingle.py: It runs one instance.
    - main_runAll_OPL.py: It runs the 20 instances used to do the report (ILM vs Heuristic analysis).
    - main_runAll_Heur.py: It runs the 100 instances used to do the report (Heuristic analysis).

# GRASP #
The folder GRASP/ contains the python project that implements the GRASP. 
You can run three different files:
    - main_runSingle.py: It runs one instance.
    - main_runAll_OPL.py: It runs the 20 instances used to do the report (ILM vs Heuristic analysis).
    - main_runAll_Heur.py: It runs the 100 instances used to do the report (Heuristic analysis).

# Intance generator #
The folder InstanceGenerator/ contains the python project that implements the instance generator.
If you run the main.py file it will generate the .dat files inside the /CPLEX_Instances and the .py files inside /Python_Instance.

# Instances #
The folder Instances/ contains the instances used to do the report.