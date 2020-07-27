# AMMM Course Project #

Project of AMMM (Algorithmic Methods for Mathematical Models) - January 2017

### Problem statement

The problem studied in this work consists on designing the schedule of the nurses for a hospital. The number of
nurses to be assigned to work (or not) is nNurses and the number of hours of the schedule is nHours. For every
hour there is a demand of nurses that have to work that hour.
Every nurse must be assigned the hours that he/she works (if it is assigned to work) and the hours that he/she
is resting (hours where he/she is at the hospital but not working). However, these working hours must be assigned
taking into account the following constraints:
- Each nurse must work between minHours and maxHours (if he/she works)
- A nurse only can stay at the hospital at most maxPresence hours.
- A nurse can only work maxConsecutive consecutive hours at most.
- A nurse cannot rest two or more hours consecutively.
- The demand must be satisfied.

The objective is to minimize the total number of working nurses.

The problem is solved using integer linear programming and meta-heuristics (BRKGA & GRASP).

## Content:

### ILM ##
The folder CPLEX-AMMM/ is the main folder of the CPLEX project that contains the model that solves the problem. 
The project contains two exec config: 
    - RunOne: It runs only one instance.
    - RunAll: It runs the 20 instances used to do the report and it checks all constraints.

### BRKGA ##
The folder BRKGA/ contains the python project that implements the BRKGA. 
You can run three different files:
    - main_runSingle.py: It runs one instance.
    - main_runAll_OPL.py: It runs the 20 instances used to do the report (ILM vs Heuristic analysis).
    - main_runAll_Heur.py: It runs the 100 instances used to do the report (Heuristic analysis).

### GRASP ##
The folder GRASP/ contains the python project that implements the GRASP. 
You can run three different files:
    - main_runSingle.py: It runs one instance.
    - main_runAll_OPL.py: It runs the 20 instances used to do the report (ILM vs Heuristic analysis).
    - main_runAll_Heur.py: It runs the 100 instances used to do the report (Heuristic analysis).

### Intance generator ##
The folder InstanceGenerator/ contains the python project that implements the instance generator.
If you run the main.py file it will generate the .dat files inside the /CPLEX_Instances and the .py files inside /Python_Instance.

### Instances ##
The folder Instances/ contains the instances used to do the report.
