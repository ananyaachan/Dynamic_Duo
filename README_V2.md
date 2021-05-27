# Instruction 

For our project, we constructed an interactive visualization program to visualize how a given network changes over time. Our entire project, including the interactive interface, is carried out on Jupyter Notebook. 

0. Packages Required

Numpy, Pandas, Random, NetworkX, Bokeh, Ipywidgets

1. Creating Pseudo-Data 

Our end product takes in user-inputted datasets. For demonstration purposes, we created the following sample data: 
- A `nodes` dataframe consisted of 40 nodes, each with a randomly assigned opinion that's either 0 or 1;  
- An `edges` dataframe consisted of 100 edges, with randomly selected starting and ending nodes.
- A `nodes2` dataframe consisted of 40 nodes, each with a randomly assigned opinion that's a 2-digit decimal between 0 and 1;  

2. Creating Network

We wrote a `make_network` function that creates a network based on the given nodes and edges dataframe. The resulting network contains four attributes:
- opinion 
- degree 
- size 
- edge color

3. Implementation in Bokeh (Maybe combine 3 and 4 together?)

We plotted the network in Bokeh, which is a visualization package that comes with a bunch of interactive tools. In our plot, the node color reflects the opinion of the node; the size reflects the degree of the node, which is one way of interpreting connectivity; and finally the edge color reflects whether the neighboring nodes are in discordant opinions. 

4. Plot function 

Here we wrote a `make_plot` function that automates the plotting process. If `continuous = True`, a histogram of the opinion distribution at the current time will be included on the right hand side. Otherwise, if the model is discrete, a line plot of the opinion history up till the current time will be included on the right hand side to represent the percent change in opinion over time for each opinion (0 and 1).

5. Update function 

After we figured out how to visualize a given network, we had to update the network based on existing opinion dynamics models. Our visualization program can update our network based on three kinds of opinion dynamics models:
- Threshold model
- Voter model
- Bounded-confidence model

In order to implement these models, we first researched and understood what each model means in the realm of opinion dynamics, and how we can implement this through code. The threshold and voter models are discrete models, i.e. the opinions are in discrete values - so a node (analogous to a person in a social network) has either one opinion or the other. Our discrete models only accounted for 2 kinds of opinions, labelled as 0 and 1. The bounded-confidence model however is a continuous model, which means that the opinions of the nodes are labelled as a decimal between 0 and 1.

After we understood what happens at every update for each model, we wrote the code to update the network for each epoch. However, we still had to figure out how to represent the updates in only one figure, instead of a figure after each update, so that it is easier to visualize the changes the network goes through. We first used gifs to represent how the network changed overtime, however this way did not incorporate the interactive features of our Bokeh plots. Hence, we worked with widges, using ipywidgets library, in order to preserve the features while showing the changes to a network over time.

6. Adding widgets 


