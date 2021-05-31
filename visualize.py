#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 03:05:59 2021

@author: Andy, Ananya, Tiana
"""
import update_viz
from update_viz import update
from IPython.display import display
import ipywidgets as widgets
import network
import networkx as nx

epochs = 200
    
def set_network(nodes_df, edges_df):
    # Make a network using the user input data 
    global G_origin
    G_origin = network.make_network(nodes_df, edges_df)
    global G
    G = G_origin.copy()
    global nodes
    nodes = nodes_df
    update_viz.set_nodes(nodes_df)
    global edges
    edges = edges_df
    update_viz.set_edges(edges_df)
    

# Set default values

# Threshold model parameters
thres_val = 0.5 # Threshold using in the model
sync_val = False # Synchronous update 
d_thres = {} # Dictionary for threshold model plots
global fixed_layout
fixed_layout = nx.spring_layout # initialize fixed_layout as spring_layout 

# Bounded-confidence model parameters
c_val = 0.5 # c value in the model
m_val = 0.5 # m value in the model
d_bc = {} # Dictionary for bounded-confidence model plots

# Voter model parameters
p_val = 0.4 # probability below which the node will rewire 
rts_val = False # rewire_to_same value 
d_v = {} # Dictionary for voter model plots


# a helper function to update network layout 
def set_layout(layout):
    global fixed_layout 
    fixed_layout = layout 

    
# Define interactive functions
def display_timestamps_threshold(t):
    #global prev_epochs_thres 
    # Create a unique identifier for the combination of sync_val and thres_val
    id_thres = thres_val + 2 if sync_val == True else thres_val
    # If the plots given thres_val and sync_val are not stored, calculate; otherwise load
    if(id_thres not in d_thres or len(d_thres[id_thres]) < epochs):
        d_thres[id_thres]= update(G_origin.copy(), "threshold", [], [], epochs, threshold = thres_val, synchronous = sync_val)
    # Display the plot
    plot = d_thres[id_thres][t]
    update_viz.show(plot)

def display_timestamps_bounded_confidence(t):
    global prev_epochs_bc 
    # Create a unique identifier for the combination of c_val and m_val
    id_bc = str(c_val) + str(m_val) 
    # If the plots given c_val and m_val are not stored, calculate; otherwise load
    if(id_bc not in d_bc or len(d_bc[id_bc]) < epochs):
        d_bc[id_bc]= update(G_origin.copy(), "bounded-confidence", [], [], epochs, c = c_val, m = m_val)
    # Display the plot
    plot = d_bc[id_bc][t]
    update_viz.show(plot)

def display_timestamps_voter(t):
    global prev_epochs_voter 
    # Create a unique identifier for the p_val
    id_v = p_val + 2 if rts_val == True else p_val
    # If the plots given p are not stored, calculate; otherwise load
    if(id_v not in d_v or len(d_v[id_v]) < epochs):
        d_v[id_v]= update(G_origin.copy(), "voter", [], [], epochs, p = p_val, rewire_to_same = rts_val)
    # Display the plot
    plot = d_v[id_v][t]
    update_viz.show(plot)

#choose epochs
def choose_epochs(e):
    global epochs
    epochs = e
    time_slider_threshold.max = e
    time_slider_voter.max = e
    time_slider_bounded_confidence.max = e

# Update thres_val
def change_thres(thres):
    global thres_val 
    thres_val = thres
    
# Update sync_val    
def change_sync(s):
    global sync_val
    sync_val = s
    
# Update c_val    
def change_c(c):
    global c_val
    c_val = c
    
# Update m_val          
def change_m(m):
    global m_val
    m_val = m
    
# Update p_val          
def change_p(p):
    global p_val
    p_val = p

#  Update rewire_to_same_val
def change_rewire(r):
    global rts_val
    rts_val = r

# Update whether the opinions are continuous
def display_cont(continuous):
    if continuous == 1: #if true only bounded-confidence method can be used 
        widgets.interact(change_c, c=c_slider)
        widgets.interact(change_m, m=m_slider)
        widgets.interact(display_timestamps_bounded_confidence, t=time_slider_bounded_confidence)
    elif continuous == 0: #else the user will be prompted to choose threshold or voter 
        widgets.interact(display_dropdown, model = model_dropdown) 
        
# Display the epochs selection widget and update the default value of epochs using user's input
def display_epochs_selection():
    widgets.interact(choose_epochs, e=epochs_intbox)
    
# Display a given set of sliders depending on the user's selection of updating method
def display_dropdown(model):
    # If the user chooses threshold model
    if model == 0:
        widgets.interact(change_thres, thres=threshold_slider)
        widgets.interact(change_sync, s=sync_checkbox)
        widgets.interact(display_timestamps_threshold, t=time_slider_threshold)
    # If the user chooses voter's model
    elif model == 1:
        widgets.interact(change_p, p=p_slider)
        widgets.interact(change_rewire, r=rewire_checkbox)
        widgets.interact(display_timestamps_voter, t=time_slider_voter)
    else: 
        print("Select Model")

# Define all the widgets 

# Textbox for epochs, bounded between 0 to 1000
epochs_intbox = widgets.widgets.BoundedIntText(
    value=100,
    min=0,
    max=1000,
    step=1,
    description='Epochs:',
    disabled=False
)

# Dropdown menu for updating methods
cont_dropdown = widgets.Dropdown(
    options=[('Select', -1), ('True', 1), ('False', 0)],
    value=-1,
    description='Continuity',
    disabled=False,
)

# Dropdown menu for updating methods
model_dropdown = widgets.Dropdown(
    options=[('Choose Model', -1), ('Threshold', 0), ('Voters', 1)],
    value=-1,
    description='Model:',
    disabled=False,
)

# time_slider for threshold model
time_slider_threshold = widgets.IntSlider(
    value=0,
    min=0,
    max=epochs,
    step=1,
    description='Time:',
    disabled=False,
    continuous_update=False, #to reduce wait time
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

# threshold_slider
threshold_slider = widgets.FloatSlider(
    value=0.5,
    min=0,
    max=1,
    step=0.1,
    description='Threshold:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f'
)

# sync_checkbox
sync_checkbox = widgets.Checkbox(
    value=False,
    description='Synchronous',
    indent=True
)

# time_slider for bounded-confidence model
time_slider_bounded_confidence = widgets.IntSlider(
    value=0,
    min=0,
    max=epochs,
    step=1,
    description='Time:',
    disabled=False,
    continuous_update=False, #to reduce wait time
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

# c_slider
c_slider = widgets.FloatSlider(
    value=0.5,
    min=0,
    max=1,
    step=0.1,
    description='Comp rate',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f'
)

# m_slider
m_slider = widgets.FloatSlider(
    value=0.5,
    min=0,
    max=1,
    step=0.1,
    description='Update rate:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f'
)

# p_slider
p_slider = widgets.FloatSlider(
    value=0.5,
    min=0,
    max=1,
    step=0.1,
    description='Rewire rate:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f'
)

# rewire_to_same_checkbox
rewire_checkbox = widgets.Checkbox(
    value=False,
    description='Only rewire to the same nodes ',
    indent=True
)

# time_slider for voter model
time_slider_voter = widgets.IntSlider(
    value=0,
    min=0,
    max=epochs,
    step=1,
    description='Time:',
    disabled=False,
    continuous_update=False, #to reduce wait time
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

def interact():
    # Show the output
    update_viz.output_notebook()
    print('Select if the opinions are continuous. If true, only Bounded-Confidence Model can be used.')
    return widgets.interact(display_cont, continuous=cont_dropdown)
