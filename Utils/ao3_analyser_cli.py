import argparse
import os
from numpy import integer

from sympy import arg
import Utils.scraper_script as scraper
import Modules.NetBuilder.net_builder as net_builder
import Modules.NetVisualizer.net_visualizer as net_visualizer
import Modules.NetAnalyser.net_analyser as net_analiser
import pandas as pd
# # CLI

parser = argparse.ArgumentParser(prog="ao3_analyser")

# ## TagScra
parser.add_argument("-ts", "--TagScra",
                    help="Call TagScra Module witht a list of focus tags as arguments to mine. Genereate a JSON file with the RATAS",
                    nargs='+'
                    )
parser.add_argument("-ao3_v", "--AO3Version",
                    help="TagScra argument that specifies the version (year) for which TagScra accesses AO3 using the Wayback Machine",
                    type=str,
                    default='current',
                    nargs=1
                    )
parser.add_argument("--NonCanonical",
                    help="TagScra argument that mines and genereates all non canonical tags related with the focus tag received as argument",
                    action='store_true',
                    default=False
                    )
# ##
parser.add_argument("--ExpandRATAS", help="""Call TagScra to expand a RATAS. It receives a RATAS JSON file mining all canonical tags for its expansion. It outputs a RATAS JSON file with the Expanded RATAS.""",
                    type=str)
parser.add_argument("--ExpandFullRATAS", help="""Call TagScra to fully expand a RATAS. It receives an Expanded RATAS JSON file and a TXT with all non-canonical tags. It outputs a JSON file with the Fully Expanded RATAS.""",
                    nargs=2)


# ## DaScra
parser.add_argument("-ds", "--DaScra",
                    help="Calls DaScra Module witht the Tag to mine all its fan-works and genereate a xlsx file with the Story-Set metadata",
                    type=str
                    # default='Disability'
                    )
parser.add_argument("--StoryNumber", help="DaScra argument to set the number of fan-work to scrap",
                    type=int,
                    default=1000)

# ## TagScra & DaScra0
parser.add_argument("-o","--OutputName", help="Set the name of the file generated file",
                    type=str,
                    default='default_name')
parser.add_argument("-op","--OutputPath", help="Set the path to store the generated file",
                    type=str,
                    default='./OutputFiles/')


# ## Netbuilder & Visualizer
parser.add_argument("-gn","--GenerateNetwork", help="Build a RATA and generates its visualization. Recieves a RATAS JSON file. Outputs and shows the visualization of the RATAS.",
                    type=str, nargs=1)

parser.add_argument("--GenerateFullTagNetwork", help="Build the Story-Set & RATAS Full Tag Network and generates its visualization. Recieves a RATAS JSON file and a Story-Set. Outputs and shows the visualization of the Full Tag Network.",
                    nargs=2)
parser.add_argument("--GenerateSynTagNetwork", help="Build the Story-Set & RATAS Syn Tag Network and generates its visualization. Recieves a RATAS JSON file and a Story-Set. Outputs and shows the visualization of the Syn Tag Network.",
                    nargs=2)
parser.add_argument("--GenerateCanonicalTagNetwork", help="Build the Story-Set & RATAS Canonical Tag Network and generates its visualization. Recieves a RATAS JSON file and a Story-Set. Outputs and shows the visualization of the Canonical Tag Network.",
                    nargs=2)
parser.add_argument("--GenerateFreeFormTagNetwork", help="Build the Story-Set & RATAS Free-Form Tag Network and generates its visualization. Recieves a RATAS JSON file and a Story-Set. Outputs and shows the visualization of the Free-Form Tag Network.",
                    nargs=2)
parser.add_argument("--StorySetYear", help="Set the year of the Story-Set & RATAS Netowrks. It filters the Sotry-Set for all the fan-works before the year inputed as argument.",
                    default=2022)

# ## Visualizer -- Net Diff, Intersection, etc
parser.add_argument("-gs","--GenerateSimilarites", help="Generates the visualizations highlighting the similarities between two RATAS. It receives two RATAS JSON files assuming the first is the older version.",
                    nargs=2)
parser.add_argument("-gd","--GenerateDifferences", help="Generates the visualizations highlighting the differences between two RATAS. It receives two RATAS JSON files assuming the first is the older version.",
                    nargs=2)


# ## Reports
parser.add_argument("--GenerateRATASProperties", help="Generates a report with the main properties of a snapshot of a RATAS. It receives a RATAS JSON files. It outputs a xslx file with different information of the RATAS.",
                    nargs=1)
parser.add_argument("--GenTagDiff", help="Generates a report with the differences of two RATAS. It receives two RATAS JSON files assuming the first one is the older version. It outputs a xslx file with the differences between the RATAS.",
                    nargs=2)
parser.add_argument("--GenTagDiffDir", help="Generates a report with the differences between a set of RATAS. It receives directory full of  RATAS JSON files assuming they are sorted from older to most recent version. It outputs a xslx file with the differences between the RATAS.",
                    nargs=1)
def parse():
    """
    Parse the arguments in the CLI and call the methods
    """
    args = parser.parse_args()

    print()

    if args.TagScra and not args.NonCanonical :
        print('='*15 + " Invoking TagScra " + '='*15)
        scraper.tagscra_list(args.TagScra,out_path=args.OutputPath,out_name=args.OutputName, av=args.AO3Version)
        return []
    elif args.TagScra and args.NonCanonical:
        scraper.tagscra_non_canonical(args.TagScra,out_path=args.OutputPath,out_name=args.OutputName, av=args.AO3Version)
        return []
    elif args.DaScra:
        print('='*15 + " Invoking DaScra " + '='*15)
        scraper.dascra_whole_tag_works(args.DaScra,out_path=args.OutputPath,out_name=args.OutputName, story_number=args.StoryNumber)
        return []
    elif args.ExpandRATAS:
        print(" Expanding RATAS "+args.ExpandRATAS)
        scraper.expand_rata(args.ExpandRATAS, create_new_file='expanded_rata')
    elif args.ExpandFullRATAS:
        print(" Expanding to FULL RATAS "+args.ExpandFullRATAS[0])
        file_name= os.path.basename(args.ExpandFullRATAS[0])[:-5]+'_full' if args.OutputName=="default_name" else args.OutputName
        scraper.expand_to_full_rata(args.ExpandFullRATAS[0],args.ExpandFullRATAS[1], create_new_file=file_name)
    elif args.GenerateNetwork:
        print(" Invoking NetBuilder and NetVisualizer")
        rata_json= scraper.read_JSON(args.GenerateNetwork)
        g= net_builder.net_build(rata_json)
        file_name = os.path.basename(args.GenerateNetwork)[:-5] if args.OutputName=="default_name" else args.OutputName
        heading="File: "+args.GenerateNetwork+'<br>'+file_name
        
        net_visualizer.net_visualize(g, 
                            headings=heading,
                            file_name=file_name)
    elif args.GenerateFullTagNetwork or args.GenerateCanonicalTagNetwork or args.GenerateSynTagNetwork or args.GenerateFreeFormTagNetwork:
        print(" Invoking NetBuilder and NetVisualizer")
        
        if args.GenerateFullTagNetwork:
            type="Full"
            my_arguments=args.GenerateFullTagNetwork
        elif args.GenerateCanonicalTagNetwork:
            type="Canonical"
            my_arguments=args.GenerateCanonicalTagNetwork
        elif args.GenerateSynTagNetwork:
            type="Syn"
            my_arguments=args.GenerateSynTagNetwork
        elif args.GenerateFreeFormTagNetwork:
            type="FreeForm"
            my_arguments=args.GenerateFreeFormTagNetwork
        
        rata_json= scraper.read_JSON(my_arguments[0])
        g= net_builder.net_build(rata_json)

        file_name = os.path.basename(my_arguments[0])[:-5]+"_"+type+"_Network" if args.OutputName=="default_name" else args.OutputName
        heading="File: "+my_arguments[0]+'<br>'+file_name+'<br>'+os.path.basename(my_arguments[1])[:-5]
        

        df=scraper.prepare_df_ratas(my_arguments[1])
        tag_net = net_builder.generate_story_set_net(type,df,g,year=args.StorySetYear)
        net_visualizer.net_visualize_story_set(tag_net, 
                            headings=heading,
                            file_name=file_name)   
    
    elif args.GenerateSimilarites:
        print(" Invoking NetBuilder and NetVisualizer ~~ Similarities ")
        
        rata_json_a= scraper.read_JSON(args.GenerateSimilarites[0])
        G= net_builder.net_build(rata_json_a)
        file_name_a = os.path.basename(args.GenerateSimilarites[0])[:-5] if args.OutputName=="default_name" else args.OutputName
        heading_a="File: "+args.GenerateSimilarites[0]+'<br>'+file_name_a
        G.name=file_name_a

        rata_json_b= scraper.read_JSON(args.GenerateSimilarites[1])
        H= net_builder.net_build(rata_json_b)
        file_name_b = os.path.basename(args.GenerateSimilarites[1])[:-5] if args.OutputName=="default_name" else args.OutputName
        heading_b="File: "+args.GenerateSimilarites[1]+'<br>'+file_name_b
        H.name=file_name_b

        net_visualizer.get_visuals_older_vs_newest(G,H,headings=[heading_a,heading_b],file_names=[file_name_a,file_name_b], number_comparison=5)
    elif args.GenerateDifferences:
        print(" Invoking NetBuilder and NetVisualizer ~~ Diff ")
        
        rata_json_a= scraper.read_JSON(args.GenerateDifferences[0])
        G= net_builder.net_build(rata_json_a)
        
        file_name_a = os.path.basename(args.GenerateDifferences[0])[:-5] if args.OutputName=="default_name" else args.OutputName
        file_name_b = os.path.basename(args.GenerateDifferences[1])[:-5] if args.OutputName=="default_name" else args.OutputName
        heading_a="Files: "+args.GenerateDifferences[0]+'<br>'+args.GenerateDifferences[1]+'<br> Disaplaying diff from: '+file_name_a+ " to: "+file_name_b
        heading_b="Files: "+args.GenerateDifferences[1]+'<br>'+args.GenerateDifferences[0]+'<br> Disaplaying diff from: '+file_name_b+ " to: "+file_name_a

        rata_json_b= scraper.read_JSON(args.GenerateDifferences[1])
        H= net_builder.net_build(rata_json_b)

        net_visualizer.get_vis_G_diff_H(G,H,title=heading_a, file_name='diff_'+file_name_a+'_'+file_name_b)
        net_visualizer.get_vis_G_diff_H(H,G,title=heading_b,file_name='diff_'+file_name_b+'_'+file_name_a)
    elif args.GenerateRATASProperties:
        print(" Invoking NetBuilder-NetAnalyser~ Generating RATAS Properties")
        rata= scraper.read_JSON(args.GenerateRATASProperties[0])
        net= net_builder.net_build(rata)
        dfs=net_analiser.get_G_properties(net)

        file_path=args.OutputPath+args.OutputName if not args.OutputName=='default_name' else args.OutputPath+'rata_properties'

        net_analiser.save_xls(dfs,file_path)
    elif args.GenTagDiff:
        print(" Invoking NetBuilder-NetAnalyser~Generating Tag Differences between Two RATAS")
        
        rata_a= scraper.read_JSON(args.GenTagDiff[0])
        net_a= net_builder.net_build(rata_a)
        net_a.name=os.path.basename(args.GenTagDiff[0])[:-5]


        rata_b= scraper.read_JSON(args.GenTagDiff[1])
        net_b= net_builder.net_build(rata_b)
        net_b.name=os.path.basename(args.GenTagDiff[1])[:-5]
        
        file_name=args.OutputName if not args.OutputName=='default_name' else 'rata_properties'
        

        net_analiser.generate_tag_diff_dataset(net_a,net_b, path=args.OutputPath, file_name=file_name)
    elif args.GenTagDiffDir:
        print(" Invoking NetBuilder-NetAnalyser~Generating Tag Differences between Multiple RATAS tp get Political Acts")
        
        # read_json_rata
        if not  os.path.isdir(args.GenTagDiffDir[0]):
            print()
            print("The argument needs to be a Dir with only JSON RATAS")
            return
        net_list, net_names= scraper.read_json_rata(args.GenTagDiffDir[0])
        
        file_name=args.OutputName if not args.OutputName=='default_name' else 'rata_properties'
        

        net_analiser.gen_tags_dataset_list(net_list, net_names=net_names, path=args.OutputPath, file_name=file_name)
    
    print()