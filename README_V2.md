# Instruction 

For our project, we constructed an interactive visualization program to visualize how a given network changes over time. Our entire project, including the interactive interface, is carried out on Jupyter Notebook. 

0. Packages Required

Numpy, Pandas, Random, NetworkX, Bokeh, Ipywidgets

1. Creating Pseudo-Data 

Our end product takes in user-inputted datasets. For demonstration purposes, we created the following sample data: 
- A `nodes` dataframe consisted of 40 nodes, each with a randomly assigned discrete opinion;  
- An `edges` dataframe consisted of 100 edges, with randomly selected starting and ending nodes;
- A `nodes2` dataframe consisted of 40 nodes, each with a randomly assigned continuous opinion.  

2. Creating Network

We wrote a `make_network` function that creates a network based on the given nodes and edges dataframe. The resulting network contains three node attributes: opinion, degree, size and one node attribute: edge_color.


3. Plotting with Bokeh 

Here we wrote a `make_plot` function that automates the plotting process. The function takes in 3-7 arguments, some of which are optional depending on the value of `continuous`. 
It returns a combined plot of 1) a network plot at the current time t and 2) a line plot of opinion history up till the time t if the `continuous == False` and otherwise a histogram of the opinion distribution at time t. 

5. Update function 

After we figured out how to visualize a given network, we had to update the network based on existing opinion dynamics models. Our visualization program can update our network based on three kinds of opinion dynamics models:
- Threshold model
- Voter model
- Bounded-confidence model

In order to implement these models, we first researched and understood what each model means in the realm of opinion dynamics, and how we can implement this through code. The threshold and voter models are discrete models, i.e. the opinions are in discrete values - so a node (analogous to a person in a social network) has either one opinion or the other. Our discrete models only accounted for 2 kinds of opinions, labelled as 0 and 1. The bounded-confidence model however is a continuous model, which means that the opinions of the nodes are labelled as a two-digit decimal between 0 and 1.

A) The threshold model
- We considered two groups of opinions: Group 0, Group 1
- Each node gets assigned either to Group 0 or Group 1
- We set a threshold value, any decimal between 0 and 1 (for demonstration we set this as 0.6)
- For each update/epoch:
    - For each node:
        - if ratio of infected (Group 1) neighbors > threshold value
            -> node is put into to group 1 
- Assumption: once you go to group 1, you never go back

B) The voter model

Q-voter model using async edge-based updates.

- Each node gets randomly assigned either to Group 0 or Group 1
- Assume there’s a probability p of rewiring and 1-p of changing opinion
- For each update:
    - Randomly select an edge
    - If the two nodes connected by the edge are discordant
        - For one node at an end we choose a random number r from the uniform distribution U(0, 1)
        - if r < p, then that node rewires (the edge is rewired) to a random node
        - else, it adopts the opinion of the node at the other end of the edge

C) The bounded-confidence model




After we understood what happens at every update for each model, we wrote the code to update the network for each epoch. However, we still had to figure out how to represent the updates in only one figure, instead of a figure after each update, so that it is easier to visualize the changes the network goes through. We first used gifs to represent how the network changed overtime, however this way did not incorporate the interactive features of our Bokeh plots. Hence, we worked with widges, using ipywidgets library, in order to preserve the features while showing the changes to a network over time.

6. Adding widgets 

We created a widget in order for a user to be able to input their nodes and edges dataframes. We found that we could do this using ipywidgets.FileUpload, and the user could directly upload a csv file for their nodes and edges. After this, we run checks (using assert) to ensure that the dataframe is formatted correctly. This enables the users to play around with the visualization program with their own data for networks.