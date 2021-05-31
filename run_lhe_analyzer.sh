#!/bin/bash
#TODO SM
#gunzip tth_sm/Events/run_02/unweighted_events.lhe.gz
#gunzip tth_sm_prod/Events/run_01/unweighted_events.lhe.gz

#TODO all wislons to zero
#gunzip tth_smeft/Events/run_10/unweighted_events.lhe.gz
#gunzip tth_smeft_prod/Events/run_01/unweighted_events.lhe.gz

#TODO CPT
#gunzip tth_smeft/Events/run_11/unweighted_events.lhe.gz
#gunzip tth_smeft_prod/Events/run_02/unweighted_events.lhe.gz

#TODO CTG
#gunzip tth_smeft/Events/run_12/unweighted_events.lhe.gz
#gunzip tth_smeft_prod/Events/run_03/unweighted_events.lhe.gz

#python
#TODO SM
#python lhe_analyzer_decayed.py tth_sm/Events/run_02/unweighted_events.lhe ./root_files/sm_tth.root
python lhe_analyzer.py tth_sm_prod/Events/run_01/unweighted_events.lhe ./root_files/sm_tth_prod.root

#TODO all wilsons to zero
#python lhe_analyzer_decayed.py tth_smeft/Events/run_10/unweighted_events.lhe ./root_files/smeft_tth_wilson_zero.root
python lhe_analyzer.py tth_smeft_prod/Events/run_01/unweighted_events.lhe ./root_files/smeft_tth_wilson_zero_prod.root

#TODO CPT
#python lhe_analyzer_decayed.py tth_smeft/Events/run_11/unweighted_events.lhe ./root_files/smeft_tth_wilson_cpt.root
python lhe_analyzer.py tth_smeft_prod/Events/run_02/unweighted_events.lhe ./root_files/smeft_tth_wilson_cpt_prod.root

#TODO CTG
#python lhe_analyzer_decayed.py tth_smeft/Events/run_12/unweighted_events.lhe ./root_files/smeft_tth_wilson_ctg.root
python lhe_analyzer.py tth_smeft_prod/Events/run_03/unweighted_events.lhe ./root_files/smeft_tth_wilson_ctg_prod.root
