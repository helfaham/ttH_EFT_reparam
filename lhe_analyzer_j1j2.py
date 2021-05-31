#!/usr/bin/env python
import sys, math, ROOT
from array import array
# loop over two distnict jets and calculate dphi
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
    h_jet1_pt  = ROOT.TH1F('jet1_pt' , 'jet1_pt' , 50, 0, 800)
    h_jet1_pt.Sumw2()

    h_jet2_pt  = ROOT.TH1F('jet2_pt' , 'jet2_pt' , 50, 0, 800)
    h_jet2_pt.Sumw2()

    h_dphi_j1j2  = ROOT.TH1F('dphi_j1j2' , 'dphi_j1j2' , 50, 0, 3)
    h_dphi_j1j2.Sumw2()
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
		PI = 3.14159265
		jet1_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
                for p in genp_ls:
		    # for each particle in an event: extract four momentum
                    i_p4 = ROOT.TLorentzVector(lhep_px(p), lhep_py(p), lhep_pz(p), lhep_E(p))
		    if lhep_status(p) == 1: # status = 1 -> final state particle #like a quark
                        if (abs(lhep_pdgID(p)) == 1 or abs(lhep_pdgID(p)) == 2
				or abs(lhep_pdgID(p) == 3 or abs(lhep_pdgID(p))) == 4
					or abs(lhep_pdgID(p)) ==5):
				   jet1_p4 += i_p4
				   l_p4 = i_p4

		        jet2_p4 = ROOT.TLorentzVector(0, 0, 0, 0)
			for s in genp_ls:
				if p != s:
				    # for each particle in an event: extract four momentum
				    ii_p4 = ROOT.TLorentzVector(lhep_px(s), lhep_py(s), lhep_pz(s), lhep_E(s))
				    if lhep_status(s) == 1: # status = 1 -> final state particle #like a quark
					if (abs(lhep_pdgID(s)) == 1 or abs(lhep_pdgID(s)) == 2
						or abs(lhep_pdgID(s) == 3 or abs(lhep_pdgID(s))) == 4
							or abs(lhep_pdgID(s)) ==5):
					   jet2_p4 += ii_p4
					   ll_p4 = ii_p4
						#dphi calculation
					   j1_px=jet1_p4.Px()
					   j1_py=jet1_p4.Py()
					   j2_px=jet2_p4.Px()
					   j2_py=jet2_p4.Py()
					   pt1=math.sqrt(j1_px**2+j1_py**2)
					   pt2=math.sqrt(j2_px**2+j2_py**2)
					   if(pt1 != 0 and pt2 != 0):
						tmp=j1_px*j2_px+j1_py*j2_py
						tmp=tmp/(pt1*pt2)
						tiny=1e-05
						if(abs(tmp) > (1+tiny)):
						   print "cosine is larger than 1, angle is complex"
						   print "warning: you may need to stop the code"
						elif(abs(tmp) >= 1):
						  tmp=math.copysign(1,tmp)
						  #print "copy sign = " + str(tmp)
						tmp=(math.acos(tmp))
					   else:
						tmp=1.00000000
					   print "final tmp = " + str(tmp)
                                           # here you fill for every pair
                                           h_dphi_j1j2.Fill(tmp, weight) 
                # for each event: store the observables in the histograms
                h_jet1_pt.Fill(jet1_p4.Pt(), weight) 
                h_jet2_pt.Fill(jet2_p4.Pt(), weight) 
                in_event = False
                continue

    # output a root file
    ofile.cd()

    print("processed %i events" %event_num)

    # normalize histo
    h_jet1_pt.Scale(1./event_num)
    h_jet2_pt.Scale(1./event_num)
    h_dphi_j1j2.Scale(1./event_num)
    print("integrated weight: %.6f" %(h_jet1_pt.GetSumOfWeights()))
    print("integrated weight: %.6f" %(h_jet2_pt.GetSumOfWeights()))
    print("file %s produced" %sys.argv[2])

    h_jet1_pt.Write()
    h_jet2_pt.Write()
    h_dphi_j1j2.Write()
    ofile.Close()
