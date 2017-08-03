import numpy as np
import csv
import glob
import os
import re



""" 	This file takes in an input of the csv files created by history.gen
	and processes the data. It outputs to a csv file, summary.csv
	that gives the probability of state in each configuration in a 10x10x10 array
	and also includes the expectation values for ubar, dbar, and glueons in each model.
"""

""" We are reading in all of the history files in a for loop and storing them in a dictionary datadict"""

histcsv = glob.glob(os.getcwd() + '/history*.csv') #generate a list of all directories of the form ./history*.csv
datadict = {}	#declare an empty dictionary to append things onto as we go along
for filename in histcsv: #itterate through the files

	with open(filename) as history: #open given file, it is refrered to as history
		raw_history = [[int(x) for x in rec] for rec in csv.reader(history, delimiter = ',')] #storing the history file into a 2D array
		#raw_history = np.delete(raw_history, (0), axis = 0) #getting rid of header row
	data = [[[0 for x1 in range(3)] for x2 in range(len(raw_history[0])/3)] for x3 in range(len(raw_history))] # Declaring a 3D array [trial][itteration][parton]
	
	for i in range(len(raw_history)):  #itterate through the entries of the 2D array
		for j in range(len(raw_history[0])): 
			if (j % 3) == 0: #Grabbing every thrird entry starting with the first (ubar values)			
				data[i][j/3][0] = raw_history[i][j]
			elif (j % 3) == 1: #Grabbing every thrird entry starting with the second (dbar values)
				data[i][(j-1)/3][1] = raw_history[i][j]
			else:		#Grabbing every thrird entry starting with the third (gluon values)
				data[i][(j-2)/3][2] = raw_history[i][j]
	
	datadict[filename.replace('history_', '').replace('.csv', '').replace((os.getcwd() + "/"), '')] = data #storing the data into a dictionary file that identifies model parameters with the array of states

''' The file has been put into the running code, now we are going to create lists that contain the model parameters as discerned by the file names. This will allow us to itterate easily through model parameters'''

f_qq_gg = [] #empty list that will contain the file names
f_qq = [] #empty list that will contain the f_g_qq values
f_gg = [] #empty list that will contain the f_g_gg values
i = 0 #itterative variable
for files in datadict.keys(): #itterate through all the dictionaries we have
	f_qq_gg.append(files.split('_')) #Generate list of tuples of data
	f_qq_gg[i][0] = float(f_qq_gg[i][0]) #Convert to float for increased precision
	f_qq_gg[i][1] = float(f_qq_gg[i][1]) #i.bid
	if f_qq_gg[i][0] not in f_qq:	 #Check to see if entry is in f_qq
		f_qq.append(f_qq_gg[i][0])
	if f_qq_gg[i][1] not in f_gg:
		f_gg.append(f_qq_gg[i][1])
	i += 1

f_qq = sorted(f_qq)
f_gg = sorted(f_gg)

''' \preprocessing. Now, we are going to process the data that we have loaded into Python'''

''' The first step is to generate a dictionary of expectation values for the various model parameters'''

expectation_vals = {} #Create empty dictionary
stdevs = {}
asymstd = {}
asyml = [[0 for x1 in range(len(datadict["1._1."]))] for x2 in range(len(datadict['1._1.']))]
for qq in f_qq: 	#itterate through a model parameter
	if qq >= 1 or qq == 0:
		qqs = str(qq).replace('.0', '.') #generate the string that is associated for interatction with datadict
	else:
		qqs = str(qq)
	
	for gg in f_gg: #Same
		if gg >= 1 or gg == 0:
			ggs = str(gg).replace('.0', '.')
		else:
			ggs = str(gg)
		#datadict[(qqs + '_' + ggs)]
		expectation_vals[qqs + "_" + ggs] = np.mean(datadict[(qqs + '_' + ggs)], axis = (0,1)) #Assign the 3-tuple of expectation values to the appropriate dictionary
		stdevs[qqs + "_" + ggs] = np.std(datadict[qqs+'_'+ggs], axis = (0,1))
		for k in range(len(datadict[qqs+'_'+ggs])):
			for j in range(len(datadict[qqs+'_'+ggs])):
				asyml[k][j] = datadict[qqs+'_'+ggs][k][j][1] - datadict[qqs+'_'+ggs][k][j][0]
		asymstd[qqs+'_'+ggs] = np.std(asyml)
"""This section calculates probability tensors for the various configurations"""

prob_tensor = {}

for qq in f_qq:
	if qq >= 1 or qq == 0:
		qqs = str(qq).replace('.0', '.')
	else:
		qqs = str(qq)
	for gg in f_gg:
		if gg >= 1 or gg == 0:
			ggs = str(gg).replace('.0', '.')
		else:
			ggs = str(gg)
		
		tensor = [[[float(0) for x in range(10)] for x in range(10)] for x in range(10)]
		sum_count = float(0)
		for i in range(10):
			for j in range(10):
				for k in range(10):
					for a in range(len(datadict[qqs+ "_" + ggs])):
						tensor[i][j][k] += datadict[qqs + '_' + ggs][a].count([i,j,k])
						sum_count += datadict[qqs + '_' + ggs][a].count([i,j,k])
		tensor = np.array(tensor) / sum_count
		prob_tensor[qqs+'_'+ggs] = tensor
"""Now for the fun part! The output file!!!!!!!!!!!!!!!"""

with open('expectationvals.csv', 'wb') as expect:
	expect.write('ubar,')	
	for gg in f_gg:
		expect.write(str(gg) + ',,')
	expect.write("\n")	
	for qq in f_qq:
		if qq >= 1 or qq == 0:
			qqs = str(qq).replace('.0', '.')
		else:
			qqs = str(qq)

		expect.write(str(qq) + ',')

		for gg in f_gg:
			if gg >= 1 or gg == 0:
				ggs = str(gg).replace('.0', '.')
			else:
				ggs = str(gg)			
			
			expect.write(str(expectation_vals[qqs + '_' + ggs][0]) + ',+/-' + str(stdevs[qqs+'_'+ggs][0]) + ',')

		expect.write("\n")
	expect.write("dbar")
	expect.write("\n")
	for qq in f_qq:
		if qq >= 1 or qq == 0:
			qqs = str(qq).replace('.0', '.')
		else:
			qqs = str(qq)

		expect.write(str(qq) + ',')

		for gg in f_gg:
			if gg >= 1 or gg == 0:
				ggs = str(gg).replace('.0', '.')
			else:
				ggs = str(gg)			
			
			expect.write(str(expectation_vals[qqs + '_' + ggs][1]) + ',+/-' + str(stdevs[qqs+'_'+ggs][1]) + ',')

		expect.write("\n")
	expect.write("gluons")
	expect.write("\n")
	for qq in f_qq:
		if qq >= 1 or qq == 0:
			qqs = str(qq).replace('.0', '.')
		else:
			qqs = str(qq)

		expect.write(str(qq) + ',')

		for gg in f_gg:
			if gg >= 1 or gg == 0:
				ggs = str(gg).replace('.0', '.')
			else:
				ggs = str(gg)			
			
			expect.write(str(expectation_vals[qqs + '_' + ggs][2])+ ',+/-' + str(stdevs[qqs+'_'+ggs][2])  + ',')

		expect.write("\n")
	expect.write("dbar - ubar")
	expect.write("\n")
	for qq in f_qq:
		if qq >= 1 or qq == 0:
			qqs = str(qq).replace('.0', '.')
		else:
			qqs = str(qq)

		expect.write(str(qq) + ',')

		for gg in f_gg:
			if gg >= 1 or gg == 0:
				ggs = str(gg).replace('.0', '.')
			else:
				ggs = str(gg)			
			
			expect.write(str(expectation_vals[qqs + '_' + ggs][1] - expectation_vals[qqs + '_' + ggs][0] ) + ',+/-' + str(asymstd[qqs+'_'+ggs]) + ',')

		expect.write("\n")
	expect.write("dbar/ubar")
	expect.write("\n")
	for qq in f_qq:
		if qq >= 1 or qq == 0:
			qqs = str(qq).replace('.0', '.')
		else:
			qqs = str(qq)

		expect.write(str(qq) + ',')

		for gg in f_gg:
			if gg >= 1 or gg == 0:
				ggs = str(gg).replace('.0', '.')
			else:
				ggs = str(gg)			
			
			expect.write(str(np.float64(expectation_vals[qqs + '_' + ggs][1]) / expectation_vals[qqs + '_' + ggs][0] ) + ',')

		expect.write("\n")

with open('probdistro.csv', 'wb') as prob:
	for gg in f_gg:
		prob.write(str(gg))
		prob.write(",,,,,,,,,,,,,")
	prob.write('\n')
	prob.write(',,')	
	for gg in f_gg:
		for k in range(10):
			prob.write(str(k+1))
			prob.write(",")
		prob.write(",,,")
	prob.write("\n")
	for qq in f_qq:
		if qq >= 1 or qq == 0:
			qqs = str(qq).replace('.0', '.')
		else:
			qqs = str(qq)
		for i in range(10):
			for j in range(i+1):
				for gg in f_gg:
					if gg >= 1 or gg == 0:
						ggs = str(gg).replace('.0', '.')
					else:
						ggs = str(gg)	
					for k in range(10):
						if k == 0:
							prob.write(str(i) + ',' + str(j)+',')
						prob.write(str(prob_tensor[qqs + '_' + ggs][i][j][k]) + ',')
					prob.write(',')
				prob.write('\n')
		prob.write('\n')

