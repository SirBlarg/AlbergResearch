import random
import numpy as np
import scipy
import matplotlib.pyplot as plt

f_g_qq = [0.001,0.01,0.1,1,10,100,1000] #List of ratios of gluon to quark antiquartk splitting
f_g_gg = [0.001,0.01,0.1,1,10,100,1000] #List of ratios of gluon to gluon gluon splitting
print('please enter desired number of itterations')
itterations = int(raw_input()) #Get the number of steps from user input
print('Please enter the number of desired trials')
trials = int(raw_input()) #Get the number of trials from user input
print('Please enter the probability of staying in a given state')
transition = 1 - float(raw_input())


#Defining Data table
data = [ [ [ [0 for x4 in range(trials)] for x3 in range(itterations)] for x2 in range(len(f_g_gg))] for x1 in range(len(f_g_qq)) ]
#Data is stored as [gluon quark antiquark splitting][gluon to gluon gluon splitting][itteration number][trial number]

#MonteCarlo Simulation
for l in range(trials):
	for i in range(len(f_g_qq)):
		for j in range(len(f_g_gg)):
			state = [0,0,0]
			for k in range(itterations):
				ubar = state[0]
				dbar = state[1]
				g = state[2]
				Np = 3 + 2*ubar + 2*dbar
				nssp_k_k1 =Np * 1 #Because we normalized f_q_qg
				nssp_i1_k1 = g * f_g_qq[i] #Probability of a gluon becoming a u ubar pair
				nssp_j1_k1 = nssp_i1_k1 #Probability of a gluon becoming a d dbar pair
				nssp_g_gg = g * f_g_gg[j] #Probability of a gluon splitting into two gluons
				nssp_gg_g = Np * g  + .5* g * (g-1)*f_g_gg[j] #Probability of two gluons contracting into one. Note f_q_qg is unitary
				nssp_k1_i1 = (ubar+2)*ubar*f_g_qq[i] #Probability of a u ubar pair anihilating and becoming a gluon
				nssp_k1_j1 = (dbar+1)*dbar*f_g_qq[i] #Probability of a d dbar pair anihilating and becoming a gluon		
				C_0 = (nssp_k_k1 + nssp_i1_k1 + nssp_j1_k1 + nssp_g_gg + nssp_gg_g + nssp_k1_i1 + nssp_k1_j1)*transition #Computing Normalization Constant
			
				p_k_k1 = nssp_k_k1 / C_0 #Normalizing all processes
				p_i1_k1 = nssp_i1_k1 / C_0
				p_j1_k1 = nssp_j1_k1 / C_0
				p_g_gg = nssp_g_gg / C_0
				p_gg_g = nssp_gg_g / C_0
				p_k1_i1 = nssp_k1_i1 / C_0
				p_k1_j1 = nssp_k1_j1 / C_0
	
				nr_k_k1 = p_k_k1 #Setting Intervals on (0,1) that are proportional to probabilities
				nr_i1_k1 = nr_k_k1 + p_i1_k1 #e.g. nr_i1_k1 will take anything between nr_k_k1 and its own 	value.
				nr_j1_k1 = nr_i1_k1 + p_j1_k1 #Setting up intervals for dart method
				nr_g_gg = nr_j1_k1 + p_g_gg
				nr_gg_g = nr_g_gg + p_gg_g
				nr_k1_i1 = nr_gg_g + p_k1_i1
				nr_k1_j1 = nr_k1_i1 + p_k1_j1
				
				dart = random.random()
			
				if dart < nr_k_k1:			#We through a dart at the interval (0,1)
					state[2] = state[2]+1		#where falling on a certain part of the
				elif dart < nr_i1_k1:			#numberline indicates a certain transition.
					state[0] = state[0] + 1		#The width of each section is weighted by
					state[2] = state[2] - 1		#ssp, or state shift probability.
				elif dart < nr_j1_k1:
					state[1] = state[1] + 1
					state[2] = state[2] - 1
				elif dart < nr_g_gg:
					state[2] = state[2] + 1
				elif dart < nr_gg_g:
					state[2] = state[2] - 1
				elif dart < nr_k1_i1:
					state[0] = state[0] - 1
					state[2] = state[2] + 1
				elif dart < nr_k1_j1:
					state[1] = state[1] - 1
					state[2] = state[2] + 1
				data[i][j][k][l] = state		#Stroing the state information for the given frequency ratio
									#itteration number, and trial number accordingly.
	#End MonteCarlo Simulation

	#Now lets get some summary statistics!

	#Expectation value for ubar and dbar(average number of ubars and dbars)
	#We evaluate this using the last trial, and average it over all trials
mean_ubar = [[0 for x2 in range(len(f_g_gg))] for x1 in range(len(f_g_qq))] #Initializing lists
mean_dbar = [[0 for x2 in range(len(f_g_gg))] for x1 in range(len(f_g_qq))]
mean_data = [[0 for x2 in range(len(f_g_gg))] for x1 in range(len(f_g_qq))]
dmu = [[0 for x2 in range(len(f_g_gg))] for x1 in range(len(f_g_qq))]
dqu = [[0 for x2 in range(len(f_g_gg))] for x1 in range(len(f_g_qq))]
for i in range(len(f_g_qq)): #Itterating through all ratio configurations
	for j in range(len(f_g_gg)):
		mean_data[i][j] = map(sum,zip(*data[i][j][itterations-1])) #Creating an array of the sum of states of all trials in the i,j ratio configuration
		mean_data[i][j] = map(lambda x: float(x)/float(trials), mean_data[i][j]) #Dividing by the number of trials to attain averages
		mean_ubar[i][j] = mean_data[i][j][0]	#Pulling out average ubar into simple array
		mean_dbar[i][j] = mean_data[i][j][1]
		dmu[i][j] = (mean_dbar[i][j] - mean_ubar[i][j])*100 #Getting ubar dbar difference * 100
		#print mean_dbar[i][j], mean_ubar[i][j]
		#dqu[i][j] = mean_dbar[i][j] / mean_ubar[i][j]
print('\n'.join(['	'.join(['{:4}'.format(item) for item in row])  #Printing the array
      for row in dmu]))



