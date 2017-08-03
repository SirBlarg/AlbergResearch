import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as color
from Tkinter import Tk
from tkFileDialog import askopenfilename

def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return float(r)/255, float(g)/255, float(b)/255, 1

filename = askopenfilename()

with open(filename) as history:
	raw_history = [[int(x) for x in rec] for rec in csv.reader(history, delimiter = ',')]
	raw_history = np.delete(raw_history, (0), axis = 0)
data = [[[0 for x1 in range(3)] for x2 in range(len(raw_history[0])/3)] for x3 in range(len(raw_history))]
#print len(raw_history)
for i in range(len(raw_history)):
	for j in range(len(raw_history[0])):
		if (j % 3) == 0:
			data[i][j/3][0] = raw_history[i][j]
		elif (j % 3) == 1:
			data[i][(j-1)/3][1] = raw_history[i][j]
		else:
			data[i][(j-2)/3][2] = raw_history[i][j]
vertex_count = {}
"""for i in range(len(data)):
	for j in range(len(data[0])):
		if str(data[i][j]) in vertex_count.keys():
			vertex_count[str(data[i][j])] += 1
		else:
			vertex_count[str(data[i][j])] = 1
print vertex_count						This is for looking at all trials"""
verticies = []
#Now we are just going to look at the 0 trial
for i in range(len(data[0])):
	if str(data[0][i]) in vertex_count.keys():
		vertex_count[str(data[0][i])] += 1
	else:
		vertex_count[str(data[0][i])] = 1
		verticies.append(data[0][i])
edgy_edges = []
edges = []

for i in range(len(data[0])-1):
	if (data[0][i][0] > data[0][i+1][0]):
		edge = [data[0][i],data[0][i+1]]
		edges.append(edge)
	elif data[0][i][0] < data[0][i+1][0]:
		edge = [data[0][i+1],data[0][i]]
		edges.append(edge)
	elif data[0][i][1] > data[0][i+1][1]:
		edge = [data[0][i],data[0][i+1]]
		edges.append(edge)
	elif data[0][i][1] < data[0][i+1][1]:
		edge = [data[0][i+1],data[0][i]]
		edges.append(edge)
	elif data[0][i][2] > data[0][i+1][2]:
		edge = [data[0][i],data[0][i+1]]
		edges.append(edge)
	elif data[0][i][2] < data[0][i+1][2]:
		edge = [data[0][i+1],data[0][i]]
		edges.append(edge)
	if edge not in edgy_edges:
		edgy_edges.append(edge)
edgy_colors = []
for item in edgy_edges:
	edgy_colors.append(np.log(edges.count(item)))

ubar = []
dbar = []
glue = []
for i in range(len(verticies)):
	ubar.append(verticies[i][0])
	dbar.append(verticies[i][1])
	glue.append(verticies[i][2])
#Axes3D.scatter(xs, ys, zs=0, zdir='z', s=20, c=None, depthshade=True, *args, **kwargs)
vertex_color = []
for i in range(len(verticies)):
	vertex_color.append(vertex_count[str(verticies[i])])
heat_min = min(edgy_colors)
heat_max = max(edgy_colors)
for i in range(len(edgy_colors)):
	edgy_colors[i] = rgb(heat_min, heat_max, edgy_colors[i])
	#edgy_colors[i] = float(edgy_colors[i])/float(heat_max)
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(ubar,dbar,glue, s = 500, c = vertex_color, depthshade = False)
for i in range(len(edgy_edges)):
	ax.plot([edgy_edges[i][0][0],edgy_edges[i][1][0]],[edgy_edges[i][0][1],edgy_edges[i][1][1]],([edgy_edges[i][0][2],edgy_edges[i][1][2]]), c = (edgy_colors[i]), linewidth = 5)
plt.show()

		


