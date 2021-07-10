# Path Planning 
This is my solution for the [the problem](https://stackblitz.com/edit/angular-ft5q31?file=src/app/app.component.ts) you proposed



## Algorithm 
Since the priority is to find a fast algorithm that finds a path and not necessary a shortest one, a variant of [Rapidly-exploring random](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree) tree algorithm is is a good candidate. Recall that the main steps of that algorithm are:

![](https://s6.gifyu.com/images/movie439a511ef7c6f5d6.gif)

### I. Computing a randomly-generated tree with ***Start*** and ***Goal*** are in its vertices.
   1. *G_start* (respec. *G_goal*) is a tree with one node ***Start*** (respec. ***Goal***). 

   2. P := randomly chosen yellow cell in the grid that is neither  ***Start*** nor ***Goal***.

   3. Using the P, for both *G_start* and *`$G_goal$`* find two points *$`P_start$`* and *P_goal* that are close enough to *G_start* and *G_goal* respectively. 

   4. Check wether there exists an "simple path"[<sup>[1]</sup>](#fn1) between P_start and *G_start*. If so, add that path to  *G_start*, preserving the information about the parents of each node  in both   G_start and  G_goal  (the same for *P_goal* and *G_goal*).[<sup>[2]</sup>](#fn2) 

5. If P= P_start = P_goal  and both simple paths exist, return Tree=  <img src="https://latex.codecogs.com/gif.latex?G_start \cup G_goal t " /> 

6. Otherwise, compute a new P and go to Step 3




### II. Finding a path between from ***Start*** to ***Goal***

1. Using the parent information, build $Path_1$ a path between the last P and ***Start*** (Do the same for ***Goal*** and call it $Path_2$)
2. Return the concatination of  Rrversed($Path_1$) and  $Path_2$, after removing the duplication of P.

---





<span id="fn1">  [1]   Simple path is a path that is  computed in a fast way.  The algorithm of computing such a path depends on the conditions imposed on the motion. In my codes, I allowed diagonal motion.  </span>

<span id="fn2">  [2]  Recall that Start and Goal are the roots of   *G_start* and *G_goal*  respectively.


<img href="/content/movie.gif" >

## How to use the codes 
we have the following functions *myPathPlanning*,  *plotting*. 

## *myPathPlanning(grid, start,goal,d=4,anim=False)* 

### Input



> **grid**: a $2$-dimensional list of lists of the values $\{1,0\} $ 

> **start,goal**: two tupes of intefer representing the start and goal

> **d**: variable representing the local search bounds.


> **anim**: if anim is True, then a file movie.gif is generated. This files describes the algorithm using animation.


### Output 
a list of tuples that represent the path from start to goal


## *plotting(grid,start,goal ,path=[])* 
Plots the results from the previous function. 

*grid,start and goal* are as in *myPathPlanning*. *path* is the output of *myPathPlanning*.


## Example

### Computing the path:


```Python
from rrt import plotting, myPathPlanning
from pprint import pprint 

grid =[[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0], 
       [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
       [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], 
       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
       [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1], 
       [0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1], 
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1], 
       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1], 
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], 
       [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0], 
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1], 
       [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0], 
       [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]




start=[0,1]
goal=[17,14]

path=myPathPlanning(grid, start,goal)

pprint(path,compact=True)
```

The results:
```
[(0, 1), (1, 2), (1, 3), (2, 4), (3, 5), (3, 6), (3, 7), (4, 8), (5, 8), (6, 9),
 (7, 8), (8, 7), (9, 7), (10, 7), (11, 8), (12, 9), (13, 9), (13, 9), (13, 10),
 (13, 11), (13, 12), (13, 13), (14, 13), (15, 13), (16, 13), (17, 14)]
```
### Plotting the path:

```
plotting(grid,start,goal ,path=path)
```

> ![](data:image/png;base64,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)

## Animating the algorithm (for local use only) 
```
from google.colab import files
path=myPathPlanning(grid, start,goal,anim=True,diric="imges/")
# This command generates a set of images .... delete them everytime you use it.
```
