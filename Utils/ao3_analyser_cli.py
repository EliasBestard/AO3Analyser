import argparse
import os

from sympy import arg
import Utils.scraper_script as scraper
import Modules.NetBuilder.net_builder as net_builder
import Modules.NetVisualizer.net_visualizer as net_visualizer
import Modules.NetAnalyser.net_analyser as net_analiser
# # CLI

parser = argparse.ArgumentParser(prog="ao3_analyser")

# ## TagScra
parser.add_argument("-ts", "--TagScra",
                    help="Call TagScra Module witht the list of Tags as arguments to mine and genereate a JSON with the RATAS",
                    nargs='+'
                    )
parser.add_argument("-ao3_v", "--AO3Version",
                    help="Version (year) for which scrap AO3 the tag when calling TagScra",
                    type=str,
                    default='current'
                    )
parser.add_argument("--NonCanonical",
                    help="Call TagScra Module witht the list of Tags as arguments to mine and genereate all non canonical tags under each tag",
                    action='store_true',
                    default=False
                    )

# ## DaScra
parser.add_argument("-ds", "--DaScra",
                    help="Call DaScra Module witht the Tag to mine all its works and genereate a JSON with the RATAS",
                    type=str
                    # default='Disability'
                    )
parser.add_argument("--StoryNumber", help="Number of stories to scrap when calling DaScra ",
                    type=int,
                    default=1000)

# ## TagScra & DaScra0
parser.add_argument("-o","--OutputName", help="Name of the file result",
                    type=str,
                    default='default_name')
parser.add_argument("-op","--OutputPath", help="Path of the output",
                    type=str,
                    default='./OutputFiles/')
# ##
parser.add_argument("--ExpandRATAS", help="""Read RATA JSON file expands it mining all the canonical tags to get they sub tags and synned tags """,
                    type=str)
parser.add_argument("--ExpandFullRATAS", help="""Read RATA JSON file expands it adding all the non canonical tags from a non_canonical file outputed by TagScra""",
                    nargs=2)

# ## Netbuilder & Visualizer
parser.add_argument("-gn","--GenerateNetwork", help="Read a RATA JSON file and build the Network representation and creates its visualization. Receives the path of the JSON file",
                    type=str)

# ## Visualizer -- Net Diff, Intersection, etc
parser.add_argument("-gs","--GenerateSimilarites", help="Given two RATAS JSON files generates boths visualiations highlighting the similarities assuming the first one is an old version of the second one",
                    nargs=2)
parser.add_argument("-gd","--GenerateDifferences", help="""Given two RATAS JSON files generates one visualization that highlights the differences of two RATAS
                     Blue Nodes represents nodes in the difference (in the second file that are not in the first file)
                     Red Nodes represents nodes in the intersection (in the second file and the first file) """,
                    nargs=2)


# ## Reports
parser.add_argument("--GenerateRATASProperties", help="""""",
                    nargs=1)
parser.add_argument("--GenTagDiff", help="""""",
                    nargs=2)
parser.add_argument("--GenTagDiffDir", help="""""",
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