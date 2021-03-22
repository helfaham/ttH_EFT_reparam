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
    file_sm_prod = main_dir + "/root_files/sm_tth_prod.root"

    file_zero = main_dir + "/root_files/smeft_tth_wilson_zero.root"
    file_zero_prod = main_dir + "/root_files/smeft_tth_wilson_zero_prod.root"

    file_cpt = main_dir + "/root_files/smeft_tth_wilson_cpt.root"
    file_cpt_prod = main_dir + "/root_files/smeft_tth_wilson_cpt_prod.root"

    file_ctg = main_dir + "/root_files/smeft_tth_wilson_ctg.root"
    file_ctg_prod = main_dir + "/root_files/smeft_tth_wilson_ctg_prod.root"

    ifile_sm = ROOT.TFile.Open(file_sm)
    ifile_sm_prod = ROOT.TFile.Open(file_sm_prod)

    ifile_zero = ROOT.TFile.Open(file_zero)
    ifile_zero_prod = ROOT.TFile.Open(file_zero_prod)

    ifile_cpt = ROOT.TFile.Open(file_cpt)
    ifile_cpt_prod = ROOT.TFile.Open(file_cpt_prod)

    ifile_ctg = ROOT.TFile.Open(file_ctg)
    ifile_ctg_prod = ROOT.TFile.Open(file_ctg_prod)
    
    histo_dc = {
      'higgs_pt': ('pt_{higgs} [GeV]', 0, 800),
      #'higgs_mass': ('mass_{higgs} [GeV]', 0, 200),
    }

    color_sm = 633  # red
    color_sm_prod = 6  # purple

    color_zero = 1   # black
    color_zero_prod = 16   # grey

    color_cpt = 797  # orange
    color_cpt_prod = 5  # yellow

    color_ctg = 824  # green
    color_ctg_prod = 4  # blue

    color_sm_prod_sm_fc = 6 
    color_zero_prod_zero_fc = 16 
    color_cpt_prod_cpt_fc = 5
    color_ctg_prod_ctg_fc = 4 

    ROOT.gROOT.SetBatch()

    for histo_key in histo_dc:

        canvas = ROOT.TCanvas(histo_key, histo_key, 1000, 910)

        histo_sm = ifile_sm.Get(histo_key)
        histo_sm_prod = ifile_sm_prod.Get(histo_key)

        histo_zero = ifile_zero.Get(histo_key)
        histo_zero_prod = ifile_zero_prod.Get(histo_key)

        histo_cpt = ifile_cpt.Get(histo_key)
        histo_cpt_prod = ifile_cpt_prod.Get(histo_key)

        histo_ctg = ifile_ctg.Get(histo_key)
        histo_ctg_prod = ifile_ctg_prod.Get(histo_key)

        print("sm: %.4f pb" %(histo_sm.GetSumOfWeights()))
        print("sm prod: %.4f pb" %(histo_sm_prod.GetSumOfWeights()))

        print("smeft zero wilson: %.4f pb" %(histo_zero.GetSumOfWeights()))
        print("smeft zero wilson prod: %.4f pb" %(histo_zero_prod.GetSumOfWeights()))

        print("smeft cpt wilson: %.4f pb" %(histo_cpt.GetSumOfWeights()))
        print("smeft cpt wilson prod: %.4f pb" %(histo_cpt_prod.GetSumOfWeights()))

        print("smeft ctg wilson: %.4f pb" %(histo_ctg.GetSumOfWeights()))
        print("smeft ctg wilson prod: %.4f pb" %(histo_ctg_prod.GetSumOfWeights()))


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

        #histo_zero.Draw('hist,same')
        #histo_zero.SetStats(0)
        #histo_zero.SetLineColor(color_zero)
        #histo_zero.SetLineWidth(3)

        #histo_cpt.Draw('hist,same')
        #histo_cpt.SetStats(0)
        #histo_cpt.SetLineColor(color_cpt)
        #histo_cpt.SetLineWidth(3)

        histo_ctg.Draw('hist,same')
        histo_ctg.SetStats(0)
        histo_ctg.SetLineColor(color_ctg)
        histo_ctg.SetLineWidth(3)

        histo_sm_prod.Draw('hist,same')
        histo_sm_prod.SetStats(0)
        histo_sm_prod.SetLineColor(color_sm_prod)
        histo_sm_prod.SetLineWidth(3)

        #histo_zero_prod.Draw('hist,same')
        #histo_zero_prod.SetStats(0)
        #histo_zero_prod.SetLineColor(color_zero_prod)
        #histo_zero_prod.SetLineWidth(3)

        #histo_cpt_prod.Draw('hist,same')
        #histo_cpt_prod.SetStats(0)
        #histo_cpt_prod.SetLineColor(color_cpt_prod)
        #histo_cpt_prod.SetLineWidth(3)

        histo_ctg_prod.Draw('hist,same')
        histo_ctg_prod.SetStats(0)
        histo_ctg_prod.SetLineColor(color_ctg_prod)
        histo_ctg_prod.SetLineWidth(3)

        leg = ROOT.TLegend(.95,.65,.65,.95) #STXS
        leg.AddEntry(histo_sm, "sm fc","l")
        #leg.AddEntry(histo_zero, "smeft fc cpt=0 ctg=0","l")
        #leg.AddEntry(histo_cpt, "smeft fc cpt=1 ctg=0","l")
        leg.AddEntry(histo_ctg, "smeft fc cpt=0 ctg=1","l")

        leg.AddEntry(histo_sm_prod, "sm pr","l")
        #leg.AddEntry(histo_zero_prod, "smeft pr cpt=0 ctg=0","l")
        #leg.AddEntry(histo_cpt_prod, "smeft pr cpt=1 ctg=0","l")
        leg.AddEntry(histo_ctg_prod, "smeft pr cpt=0 ctg=1","l")
        leg.SetTextSize(.035)
        leg.Draw()

        canvas.cd()

        ratio_sm_prod_sm_fc = histo_sm_prod.Clone()
        ratio_sm_prod_sm_fc.Divide(histo_sm)

        ratio_zero_prod_zero_fc = histo_zero_prod.Clone()
        ratio_zero_prod_zero_fc.Divide(histo_zero)

        ratio_cpt_prod_cpt_fc = histo_cpt_prod.Clone()
        ratio_cpt_prod_cpt_fc.Divide(histo_cpt)

        ratio_ctg_prod_ctg_fc = histo_ctg_prod.Clone()
        ratio_ctg_prod_ctg_fc.Divide(histo_ctg)

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


        ratio_sm_prod_sm_fc.Draw('hist')
        ratio_sm_prod_sm_fc.SetStats(0)
        ratio_sm_prod_sm_fc.SetLineColor(color_sm_prod_sm_fc)
        ratio_sm_prod_sm_fc.SetLineStyle(1)
        ratio_sm_prod_sm_fc.SetLineWidth(3)
        ratio_sm_prod_sm_fc.GetYaxis().SetRangeUser(0.0,2.0)
        ratio_sm_prod_sm_fc.GetXaxis().SetLabelSize(0.1)
        ratio_sm_prod_sm_fc.GetXaxis().SetLabelOffset(0.01)
        ratio_sm_prod_sm_fc.GetYaxis().SetLabelSize(0.1)
        ratio_sm_prod_sm_fc.GetYaxis().SetLabelOffset(0.01)
	ratio_sm_prod_sm_fc.GetXaxis().SetTitle(histo_dc[histo_key][0])
        ratio_sm_prod_sm_fc.GetXaxis().SetTitleSize(0.1)
	ratio_sm_prod_sm_fc.GetYaxis().SetTitle("prod/full-chain")
        ratio_sm_prod_sm_fc.GetYaxis().SetTitleSize(0.1)
        ratio_sm_prod_sm_fc.GetYaxis().SetTitleOffset(0.7)

        ratio_sm_prod_sm_fc.SetTitle("")

        #ratio_zero_prod_zero_fc.Draw('hist,same')
        #ratio_zero_prod_zero_fc.SetLineColor(color_zero_prod_zero_fc)
        #ratio_zero_prod_zero_fc.SetLineStyle(1)
        #ratio_zero_prod_zero_fc.SetLineWidth(3)

        #ratio_cpt_prod_cpt_fc.Draw('hist,same')
        #ratio_cpt_prod_cpt_fc.SetLineColor(color_cpt_prod_cpt_fc)
        #ratio_cpt_prod_cpt_fc.SetLineStyle(1)
        #ratio_cpt_prod_cpt_fc.SetLineWidth(3)

        ratio_ctg_prod_ctg_fc.Draw('hist,same')
        ratio_ctg_prod_ctg_fc.SetLineColor(color_ctg_prod_ctg_fc)
        ratio_ctg_prod_ctg_fc.SetLineStyle(1)
        ratio_ctg_prod_ctg_fc.SetLineWidth(3)

        leg2 = ROOT.TLegend(.065,.22,.22,.065) #STXS
        #leg2 = ROOT.TLegend(.89,.65,.65,.89) #STXS
        leg2.AddEntry(ratio_sm_prod_sm_fc, "sm","l")
        #leg2.AddEntry(ratio_zero_prod_zero_fc, "cpt=0 ctg=0","l")
        #leg2.AddEntry(ratio_cpt_prod_cpt_fc,  "cpt=1 ctg=0","l")
        leg2.AddEntry(ratio_ctg_prod_ctg_fc, "cpt=0 ctg=1","l")
        leg2.SetTextSize(0.065)
        leg2.Draw()

        canvas.cd()

	
        #canvas.Write()
	canvas.SaveAs("./plots/plot_prod_ctg_" + histo_key + ".pdf")


