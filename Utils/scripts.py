import json
from Modules.NetVisualizer.net_visualizer import *
from Modules.NetBuilder.net_builder import net_build


def visualize_ratas_json(ratas_file, hierarchical_layout=False,node_sizes=True, headings='',file_name='nx', show_it=True):
    """
    Read a JSON file with different rooted-RATAS to create a NetworkX directed Graph and its visualization in pyvis
    return graph G and pyvis visualization
    """
    with open(ratas_file, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    f.close()
    
    G = net_build(current_data)
    current_dis=net_visualize(G, hierarchical_layout,node_sizes,headings,file_name)

    return G,current_dis