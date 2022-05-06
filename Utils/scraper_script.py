# %%
from cProfile import label
import subprocess
import sys
import time
import random
import json
# import asyncio

# %%



def dascra_whole_tag_works(tag='Supernatural (TV 2005)', story_number=20):
    args_to_tags_scraper=['node', './Modules/DaScra/scraper.js']
    args_to_tags_scraper.extend(['-of','whole_'+tag+'_dascra_output'])
    args_to_tags_scraper.extend(['-op','./OutputFiles/'])
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

def tagscra_list(tags=[], tags_per_iteration=30, of='_tagscra_output_',op='./OutputFiles/',av='current'):

    args_to_tags_scraper=['node', './Modules/TagScraping/scraper.js']
    args_to_tags_scraper.extend(['-of',of])
    args_to_tags_scraper.extend(['-op',op])
    args_to_tags_scraper.extend(['-av',av])
    args_to_tags_scraper.extend(['-c'])
    args_to_tags_scraper.extend(['-v'])
    args_to_tags_scraper.extend(['-t'])




    with open(op+of+'.json', 'r', encoding='utf-8') as f:
        # Load the JSON
        current_data = json.load(f)
    f.close()
    
    tags=[item.replace("/",'*s*').replace(".",'*d*').replace('?','*q*') for item in tags if not item in current_data.keys()]
    print(len(tags))

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
            # for c in iter(lambda: process.stdout.read(1), b''): 
            #     sys.stdout.write(c.decode())
        print('')
        print('='*15+' Waiting '+str(waiting_time)+' minutes: '+time.ctime()+" "+'='*15)
        time.sleep(60*waiting_time) if i<tag_batch-1 else None
        args_to_tags_scraper = args_to_tags_scraper[:args_to_tags_scraper.index('-t')+1]

# tag,story_number=sys.argv[1:]
# dascra_whole_tag_works(tag, int(story_number))


# tag=["Disability", "Dsiable"]
# tagscra_list(tag)
