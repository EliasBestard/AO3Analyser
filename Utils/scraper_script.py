# %%
import subprocess
import sys
import time
import random
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

tag,story_number=sys.argv[1:]

dascra_whole_tag_works(tag, int(story_number))

