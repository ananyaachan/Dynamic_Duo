# Instruction 

For our project, we constructed an interactive visualization program that visualizes how a given network changes over time. Our entire project, including the interactive interface, is carried out on Jupyter Notebook. 

0. Packages Required
Numpy, Pandas, Random, NetworkX, Bokeh, Ipywidgets

1. Creating Pseudo-Data 

Our end product takes in user-inputted datasets. For demonstration purposes, we created the following sample data: 
- A `nodes` dataframe consisted of 40 nodes, each with a randomly assigned opinion that's either 0 or 1;  
- An `edges` dataframe consisted of 100 edges, with randomly selected starting and ending nodes.
- A `nodes2` dataframe consisted of 40 nodes, each with a randomly assigned opinion that's a 2-digit decimal between 0 and 1;  

2. Creating Network

We wrote a `make_network` function that creates a network based on the given nodes and  edges dataframe. The resulting network contains four attributes 1. opinion, 2. degree, 3. size, and 4. edge color. 

3. Implementation in Bokeh (Maybe combine 3 and 4 together?)

We plotted the network in Bokeh, which is a visualization package that comes with a bunch of interactive tools. In our plot, the node color reflects the opinion of the node; the size reflects the degree of the node, which is one way of interpreting connectivity; and finally the edge color reflects whether the neighboring nodes are in discordant opinions. 

4. Make_Plot function 

Here we wrote a `make_plot` function that automates the plotting process. If `continuous = True`, a histogram of the opinion distribution at the current time will be included on the right hand side. Otherwise a line plot of the opinion history up till the current time will be included on the right hand side. 

5. Update function 



6. Adding widgets 


