import networkx as nx

import os


def add_non_canonical_nodes(G:nx.DiGraph,non_canonical_file):
    """add_non_canonical_nodes Updates G DiGraph and adds all the tags in non_canonical_file as freeform
        iterates for all the non_canonical tags and add the ones that does not belong to the RATA as freeform tags,
        asumes that the ones that belongs are synned_tags 

    :param G: Graph rooted-RATA
    :param non_canonical_file: non_canonical tags for the root of the RATA
    """
    if os.path.isfile(non_canonical_file):
        file= open(non_canonical_file,'r',encoding='UTF8').read()
        file=file.split(',')
        print(len(file))
        file=[item for item in file if not item in G.nodes]
        print(len(file))
        for tag in file:
            G.add_node(tag) if not G.has_node(tag) else None
            G.nodes[tag]['group']="freeform_tag"
            G.nodes[tag]['type']="freeform_tag"
            G.nodes[tag]['title']=tag
            G.nodes[tag]['color']='#5D6D7E'


def net_build(data:dict):
    """net_build Builds a NetwrokX DiGraph from a dictionary that contains all the rooted-RATAS as keys and they connections, type
            Properties of Nodes:
                color: Red for Metatags, Blue for current tags (mined tags), Orange first children, Yellow grandchildren and bellow
                type: canonical_tag, freeform_tag, synned_tag, or connection_node for the node conecting a group of synned tags with their canonical_tag
                synned_tags: list of all synned tags, ONLY for canonical tags
                title: Name of the tag
                shape: connection_nodes square, synned_tags triangle, all the rest: circle


    :param dict data: dictionary containing all RATAS 
    :return: DiGraph
    """    

    G = nx.DiGraph()
    for tag in data:
        if tag==None:
            continue
        tag=tag.strip()
        if data[tag]["type"]=="canonical_tag":
            
            data[tag]["synned_tags"].remove('') if '' in data[tag]["synned_tags"] else None

            G.add_node(tag) if not G.has_node(tag) else None 
            G.nodes[tag]['type']="canonical_tag"
            G.nodes[tag]['group']=0
            G.nodes[tag]['synned_tags']=data[tag]['synned_tags']
            G.nodes[tag]['title']="<h3>"+tag+"<h3>" 
            # G.nodes[tag]['title']="<h3>"+tag+"<h3>" + "<br> ".join(data[tag]['synned_tags'])
            G.nodes[tag]['color']='#2E86C1'
            

            __add_full_subtags(G,data[tag]['subtags'],tag) 
            __add_metatags(G,data,tag)
            __add_synned_tags(G,tag,data[tag]['synned_tags'])  if len(data[tag]['synned_tags'])>0 else None

        elif data[tag]["type"]=="freeform_tag":
            G.add_node(tag) if not G.has_node(tag) else None
            G.nodes[tag]['group']="freeform_tag"
            G.nodes[tag]['type']="freeform_tag"
            G.nodes[tag]['title']=tag
            G.nodes[tag]['color']='#5D6D7E'
        
        elif data[tag]["type"]=="synned_tag":
            G.add_node(tag) if not G.has_node(tag) else None
            G.nodes[tag]['group']="synned_tag"
            G.nodes[tag]['type']="synned_tag"
            G.nodes[tag]['shape']='triangle'
            G.nodes[tag]['color']='#BB8FCE'

            canonical_tag=data[tag]["cannonical_tag"]
            if not G.has_node(data[tag]["cannonical_tag"]):
                G.add_node(canonical_tag) 
                G.nodes[canonical_tag]['type']="canonical_tag"
                G.nodes[canonical_tag]['group']=0
                G.nodes[canonical_tag]['title']="<h3>"+canonical_tag+"<h3>" 
                G.nodes[canonical_tag]['color']='#2E86C1'
            __add_synned_tags(G,canonical_tag,[tag])

    __update_title(G)
    return G

def __add_synned_tags(G:nx.DiGraph, node, synned_tags:list):
    """__add_synned_tags Updates a G: DiGraph for a canonical_tag adding to it a list of synned tags

    :param G: Digraph
    :param node: canonical_tag
    :param synned_tags: syn tags to attach to node
    """    
    synned_tag_node=node+'_synned_tags'
    
    G.add_node(synned_tag_node)
    G.add_edge(node,synned_tag_node)
    G.add_edge(synned_tag_node,node)
    G.nodes[synned_tag_node]['type']='connection_node'
    G.nodes[synned_tag_node]['group']="connection_node"
    G.nodes[synned_tag_node]['title']=node+'_synned_tags'
    G.nodes[synned_tag_node]['shape']='square'
    G.nodes[synned_tag_node]['color']='#8E44AD'

    for tag in synned_tags:
        G.add_node(tag)
        G.add_edge(synned_tag_node,tag)
        G.nodes[tag]['type']='synned_tag'
        G.nodes[tag]['shape']='triangle'
        G.nodes[tag]['color']='#BB8FCE'
        G.nodes[tag]['group']="synned_tag"

def __add_metatags(G:nx.DiGraph,data, tag):
    """__add_metatags Given a graph G and the scrapped data from TagScraper (JSON) and a canonical_tag
    Updates G adding the metatags to the tag 

    :param G: DiGraph  RATAS
    :param data: data dictionary with all teh RATAS information
    :param tag: canonical tag
    """ 
    
    for item in data[tag]["metatags"]:
        if item=="" or (G.has_node(item) and G.has_edge(item, tag)):
            continue
        G.add_node(item)
        G.nodes[item]['group']=min(G.nodes[item]['group'],1) if G.nodes[item].__contains__('group') else 1
        G.nodes[item]['title']=G.nodes[item]['title'] if G.nodes[item].__contains__('title') else item
        G.nodes[item]['color']=G.nodes[item]['color'] if G.nodes[item].__contains__('color') else "#CB4335"
        G.nodes[item]['type']='canonical_tag'
        G.add_edge(item, tag)

    
def __add_full_subtags(G:nx.DiGraph,data, metatag):
    """__add_full_subtags Given a graph G and the scrapped data from TagScraper (JSON) and a metatag
    adds the all their ongoing connections

    :param G: RATAS DiGraph
    :param data: _description_
    :param metatag: _description_
    """    
    
    my_stack=[]
    for item in data:
        if item=='':
            continue
        if type(item)==str:
            G.add_node(item) if not G.has_node(item) else None 
            G.add_edge(metatag,item) if not G.has_edge(metatag,item) else None
            G.nodes[item]['type']='canonical_tag'
            G.nodes[item]['title']=item
            G.nodes[item]['color']='#CA6F1E'
            G.nodes[item]['group']=2

        else:
            current_tag=list(item.keys())[0]
            G.add_node(current_tag) if not G.has_node(current_tag) else None 
            G.add_edge(metatag,current_tag) if not G.has_edge(metatag,current_tag) else None
            G.nodes[current_tag]['type']='canonical_tag'
            G.nodes[current_tag]['title']=current_tag
            G.nodes[current_tag]['color']="#CA6F1E"
            G.nodes[current_tag]['group']=2
            my_stack.append(item)
    count_group=2
    while (len(my_stack)>0):
        count_group+=1
        current_element = my_stack.pop(0)
        current_tag = list(current_element.keys())[0]

        for item in current_element[current_tag]:
            if item==''or item==None:
                continue
            if type(item)==str:
                G.add_node(item) if not G.has_node(item) else None 
                G.add_edge(current_tag,item) if not G.has_edge(current_tag,item) else None
                G.nodes[item]['type']='canonical_tag'
                G.nodes[item]['title']=item
                G.nodes[item]['color']="#D4AC0D"
                G.nodes[item]['group']=count_group
            else:
                next_tag = list(item.keys())[0]
                G.add_node(next_tag) if not G.has_node(next_tag) else None 
                G.add_edge(current_tag, next_tag) if not G.has_edge(current_tag,next_tag) else None
                G.nodes[next_tag]['type']='canonical_tag'
                G.nodes[next_tag]['title']=next_tag
                G.nodes[next_tag]['color']="#D4AC0D"
                G.nodes[next_tag]['group']=count_group

                my_stack.append(item)


def __update_title(G:nx.DiGraph):
    """__update_title Updates the title of all the nodes in a Graph
        no title for synned tags
    :param G: RATA
    """    
    for node in G.nodes:
        #if it is not a synned tag which are the ones without a title
        if G.nodes[node]['type']=='canonical_tag' or G.nodes[node]['type']=='freeform_tag':
            title = "<br> Subtags: "+str(G.out_degree(node))
            title += "<br> Metatags: "+str(G.in_degree(node))
            # title += "<br>Subtags: "+G.out_degree(node)
            G.nodes[node]['title']=G.nodes[node]['title']+title 
        if  G.nodes[node]['type']=='connection_node':
            title = "<br> Synned Tags: "+str(G.out_degree(node))
            G.nodes[node]['title']=G.nodes[node]['title']+title 



