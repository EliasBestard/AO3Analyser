import json
import os
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
    current_dis=net_visualize(G, hierarchical_layout,node_sizes,headings,file_name, show_it)

    return G,current_dis


#%% Report Generation
def get_G_info(G:nx.DiGraph, g_name='name', w_mode='w'):
    info_dic={}

    info_dic['report_info']= ''' Report Node information of nodes with
    outdegree greater than 4, or indegree greater than 1
    report total amount of nodes, edges, leaves, freeform/canonical/synned tags, nodes with more than 4 subtags, 
    '''
    info_dic['name']= g_name
    
    big_nodes=[]
    leaves_count=0
    freeform_tags_count=0
    synned_tags_count=0
    canonical_tags_count=0
    conection_node_count=0

    for node in G.nodes:
        if G.out_degree(node)>4:
            big_nodes.append(node)
        if G.out_degree(node)>4 and G.in_degree(node)<=1:
            info_dic[node+"_out_degree"]=G.out_degree(node)
            info_dic[node+"_in_degree"]=G.in_degree(node)
        if G.in_degree(node)>1:
            info_dic[node+"_in_degree"]=G.in_degree(node)
            info_dic[node+"_metatags"]=','.join([y for y in G.predecessors(node)])
        if 'synned_tags' in G.nodes[node]:
            info_dic[node+"_synned_tags"]=','.join(G.nodes[node]['synned_tags'])
            info_dic[node+"_synned_tags_count"]=len(G.nodes[node]['synned_tags'])


        leaves_count = leaves_count +1 if G.in_degree(node)!=0 and G.out_degree(node)==0 and G.nodes[node]['type']=='canonical_tag' else leaves_count
        freeform_tags_count = freeform_tags_count +1 if G.nodes[node]['type']=='freeform_tag' else freeform_tags_count
        synned_tags_count = synned_tags_count +1 if G.nodes[node]['type']=='synned_tag' else synned_tags_count
        canonical_tags_count = canonical_tags_count +1 if G.nodes[node]['type']=='canonical_tag' else canonical_tags_count
        conection_node_count = conection_node_count +1 if G.nodes[node]['type']=='connection_node' else conection_node_count

    info_dic["big_nodes"]=', '.join(big_nodes)
    info_dic["total_nodes"]=G.nodes.__len__()
    info_dic["total_edges"]=G.edges.__len__()
    info_dic['total_canonical_leaves'] = leaves_count
    info_dic['total_freeform'] = freeform_tags_count
    info_dic['total_synned'] = synned_tags_count
    info_dic['total_canonical'] = canonical_tags_count
    info_dic['total_canonical_synned_connection_nodes'] = conection_node_count

    generate_report(info_dic,'report_G', w_mode)
    return info_dic

def get_G_diff_H_info(G:nx.DiGraph, H:nx.DiGraph, g_name='G_name', h_name='H_name', w_mode='w'):
    '''G-H= the subgraph of the nodes that are in G and not in H'''

    # LIst of  Nodes/edges that are in G that are not in H
    G_list_nodes=[node for node in G.nodes if not H.has_node(node)]


    g = G.subgraph(G_list_nodes)

    info_dic={}

    info_dic['report_info']= ''' Report information of the diff of two Networks
    report total amount of nodes/edges of both graphs,
    report nodes/edges that are in G that are not in H,
    report nodes/edges that are in G that are in H,
    '''
    info_dic['G_name']="G_name= "+g_name
    info_dic['G_total_nodes']=len(G.nodes)
    info_dic['G_total_edges']=len(G.edges)
    
    info_dic['H_name']="H_name= "+h_name
    info_dic['H_total_nodes']=len(H.nodes)
    info_dic['H_total_edges']=len(H.edges)
    
    info_dic['G_diff_H_total_nodes']=len(g.nodes)
    info_dic['G_diff_H_total_edges']=len(g.edges)

    info_dic['G_diff_H_nodes']=', '.join(list(g.nodes))
    info_dic['G_diff_H_edges']=str(list(g.edges))
    
    big_nodes=[]
    canonical_tags_count=0
    canonical_tags=[]
    synned_tags_count=0
    synned_tags=[]
    freeform_tags_count=0
    freeform_tags=[]
    conection_node_count=0
    leaves_count=0
    
    for node in g.nodes:
        leaves_count = leaves_count +1 if G.in_degree(node)!=0 and G.out_degree(node)==0 and G.nodes[node]['type']=='canonical_tag'else leaves_count
        if G.nodes[node]['type']=='freeform_tag':
            freeform_tags_count+=1
            freeform_tags.append(node)

        if G.nodes[node]['type']=='synned_tag':
            synned_tags_count+=1
            synned_tags.append(node)

        if G.nodes[node]['type']=='canonical_tag':
            canonical_tags_count+=1
            canonical_tags.append(node)

        conection_node_count = conection_node_count +1 if G.nodes[node]['type']=='connection_node' else conection_node_count
     
        if G.out_degree(node)>4:
            big_nodes.append(node)
        if G.out_degree(node)>4 and G.in_degree(node)<=1:
            info_dic[node+"_diff_out_degree"]=G.out_degree(node)
            info_dic[node+"_diff_in_degree"]=G.in_degree(node)
        if G.in_degree(node)>1:
            info_dic[node+"_diff_in_degree"]=G.in_degree(node)
            info_dic[node+"_diff_metatags"]=','.join([y for y in G.predecessors(node)])
        if 'synned_tags' in G.nodes[node]:
            info_dic[node+"_diff_synned_tags"]=','.join(G.nodes[node]['synned_tags'])
            info_dic[node+"_diff_synned_tags_count"]=len(G.nodes[node]['synned_tags'])

    info_dic["diff_big_nodes"]=', '.join(big_nodes)
    info_dic['diff_total_canonical_leaves'] = leaves_count
    info_dic['diff_total_freeform'] = freeform_tags_count
    info_dic['diff_freeform_tags'] = ', '.join(freeform_tags)
    info_dic['diff_total_synned'] = synned_tags_count
    info_dic['diff_synned_tags'] = ', '.join(synned_tags)
    info_dic['diff_total_canonical'] = canonical_tags_count
    info_dic['diff_sanonical_tags'] = ', '.join(canonical_tags)
    info_dic['diff_total_canonical_synned_connection_nodes'] = conection_node_count

    generate_report(info_dic, 'report_diff_G_H', w_mode)
    return info_dic


def get_G_H_political_acts_info(G:nx.DiGraph, H:nx.DiGraph, g_name='G_name', h_name='H_name', w_mode='w'):
    ''' 
    Mines the quantitative information of Political Acts done from H: old version of the network to G: new version
    returns a dictionary with all the changes:
    new syn/canonical/freeform tags
    removed tags
    canonized tags
    synonized tags
    '''
    info_dic={}

    info_dic['report_info']= ''' Report information of the Political acts displayed through time being G new version and H old version of the same network
    new type of tags
    canonized tags
    synonized tags
    removed tags
    '''
    info_dic['G_name']="G_name= "+g_name
    info_dic['G_total_nodes']=len(G.nodes)
    info_dic['G_total_edges']=len(G.edges)
    
    info_dic['H_name']="H_name= "+h_name
    info_dic['H_total_nodes']=len(H.nodes)
    info_dic['H_total_edges']=len(H.edges)
      
    canonized_tags=[]
    synonized_tags=[]

    new_freeform_tags=[]
    new_canonical_tags=[]
    new_syn_tags=[]
    
    removed_tags=[node for node in H.nodes if not G.has_node(node)]
    
    for node in G.nodes:
        
        canonized_tags.append(node) if H.has_node(node) and H.nodes[node]['type']=='freeform_tag' and G.nodes[node]['type']=='canonical_tag' else None
        synonized_tags.append((node,G.successors(node))) if H.has_node(node) and H.nodes[node]['type']=='canonical_tag' and G.nodes[node]['type']=='synned_tag' else None
        new_freeform_tags.append(node) if not H.has_node(node) and G.nodes[node]['type']=='freeform_tag' else None
        new_canonical_tags.append(node) if not H.has_node(node) and G.nodes[node]['type']=='canonical_tag' else None
        new_syn_tags.append(node) if not H.has_node(node) and G.nodes[node]['type']=='synned_tag' else None
        
    info_dic["canonized_tags"]=', '.join(canonized_tags)
    info_dic["canonized_tags_total"]=len(canonized_tags)
    
    info_dic["new_canonical_tags"]=len(new_canonical_tags)
    info_dic["new_canonical_tags_total"]=len(new_canonical_tags)

    info_dic["synonized_tags"]=', '.join(synonized_tags)
    info_dic["synonized_tags_total"]=len(synonized_tags)

    info_dic["new_syn_tags"]=len(new_syn_tags)
    info_dic["new_syn_tags_total"]=len(new_syn_tags)

    info_dic["new_freeform_tags"]=', '.join(new_freeform_tags)
    info_dic["new_freeform_tags_total"]=len(new_freeform_tags)

    info_dic["removed_tags"]=', '.join(removed_tags)
    info_dic["removed_tags_total"]=len(removed_tags)

    generate_report(info_dic, 'report_political_acts', w_mode)
    return info_dic

def generate_report(info_dic:dict, file_name='report', w_mode='w'):
    # f = open(file_name+".txt", "a")
    f = open(file_name+".txt", w_mode)
    f.write("="*100)
    f.write("\n")

    previous='-1'

    
    for item in info_dic:
        current= item.split("_")[0]
        if current!=previous:
            previous=current
            temp='='*100
            f.write('    '+temp)
            f.write("\n")

        info = info_dic[item]
        
        if item.__contains__('_metatags') or item.__contains__('degree'):
            f.write("\n")
            f.write('    '+item+" = "+ str(info)+"\n")
        else:
            f.write('    '+item+" = "+ str(info)+"\n")
    f.close()



def read_json_rata(database_path):
    """
    Recieves a File/Dir path to build the Networks
    FILE must be a JSON file with a RATAS mined
    DIR must be a directory only containing FILES

    return-> a list of networkX Nets
    """
    disability_graph_list=[]
    if os.path.isdir(database_path):
        for filename in os.listdir(database_path):
            # Get the path
            file_path=os.path.join(os.path.abspath(database_path), filename)
            # Open The JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                # Load the JSON
                current_data = json.load(f)
            f.close()
            # Build the Network
            g= net_build(current_data)
            # Append it to the list
            disability_graph_list.append(g)
    elif os.path.isfile(database_path):
        with open(database_path, 'r', encoding='utf-8') as f:
            # Load the JSON
            current_data = json.load(f)
        f.close()
        # Build the Network
        g= net_build(current_data)
        # Append it to the list
        disability_graph_list.append(g)
    return disability_graph_list

















