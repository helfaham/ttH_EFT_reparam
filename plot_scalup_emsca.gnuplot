#!/bin/bash
reset

set lmargin 10 
set rmargin 0 

set terminal postscript portrait enhanced mono dashed lw 1.0 "Helvetica" 14 
#set terminal pdf font "Helvetica,14" enhanced dashed size 12 cm, 8 cm
set size 1.5,1.5
#set size ratio 0.5
set key horizontal 
set key font "8"
set key samplen "1.0"
set output "scalup_emsca.pdf"


set style line 1 dt 1 lc 7 lw 1.8 ps 0.4
set style line 2 dt 1 lc 8 lw 1.8 ps 0.4
set style line 3 dt 1 lc 20 lw 1.8 ps 0.4
set style line 4 dt 1 lc 9 lw 1.8 ps 0.4
#set style line 5 dt 1 lc 11 lw 1.8 ps 0.4

set style line 6 dt 2 lc 7 lw 2.0 ps 0.4  
set style line 7 dt 2 lc 8 lw 2.0 ps 0.4
set style line 8 dt 2 lc 20 lw 2.0 ps 0.4
set style line 9 dt 2 lc 9 lw 2.0 ps 0.4
#set style line 10 dt 2 lc 11 lw 2.0 ps 0.4

set style data histeps

set multiplot
set tics front

nevents=5000000


set label "ttH production at the LHC, 13 TeV" font ",14" at graph 0.1, graph 0.98
set label "(SM)EFTat(N)LO, fixed scale=172GeV" font ",10" at graph 0.1, graph 0.95
set label "FO=0.002/200K, param card=default (not equalised)" font ",8" at graph 0.1, graph 0.93
set xrange [0:450]
set yrange [1e-4:3e00]
set origin 0.00, 0.15
set size 1.4, 1.0
set bmargin 0 
set tmargin 0
set xtics 50 nomirror
set ytics 10
set mxtics 2
set mytics 10
set ylabel "{/Symbol s} per bin [pb]"
#set xtics nomirror
set logscale y
set format y '10^{%T}'
set key at graph 0.97, graph 0.9 noautotitles spacing 2.4
set label front 'MadGraph5\_aMC\@NLO' font "Courier,11" rotate by 90 at graph 1.02, graph 0.04
set xlabel 'pT(h)[GeV]'
#set xlabel 'delR(tt)'

plot \
"./tth_sm_fo/Events/run_08/higgs_pT_.dat" u 2:3 ls 1 t "SM NLO" , \
"./tth_sm_fo_pythia/Events/run_06/higgs_pT.dat" u 2:3 ls 6 t "SM NLO+PS" , \
"./tth_smeft_fo_NEW/Events/run_01/higgs_pT_.dat" u 2:3 ls 2 t "NLO cpg\=1" , \
"./tth_smeft_fo_pythia_NEW/Events/run_05/higgs_pT.dat" u 2:3 ls 7 t "NLO+PS cpg\=1" , \
"./tth_smeft_fo_NEW/Events/run_02/higgs_pT_.dat" u 2:3 ls 3 t "NLO ctp\=1" , \
"./tth_smeft_fo_pythia_NEW/Events/run_06/higgs_pT.dat" u 2:3 ls 8 t "NLO+PS ctp\=1" , \
"./tth_smeft_fo_NEW/Events/run_03/higgs_pT_.dat" u 2:3 ls 4 t "NLO ctg\=1" , \
"./tth_smeft_fo_pythia_NEW/Events/run_14/higgs_pT.dat" u 2:3 ls 9 t "NLO+PS ctg\=1" , \

unset multiplot

!open "scalup_emsca.pdf"

