#!/bin/bash
gunzip tth_sm_not_decayed/Events/run_01/unweighted_events.lhe.gz
gunzip tth_sm/Events/run_01/unweighted_events.lhe.gz
gunzip tth_smeft/Events/run_01/unweighted_events.lhe.gz
gunzip tth_smeft/Events/run_02/unweighted_events.lhe.gz
gunzip tth_smeft/Events/run_03/unweighted_events.lhe.gz

python lhe_analyzer.py tth_sm_not_decayed/Events/run_01/unweighted_events.lhe sm_tth_not_decayed.root
python lhe_analyzer_decayed.py tth_sm/Events/run_01/unweighted_events.lhe sm_tth.root
python lhe_analyzer_decayed.py tth_smeft/Events/run_01/unweighted_events.lhe smeft_tth_wilson_zero.root
python lhe_analyzer_decayed.py tth_smeft/Events/run_02/unweighted_events.lhe smeft_tth_wilson_cpt.root
python lhe_analyzer_decayed.py tth_smeft/Events/run_03/unweighted_events.lhe smeft_tth_wilson_ctg.root
