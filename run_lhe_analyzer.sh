#!/bin/bash
gunzip tth_sm/Events/run_02/unweighted_events.lhe.gz

gunzip tth_smeft/Events/run_07/unweighted_events.lhe.gz
#gunzip tth_smeft_prod_only/Events/run_01/unweighted_events.lhe.gz

gunzip tth_smeft/Events/run_08/unweighted_events.lhe.gz

gunzip tth_smeft/Events/run_09/unweighted_events.lhe.gz

#python
python lhe_analyzer_decayed.py tth_sm/Events/run_02/unweighted_events.lhe ./root_files/sm_tth.root

python lhe_analyzer_decayed.py tth_smeft/Events/run_07/unweighted_events.lhe ./root_files/smeft_tth_wilson_zero.root
#python lhe_analyzer_decayed.py tth_smeft_prod_only/Events/run_01/unweighted_events.lhe ./root_files/smeft_tth_wilson_zero.root

python lhe_analyzer_decayed.py tth_smeft/Events/run_08/unweighted_events.lhe ./root_files/smeft_tth_wilson_cpt.root

python lhe_analyzer_decayed.py tth_smeft/Events/run_09/unweighted_events.lhe ./root_files/smeft_tth_wilson_ctg.root
