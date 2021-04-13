#!/bin/bash
reset

set lmargin 10
set rmargin 0

set terminal postscript portrait enhanced mono dashed lw 1.0 "Helvetica" 14 
#set terminal pdf font "Helvetica,14" enhanced dashed size 12 cm, 8 cm
#set size ratio 0.75 
set key font "11"
set key samplen "1.1"
set output "scalup_emsca.pdf"


set style line 1 dt 1 lc 16 lw 1.8 ps 0.4
set style line 2 dt 1 lc 8 lw 1.8 ps 0.4
set style line 3 dt 1 lc 14 lw 1.8 ps 0.4  
set style line 4 dt 1 lc 12 lw 1.8 ps 0.4
set style line 5 dt 1 lc 10 lw 1.8 ps 0.4

set style data histeps

set multiplot
set tics front

nevents=5000000


set label "ttH production at the LHC, 13 TeV" font ",14" at graph 0.1, graph 0.94
#set label "NLO + PS" font ",12" at graph 0.1, graph 0.88
set xrange [0:500]
set yrange [1e-4:3e-2]
set origin 0.00, 0.15
set size 0.9, 0.8
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
set xlabel 'pT(h)[GeV] using pdgID==25'


plot \
"./tth_smeft_fo/Events/run_13/dats/higgs_pT_.dat" u 2:3 ls 1 t "NLO", \
"./tth_smeft_fo_pythia/Events/run_10/dats/higgs_pT.dat" u 2:3 ls 2 t "NLO+PS", \
\
#"./tth_smeft_fo/Events/run_13/dats/higgs_pT_.dat" u 2:3 ls 12 , \
#"./tth_smeft_fo_pythia/Events/run_10/dats/higgs_pT.dat" u 2:3 ls 13 , \





unset multiplot

!open "scalup_emsca.pdf"




