#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 02:53:58 2021

@author: Andy, Ananya, Tiana
"""
import networkx as nx

def set_opinion_attrs(G, nodes):
    '''
    Sets the opinion attribute of a network G
    '''
    #creating attribute dictionary
    opinion_dict = {}
    for i in range(len(nodes)):  
        opinion_dict[i] = nodes['opinion'][i]
    #set attribute 
    nx.set_node_attributes(G, opinion_dict, 'opinion')
    
def set_degree_attrs(G):
    '''
    Sets the degree attribute of a network G 
    '''
    #get the degree dictionary from G
    degree_dict = dict(G.degree(G.nodes()))
    
    #set the attributes
    nx.set_node_attributes(G, degree_dict, 'degree')
    
def set_color_attrs(G):
    '''
    Sets the edge color attributes of a network G    
    '''
    edge_color = {}

    #The edge color is orange if the two neighboring nodes hold different opinions and black otherwise.
    for start_node, end_node, _ in G.edges(data=True): 
        e_color = "orange" if G.nodes[start_node] ['opinion']!= G.nodes[end_node]['opinion'] else "black"
        edge_color[(start_node, end_node)] = e_color
        
    #set attributes
    nx.set_edge_attributes(G, edge_color, "edge_color")

def make_network(nodes, edges):
    '''
    returns a network object based on given nodes and edges dataframe
    '''
    G = nx.Graph()
    G.add_nodes_from(nodes['ind']) #add the nodes 
    G.add_edges_from(edges['tup'])  #add the edges 
    #set attributes
    set_opinion_attrs(G, nodes)
    set_degree_attrs(G)
    set_color_attrs(G)
    return G
    