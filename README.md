# Project Proposal by Dynamic-Duo


### I. Abstract

The objective of our project is to construct a front-end system for visualizing opinion dynamics. The system would be built upon existing packages such as networkx and plotly. 

### II. Deliverables

Our deliverable would be a front-end system for visualizing opinion dynamics. It takes in the following inputs:
- A network (Can also be simulated given the # of nodes + Initial conditions *)
- A model (Each may come with some customized arguments) 
- Threshold Model, Voter Model, or Bounded-Confidence Model
	- BCM might be tricky here considering its continuous nature 
- A starting time point (by default 0)
- An ending time point (T) 
- Number of steps (n)

And it returns a visualization which should include the following features:
- An animated plot of how the network evolved with each small increment of time
- At each time point, the graph should use color to indicate the opinion and size to indicate the influence of each node  (i.e. how many neighbors it is connected to)
- A “drag and build” bar where the user can control the time *
- A zoom-in function where the user can select one specific node and its neighbors to look at *

A 150% successful project should include every feature including the ones with asterisks

A 100% successful project should include all the features without asterisks. 

A 70% successful project should still include the animated plot of how the network evolved over time. It’s may have certain problems for certain model.

### III. Resources Required

We would not need a dataset because our system should be able to take in user-inputted networks. We do, however, need to build a medium through which the users can interact with our system. 

### IV. Tools/Skills Required

Packages that we’ll need include networkx, plotly, and matplotlib.animation. 

There are two main tasks we need to address for this project. The first is to demonstrate the change in dynamics over time. To do so, we need to save the plot for (T/n) discrete time points and put it together in an animation, this is when matplotlib.animation comes in handy. However, the amount of computation can be a lot when T gets very large or n gets very small. 

The second problem is to put this visualization system on a medium through which the users can interact with the system. This may involve building a website/application. Ideally, we should include a “drag and build” bar where the user can control what time point they want to see and a zoom-in function where the user can select one specific node and its neighbor to look at. 
