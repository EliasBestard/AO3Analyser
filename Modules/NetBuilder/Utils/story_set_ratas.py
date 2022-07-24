import networkx as nx
import pandas as pd
from Modules.NetBuilder.net_builder import net_build


def generate_story_set_net(type,df,ratas,year=2022):
    
    df=df[:500]
    additional_tags=process_story_set(df,ratas)

    df=df.loc[df["Updated"]<pd.Timestamp(int(year), 12, 31)]
    
    if type=="Full":
        net=story_set_full_tag_net(df,ratas,additional_tags)
    else:
        net=story_set_x_tag_net(type,df,ratas,additional_tags)
    return net


def process_story_set(stories_df,ratas):
    stories_df["DisabilityTags"]=stories_df.AdditionalTags.apply(lambda x : [item for item in x if ratas.has_node(item)])

    additional_tags={}

    for title, tag_list in zip(stories_df['Title'],stories_df['DisabilityTags']):
        for tag in tag_list:
            if not tag in additional_tags:
                additional_tags[tag]=[title]
            else:
                additional_tags[tag].append(title) if not title in additional_tags[tag] else None
    
    return additional_tags
    


def story_set_full_tag_net(df:pd.DataFrame,ratas:nx.DiGraph,additional_tags:dict):
    fulltag_net=nx.Graph()

    fulltag_net.add_nodes_from(df['Title'])
    # del(stories_df)

    for tag,list_titles in additional_tags.items():
        temp=nx.complete_graph(list_titles)
        fulltag_net.add_edges_from(list(nx.edges(temp)))

        if ratas.nodes[tag]['type']=='freeform_tag':
            for edges in list(nx.edges(temp)):
                fulltag_net[edges[0]][edges[1]]['color']='blue'
        if ratas.nodes[tag]['type']=='canonical_tag':
            for edges in list(nx.edges(temp)):
                fulltag_net[edges[0]][edges[1]]['color']='red'

        if ratas.nodes[tag]['type']=='synned_tag':
            for edges in list(nx.edges(temp)):
                fulltag_net[edges[0]][edges[1]]['color']='green'

    return fulltag_net


def story_set_x_tag_net(type,df:pd.DataFrame, ratas:nx.DiGraph, additional_tags:dict):
    _net=nx.Graph()
    _net.add_nodes_from(df['Title'])


    for tag,list_titles in additional_tags.items():
        temp=nx.complete_graph(list_titles)
        
        if type=="FreeForm" and ratas.nodes[tag]['type']=='freeform_tag':
            _net.add_edges_from(list(nx.edges(temp)))

        if type=="Canonical" and ratas.nodes[tag]['type']=='canonical_tag':
            _net.add_edges_from(list(nx.edges(temp)))

        if type=="Syn" and ratas.nodes[tag]['type']=='synned_tag':
            _net.add_edges_from(list(nx.edges(temp)))
    return _net

