
main {
	//ERROR WHEN FILE NOT FOUND
	for(var i=1; i <= 20; i++){
		//Test file
		var sourceFile = "cplex_instance" + i +".dat"
		writeln("-------------------------------")
	 	writeln("------"+sourceFile + "------")
	 	writeln("-------------------------------")
	 	writeln("   - Init Time: " + new Date() )
	 	//Initialization
		var src = new IloOplModelSource("model.mod");
	 	var def = new IloOplModelDefinition(src);
	 	var cplex = new IloCplex();
		cplex.epgap=0.01;
		cplex.tilim= 60*60*1 +60; //Max 1 hours
		var model = new IloOplModel(def,cplex);
	 	var data = new IloOplDataSource("Instances/"+sourceFile);
	 	
	 	model.addDataSource(data);
	 	
	 	//Generate model
	 	var start = new Date();
	 	model.generate();
	 	var end = new Date();
	 	var generateTime = (end.getTime()-start.getTime())/1000.;
	 	
	 	
	 	//Solve model
		var start2 = new Date();
	 	var hasSolution = cplex.solve();
	 	var end2 = new Date();
	 	var solveTime = (end2.getTime()-start2.getTime())/1000.
		
	 	if (!hasSolution) {
	 		writeln("  NO! solution found");
	 			
	 		
	 	}
	 	else {
	 		writeln("  Solution found ")	 	
	 		writeln("  Cost " + cplex.getObjValue() + "");
	 		
	 		//Check valid objective function
	 		var workingNurses = 0;
	 		for(var j = 1; j <= model.nNurses; ++j){
	 			if(model.x_i[j]==1)
	 				workingNurses +=1;	 		
	 		}
	 		var validObjFunc = (workingNurses == cplex.getObjValue())
	 		writeln("  Correct obj func: " + validObjFunc);
	 		if(!validObjFunc) writeln("/////////////////ERROR////////////////////")
	 		
	 		//Check the 5 constrains
	 		var validMinH = true;
	 		var validMaxH = true;
	 		var validConsec = true;
	 		var validMaxPresence = true;
	 		var validRest = true;
	 		var validDemand = true;
	 		for(var j = 1; j <= model.nNurses; ++j){
	 			 if(model.x_i[j]==1){ //If works
	 			 	
	 			 	//Total hours
	 			 	var nHours = 0;
	 			 	//Ini hour
	 			 	var iniH = 0;
	 			 	var firstH = true;
	 			 	
	 			 	//Consec hours
	 			 	var consec = 0;
	 			 	//Check rest
	 			 	var consecNoWork = 0;
	 			 	for(var k=1; k<=model.nHours; ++k){
	 			 		if(model.x_ih[j][k]==1){
	 			 			nHours +=1;	
	 			 			consec += 1;
	 			 			if(firstH) {
	 			 				 iniH = k;
	 			 				 firstH = false;
	 			 				 consecNoWork = 0;			 			
	 			 			}	 			 		
	 			 			if(k-iniH+1 > model.maxPresence) validMaxPresence = false;
	 			 			if(consec > model.maxConsec) validConsec = false;
	 			 			if(consecNoWork>1) validRest = false;
	 			 			consecNoWork = 0;	
       					}
       					else{
       						consec = 0; 
       						consecNoWork +=1;      					
       					}	 			 				 	
	 			 	}
	 			 	if(model.minHours > nHours)	validMinH = false;	 			 	
	 			 	if(model.maxHours < nHours)	validMaxH = false;
	 			 	
	 			 }	 			
	 		}
			for(var h = 1; h<= model.nHours;++h){
				var nursesHour = 0;
				for(var j = 1; j <= model.nNurses; ++j){
					if(model.x_ih[j][h]==1) nursesHour +=1;
				}
				if(model.demand[h]> nursesHour) validDemand = false;			
			}
	 		writeln("  Conditions: [" + validMinH + ", "+ validMaxH + ", "+ validMaxPresence+  ", "+ validConsec+ ", "+ validRest+ ", "+ validDemand +"]");
	 		if(!validMinH || !validMaxH || !validMaxPresence || !validConsec || !validRest|| !validDemand) 
	 			writeln("/////////////////////////////////ERROR/////////////////////////////////////")
	 	}
	 	writeln("  Problem generated in " + generateTime + " seconds");
	 	writeln("  Problem solved in " + solveTime + " seconds");
	 	if(solveTime>60*60*1){
	 		writeln("######################################################### ERROR stopped by the program")	 	
	 	}
	 	else if(solveTime>60*7){
	 		writeln("######################################################### More than 7 min")	 	
	 	}
		model.end();
	 	data.end();
	 	def.end();
	 	cplex.end();
	 	src.end();
	 	writeln("")
	}
	 
 
 
};