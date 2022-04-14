# %%
from subprocess import check_output
import json
import networkx as nx
import matplotlib.pyplot as plt 
from pyvis.network import Network
from NetVisualizer.net_visualizer import net_visualize
from NetBuilder.net_builder import net_build
import pandas as pd

# %% [markdown]
# ## DaScra
# Uses Ricky's code to mine the archive and get a set of stories in a fandom and their information

# %%
# rick=['node', './DaScra/scraper.js']
# d = check_output(rick)

# %%
stories_df= pd.read_excel('dascra_output.xlsx',
              dtype={
                  'Additional Tags:': str, 'Archive Warning:': str,
                  'Author:': str, 'Bookmarks:': str,
                  'Category:': str, 'Chapters:': str,
                  'Characters:': str, 'Comments:': str,
                  'Fandom:': str, 'Hits:': int,
                  'Kudos:': int, 'Language:': str,
                  'Rating:': str, 'Relationship:': str,
                  'Series:': str, 'Part:': float,
                  'Source URL:': str, 'Title:': str,
                  'Updated:': str, 'Words:': str,
              }) 


# DO it better all in one pass
additional_tags=','.join([','.join(tags.split(",")) for tags in stories_df["Additional Tags:"]]).replace("/",'*s*').split(',')
print(len(additional_tags))
additional_tags = [item.strip() for item in additional_tags]
additional_tags=list(set(additional_tags))
print(len(additional_tags))

# %% [markdown]
# ## TagScra
# From a set of tags it scrap the RATAS in the archive and create JSON files with the info

# %%
tag_structure_file_name='current_tag_net'
# tag_structure_file_name='old_tag_net'

# tags_to_mine=['node', './TagScraping/scraper.js',"Reincarnation",'A lot of past lives','she lived 4 lives already',"Alternate Universe - Canon Divergence"]
# tags_to_mine=['node', './TagScraping/scraper.js',"Hogwarts Eighth Year",'Hogwarts Era',"Hogwarts Fourth Year"]
# tags_to_mine=['node', './TagScraping/scraper.js',tag_structure_file_name ,"Deaf Character", "Disability","Hogwarts Eighth Year",'Hogwarts Era',"Hogwarts Fourth Year"]
tags_to_mine=['node', './TagScraping/scraper.js',tag_structure_file_name ,"Disabled Character",]


# tags_to_mine=['node', './TagScraping/scraper.js,tag_structure_file_name']
# tags_to_mine.extend(additional_tags)

# p = check_output(tags_to_mine)

# %%
with open('./'+tag_structure_file_name+'.json', 'r', encoding='utf-8') as f:
  data = json.load(f)
f.close()

# %% [markdown]
# ## Building the Network and Visuals

# %%
G = net_build(data)
net_visualize(G, hierarchical_layout=False, node_sizes=True,headings="Tag Network of: "+ ",".join(tags_to_mine[3:]), file_name=tag_structure_file_name)

# %% [markdown]
# ## Getting the difference
# 

# %%
with open('./old_tag_net.json', 'r', encoding='utf-8') as f:
  old_data = json.load(f)

G_old= net_build(old_data)
net_visualize(G_old, hierarchical_layout=False, node_sizes=True,headings="Tag Network of: "+ ",".join(tags_to_mine[3:]), file_name="old_tag_net")


# %%
# INtersection
g= nx.intersection(G,G_old)
for node in g.nodes:
    g.nodes[node]['group']=G.nodes[node]['group']
    g.nodes[node]['title']=G.nodes[node]['title']
net_visualize(g, hierarchical_layout=False, node_sizes=True,headings="Intersection", file_name="temp")
    

# %%
for node in g.nodes:
    G.nodes[node]['group']=10
for node in G.nodes:
    G.nodes[node]['group']=10 if G.nodes[node]['group']==10 else 0
    G.nodes[node]['color']='green' if G.nodes[node]['group']==10 else 'blue'
net_visualize(G, hierarchical_layout=False, node_sizes=True,headings="Intersection", file_name="temp")



