@REM @REM Scrap Disability Story Set DaScra
@REM python .\ao3_analyser.py -ds 'Disability' -o story_set_disability    


@REM @REM TagScra Scrap Disability RATA 
@REM python.exe .\ao3_analyser.py -ts Disability -o rata_disability_current 
@REM python.exe .\ao3_analyser.py -ts "Blind Albedo (Genshin Impact)" -o jjjjj 
@REM python.exe .\ao3_analyser.py -ts Disability -o rata_disability_2013 -ao3_v 2013  


@REM @REM Expand a RATA JSON
@REM python .\ao3_analyser.py --ExpandRATAS .\OutputFiles\rata_disability_current.json  -o rata_disability_current_expanded

@REM @REM Scrap Non-Canonical Tags of DIsability
@REM python.exe .\ao3_analyser.py -ts Disability --NonCanonical -o non_canonical_disability   

@REM @REM FULL Expansion 
@REM python.exe .\ao3_analyser.py --ExpandFullRATAS .\OutputFiles\rata_disability_current_expanded.json .\OutputFiles\non_canonical_disability.txt  -o rata_disability_current_expanded_full




@REM @REM Generate Visualization of a disability RATAS
@REM python.exe .\ao3_analyser.py -gn .\OutputFiles\disability_ratas_current\rata_disability_current.json -o CURRENT   
@REM python.exe .\ao3_analyser.py -gn .\OutputFiles\disability\rata_disability_current_expanded.json   
@REM python.exe .\ao3_analyser.py -gn .\OutputFiles\disability\rata_disability_current_expanded_full.json   
@REM python.exe .\ao3_analyser.py -gn .\legend_current.json   
@REM python.exe .\ao3_analyser.py -gn .\legend_current_expanded.json   
@REM python.exe .\ao3_analyser.py -gn .\legend_current_expanded_full.json   

@REM python.exe .\ao3_analyser.py -gn .\OutputFiles\aaaaaa\previous.json
@REM python.exe .\ao3_analyser.py -gn ".\OutputFiles\aaaaaa\previous copy.json"
@REM python.exe .\ao3_analyser.py -gn ".\OutputFiles\disability\rata_disability_curren.json"   



@REM @REM Generate Visualization of similarities between two disability RATAS version
@REM python.exe .\ao3_analyser.py -gs .\OutputFiles\disability\rata_disability_2013.json .\OutputFiles\disability_ratas_current\rata_disability_current.json
@REM python.exe .\ao3_analyser.py -gs .\OutputFiles\disability\rata_disability_2013.json .\OutputFiles\disability\rata_disability_current_expanded_full.json

@REM @REM Generate Visualization of differences between two disability RATAS version
@REM python.exe .\ao3_analyser.py -gd .\OutputFiles\disability\rata_disability_2013.json .\OutputFiles\disability\rata_disability_current_expanded_full.json
python.exe .\ao3_analyser.py -gd .\OutputFiles\disability\rata_disability_2013.json .\OutputFiles\disability_ratas_current\rata_disability_current.json



@REM python.exe .\ao3_analyser.py -gs .\OutputFiles\disability_ratas_old\rata_disability_2013.json .\OutputFiles\disability_ratas_old\rata_disability_2014.json




@REM @REM Generate report of properties of a disability RATAS current
@REM python .\ao3_analyser.py --GenerateRATASProperties ./OutputFiles/disability_ratas_current/rata_disability_current_expanded.json -o .\report_disability_expanded
@REM python .\ao3_analyser.py --GenerateRATASProperties ./OutputFiles/disability_ratas_current/rata_disability_current_expanded_full.json -o .\report_disability_expanded_full

@REM @REM Generate report of political acts/ differences between two different Verions of disability RATAS 2013 vs current
@REM python .\ao3_analyser.py --GenTagDiff .\OutputFiles\disability\rata_disability_current_expanded_full.json .\OutputFiles\disability\rata_disability_2013.json -o reports_diff_disability_current_2013

@REM @REM Generate report of political acts of all disability RATAS version
@REM python .\ao3_analyser.py --GenTagDiffDir .\OutputFiles\disability\ -o all_disabilities_comparison
@REM python .\ao3_analyser.py --GenTagDiffDir .\OutputFiles\disability_2\ -o all_disabilities_comparison_2




@REM @REM Generate Visualization of a Story-Set & disability RATAS
@REM python.exe .\ao3_analyser.py --GenerateFullTagNetwork ./OutputFiles/disability/rata_disability_current_expanded_full.json ./OutputFiles/disability_ratas_current/dascra_output_disability.xlsx -o disability_full_tag_net

@REM python.exe .\ao3_analyser.py --GenerateCanonicalTagNetwork ./OutputFiles/disability/rata_disability_current_expanded_full.json ./OutputFiles/disability_ratas_current/dascra_output_disability.xlsx -o disability_canonical_tag_net
@REM python.exe .\ao3_analyser.py --GenerateCanonicalTagNetwork ./OutputFiles/disability/rata_disability_2013.json ./OutputFiles/disability_ratas_current/dascra_output_disability.xlsx -o disability_canonical_tag_net_2013 --StorySetYear 2013


@REM python.exe .\ao3_analyser.py --GenerateSynTagNetwork ./OutputFiles/disability/rata_disability_current_expanded_full.json ./OutputFiles/disability_ratas_current/dascra_output_disability.xlsx -o disability_syn_tag_net
@REM python.exe .\ao3_analyser.py --GenerateFreeFormTagNetwork ./OutputFiles/disability/rata_disability_current_expanded_full.json ./OutputFiles/disability_ratas_current/dascra_output_disability.xlsx -o disability_freeform_tag_net
   
@REM python.exe .\ao3_analyser.py -gn .\OutputFiles\disability\rata_disability_current_expanded.json   
@REM python.exe .\ao3_analyser.py -gn .\OutputFiles\disability\rata_disability_current_expanded_full.json   

@REM python.exe .\ao3_analyser.py -gn .\legend_current.json   
@REM python.exe .\ao3_analyser.py -gn .\legend_current_expanded.json   
@REM python.exe .\ao3_analyser.py -gn .\legend_current_expanded_full.json   




PAUSE