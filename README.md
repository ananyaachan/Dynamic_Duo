# Instruction 

For our project, we constructed an interactive visualization program to visualize how a given network changes over time. To see the clean version of our final product, with all
functions imported as modules, please go to `Opinion Dynamics Program.ipynb`. To see the details of how we get to our final product, please go to `od_newest.ipynb`

The clean version of our project consists of five modules:
- `pseudodata.py`: creates the sample datasets (`nodes`, `edges`, `nodes2`)
- `network.py`: contains the `make_network` function 
- `update_viz.py`: contains the `make_plot` and `update` function
 
	- Depends on your version of Bokeh, you might encounter an error when the program gets to `from bokeh.plotting import from_networkx`, in which case simply replace the command with  `from bokeh.models.graphs import from_networkx`
	
- `upload_data.py`: creates an uploading interface and checks if the the data provided by the user is correctly formatted
- `visualize.py`: creates the main visualization interface that allows the user to customize parameters and view the network at various time stamps. 

If you'd like to learn more about the functions mentioned above or about our work process in general, we included a brief summary below. 


## Creating Pseudo-Data 

Our end product takes in user-inputted datasets. For demonstration purposes, we created the following sample data: 
- A `nodes` dataframe consisted of 40 nodes, each with a randomly assigned discrete opinion;  
- An `edges` dataframe consisted of 100 edges, with randomly selected starting and ending nodes;
- A `nodes2` dataframe consisted of 40 nodes, each with a randomly assigned continuous opinion.  

## Creating Network

We wrote a `make_network` function that creates a network based on the given nodes and edges dataframe. The resulting network contains three node attributes: opinion, degree, size and one node attribute: edge_color.


## Plotting with Bokeh 

Here we wrote a `make_plot` function that automates the plotting process. The function takes in 3-7 arguments, some of which are optional depending on the value of `continuous`. 
It returns a combined plot of 1) a network plot at the current time t and 2) a line plot of opinion history up till the time t if the `continuous == False` and otherwise a histogram of the opinion distribution at time t. 

## Implementing Update Methods 

After we figured out how to visualize a given network, we had to update the network based on existing opinion dynamics models. Our visualization program can update our network based on three kinds of opinion dynamics models:
- Threshold model
- Voter model
- Bounded-confidence model

In order to implement these models, we first researched and understood what each model means in the realm of opinion dynamics, and how we can implement this through code. The threshold and voter models are discrete models, i.e. the opinions are in discrete values - so a node (analogous to a person in a social network) has either one opinion or the other. Our discrete models only accounted for 2 kinds of opinions, labelled as 0 and 1. The bounded-confidence model however is a continuous model, which means that the opinions of the nodes are labelled as a two-digit decimal between 0 and 1.


All the numerical parameters in mentioned below are between 0 and 1 unless otherwise stated. 

### The Threshold Model
In the threshold model, we update each node's opinion based on the opinions of its neighbouring nodes. The user can choose a `threshold` level, and whether to use `synchronous` or `asynchronous` update. For each individual node, we compute the percentage of its neighbour nodes that have the opposite opinion, denote the percentage as `diff_ratio`. If `diff_ratio` is greater than `threshold`, we then change the opinion of that node to the opposite value (0 to 1; 1 to 0). If the updating method is `synchronous`, then the change to each node's opinion in a certain round will be reflected at once after that round. Otherwise, if the updating method is `asynchronous`, then the changeto each node's opinion will be updated one by one, ordered by the index of that node.


### The Voter Model

Q-voter model using async edge-based updates.

- Each node gets randomly assigned either to Group 0 or Group 1
- Assume there’s a probability p of rewiring and 1-p of changing opinion
- For each update:
    - Randomly select an edge
    - If the two nodes connected by the edge are discordant
        - For one node at an end we choose a random number r from the uniform distribution U(0, 1)
        - if r < p, then that node rewires (the edge is rewired) to a random node
        - else, it adopts the opinion of the node at the other end of the edge

### The Bounded-Confidence Model

Again, we assume that the opinions are continuously distributed between 0 and 1 for the Bounded-Confidence Model. For each epoch, we randomly select an edge and calculate the difference between the two nodes' opinions, which we call `delta`. If this difference is smaller than the compromise threshold `c`, both nodes will compromise: that is, they change their opinion by `m*delta`, where `m` is a previously defined update rate. Otherwise nothing gets changed. 


## Adding widgets 

After we understood what happens at every update for each model, we wrote the code to update the network for each epoch. However, we still had to figure out how to represent the updates in only one figure, instead of a figure after each update, so that it is easier to visualize the changes the network goes through. We first used gifs to represent how the network changed overtime, however this way did not incorporate the interactive features of our Bokeh plots. Hence, we worked with widges, using ipywidgets library, in order to preserve the features while showing the changes to a network over time.

### The Uploading Interface 

We created a widget in order for a user to be able to input their nodes and edges dataframes. We found that we could do this using ipywidgets.FileUpload, and the user could directly upload a csv file for their nodes and edges. After this, we run checks (using assert) to ensure that the dataframe is formatted correctly. This enables the users to play around with the visualization program with their own data for networks.


### The Main Visualization Interface 
After the user supplies our program with a correctly formatted dataset, he/she can now access the main visualization interface. First, the user needs to select whether the opinions are continuous. If true, only the Bounded-Confidence Model can be used; otherwise the user can choose between Threshold or Voter Model. Each model comes with several unique parameters that the user can then specify. All three models come with a time slider through which the user can view the plot at various time stamps. 

*WARNINGS:* 
1. The plot will NOT reflect the change in parameters until the user drag the time slider.
2. Sometimes there will be a small lag, but it shouldn't take more than a few seconds. If somehow the plot is stuck, try dragging the time slider or rerun the cells above. 
3. If the user made the wrong selection regarding the continuity of opinions, the visualization will still be displayed but no meaningful conclusions can be drawn. 





