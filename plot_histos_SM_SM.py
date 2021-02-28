#!/usr/bin/env python
import sys, math, ROOT, array, numpy

def KILL(log):
    print '\n@@@ FATAL -- '+log+'\n'
    raise SystemExit


### main
if __name__ == '__main__':

#    if len(sys.argv) < 2:
#        KILL('command-line arguments required: .root input files')
#    ifile_ls = [ROOT.TFile.Open(f) for f in sys.argv[1:]]
  
    main_dir = "/home/elfaham/Downloads/tzw/working_dir/ttH_EFT_reparam"

    file_sm = main_dir + "/pure_SM_root_files/SM_tth.root"
    file_sm_decayed = main_dir + "/pure_SM_root_files/SM_tth_madspin.root"
    #file_sm_decayed_ps = main_dir + "/pure_SM_root_files/SM_tth_madspin_PS.root"
    file_sm_ps = main_dir + "/pure_SM_root_files/SM_tth_PS_only.root"

    ifile_sm = ROOT.TFile.Open(file_sm)
    ifile_sm_decayed = ROOT.TFile.Open(file_sm_decayed)
    #ifile_sm_decayed_ps = ROOT.TFile.Open(file_sm_decayed_ps)
    ifile_sm_ps = ROOT.TFile.Open(file_sm_ps)

    
    histo_dc = {
      'higgs_pt': ('pt_{higgs} [GeV]', 0, 1000),
      'higgs_mass': ('mass_{higgs} [GeV]', 0, 500),
    }

    color_sm = 1  # black
    color_sm_decayed = 633   # black
    #color_sm_decayed_ps = 797  # orange
    color_sm_ps = 797  # orange
    color_ratio = 824 # green


    ROOT.gROOT.SetBatch()

    for histo_key in histo_dc:

        canvas = ROOT.TCanvas(histo_key, histo_key, 800, 725)

        histo_sm = ifile_sm.Get(histo_key)
        histo_sm_decayed = ifile_sm_decayed.Get(histo_key)
        #histo_sm_decayed_ps = ifile_sm_decayed_ps.Get(histo_key)
        histo_sm_ps = ifile_sm_ps.Get(histo_key)

        print("SM xsec: %.4f pb" %(histo_sm.GetSumOfWeights()))
        print("SM_madspin xsec: %.4f pb" %(histo_sm_decayed.GetSumOfWeights()))
        #print("SM_madspin_ps xsec: %.4f pb" %(histo_sm_decayed_ps.GetSumOfWeights()))	
        print("SM_ps xsec: %.4f pb" %(histo_sm_ps.GetSumOfWeights()))
	
	# histograms pad
        pad1 = ROOT.TPad("histo_pos","histo_pos",0., 0.35, 1, 1)
        pad1.SetTopMargin(0.05)
        pad1.SetBottomMargin(0)
        pad1.SetLeftMargin(0.15)
	pad1.SetGridx()
	pad1.SetLogy()
	pad1.Draw()
	pad1.cd()


        # EFT histograms separately

        histo_sm.Draw('hist')
        histo_sm.SetStats(0)
        histo_sm.SetLineColor(color_sm)
        histo_sm.SetLineWidth(3)
	histo_sm.GetYaxis().SetRangeUser(2e-6,.2) 
        histo_sm.GetYaxis().SetLabelSize(0.05)
	histo_sm.GetXaxis().SetTitle(histo_dc[histo_key][0])
        histo_sm.GetXaxis().SetTitleSize(0.05)
        if histo_dc[histo_key][0] == "higgs_pt": #TODO
		histo_sm.GetYaxis().SetTitle("d#sigma/dpT(H) [pb/10 GeV]")
        elif histo_dc[histo_key][0] == "higgs_mass": #TODO
		histo_sm.GetYaxis().SetTitle("d#sigma/dM(H) [pb/5 GeV]")
        histo_sm.GetYaxis().SetTitleSize(0.05)


	histo_sm.SetTitle("")
   
        histo_sm_decayed.Draw('hist,same')
        histo_sm_decayed.SetStats(0)
        histo_sm_decayed.SetLineColor(color_sm_decayed)
        histo_sm_decayed.SetLineWidth(3)

        histo_sm_ps.Draw('hist,same')
        histo_sm_ps.SetStats(0)
        histo_sm_ps.SetLineColor(color_sm_ps)
        histo_sm_ps.SetLineWidth(3)

        leg = ROOT.TLegend(.95,.75,.75,.95) 
        leg.AddEntry(histo_sm, "SM","l")
        leg.AddEntry(histo_sm_decayed, "SM+Madspin","l")
        leg.AddEntry(histo_sm_ps, "SM+PS","l")
        leg.SetTextSize(.035)
        leg.Draw()

        canvas.cd()

        ratio = histo_sm.Clone()
        ratio.Divide(histo_sm_decayed)

        # lower pad: ratio model/EFT tot
        pad2 = ROOT.TPad("histo_ratio","histo_ratio",0., 0.0 , 1, 0.35)
        pad2.SetTopMargin(0.0)
        pad2.SetLeftMargin(0.15)
        pad2.SetBottomMargin(0.27)
        pad2.SetGridx()
        pad2.SetGridy()
        #pad2.SetLogy()
        pad2.Draw()
        pad2.cd()


        ratio.Draw('hist')
        ratio.SetStats(0)
        ratio.SetLineColor(color_ratio)
        ratio.SetLineStyle(1)
        ratio.SetLineWidth(3)
        ratio.GetYaxis().SetRangeUser(.8,2.5)
        ratio.GetXaxis().SetLabelSize(0.1)
        ratio.GetXaxis().SetLabelOffset(0.01)
        ratio.GetYaxis().SetLabelSize(0.1)
        ratio.GetYaxis().SetLabelOffset(0.01)
	ratio.GetXaxis().SetTitle(histo_dc[histo_key][0])
        ratio.GetXaxis().SetTitleSize(0.1)
	ratio.GetYaxis().SetTitle("sm/sm_ms ")
        ratio.GetYaxis().SetTitleSize(0.1)
        ratio.GetYaxis().SetTitleOffset(0.7)

        ratio.SetTitle("")

        #leg2 = ROOT.TLegend(.6,.3,.9,.65)
        #leg2.AddEntry(ratio, " sm_decayedwgt(EFT) / rwgt (EFT)","l") #TODO
        #leg2.SetTextSize(0.065)
        #leg2.Draw()

        canvas.cd()

	
        #canvas.Write()
	canvas.SaveAs("./plots/pure_SM_plot_" + histo_key + ".pdf")


