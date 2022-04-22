# %%
from subprocess import check_output
import networkx as nx
from pyvis.network import Network
from Modules.NetVisualizer.net_visualizer import *
from Modules.NetBuilder.net_builder import net_build
from Utils.scripts import visualize_ratas_json

# %%
visualize_ratas_json('./OutputFiles/disability_rata_current.json',headings='Disability Rata currently', file_name='disability_rata_current')

# %%
visualize_ratas_json('./OutputFiles/disability_rata_2013.json',headings='Disability Rata 2013', file_name='disability_rata_2013')

