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

    file_sm = main_dir + "/root_files/sm_tth.root"
    file_zero = main_dir + "/root_files/smeft_tth_wilson_zero.root"
    file_cpt = main_dir + "/root_files/smeft_tth_wilson_cpt.root"
    file_ctg = main_dir + "/root_files/smeft_tth_wilson_ctg.root"


    ifile_sm = ROOT.TFile.Open(file_sm)
    ifile_zero = ROOT.TFile.Open(file_zero)
    ifile_cpt = ROOT.TFile.Open(file_cpt)
    ifile_ctg = ROOT.TFile.Open(file_ctg)
    
    histo_dc = {
      'higgs_pt': ('pt_{higgs} [GeV]', 0, 600),
      #'higgs_mass': ('mass_{higgs} [GeV]', 0, 200),
    }

    color_sm = 633  # red
    color_zero = 1   # black
    color_cpt = 797  # orange
    color_ctg = 824  # green

    color_sm_zero = 1 
    color_sm_cpt = 797 
    color_sm_ctg = 824 


    ROOT.gROOT.SetBatch()

    for histo_key in histo_dc:

        canvas = ROOT.TCanvas(histo_key, histo_key, 800, 725)

        histo_sm = ifile_sm.Get(histo_key)
        histo_zero = ifile_zero.Get(histo_key)
        histo_cpt = ifile_cpt.Get(histo_key)
        histo_ctg = ifile_ctg.Get(histo_key)

        print("sm: %.4f pb" %(histo_sm.GetSumOfWeights()))
        print("smeft zero wilson: %.4f pb" %(histo_zero.GetSumOfWeights()))
        print("smeft cpt wilson: %.4f pb" %(histo_cpt.GetSumOfWeights()))
        print("smeft ctg wilson: %.4f pb" %(histo_ctg.GetSumOfWeights()))

	# histograms pad
	 
        pad1 = ROOT.TPad("histo_pos","histo_pos",0., 0.35, 1, 1)
        pad1.SetTopMargin(0.05)
        pad1.SetBottomMargin(0)
        pad1.SetLeftMargin(0.15)
	pad1.SetGridx()
	pad1.SetLogy()
	pad1.Draw()
	pad1.cd()


        histo_sm.Draw('hist')
        histo_sm.SetStats(0)
        histo_sm.SetLineColor(color_sm)
        histo_sm.SetLineWidth(3)
	#histo_sm.GetYaxis().SetRangeUser(2e-6, 2) #STXS
	histo_sm.GetYaxis().SetRangeUser(2e-6,.2) 
        histo_sm.GetYaxis().SetLabelSize(0.05)
	histo_sm.GetXaxis().SetTitle(histo_dc[histo_key][0])
        histo_sm.GetXaxis().SetTitleSize(0.05)
	#histo_sm.GetYaxis().SetTitle("d#sigma/dpT(H) [STXS]") #STXS
	histo_sm.GetYaxis().SetTitle("d#sigma/dpT(H)")
        histo_sm.GetYaxis().SetTitleSize(0.05)


	histo_sm.SetTitle("")
   
        histo_zero.Draw('hist,same')
        histo_zero.SetStats(0)
        histo_zero.SetLineColor(color_zero)
        histo_zero.SetLineWidth(3)

        histo_cpt.Draw('hist,same')
        histo_cpt.SetStats(0)
        histo_cpt.SetLineColor(color_cpt)
        histo_cpt.SetLineWidth(3)

        histo_ctg.Draw('hist,same')
        histo_ctg.SetStats(0)
        histo_ctg.SetLineColor(color_ctg)
        histo_ctg.SetLineWidth(3)

        leg = ROOT.TLegend(.95,.75,.75,.95) #STXS
        #leg = ROOT.TLegend(.85,.55,.55,.75)
        leg.AddEntry(histo_sm, "sm","l")
        leg.AddEntry(histo_zero, "smeft cpt=0 ctg=0","l")
        leg.AddEntry(histo_cpt, "smeft cpt=1 ctg=0","l")
        leg.AddEntry(histo_ctg, "smeft cpt=0 ctg=1","l")
        leg.SetTextSize(.035)
        leg.Draw()

        canvas.cd()

        ratio_zero_sm = histo_zero.Clone()
        ratio_zero_sm.Divide(histo_sm)

        ratio_cpt_sm = histo_cpt.Clone()
        ratio_cpt_sm.Divide(histo_sm)

        ratio_ctg_sm = histo_ctg.Clone()
        ratio_ctg_sm.Divide(histo_sm)

        # lower pad
        pad2 = ROOT.TPad("histo_ratio","histo_ratio",0., 0.0 , 1, 0.35)
        pad2.SetTopMargin(0.0)
        pad2.SetLeftMargin(0.15)
        pad2.SetBottomMargin(0.27)
        pad2.SetGridx()
        pad2.SetGridy()
        #pad2.SetLogy()
        pad2.Draw()
        pad2.cd()


        ratio_zero_sm.Draw('hist')
        ratio_zero_sm.SetStats(0)
        ratio_zero_sm.SetLineColor(color_sm_zero)
        ratio_zero_sm.SetLineStyle(1)
        ratio_zero_sm.SetLineWidth(3)
        ratio_zero_sm.GetYaxis().SetRangeUser(-1.0,9.0)
        ratio_zero_sm.GetXaxis().SetLabelSize(0.1)
        ratio_zero_sm.GetXaxis().SetLabelOffset(0.01)
        ratio_zero_sm.GetYaxis().SetLabelSize(0.1)
        ratio_zero_sm.GetYaxis().SetLabelOffset(0.01)
	ratio_zero_sm.GetXaxis().SetTitle(histo_dc[histo_key][0])
        ratio_zero_sm.GetXaxis().SetTitleSize(0.1)
	ratio_zero_sm.GetYaxis().SetTitle("smeft/sm")
        ratio_zero_sm.GetYaxis().SetTitleSize(0.1)
        ratio_zero_sm.GetYaxis().SetTitleOffset(0.7)

        ratio_zero_sm.SetTitle("")


        ratio_cpt_sm.Draw('hist,same')
        ratio_cpt_sm.SetLineColor(color_sm_cpt)
        ratio_cpt_sm.SetLineStyle(1)
        ratio_cpt_sm.SetLineWidth(3)

        ratio_ctg_sm.Draw('hist,same')
        ratio_ctg_sm.SetLineColor(color_sm_ctg)
        ratio_ctg_sm.SetLineStyle(1)
        ratio_ctg_sm.SetLineWidth(3)


        leg2 = ROOT.TLegend(.95,.75,.75,.95) #STXS
        leg2.AddEntry(ratio_zero_sm, "cpt=0 ctg=0","l")
        leg2.AddEntry(ratio_cpt_sm,  "cpt=1 ctg=0","l")
        leg2.AddEntry(ratio_ctg_sm, "cpt=0 ctg=1","l")
        leg2.SetTextSize(0.065)
        leg2.Draw()

        canvas.cd()

	
        #canvas.Write()
	canvas.SaveAs("./plots/plot_" + histo_key + ".pdf")


