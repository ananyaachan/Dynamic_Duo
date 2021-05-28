#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 03:03:17 2021

@author: Ananya
"""

import io
import ipywidgets as widgets
import pandas as pd

# upload nodes dataframe
nodes_upload = widgets.FileUpload(
    accept='.csv',  
    multiple=False  
)

def check_and_return_nodes(nodes_upload):
    if(len(nodes_upload.value)) == 1:
        nodes = list(nodes_upload.value.values())[0]
        content = nodes['content']
        content = io.StringIO(content.decode('utf-8'))
        nodes = pd.read_csv(content)
        assert 'ind' and 'opinion' in nodes.columns, 'Columns are not named correctly'
        assert nodes['ind'].dtype == 'int64', 'ind column does not have dtype = int'
        assert nodes['opinion'].dtype == 'int64' or nodes['opinion'].dtype == 'float', 'opinion column does not have numeric dtype'
        return nodes

#upload edges dataframe
edges_upload = widgets.FileUpload(
    accept='.csv',  
    multiple=False  
)

def check_and_return_edges(edges_upload):
    if(len(edges_upload.value)) == 1:
        edges = list(edges_upload.value.values())[0]
        content = edges['content']
        content = io.StringIO(content.decode('utf-8'))
        edges = pd.read_csv(content)
        assert 'start' and 'end' in edges.columns, 'Columns are not named correctly'
        assert edges['start'].dtype == 'int64', 'start column does not have dtype = int'
        assert edges['end'].dtype == 'int64', 'end column does not have dtype = int'
        edges['tup'] = list(zip(edges.start, edges.end))
        return edges
    
# Check if the user uploads both files
use_own_model = False
if(len(edges_upload.value) == 1 and len(nodes_upload.value) == 1):
    use_own_model = True