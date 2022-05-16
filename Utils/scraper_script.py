
import subprocess
import sys
import time
import random
import json
import os
from Modules.NetBuilder.net_builder import net_build


def dascra_whole_tag_works(tag='Disability', story_number=20, **kwargs):
    '''
    Scrap all the stories for an specific tag
    Scripts that calls DaScra continuously until all stories for the tag specified are scraped
    Wait between 4-8 minutes between calls to do not overwhelm AO3 website


    It calls DaScra with: 
        -of out_name -op out_path -t tag -c -v

    :param tag: tag to mine the stories from
    :param story_number: number of stories wants to mine
    :param **kwargs: 'out_path' = './OutputFiles/', 'out_name' = 'dascra_output_'+tag_name
    :return None: generates/updates an Excel File with all the metadata for the stories
    '''

    out_path=kwargs['out_path'] if 'out_path' in kwargs else './OutputFiles/'
    out_name=kwargs['out_name'] if 'out_name' in kwargs else 'dascra_output_'+tag
    # verbose = 'verbose' in kwargs

    args_to_tags_scraper=['node', './Modules/DaScra/dascra.js']
    args_to_tags_scraper.extend(['-of',out_name])
    args_to_tags_scraper.extend(['-op',out_path])
    args_to_tags_scraper.extend(['-t', tag])
    args_to_tags_scraper.extend(['-c'])
    args_to_tags_scraper.extend(['-v']) 

    story_number=max(story_number//1000,1)
    for i in range(0,story_number):
        waiting_time= random.randint(4,8)
        print('')
        print('='*20+str(i+1)+"/"+str(story_number)+'='*20)
        with open('test.log', 'wb') as f: 
            process = subprocess.Popen(args_to_tags_scraper, stdout=subprocess.PIPE)
            for c in iter(lambda: process.stdout.read(1), b''): 
                sys.stdout.write(c.decode())
        print('')
        print('='*15+' Waiting '+str(waiting_time)+' minutes: '+time.ctime()+" "+'='*15)
        time.sleep(60*waiting_time) if i<story_number-1 else None

def tagscra_list(tags=[], tags_per_iteration=30, **kwargs):
    '''
    Scrap all the tags metadata for a list of tags
    Calls TagScra continuously until all tags are mined
    Wait between 4-5 minutes between a number of tags_per_iteration avoiding to overwhelm AO3 website


    It calls TagScra with: 
        -of out_name -op out_path -t tag -c -v -av av

    :param tags: list of tags to mine 
    :param tags_per_iteration: number of tags will mine for iteration before wait a number of minutes
    :param **kwargs: 'av' = 'current', 'out_path' = './OutputFiles/', 'out_name' = 'tagscra_output_'+av
    :return None: generates/updates a JSON File with all the metadata (RATAS) for the tags
    '''
    
    av = kwargs['av'] if 'av' in kwargs else 'current'
    out_path=kwargs['out_path'] if 'out_path' in kwargs else './OutputFiles/'
    out_name=kwargs['out_name'] if 'out_name' in kwargs else 'tagscra_output_'+av

    args_to_tags_scraper=['node', './Modules/TagScra/tagscra.js']
    args_to_tags_scraper.extend(['-of',out_name])
    args_to_tags_scraper.extend(['-op',out_path])
    args_to_tags_scraper.extend(['-av',av])
    args_to_tags_scraper.extend(['-c'])
    args_to_tags_scraper.extend(['-v'])
    args_to_tags_scraper.extend(['-t'])

    # if the file exists makes sure to mine tags that has not been mined already
    if os.path.isfile(out_path+out_name+'.json'):
        with open(out_path+out_name+'.json', 'r', encoding='utf-8') as f:
            # Load the JSON
            current_data = json.load(f)
        f.close()
    else: current_data={}    
    tags=[item.replace("/",'*s*').replace(".",'*d*').replace('?','*q*') for item in tags if not item in current_data.keys()]

    tag_batch = len(tags)//tags_per_iteration +1

    for i in range(0,tag_batch):
        batch= tags[i*tags_per_iteration:tags_per_iteration*(1+i)]
        # batch=list(map(lambda x: x.replace("/",'*s*').replace(".",'*d*'),batch))
        args_to_tags_scraper.extend(batch)

        waiting_time= random.randint(4,5)
        print('')
        print('='*40+" BATCH "+'='*40)
        print('='*40+str(i+1)+"/"+str(tag_batch)+'='*40)
        with open('test.log', 'wb') as f: 
            process = subprocess.Popen(args_to_tags_scraper, stdout=subprocess.PIPE)
            for c in iter(lambda: process.stdout.read(1), b''): 
                sys.stdout.write(c.decode())
        print('')
        print('='*15+' Waiting '+str(waiting_time)+' minutes: '+time.ctime()+" "+'='*15)
        time.sleep(60*waiting_time) if i<tag_batch-1 else None
        args_to_tags_scraper = args_to_tags_scraper[:args_to_tags_scraper.index('-t')+1]

def expand_rata(tag_scra_file, **kwargs):
    """expand_to_full_rata read a JSON file with its RATAS and expands it scrapping all the canonical tags
        will create a copy if required in th arguments 
    :param tag_scra_file: file to extend
    : kwargs['create_new_file']: name of the copy 
    """    
    rata= read_JSON(tag_scra_file)
    g= net_build(rata)

    # get nly the canonical nodes
    canonical_nodes =[node for node in g.nodes if g.nodes[node]['type']=='canonical_tag' and not g.nodes[node]['group']==0]
    out_name = os.path.basename(os.path.realpath(tag_scra_file))[:-5]
    out_path = os.path.dirname(os.path.realpath(tag_scra_file))+"\\"
    if 'create_new_file' in kwargs:
        with open(out_path+kwargs['create_new_file']+'.json', 'w',encoding='utf-8') as f:
            json.dump(rata, f,ensure_ascii=False)
        out_name = kwargs['create_new_file']
    tagscra_list(canonical_nodes,out_name=out_name,out_path=out_path)

def tagscra_non_canonical(tags=[], **kwargs):
    '''
    Scrap all non canonical tags under the Tag search in AO3
    Calls TagScra to generate a list of all non canonical tags of a list of tags
    Wait between 4-5 minutes between each tag in the list avoiding to overwhelm AO3 website


    It calls TagScra with: 
        -of out_name -op out_path -t tag -v -av av -ff

    :param tags: list of tags to mine 
    :param **kwargs: 'av' = 'current', 'out_path' = './OutputFiles/', 'out_name' = 'non_canonical_tagscra_output_'+tag
    :return None: generates/updates a JSON File with all the metadata (RATAS) for the tags
    '''
    
    av = kwargs['av'] if 'av' in kwargs else 'current'
    out_path=kwargs['out_path'] if 'out_path' in kwargs else './OutputFiles/'
    out_name=kwargs['out_name'] if 'out_name' in kwargs else 'tagscra_output_'

    args_to_tags_scraper=['node', './Modules/TagScra/tagscra.js']
    args_to_tags_scraper.extend(['-op',out_path])
    args_to_tags_scraper.extend(['-av',av])
    args_to_tags_scraper.extend(['-v'])
    args_to_tags_scraper.extend(['-ff'])
    args_to_tags_scraper.append('-of')

    for i in range(0,len(tags)):
        args_to_tags_scraper.append(out_name+tags[i]) 
        args_to_tags_scraper.append('-t')
        args_to_tags_scraper.append(tags[i])

        waiting_time= random.randint(4,5)
        print('')
        print('='*40+str(i+1)+"/"+str(len(tags))+'='*40)
        with open('test.log', 'wb') as f: 
            process = subprocess.Popen(args_to_tags_scraper, stdout=subprocess.PIPE)
            for c in iter(lambda: process.stdout.read(1), b''): 
                sys.stdout.write(c.decode())
        print('')
        print('='*15+' Waiting '+str(waiting_time)+' minutes: '+time.ctime()+" "+'='*15)
        # time.sleep(60*waiting_time) if i<len(tags)-1 else None

        args_to_tags_scraper = args_to_tags_scraper[:args_to_tags_scraper.index('-of')+1]

def expand_to_full_rata(rata_file,non_canonical_file, **kwargs):
    """expand_to_full_rata read a JSON file with its RATAS and a non_canonical RATAS file, both ouputs of TagScra
        Adds all freeform Tags to it 
    :param rata_file: file to extend
    :param non_canonical_file: file to extend
    : kwargs['create_new_file']: name of the copy 
    """    
    rata= read_JSON(rata_file)
    if os.path.isfile(non_canonical_file) and not rata=={}:
        g= net_build(rata)
        freeform_tags = open(non_canonical_file,'r', encoding='utf-8').read().split(',')
        freeform_tags=[tag for tag in freeform_tags if not tag in g.nodes]
        for tag in freeform_tags:
            rata[tag]={
                'type': 'freeform_tag',
                "parent_tags": [
                    "No Fandom"
                ],
                "synned_tags": [
                    ""
                ],
                "subtags": [
                    ""
                ],
                "metatags": [
                    ""
                ]
            }
        
        out_name= kwargs['create_new_file'] if 'create_new_file' in kwargs else 'full_tag_net'
        with open(os.path.dirname(os.path.realpath(rata_file))+"\\"+out_name+'.json', 'w',encoding='utf-8') as f:
            json.dump(rata, f,ensure_ascii=False)

def read_JSON(ratas_file):
    """read_JSON reads a JSON file outputed by TagScra and returns the dictionary with all teh RATAS

    :param ratas_file: path of the JSON file
    :return: return the dictionary containing all the RATAS with each root as key, {} if the file does not exists or empty
    """

    if os.path.isfile(ratas_file):
        with open(ratas_file, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        f.close()

        for key, value in dict(current_data).items():
            if value is None:
                del current_data[key]
    
        return current_data
    return {}

def read_json_rata(database_path):
    """
    Recieves a File/Dir path to build the Networks
    FILE must be a JSON file with a RATAS mined
    DIR must be a directory only containing FILES

    return-> a list of networkX Nets
    """
    disability_graph_list=[]
    net_names=[]
    if os.path.isdir(database_path):
        for filename in os.listdir(database_path):
            # Get the path
            file_path=os.path.join(os.path.abspath(database_path), filename)
            if not filename[-5:]=='.json':
                continue
            # Build the Network
            g= net_build(read_JSON(file_path))
            # Append it to the list
            disability_graph_list.append(g)
            net_names.append(filename[:-5])
    elif os.path.isfile(database_path):
        g=net_build(read_JSON(database_path))
        # Append it to the list
        disability_graph_list.append(g)
    return (disability_graph_list,net_names)

# tag,story_number=sys.argv[1:]
# dascra_whole_tag_works(tag, int(story_number))

# tag,story_number=sys.argv[1:]
# dascra_whole_tag_works(tag, int(story_number))
# tag=["Disability", "Dsiable"]
# tagscra_list(tag)
# tagscra_non_canonical(tag)
