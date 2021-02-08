#!/usr/bin/env python
import sys, math, ROOT

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
    h_higgs_pt  = ROOT.TH1F('higgs_pt' , 'higgs_pt' , 100, 0, 1000)
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
                if len(l0.split()) == 6:
                    weight = float(line.split()[2])
                    #print weight
                    continue

                genp_ls.append(l0)

            else:
                ### event analysis

	        # define the four momentum of the dilepton pair. 

		higgs_p4 = ROOT.TLorentzVector(0, 0, 0, 0)

                for p in genp_ls:

		    # for each particle in an event: extract four momentum
                    i_p4 = ROOT.TLorentzVector(lhep_px(p), lhep_py(p), lhep_pz(p), lhep_E(p))
		   
		    if lhep_status(p) == 1: # status = 1 -> final state particle

			# e or mu
                        if abs(lhep_pdgID(p)) == 25: 
                           higgs_p4 += i_p4
                           l_p4 = i_p4


                	
                # for each event: store the observables in the histograms

                h_higgs_pt.Fill(higgs_p4.Pt(), weight) 

                in_event = False
                continue

    # output a root file
    ofile.cd()

    print("processed %i events" %event_num)

    # normalize histo
    h_higgs_pt.Scale(1./event_num)
    print("integrated weight: %.6f" %(h_higgs_pt.GetSumOfWeights()))
    print("file %s produced" %sys.argv[2])

    h_higgs_pt.Write()

    ofile.Close()
