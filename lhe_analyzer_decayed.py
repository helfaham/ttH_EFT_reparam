#!/usr/bin/env python
import sys, math, ROOT
from array import array

def KILL(log):
    print '\n@@@ FATAL -- '+log+'\n'
    raise SystemExit

def lhep_pdgID  (line): return int  (line.split()[ 0])
def lhep_status (line): return int  (line.split()[ 1])
def lhep_mother1(line): return int  (line.split()[ 2])
def lhep_mother2(line): return int  (line.split()[ 3])
def lhep_px     (line): return float(line.split()[ 6])
def lhep_py     (line): return float(line.split()[ 7])
def lhep_pz     (line): return float(line.split()[ 8])
def lhep_E      (line): return float(line.split()[ 9])
def lhep_M      (line): return float(line.split()[10])

def print_lhep(l):
    print lhep_pdgID  (l),
    print lhep_status (l),
    print lhep_mother1(l),
    print lhep_mother2(l),
    print lhep_px     (l),
    print lhep_py     (l),
    print lhep_pz     (l),
    print lhep_E      (l),
    print lhep_M      (l)

    return

### main
if __name__ == '__main__':

    if len(sys.argv)-1 != 2:
        KILL('two command-line arguments required: [1] input .lhe file, [2] output .root file')

    ifile = file      (sys.argv[1], 'r')
    ofile = ROOT.TFile(sys.argv[2], 'recreate')

    ###

    event_num_max = -1

    ## define relevant histograms
    #xedges = [0,60,120,200,300,450,1000] #for STXS
    #xbins = len(xedges)
    #runArray = array('d',xedges + [xedges[-1]+1])
    h_higgs_mass  = ROOT.TH1F('higgs_mass' , 'higgs_mass' , 100, 0, 500)
    h_higgs_pt  = ROOT.TH1F('higgs_pt' , 'higgs_pt' , 100, 0, 1000)
    #h_higgs_pt  = ROOT.TH1F('higgs_pt' , 'higgs_pt' , xbins, runArray) 
    h_higgs_mass.Sumw2()
    h_higgs_pt.Sumw2()
  
    event_num, in_event = 0, False

    # reads the lhe and looks into the events
    for line in ifile:
        if line[:1] == '#': continue
        if line.startswith('<scales'): continue

        if event_num_max > 0:
            if event_num > event_num_max: continue

        if line.startswith('<event>'):
            event_num += 1

            genp_ls = []
            in_event = True
            continue

        if in_event:
            if not line.startswith('</event>'):
                l0 = line.strip('\n')
                if l0.startswith('<'): continue
                if l0.startswith('   <'): continue
                if len(l0.split()) == 6:
            	    #print line
                    weight = float(line.split()[2])
                    #print weight
                    continue

                genp_ls.append(l0)

            else:
                ### event analysis

	        # define the four momentum of the pair. 
		higgs_p4 = ROOT.TLorentzVector(0, 0, 0, 0)

                for p in genp_ls:

		    # for each particle in an event: extract four momentum
                    i_p4 = ROOT.TLorentzVector(lhep_px(p), lhep_py(p), lhep_pz(p), lhep_E(p))
		   
                    #print abs(lhep_pdgID(p))
		    if lhep_status(p) == 1: #or lhep_status(p) !=1: #the b is stable here 

                        if abs(lhep_pdgID(p)) == 5:  #the b from the top decay is interfering
                           if lhep_mother1(p) == 5 or lhep_mother2(p) == 5: #number of the mother in the lhe file not the pdg
                              higgs_p4 += i_p4
                              l_p4 = i_p4


                	
                # for each event: store the observables in the histograms
                h_higgs_pt.Fill(higgs_p4.Pt(), weight) 
                #if higgs_p4.Pt() < 30: indentation below to make it work
                h_higgs_mass.Fill(higgs_p4.M(), weight) 
                in_event = False
                continue

    # output a root file
    ofile.cd()

    print("processed %i events" %event_num)

    # normalize histo
    h_higgs_pt.Scale(1./event_num)
    h_higgs_mass.Scale(1./event_num)
    print("integrated weight: %.6f" %(h_higgs_pt.GetSumOfWeights()))
    print("integrated weight: %.6f" %(h_higgs_mass.GetSumOfWeights()))
    print("file %s produced" %sys.argv[2])

    h_higgs_pt.Write()
    h_higgs_mass.Write()

    ofile.Close()
