/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Albert
 * Creation Date: 29/11/2017 at 12.24.49
 *********************************************/
int nNurses = ...;
int minHours = ...;
int maxHours = ...;
int maxConsec = ...;
int maxPresence = ...;
int nHours = ...;

range N = 1..nNurses;
range H = 1..nHours;
range H_1 = 1..(nHours-1);
int demand[h in H] = ...;

int M = nHours;
//decision variables
dvar boolean x_i[i in N];			//nurse i works or not
dvar boolean x_ih[i in N, h in H];	//nurse i works at hour h
dvar boolean wb_ih[i in N, h in H];	//nurse i works before hour h
dvar boolean wa_ih[i in N, h in H];	//nurse i works after hour h
dvar boolean r_ih[i in N, h in H];	//hurse i rests at hour h

//objective
minimize sum(i in N) x_i[i];

//constraints
subject to{
//constraint 1 (work at least minHours if works)
forall(i in N)
  sum(h in H) x_ih[i,h] >= minHours*x_i[i];
  
//constraint 2 (works at most maxHours)
forall(i in N)
  sum(h in H) x_ih[i,h] <= maxHours*x_i[i];
  
//constraint 3 (works at most maxConsecutive)
forall(i in N, t in 1..(nHours-maxConsec))
  sum(h in t..(t+maxConsec)) x_ih[i,h] <= maxConsec;
  
//constraint 4 (stays at most maxPresence)
forall(i in N, h in 1..nHours-maxPresence, h2 in h+maxPresence..nHours)
  (1-x_ih[i,h]) >= x_ih[i,h2];
  
//constraint 5 (not two consecutive rest)
forall(i in N, h in H_1)
	r_ih[i,h] + r_ih[i,h+1] <= 1;
	
//constraint 6 (satisfy demand)
forall(h in H)
  sum(i in N) x_ih[i,h] >= demand[h];
  
//constraint 7 (relations x_i and x_ih)
forall(i in N)
  nHours*x_i[i] >= sum(h in H) x_ih[i,h];
  
//constraints 8 and 9 (definition of r_ih)
forall(i in N, h in H)
  2 + r_ih[i,h] >= wb_ih[i,h] + wa_ih[i,h] + 1-x_ih[i,h];
forall(i in N, h in H)
  3*r_ih[i,h] <= wb_ih[i,h] + wa_ih[i,h] + 1-x_ih[i,h];
  
//constraints 10 and 11 (definition of wb_ih)
forall(i in N, h in H)
  wb_ih[i,h] <= sum(t in 1..(h-1)) x_ih[i,t];
forall(i in N, h in H)
  M*wb_ih[i,h] >= sum(t in 1..(h-1)) x_ih[i,t];		
  
//constraints 12 and 13 (definition of wa_ih)
forall(i in N, h in H)	//possible error fora dels limits del vector
  wa_ih[i,h] <= sum(t in (h+1)..nHours) x_ih[i,t];
forall(i in N, h in H) 
  M*wa_ih[i,h] >= sum(t in (h+1)..nHours) x_ih[i,t];
}

//postprocessing
/**execute{
	write("N \t")
	for (var h=1; h<= hours; h++)
   		write("\t" + h+ "\t");
   	writeln();
   	for (var i=1;i<=Nurses;i++) {
   		if(x_i[i] == 1) {	
   			write(i + "\t");
   			for(var h=1; h <= hours; h++) {
   				var s = "0";
   				if (x_ih[i][h] == 1)
   					s = "w";   			
   				else if (r_ih[i][h] == 1)
   					s = "r";
   			write("\t" + s + "\t");
			}
			writeln();
 		}			 	  
   }
}*/