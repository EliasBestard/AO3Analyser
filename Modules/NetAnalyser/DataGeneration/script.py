from Modules.NetVisualizer.net_visualizer import *
from Modules.NetBuilder.net_builder import net_build
import pandas as pd


def get_G_properties(G:nx.DiGraph):
    """get_G_properties mine the main properties of a RATAS and generate 4 main datasets with the general info
    
    generates 4 datasets:
    df_nodes_large_in: all nodes with more than 1 indegree, their parents and their indegree
    df_canonical_nodes_with_syn: all canonical tags that have a syn group attached with their synned_tags
    df_nodes_large_out: all nodes with more than 4 outdegree, their outdegree and indegree
    df_general_inf: General information of the RATAS as a graph, number of nodes, edges, etc.

    :param G: RATAS DiGraph
    :return: dict with the name of the dataset as key and the datasets with the RATAS information in
    """    
    # df with the general information of the graph
    df_general_inf = pd.DataFrame(columns=['Properties','Values'])
    
    dict_info={'Properties':'information','Values':''' Report Node information of nodes with
        outdegree greater than 4, or indegree greater than 1
        report total amount of nodes, edges, leaves, freeform/canonical/synned tags, nodes with more than 4 subtags, 
        '''}
    df_general_inf.append(dict_info, ignore_index = True)
    
    big_nodes=[]
    leafs_count=0
    freeform_tags_count=0
    synned_tags_count=0
    canonical_tags_count=0
    conection_node_count=0

    #Store nodes with more than one parent
    df_nodes_large_in=pd.DataFrame(columns=['Node','in_degree', 'Metatags'])
    #canonical nodes with synned tags
    df_canonical_nodes_with_syn=pd.DataFrame(columns=['Node','Count','SynnedTags'])
    # NOdes with outdegree greater than 4 
    df_nodes_large_out=pd.DataFrame(columns=['Node','out_degree', 'in_degree'])

    for node in G.nodes:
        big_nodes.append(node) if G.out_degree(node)>4 else None
        
        if G.out_degree(node)>4:
            df_nodes_large_out=df_nodes_large_out.append({
                'Node':node,
                'out_degree':G.out_degree(node),
                'in_degree':G.in_degree(node)
            }, ignore_index = True)
        if G.in_degree(node)>1:
            df_nodes_large_in=df_nodes_large_in.append({
                'Node':node,
                'Metatags':','.join([y for y in G.predecessors(node)]),
                'in_degree':G.in_degree(node)
            }, ignore_index = True)
        if 'synned_tags' in G.nodes[node] and len(G.nodes[node]['synned_tags'])>0:
            df_canonical_nodes_with_syn=df_canonical_nodes_with_syn.append({
                'Node':node,
                'SynnedTags':','.join(G.nodes[node]['synned_tags']),
                'Count':len(G.nodes[node]['synned_tags'])
                }, ignore_index = True)
        
        leafs_count = leafs_count +1 if G.in_degree(node)!=0 and G.out_degree(node)==0 and G.nodes[node]['type']=='canonical_tag' else leafs_count
        freeform_tags_count = freeform_tags_count +1 if G.nodes[node]['type']=='freeform_tag' else freeform_tags_count
        synned_tags_count = synned_tags_count +1 if G.nodes[node]['type']=='synned_tag' else synned_tags_count
        canonical_tags_count = canonical_tags_count +1 if G.nodes[node]['type']=='canonical_tag' else canonical_tags_count
        conection_node_count = conection_node_count +1 if G.nodes[node]['type']=='connection_node' else conection_node_count

    df_general_inf=df_general_inf.append({'Properties':"big_nodes",
        'Values':', '.join(big_nodes)
        }, ignore_index = True)
    df_general_inf=df_general_inf.append({'Properties':"total_nodes",
        'Values':G.nodes.__len__()
        }, ignore_index = True)
    df_general_inf=df_general_inf.append({'Properties':"total_edges",
        'Values':G.edges.__len__()
        }, ignore_index = True)
    df_general_inf=df_general_inf.append({'Properties':"total_canonical_leafs",
        'Values':leafs_count
        }, ignore_index = True)
    df_general_inf=df_general_inf.append({'Properties':"total_freeform",
        'Values':freeform_tags_count
        }, ignore_index = True)
    df_general_inf=df_general_inf.append({'Properties':"total_synned",
        'Values':synned_tags_count
        }, ignore_index = True)
    df_general_inf=df_general_inf.append({'Properties':"total_canonical",
        'Values':canonical_tags_count
        }, ignore_index = True)
    df_general_inf=df_general_inf.append({'Properties':"total_canonical_synned_connection_nodes",
        'Values':conection_node_count
        }, ignore_index = True)
    

    return {
        'general_information':df_general_inf,
        'large_indegree_nodes':df_nodes_large_in,
        'large_outdegree_nodes':df_nodes_large_out,
        'canonical_nodes_with_synset':df_canonical_nodes_with_syn
    }



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


def get_G_H_political_acts_info(G:nx.DiGraph, H:nx.DiGraph, g_name='G_name', h_name='H_name'):
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




def generate_tag_diff_dataset(G:nx.DiGraph, H:nx.DiGraph,**kwargs):
    """generate_tag_diff_dataset Generates a dataset with all the tags, its precense in each Graph and its type
    Tags | H_presence | G_presence | H_type | G_type

    :param **kwargs: generate_csv: boolean to generate the csv or not
                    path: path to save the file
                    file_name: file name
    :param G: RATAS Digraph
    :param H: RATAS Digraph
    :return: dataframe
    """    

    H.name= H.name if not H.name=='' else 'H'
    G.name= G.name if not G.name=='' else 'G'
    
    generate_csv = kwargs['generate_csv'] if 'generate_csv' in kwargs else True
    path = kwargs['path'] if 'path' in kwargs else './OutputFiles'
    file_name = kwargs['file_name'] if 'file_name' in kwargs else 'G_H_tags_report'

    df = pd.DataFrame(columns=['Tags', H.name+'_precence', G.name+'_presence', H.name+'_type', G.name+'_type','Action'])

    df.Tags=list(set(G.nodes).union(set(H.nodes)))


    for tag in df.Tags:
        df.loc[df.Tags==tag,H.name+'_precence']= H.has_node(tag)
        df.loc[df.Tags==tag,G.name+'_presence']= G.has_node(tag)
        df.loc[df.Tags==tag,H.name+'_type']= H.nodes[tag]['type'] if  H.has_node(tag) else None
        df.loc[df.Tags==tag,G.name+'_type']= G.nodes[tag]['type'] if  G.has_node(tag) else None
        if not H.has_node(tag):
            df.loc[df.Tags==tag,'Action']= 'addition'
        elif G.has_node(tag) and (H.nodes[tag]['type']=='freeform_tag' or H.nodes[tag]['type']=='synned_tag') and G.nodes[tag]['type']=='canonical_tag':
            df.loc[df.Tags==tag,'Action']= 'canonized'
        elif G.has_node(tag) and (H.nodes[tag]['type']=='freeform_tag' or H.nodes[tag]['type']=='canonical_tag') and G.nodes[tag]['type']=='synned_tag':
            df.loc[df.Tags==tag,'Action']= 'sinonized'
        elif not G.has_node(tag):
            df.loc[df.Tags==tag,'Action']= 'removed'

    if generate_csv:
        df.to_csv(path+'/'+file_name+'.csv', index=False)    
    return df

def gen_tags_dataset_list(net_list:list, **kwargs):
    """gen_tags_dataset_list generate a dataset with all the tags in all the networks and their precense in each of the networks
    :param **kwargs:
                    generate_csv: boolean to generate or not a csv
                    path: path to save the document
                    file_name: name of the csv file
                    net_names: list of names of each network
    :param net_list: network list assuming cronologycal 
    :return: df
    """    
    generate_csv = kwargs['generate_csv'] if 'generate_csv' in kwargs else True
    path = kwargs['path'] if 'path' in kwargs else './OutputFiles'
    file_name = kwargs['file_name'] if 'file_name' in kwargs else 'G_H_tags_report'
    net_names = kwargs['net_names'] if 'net_names' in kwargs else ['G_'+str(i) for i in range(len(net_list))]

    columns=["Tags"]
    [columns.extend([element+"_presence",element+"_type"]) for element in net_names]

    df = pd.DataFrame(columns=columns)
    tag_set= set(list([]))
    for element in net_list:
        tag_set=tag_set.union(set(element.nodes))
    df.Tags=list(tag_set)

    for tag in df.Tags:
        for i in range(0,len(net_list)):
            df.loc[df.Tags==tag,columns[1+i*2]]= net_list[i].has_node(tag)
            df.loc[df.Tags==tag,columns[1+i*2+1]]= net_list[i].nodes[tag]['type'] if  net_list[i].has_node(tag) else None
    net_list[-1].name=net_names[-1]
    
    for i in range(len(net_list)-1):
        net_list[i].name=net_names[i]
        df_temp= __political_acts_between_two_ratas(net_list[-1],net_list[i])
        df= df.merge(df_temp,on='Tags',how='outer')

    if generate_csv:
        df.to_csv(path+'/'+file_name+'.csv')    
    return df

def __political_acts_between_two_ratas(rata_new_ver:nx.DiGraph, rata_old_ver:nx.DiGraph,**kwargs):
    action_column='FROM_'+rata_old_ver.name+'_TO_'+rata_new_ver.name+'_Action'
    df = pd.DataFrame(columns=['Tags',action_column])
    df.Tags=list(set(rata_new_ver.nodes).union(set(rata_old_ver.nodes)))


    for tag in df.Tags:
        if not rata_old_ver.has_node(tag):
            df.loc[df.Tags==tag,action_column]= 'addition'
        elif rata_new_ver.has_node(tag) and (rata_old_ver.nodes[tag]['type']=='freeform_tag' or rata_old_ver.nodes[tag]['type']=='synned_tag') and rata_new_ver.nodes[tag]['type']=='canonical_tag':
            df.loc[df.Tags==tag,action_column]= 'canonized'
        elif rata_new_ver.has_node(tag) and (rata_old_ver.nodes[tag]['type']=='freeform_tag' or rata_old_ver.nodes[tag]['type']=='canonical_tag') and rata_new_ver.nodes[tag]['type']=='synned_tag':
            df.loc[df.Tags==tag,action_column]= 'sinonized'
        elif not rata_new_ver.has_node(tag):
            df.loc[df.Tags==tag,action_column]= 'removed'
    
    return df

def save_xls(list_dfs:dict, xls_path):
    """save_xls Save a list of data frame into different sheets of a xlsx

    :param list_dfs: _description_
    :param xls_path: _description_
    """    

    with pd.ExcelWriter(xls_path+'.xlsx') as writer:
        for name, df in list_dfs.items():
            df.to_excel(writer,name,index=False)