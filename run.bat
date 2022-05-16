@REM @REM Scrap Disability Story Set DaScra
@REM python .\ao3_analyser.py -ds -t 'Disability' -o story_set_disability    


@REM @REM TagScra Scrap Disability RATA 
@REM python.exe .\ao3_analyser.py -ts Disability -o rata_disability_current 
@REM python.exe .\ao3_analyser.py -ts Disability -o rata_disability_2013 -ao3_v 2013  


@REM @REM Expand a RATA JSON
@REM python .\ao3_analyser.py --ExpandRATAS .\OutputFiles\rata_disability_current.json  -o rata_disability_current_expanded

@REM @REM Scrap Non-Canonical Tags of DIsability
@REM python.exe .\ao3_analyser.py -ts Disability --NonCanonical -o non_canonical_disability   

@REM @REM FULL Expansion 
@REM python.exe .\ao3_analyser.py --ExpandFullRATAS .\OutputFiles\rata_disability_current_expanded.json .\OutputFiles\non_canonical_disability.txt  -o rata_disability_current_expanded_full




@REM @REM Generate Visualization of a disability RATAS
@REM python.exe .\ao3_analyser.py -gn .\OutputFiles\disability\rata_disability_current_expanded.json   

@REM @REM Generate Visualization of similarities between two disability RATAS version
@REM python.exe .\ao3_analyser.py -gs .\OutputFiles\disability\rata_disability_2013.json .\OutputFiles\disability\rata_disability_current_expanded_full.json

@REM @REM Generate Visualization of differences between two disability RATAS version
@REM python.exe .\ao3_analyser.py -gd .\OutputFiles\disability\rata_disability_2013.json .\OutputFiles\disability\rata_disability_current_expanded_full.json

@REM @REM Generate report of properties of a disability RATAS current
@REM python .\ao3_analyser.py --GenerateRATASProperties .\OutputFiles\disability\rata_disability_current_expanded_full.json .\report_disability_expanded_full

@REM @REM Generate report of political acts/ differences between two different Verions of disability RATAS 2013 vs current
@REM python .\ao3_analyser.py --GenTagDiff .\OutputFiles\disability\rata_disability_current_expanded_full.json .\OutputFiles\disability\rata_disability_2013.json -o reports_diff_disability_current_2013

@REM @REM Generate report of political acts of all disability RATAS version
@REM python .\ao3_analyser.py --GenTagDiffDir .\OutputFiles\disability\ -o all_disabilities_ver_tags


PAUSE