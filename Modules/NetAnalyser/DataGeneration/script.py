import json
import os

from Modules.NetVisualizer.net_visualizer import *
from Modules.NetBuilder.net_builder import net_build
import pandas as pd


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

def gen_tags_dataset(G:nx.DiGraph, H:nx.DiGraph, generate_csv=True, path='./OutputFiles'):
    ''' 
    Generates a dataset with all the tags, its precense in each Graph and its type
    Tags | H_presence | G_presence | H_type | G_type
    '''
    columns={}
    df = pd.DataFrame(columns=['Tags', 'H_presence', 'G_presence', 'H_type', 'G_type','Action'])

    df.Tags=list(set(G.nodes).union(set(H.nodes)))


    for tag in df.Tags:
        df.loc[df.Tags==tag,'H_presence']= H.has_node(tag)
        df.loc[df.Tags==tag,'G_presence']= G.has_node(tag)
        df.loc[df.Tags==tag,'H_type']= H.nodes[tag]['type'] if  H.has_node(tag) else nan
        df.loc[df.Tags==tag,'G_type']= G.nodes[tag]['type'] if  G.has_node(tag) else nan

        if not H.has_node(tag):
            df.loc[df.Tags==tag,'Action']= 'addition'
        elif G.has_node(tag) and (H.nodes[tag]['type']=='freeform_tag' or H.nodes[tag]['type']=='synned_tag') and G.nodes[tag]['type']=='canonical_tag':
            df.loc[df.Tags==tag,'Action']= 'canonized'
        elif G.has_node(tag) and (H.nodes[tag]['type']=='freeform_tag' or H.nodes[tag]['type']=='canonical_tag') and G.nodes[tag]['type']=='synned_tag':
            df.loc[df.Tags==tag,'Action']= 'sinonized'
        elif not G.has_node(tag):
            df.loc[df.Tags==tag,'Action']= 'removed'

    if generate_csv:
        df.to_csv(path+'/G_H_tags_report.csv')    
    return df

def gen_tags_dataset_list(net_lists:list, generate_csv=True, path='./OutputFiles'):
    ''' 
    '''
    columns=["Tags"]
    [columns.extend(["G_"+str(i)+"_presence","G_"+str(i)+"_type"]) for i in range(0, len(net_lists))]

    df = pd.DataFrame(columns=columns)
    tag_set= set(list([]))
    for element in net_lists:
        tag_set=tag_set.union(set(element.nodes))
    df.Tags=list(tag_set)

    for tag in df.Tags:
        for i in range(0,len(net_lists)):
            df.loc[df.Tags==tag,columns[1+i*2]]= net_lists[i].has_node(tag)
            df.loc[df.Tags==tag,columns[1+i*2+1]]= net_lists[i].nodes[tag]['type'] if  net_lists[i].has_node(tag) else nan

    if generate_csv:
        df.to_csv(path+'/G_H_tags_report.csv')    
    return df

