#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 02:56:21 2021

@author: Andy, Ananya, Tiana
"""
import network
import numpy as np
from bokeh.io import output_file, show, output_notebook
from bokeh.models import (BoxSelectTool, BoxZoomTool, ResetTool, Circle, EdgesAndLinkedNodes, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool,)
from bokeh.plotting import from_networkx
#replace above line with comment below if it gives you an error
#from bokeh.models.graphs import from_networkx
from bokeh.models import StaticLayoutProvider
from bokeh.transform import linear_cmap
from bokeh.plotting import figure, show
from bokeh.layouts import row
import random
import networkx as nx
import visualize

def set_nodes(nodes_df):
    global nodes
    nodes = nodes_df
    
def set_edges(edges_df):
    global edges
    edges = edges_df
    
#define a make plot function 
def make_plot(G, layout, t, epochs, history1 = [], history0 = [], bins_number = 8, continuous = False):
    '''
    Arguments:
        G = a network object
        layout = the layout that the network plot follows 
        t = the current time, will be displayed in the plot title
        history1 = a list of historical percentages of opinion 1, only needed if the opinions are discrete
        history0 = a list of historical percentages of opinion 0, only needed if the opinions are discrete 
        bins_number = the number of bins for the histogram, only needed if the opinions are continuous
        continuous = whether the opinions are continuous 
    Returns:
        The combined plot of 1) the network plot and 2) a histogram if the opinions are continuous and a line plot otherwise.
    
    '''
    fig1 = figure(plot_width=480, plot_height=480,
              x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
              title = f'Network Plot at t = {t}')

    #add additional tools
    node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("opinion", "@opinion"), ("degree", "@degree")])
    fig1.add_tools(node_hover_tool)

    #construct graph_renderer
    graph_renderer = from_networkx(G, layout, scale=1, center=(0, 0))

    #let the node color reflect the opinion and edge color reflect the discordancy between neighbors  
    graph_renderer.node_renderer.glyph = Circle(size = 20, fill_color=linear_cmap('opinion', 'Blues8', nodes['opinion'].min(), nodes['opinion'].max()))
    graph_renderer.edge_renderer.glyph = MultiLine(line_color = "edge_color", line_dash = "dashed", line_alpha=0.8, line_width=1)

    #change hovered nodes' colors
    graph_renderer.node_renderer.hover_glyph = Circle(fill_color="orange")

    #append graph_renderer to figure 1
    fig1.renderers.append(graph_renderer)
    
    #correcting format 
    fig1.xgrid.visible = False #remove horizontal gridlines
    fig1.ygrid.visible = False #remove vertical gridlines 
    fig1.axis.visible = False #remove axes 

    if continuous == False: #if the model is discrete, add a line plot on the right hand side 
        fig2 = figure(plot_width=480, plot_height=480, #initialize the line plot 
                      title = 'Change in % of Opinions Over Time',
                      x_axis_label='Epochs', y_axis_label='Percentage(from 0 to 1)',
                      x_range = [-0.1, epochs+0.1],
                     y_range = [-0.1,1.1])  
        
        opinions = list(nx.get_node_attributes(G, 'opinion').values())
        pct1 = sum(opinions)/len(opinions) #get % of opinion 1 holders
        pct0 = 1 - pct1 #get % of opinion 0 holders 
        history1.append(pct1) #append the % to the history 
        history0.append(pct0)
        #fig2.line(x = np.arange(0,t+1), y = history1[:t+1], line_color = 'orange', legend_label="% of Opinion 1")
        #fig2.line(x = np.arange(0,t+1), y = history0[:t+1], line_color = 'green', legend_label="% of Opinion 0")
        
        fig2.line(x = np.arange(0,t+1), y = history1[:t+1], line_color = 'orange')
        fig2.line(x = np.arange(0,t+1), y = history0[:t+1], line_color = 'green')
    
    else: #if the model is continuous, add a histogram on the right hand side 
        d = nx.get_node_attributes(G, 'opinion') #extract the opinions 
        opinions = list(d.values())
        hist, edges = np.histogram(opinions, range = (0,1), density = False, bins=bins_number) 

        #append the histogram to figure 2
        fig2 = figure(plot_width=480, plot_height=480,
                      title = 'Distribution of opinions')
        fig2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white")
        
    #if it's the very first plot, we'll update the layout in the visualize module 
    #this is so that all the plots after this will have the same layout 
    if layout == nx.spring_layout: 
        visualize.set_layout(graph_renderer.layout_provider.graph_layout)
        
    return row(fig1, fig2) #return combined plot


def update(G, model, history1, history0, epochs = 5, threshold = 0.6, synchronous = False, m = 0.5, c = 0.5, p = 0.4, rewire_to_same = False):

    '''
    Arguments:
        G = a network object 
        model = the updating method, takes value in threshold, voter, or bounded-confidence
        history1 = a list of historical percentages of opinion 1, only needed if the opinions are discrete
        history0 = a list of historical percentages of opinion 0, only needed if the opinions are discrete 
        epochs = number of updates 
        threshold = the threshold above which the node will change its opinion, only needed for threshold model
        synchronous = whether the update is synchronous, only needed for threshold model
        m = the update rate or how much the nodes compromise, only needed for bounded-confidence model
        c = the compromise threshold below which the two neighboring nodes will compromise, only needed for bounded-confidence model
        p = the rewire rate below which the starting node of a chosen edge will rewire, only needed for voters model
        rewire_to_same = whether the node will only rewire to nodes holding the same opinion, only needed for voters model
    Returns:
        A list of plots from time 0 to the specified number of epochs. 
    '''
    plot_list = []
    layout = nx.spring_layout
    graph_renderer = from_networkx(G, layout, scale=1, center=(0, 0))
    plot_0 = make_plot(G, visualize.fixed_layout, 0, epochs, history1, history0)
    plot_list.append(plot_0)
  
    if model == "threshold":
        if(synchronous == False):
            #asynchronous update
            for i in range(1, epochs+1): #for each update
                for n, _ in G.nodes(data=True): #for each node
                    #check how many of its neighbors has similar/same opinions
                    ngbrs = [k for k in G.neighbors(n)]
                    num_ngbrs = len(ngbrs) #number of neighbors
                    num_same_opinion = 0
                    node_opinion = G.nodes[n]['opinion']
                    for ngbr in ngbrs: 
                        if G.nodes[ngbr]['opinion'] == node_opinion:
                            num_same_opinion += 1  #calculating the number of neighbors with the same opinion
                    num_diff_opinion = num_ngbrs - num_same_opinion #number of neighbors with different opinion
                    diff_ratio = num_diff_opinion/num_ngbrs
                    if diff_ratio > threshold:
                        #change node n's opinion to the opposite side
                        G.nodes[n]['opinion'] = 0 if node_opinion == 1 else 1  
                network.set_color_attrs(G)
                plot_i = make_plot(G, visualize.fixed_layout, i, epochs, history1, history0) #creates a plot for this round of update
                plot_list.append(plot_i)
        else:
            #synchronous update
            for i in range(1, epochs+1):
                node_opinions_origin = []
                for n, _ in G.nodes(data=True):
                    node_opinions_origin.append(G.nodes[n]['opinion'])
                #for each node, check how many of its neighbors has similar/same opinions
                for n, _ in G.nodes(data=True):
                    ngbrs = [k for k in G.neighbors(n)]
                    num_ngbrs = len(ngbrs)
                    num_same_opinion = 0
                    node_opinion = node_opinions_origin[n]
                    for ngbr in ngbrs: 
                        if node_opinions_origin[ngbr] == node_opinion:
                            num_same_opinion += 1  
                    num_diff_opinion = num_ngbrs - num_same_opinion
                    diff_ratio = num_diff_opinion/num_ngbrs
                    if diff_ratio > threshold:
                        #change node n's opinion to the opposite side
                        G.nodes[n]['opinion'] = 0 if node_opinion == 1 else 1  
                network.set_color_attrs(G)
                plot_s_i = make_plot(G,visualize.fixed_layout, i, epochs, history1, history0)
                plot_list.append(plot_s_i)
    
    elif model == "voter":
        for i in range(1, epochs+1): #for each update
            edges_ = list(G.edges) #pick a random edge 
            start_ind, end_ind = random.choice(edges_)
            #if the two nodes are discordant, compare a random probablity r to p 
            if (G.nodes[start_ind]['opinion'] != G.nodes[end_ind]['opinion']): 
                r = np.random.uniform(low=0.0, high=1.0)
                if r < p: #if r is smaller than p, then we rewire the starting node 
                    ngbrs = [k for k in G.neighbors(start_ind)] 
                    
                    #rewire to a random non-neighboring node if rewire_to_same == False
                    non_ngbrs = [x for x in list(G.nodes()) if x not in ngbrs] 
                    if rewire_to_same == True: #else only rewire to nodes that share the same opinion 
                        non_ngbrs = [x for x in non_ngbrs if G.nodes[x]['opinion'] == G.nodes[start_ind]['opinion']]
                    non_ngbr = random.choice(non_ngbrs)
                    
                    #rewire the starting node to non_ngbr
                    G.remove_edge(start_ind, end_ind) 
                    G.add_edge(start_ind, non_ngbr)
                else:
                    # the node opinion is updated
                    G.nodes[start_ind]['opinion'] = G.nodes[end_ind]['opinion']                      
            network.set_color_attrs(G)
            plot_v_i = make_plot(G, visualize.fixed_layout, i, epochs, history1, history0)
            plot_list.append(plot_v_i) #creates a plot for this round of update

    elif model == "bounded-confidence":
        for i in range(1, epochs+1):
            edges_ = list(G.edges)
            start_ind, end_ind = random.choice(edges_) #select a random edge 
            delta = G.nodes[end_ind]['opinion'] - G.nodes[start_ind]['opinion'] #find the difference between the two nodes' opinion 
            if np.absolute(delta) <= c: #update the opinion iff the difference is less than the compromise threshold 
                G.nodes[start_ind]['opinion'] += m*delta 
                G.nodes[end_ind]['opinion'] -= m*delta
            plot_bc_i = make_plot(G, visualize.fixed_layout, i, epochs, bins_number = 8, continuous = True) #make the plot at current time point and append it to the plot list 
            plot_list.append(plot_bc_i)
            
    return plot_list