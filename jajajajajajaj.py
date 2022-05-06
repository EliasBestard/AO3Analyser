# %%
import json
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt 
from pyvis.network import Network
from Modules.NetVisualizer.net_visualizer import *
from Modules.NetBuilder.net_builder import net_build
from Utils.scripts import *
import pandas as pd
from random import randint
import seaborn as sns
from wordcloud import WordCloud
import collections
import numpy as np
import plotly.express as px
import math
from Utils import scraper_script


# %% [markdown]
# # Free form tags

# %%
# disability_ratas = read_json_rata('./OutputFiles/disability_rata_database/disability_rata_current.json')
disability_ratas = read_json_rata('./OutputFiles/full_disability_rata_current.json')

disability_ratas =  nx.DiGraph(disability_ratas[0])

# %%
a= open('./freeformtags.json').read()
a=a.split(',')
b=[item for item in a if not item in disability_ratas.nodes]
print(len(b))


# %%
# scraper_script.tagscra_list(b,of='disabilities_freeformtags',tags_per_iteration=40)


