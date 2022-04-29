from cgitb import enable
from cmath import nan
from bs4 import Tag
from numpy import number
from pyvis.network import Network
import networkx as nx
from sqlalchemy import null
from sympy import false, true
from random import randint

def net_visualize(G:nx.DiGraph, hierarchical_layout=True, node_sizes=False, headings="", file_name="nx", show_it=True):
    if(node_sizes):
        d = dict(G.out_degree)
        #Updating dict
        d.update((x,min(5*y if 10*y>10 else 10, 100)) for x, y in d.items())
        nx.set_node_attributes(G,d,'size')



    nt = Network("100%","100%", directed=True, heading=headings+"<br>Nodes: "+str(len(G.nodes))+"<br>Edges: "+str(len(G.edges)))
    
    options = {
      "nodes": {
        "borderWidthSelected": 3,
        "font": {
          "background": "rgba(255,255,255,0)",
          "strokeWidth": 5
        },
        "fixed": {
          "x": False,
          "y": False
        }
      },
      "edges": {
        "color": {
          "inherit": True
        },
        "width": 0,
        "smooth": False
      },
      "layout": {
        "hierarchical": {
          "levelSeparation": 400,
          "enabled": hierarchical_layout,
          "improvedLayout": False
        }
      },
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0
        },
        "forceAtlas2Based": {
          "springLength": 100
        },
        "solver": "hierarchicalRepulsion" if hierarchical_layout else "forceAtlas2Based",#"barnesHut",
        "minVelocity": 0.75
      },
      "interaction": {
        "dragView": True,
        "hover": True,
        "navigationButtons": True,
        "keyboard": {
          "enabled": True
          },
      }
    }

    # for n in G.nodes:
    #     G.nodes[n].update({'physics': False})
    
    
    # populates the nodes and edges data structures
    # pos={"Disability":(50,50)}
    
    nt.from_nx(G)
    nt.options=options  
    nt.bgcolor='#EBF5FB'
    
    # nt.toggle_physics(False)
    # nt.show_buttons(filter_=["physics"])
    # nt.show_buttons(filter_=True)
    # print(nt.nodes)
    nt.show(file_name+'.html') if show_it else None
    return nt

def get_visuals_older_vs_newest(G_old:nx.DiGraph, G_new:nx.DiGraph,number_comparison=5,hierarchical_layout=True, node_sizes=false):
  """
  """
  # G_new_large_nodes=[node for node in G_new.nodes if G_new.out_degree(node)>number_comparison]
  # G_old_large_nodes=[node for node in G_old.nodes if G_old.out_degree(node)>number_comparison]
  # colors=['#2980B9','#3164A2','#A9192A','#A91994','#5419A9','#5419A9','#19A968']
  
  large_nodes=list(set([node for node in G_new.nodes if G_new.out_degree(node)>number_comparison]+[node for node in G_old.nodes if G_old.out_degree(node)>number_comparison]))
  
  colors=[('#%06X' % randint(0, 0xFFFFFF))for i in range(len(large_nodes))]
  for i in range(0, len(large_nodes)):
    G_new.nodes[large_nodes[i]]['color']=colors[i] if G_new.has_node(large_nodes[i]) else None
    G_old.nodes[large_nodes[i]]['color']=colors[i] if G_old.has_node(large_nodes[i]) else None

  return (
    net_visualize(G_new, hierarchical_layout, node_sizes,headings="Current Network", file_name="current_network", show_it=False),
    net_visualize(G_old, hierarchical_layout, node_sizes,headings="Old Network", file_name="Old_network", show_it=False)
    )

def get_vis_G_diff_H(H:nx.DiGraph, G:nx.DiGraph,hierarchical_layout=True, title='Diff'):
  """
  """
  # H-G= H-intersection

  h= H.copy()
  # LIst of nodes and edges of the intersection(G,H)
  list_nodes=[node for node in G.nodes if h.has_node(node)]
  list_edges=[edge for edge in G.edges if h.has_edge(edge[0], edge[1])]

  for node in h.nodes:
    h.nodes[node]['color']= '#2196F3' if not node in list_nodes else '#E91E63'

  for edge in h.edges:
    h[edge[0]][edge[1]]['color']='#2196F3' if not edge in list_edges else '#E91E63'
  
  return h,net_visualize(h, hierarchical_layout=False, node_sizes=True,headings=title,show_it=False)

  



