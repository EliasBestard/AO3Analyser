from cmath import nan
from bs4 import Tag
from pyvis.network import Network
import networkx as nx
from sympy import false, true


def net_visualize(G:nx.DiGraph, hierarchical_layout=True, node_sizes=false, headings="", file_name="nx"):
    if(node_sizes):
        d = dict(G.out_degree)
        #Updating dict
        d.update((x,min(5*y if 10*y>10 else 10, 100)) for x, y in d.items())
        nx.set_node_attributes(G,d,'size')



    nt = Network("100%","100%", directed=True, heading=headings+"<br>Number of Nodes: "+str(len(G.nodes))+"<br>Number of Edges: "+str(len(G.edges)))

    options = {
        "layout": {
        "hierarchical": {
        "enabled": hierarchical_layout,
        "levelSeparation": 500,
        "direction": "UD",
        "sortMethod": "directed"}
        },
        "physics": {
          "centralGravity": 0.05,
          "timestep": 0.1,
        "hierarchicalRepulsion": {
          "centralGravity": 0.05,
          # "springLength": 50,
          "springConstant": 0,
          # "nodeDistance": 75,
          "damping": 0.11
        },
        "minVelocity": 0.75,
        # "solver": "hierarchicalRepulsion"
      },
      "nodes": {
        "font": {
          "background": "rgba(255,255,255,0)",
          "strokeWidth": 5
        }
      },
      "interaction": {
        "dragView": True,
        "hover": True,
        "navigationButtons": True,
        "tooltipDelay": 200,
        "keyboard": {
          "enabled": True
          },
      }
    }




    # options = {
    #   "nodes": {
    #     "fixed": {
    #       "x": True,
    #       "y": True
    #     }
    #   },
    #   "edges": {
    #     "color": {
    #       "inherit": True
    #     },
    #     "smooth": True
    #   },
    #   "physics": {
    #     "barnesHut": {
    #       "springLength": 150,
    #       "avoidOverlap": 0.17
    #     },
    #     "minVelocity": 0.75
    #   }
    # }

    # for n in G.nodes:
    #     G.nodes[n].update({'physics': False})
    
    
    # populates the nodes and edges data structures
    nt.from_nx(G)
    # nt.toggle_physics(True)
    
    
    # nt.options.layout.hierarchical=hierarchical_layout
    # nt.options.layout.set_separation=355
    
    # nt.options=options
    # nt.show_buttons(filter_=["layout"])

    nt.show_buttons(filter_=True)
    nt.show(file_name+'.html')

