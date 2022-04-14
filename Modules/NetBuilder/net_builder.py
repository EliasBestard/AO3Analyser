
#%%
from boto import connect_ia
import networkx as nx
from sqlalchemy import null
from sympy import false


def net_build(data):
    """
    Receives the data: JSON information mined in TagScra and build the network
    """
    G = nx.DiGraph()
    for tag in data:
        if data[tag]["type"]=="canonical_tag":
                       
            G.add_node(tag) if not G.has_node(tag) else None 
            G.nodes[tag]['group']=0
            G.nodes[tag]['title']="<h3>"+tag+"<h3>" 
            # G.nodes[tag]['title']="<h3>"+tag+"<h3>" + "<br> ".join(data[tag]['synned_tags'])
            # G.nodes[tag]['synned_tags']=data[tag]['synned_tags']
            G.nodes[tag]['color']='blue'
                        
            add_subtags(G,data[tag]['subtags'],tag)
            add_metatags(G,data,tag)

        elif data[tag]["type"]=="freeform_tag":
            G.add_node(tag) if not G.has_node(tag) else None
            G.nodes[tag]['group']="freeform_tag"
            G.nodes[tag]['title']=tag
    return G

def add_metatags(G:nx.DiGraph,data, metatag):
    """
    Given a graph G and the scrapped data from TagScraper (JSON) and a metatag
    adds the metatag to the nodes and all their incoing connections with its tags
    """
    
    for item in data[metatag]["metatags"]:
        if item=="" or (G.has_node(item) and G.has_edge(item, metatag)):
            continue
        G.add_node(item)
        G.nodes[item]['group']=min(G.nodes[item]['group'],1) if G.nodes[item].__contains__('group') else 1
        G.nodes[item]['title']=G.nodes[item]['title'] if G.nodes[item].__contains__('title') else item
        G.nodes[item]['color']=G.nodes[item]['color'] if G.nodes[item].__contains__('color') else "read"
        G.add_edge(item, metatag)

    # for item in data[metatag]["subtags"]:
    #     if item=="" or (G.has_node(item) and G.has_edge(metatag, item)):
    #         continue
    #     if type(item)==str:
    #         G.add_node(item) 
    #         G.add_edge(metatag,item)

    #         G.nodes[item]['group']=min(G.nodes[item]['group'],2) if G.nodes[item].__contains__('group') else 2
    #         G.nodes[item]['title']=G.nodes[item]['title'] if G.nodes[item].__contains__('title') else item 
    #     elif type(item)==dict:
    #         child=list(item.keys())[0]
    #         G.add_node(child) 
    #         G.add_edge(metatag,child)

    #         G.nodes[child]['group']=min(G.nodes[child]['group'],2) if G.nodes[child].__contains__('group') else 2
    #         G.nodes[child]['title']=G.nodes[child]['title'] if G.nodes[child].__contains__('title') else child

    #         for grandchild in item[child]:
    #             G.add_node(grandchild)
    #             G.add_edge(child, grandchild)

    #             G.nodes[grandchild]['group']=min(G.nodes[grandchild]['group'],3) if G.nodes[grandchild].__contains__('group') else 3
    #             G.nodes[grandchild]['title']=G.nodes[grandchild]['title'] if G.nodes[grandchild].__contains__('title') else grandchild
    return G


def add_subtags(G:nx.DiGraph,data, metatag):
    """
    Given a graph G and the scrapped data from TagScraper (JSON) and a metatag
    adds the metatag to the nodes and all their ongoing/ingoing connections with its tags
    """
    my_stack=[]
    for item in data:
        if item=='':
            continue
        if type(item)==str:
            G.add_node(item) if not G.has_node(item) else None 
            G.add_edge(metatag,item) if not G.has_edge(metatag,item) else None
            G.nodes[item]['title']=item
            G.nodes[item]['color']='yellow'
        else:
            current_tag=list(item.keys())[0]
            G.add_node(current_tag) if not G.has_node(current_tag) else None 
            G.add_edge(metatag,current_tag) if not G.has_edge(metatag,current_tag) else None
            G.nodes[current_tag]['title']=current_tag
            G.nodes[current_tag]['color']="yellow"
            my_stack.append(item)

    while (len(my_stack)>0):
        current_element = my_stack.pop(0)
        current_tag = list(current_element.keys())[0]

        for item in current_element[current_tag]:
            if item=='':
                continue
            if type(item)==str:
                G.add_node(item) if not G.has_node(item) else None 
                G.add_edge(current_tag,item) if not G.has_edge(current_tag,item) else None
                G.nodes[item]['title']=item
                G.nodes[item]['color']="orange"
            else:
                next_tag = list(item.keys())[0]
                G.add_node(next_tag) if not G.has_node(next_tag) else None 
                G.add_edge(current_tag, next_tag) if not G.has_edge(current_tag,next_tag) else None
                G.nodes[next_tag]['title']=next_tag
                G.nodes[next_tag]['color']="orange"

                my_stack.append(item)

    return G