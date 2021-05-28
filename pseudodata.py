# -*- coding: utf-8 -*-
"""
Creates pseudodata for nodes and edges dataframes.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random 

np.random.seed(1234)
#generate 40 nodes, with randomly assigned discrete opinions 
nodes = pd.DataFrame({
    "ind": np.arange(0,40),
    "opinion": np.random.randint(0,2, size = 40)
})

np.random.seed(1234)
#generate 100 edges, each with a random starting point and a random ending point 
edges = pd.DataFrame({
    "start": np.random.randint(0,40,size=100),
    "end": np.random.randint(0,40,size=100)
})

#for cases where the starting and ending nodes are the same, add 1 to the ending node 
edges['end'].loc[edges.start == edges.end] +=1

#creating a list of tuples containing starting and ending nodes
edges['tup'] = list(zip(edges['start'], edges['end']))


random.seed(1234)

#generate 40 nodes, with randomly assigned continuous opinions 
nodes2 = pd.DataFrame({
    "ind": np.arange(0,40),
})

#assign a continuous opinion between 0 and 1 to each node 
nodes2['opinion'] = nodes2['ind'].apply(lambda x: round(random.uniform(0,1),2)) 
nodes2.head()

#export nodes and edges dataframes as csv files
#will be used as sample dataset 
nodes.to_csv('nodes.csv', index = False)
edges.to_csv('edges.csv', index = False)
nodes2.to_csv('nodes2.csv', index = False)