import random
import numpy as np
import math
from matplotlib import colors
import networkx as nx
import matplotlib.pyplot as plt
import imageio
from copy import deepcopy
from PIL import Image





def closest_node(point, G):
    nodes=G.nodes
    nodes = np.asarray(nodes)
    deltas = nodes - np.asarray(point)
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    k=np.argmin(dist_2)
    return nodes[k]

def randomCellGen(grid,start,goal):
	x=int(random.uniform(0,len(grid)-1))
	y=int(random.uniform(0,len(grid[0])-1))
	return [x,y]


def isFree(G1,grid,point,color="black",d=4 ):	
	parent={}
	closest=closest_node(point, G1)
	#if grid[point[0]][point[1]]==0 :
	Vector=point-closest
	bound=random.randint(1,d)
	step_x=[0 if Vector[0]==0 else int(abs(Vector[0])/Vector[0])   ]
	step_y=[0 if Vector[1]==0 else int(abs(Vector[1])/Vector[1])   ]
	diagonal_stpsNum=min(abs(Vector[0]),abs(Vector[1]))
	nondiagonal_stpsNum=max(abs(Vector[0]),abs(Vector[1]))-min(abs(Vector[0]),abs(Vector[1]))
	steps_x=step_x*diagonal_stpsNum + [0 if abs(Vector[0]) < abs(Vector[1]) else step_x[0] ]* nondiagonal_stpsNum
	steps_y=step_y*diagonal_stpsNum + [0 if abs(Vector[1]) < abs(Vector[0]) else step_y[0] ]* nondiagonal_stpsNum
	steps_x=steps_x[:bound]
	steps_y=steps_y[:bound]
	G=nx.Graph()
	#G.add_node(tuple(point))
	tracker=np.array(closest.copy())
	for i in range(0,len(steps_x)):	
		old_tracker=tracker.copy()
		tracker= old_tracker+ np.array([steps_x[i],steps_y[i] ])
		parent[tuple(tracker)]=tuple(old_tracker)
		if grid[tracker[0]][tracker[1]] ==1:
			return [False,[],parent]
		if i >0:
			G.add_node(tuple(tracker))
			G.add_edge(tuple(old_tracker),tuple(tracker))
		else:
			G.add_edge(tuple(old_tracker),tuple(tracker))
			
	return [True,G, parent, tuple(tracker)] 

		


		
		
def plotting(grid,start,goal ,path=[]):
	
	grid_copy=deepcopy(grid)
	grid_copy[start[0]][start[1]]= -1;grid_copy[goal[0]][goal[1]]=5;
	for P in path[1:-1]:
		grid_copy[P[0]][P[1]]=3
	# create discrete colormap
	cmap = colors.ListedColormap(['brown', 'yellow','black','blue','green'])
	bounds=[-2,-0.5,0.5,1.5,3.5,6]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	fig, ax = plt.subplots()
	ax.imshow(grid_copy, cmap=cmap, norm=norm)
	# draw gridlines
	ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
	ax.set_xticks(np.arange(-.5, len(grid_copy[0]), 3));
	ax.set_yticks(np.arange(-.5, len(grid_copy), 3));
	plt.show()



def animate_plotting(grid,start,goal, path,i,color="gray",diric=""):
	for P in path:
		grid[P[0]][P[1]]=3
	# create discrete colormap
	grid[start[0]][start[1]]= -1;grid[goal[0]][goal[1]]=5;
	cmap = colors.ListedColormap(['brown', 'yellow','black',color,'green'])
	bounds=[-2,-0.5,0.5,1.5,3.5,6]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	fig1, ax1 = plt.subplots()
	ax1.imshow(deepcopy(grid), cmap=cmap, norm=norm)
	# draw gridlines
	ax1.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
	ax1.set_xticks(np.arange(-.5, len(grid[0]), 3));
	ax1.set_yticks(np.arange(-.5, len(grid), 3));
	plt.savefig(diric+"img"+str(i)+".png")
	cmap = colors.ListedColormap(['brown', 'yellow','black','yellow','green'])
	ax1.imshow(deepcopy(grid), cmap=cmap, norm=norm)
	plt.close(fig1)
	

def algo_animation(grid, start,goal,path,ind,diric=""):
	with imageio.get_writer('movie.gif', mode='I',duration=0.2) as writer:
		for filename in [diric+"img"+str(i)+".png" for i in range(ind-3)]:
			image = imageio.imread(filename)
			writer.append_data(image)
		for i in range(100):
			image = imageio.imread(diric+"img"+str(ind-1)+".png")
			writer.append_data(image)	
    	
  
    

    

def myPathPlanning(grid, start,goal,d=4,anim=False,diric=""):
	Flage=False
	G_start = nx.Graph()
	G_start.add_node(tuple(start))
	parents_start={tuple(start):"None"}
	G_goal = nx.Graph()
	G_goal.add_node(tuple(goal))
	parents_goal={tuple(goal):"None"}
	if anim ==True: ind=0;
	while not Flage:
		new_point=randomCellGen(grid,start,goal)
		Freeness_start=isFree(G_start,grid,new_point,d)
		Freeness_goal=isFree(G_goal,grid,new_point,d)
		if Freeness_start[0]:
			G_start = nx.compose(Freeness_start[1],G_start)
			parents_start.update(Freeness_start[2])
		if Freeness_goal[0]:
			G_goal = nx.compose(Freeness_goal[1],G_goal)
			parents_goal.update(Freeness_goal[2])		
		
		if anim==True:
			animate_plotting(deepcopy(grid),start,goal,list(G_start.nodes)+list(G_goal.nodes),ind,color="gray",diric=diric);ind +=1 #;plt.show() ;input("hi")
		

		if 	Freeness_start[0] and Freeness_goal[0] and Freeness_start[3]==tuple(new_point) and Freeness_goal[3]==tuple(new_point):
			Flage=True

	
	# Computing the path
	first_part=list(G_start.nodes)
	second_part=list(G_goal.nodes)
	Path1=[tuple(Freeness_start[3])]
	pointer=Path1[0]
	while True:
		new_pointer=parents_start[tuple(pointer)]
		Path1.append(new_pointer)
		pointer=new_pointer
		if pointer==tuple(start):
			break
	Path1.reverse()
	Path2=[tuple(Freeness_goal[3])]
	pointer=Path2[0]	
	while True:
		new_pointer=parents_goal[pointer]
		Path2.append(new_pointer)
		pointer=new_pointer
		if pointer==tuple(goal):
			break		
	
	grid_copy=grid[:]
	if anim==True:
		animate_plotting(deepcopy(grid),start,goal,Path1 +Path2,ind,color="blue",diric=diric);ind +=1 
		algo_animation(grid, start,goal,Path1 +Path2,ind,diric=diric)
		if ind > len(grid[0])*len(grid):
			print("There is no path")
			return [] 


	
	return Path1 +Path2




	
		







































