from pyvis.network import Network
import networkx as nx
from seaborn import color_palette

def net_visualize(G:nx.DiGraph, hierarchical_layout=False, node_sizes=True, headings="", file_name="nx", show_it=True):
  # """net_visualize _summary_

  # :param G: _description_
  # :param hierarchical_layout: _description_, defaults to False
  # :param node_sizes: _description_, defaults to True
  # :param headings: _description_, defaults to ""
  # :param file_name: _description_, defaults to "nx"
  # :param show_it: _description_, defaults to True
  # :return: _description_
  # """    
    if(node_sizes):
        d = dict(G.out_degree)
        #Updating dict
        d.update((x,min(5*y if 10*y>10 else 15, 100)) for x, y in d.items())
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
        # "minVelocity": 0,
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

    
    nt.from_nx(G)
    nt.options=options  
    nt.bgcolor='#EBF5FB'

    nt.show(file_name+'.html') if show_it else None
    return nt

def get_visuals_older_vs_newest(G_old:nx.DiGraph, G_new:nx.DiGraph,**kwargs):
  """ Generates one visualization for each network where it highlight with the same colors the main nodes they both share

    main nodes: nodes that have outdegree => than nomber_of_comparison

  :G_old, old verison of the graph
  :G_new, New verion of the graph
  :**kwargs: headings: list of two headings
            file_names: list of two file_names
            node_sizes: boolean to display node sizes depending the in/outdegree
            hierarchical_layout: boolean to display the visualizations in hierarchical layout
            number_comparison: number of the outdegree of the nodes to highlight
  """ 
  
  heading_a, heading_b = kwargs['headings'] if 'headings' in kwargs else ("Old Network","Current Network")
  file_name_a, file_name_b = kwargs['file_names'] if 'file_names' in kwargs else ("old_net", "current_net")
  show_it = kwargs['show_it'] if 'show_it' in kwargs else True
  node_sizes = kwargs['node_sizes'] if 'node_sizes' in kwargs else True
  hierarchical_layout = kwargs['hierarchical_layout'] if 'hierarchical_layout' in kwargs else False
  number_comparison = kwargs['number_comparison'] if 'number_comparison' in kwargs else 5


  large_nodes=list(set([node for node in G_new.nodes if G_new.out_degree(node)>=number_comparison]+[node for node in G_old.nodes if G_old.out_degree(node)>=number_comparison]))
  

  colors= color_palette('Set3',len(large_nodes))


  nx.set_node_attributes(G_new,"#C9CBCD",'color')
  nx.set_node_attributes(G_old,"#C9CBCD",'color')

  for i in range(0, len(large_nodes)):
    if G_new.has_node(large_nodes[i]) and G_old.has_node(large_nodes[i]):
      G_new.nodes[large_nodes[i]]['color']=colors[i] 
      G_old.nodes[large_nodes[i]]['color']=colors[i]
      G_old.nodes[large_nodes[i]]['size']=50
      G_new.nodes[large_nodes[i]]['size']=100

  nx.set_edge_attributes(G_new,"#C9CBCD",'color')      
  nx.set_edge_attributes(G_old,"#C9CBCD",'color')      

  return (
    net_visualize(G_new, hierarchical_layout, False,headings=heading_b, file_name=file_name_b, show_it=show_it),
    net_visualize(G_old, hierarchical_layout, node_sizes,headings=heading_a, file_name=file_name_a, show_it=show_it)
    )

def get_vis_G_diff_H(H:nx.DiGraph, G:nx.DiGraph,**kwargs):
  """
  Computes H-G= H-intersection(H,G) and generates the visualization in the layout of H
  Blue Nodes represent the difference H-G
  Red Nodes represet the intersection

  :H, graph
  :G, graph
  :**kwargs: title: title
            file_name: file_names
            node_sizes: boolean to display node sizes depending the in/outdegree
            hierarchical_layout: boolean to display the visualizations in hierarchical layout
  """
  # H-G= H-intersection

  show_it = kwargs['show_it'] if 'show_it' in kwargs else True
  node_sizes = kwargs['node_sizes'] if 'node_sizes' in kwargs else True
  hierarchical_layout = kwargs['hierarchical_layout'] if 'hierarchical_layout' in kwargs else False
  title = kwargs['title'] if 'title' in kwargs else 'default_title'
  file_name = kwargs['file_name'] if 'file_name' in kwargs else 'nx'


  h= H.copy()
  # LIst of nodes and edges of the intersection(G,H)
  list_nodes=[node for node in G.nodes if h.has_node(node)]
  list_edges=[edge for edge in G.edges if h.has_edge(edge[0], edge[1])]

  for node in h.nodes:
    h.nodes[node]['color']= '#2196F3' if not node in list_nodes else '#E91E63'

  for edge in h.edges:
    h[edge[0]][edge[1]]['color']='#2196F3' if not edge in list_edges else '#E91E63'
  
  return h,net_visualize(h, hierarchical_layout=hierarchical_layout, node_sizes=node_sizes,headings=title,show_it=show_it,file_name=file_name)

