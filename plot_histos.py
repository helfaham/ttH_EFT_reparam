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

    file_un = main_dir + "/unweighted.root"
    file_re = main_dir + "/reweighted.root"

    ifile_un = ROOT.TFile.Open(file_un)
    ifile_re = ROOT.TFile.Open(file_re)

    
    histo_dc = {
      'higgs_pt': ('pt_{higgs} [GeV]', 0, 1000),
    }

    color_un = 1   # black
    color_re = 797  # orange
    color_ratio = 824 # green


    ROOT.gROOT.SetBatch()

    for histo_key in histo_dc:

        canvas = ROOT.TCanvas(histo_key, histo_key, 800, 725)

        histo_un = ifile_un.Get(histo_key)
        histo_re = ifile_re.Get(histo_key)

        print("SM xsec:       %.4f pb" %(histo_un.GetSumOfWeights()))
        print("EFT xsec: %.4f pb" %(histo_re.GetSumOfWeights()))	

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

        histo_un.Draw('hist')
        histo_un.SetStats(0)
        histo_un.SetLineColor(color_un)
        histo_un.SetLineWidth(3)
	histo_un.GetYaxis().SetRangeUser(2e-6,.2)
        histo_un.GetYaxis().SetLabelSize(0.05)
	histo_un.GetXaxis().SetTitle(histo_dc[histo_key][0])
        histo_un.GetXaxis().SetTitleSize(0.05)
	histo_un.GetYaxis().SetTitle("d#sigma/dpT(H) [pb/10 GeV]")
        histo_un.GetYaxis().SetTitleSize(0.05)


	histo_un.SetTitle("")
   
        histo_re.Draw('hist,same')
        histo_re.SetStats(0)
        histo_re.SetLineColor(color_re)
        histo_re.SetLineWidth(3)

        leg = ROOT.TLegend(.85,.55,.55,.75)
        leg.AddEntry(histo_un, "SM","l")
        leg.AddEntry(histo_re, "rwgt (EFT)","l")
        leg.SetTextSize(.035)
        leg.Draw()

        canvas.cd()

        ratio = histo_un.Clone()
        ratio.Divide(histo_re)

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
	ratio.GetYaxis().SetTitle("SM / rwgt (EFT)")
        ratio.GetYaxis().SetTitleSize(0.1)
        ratio.GetYaxis().SetTitleOffset(0.7)

        ratio.SetTitle("")

        #leg2 = ROOT.TLegend(.6,.3,.9,.65)
        #leg2.AddEntry(ratio, " SM / rwgt (EFT)","l")
        #leg2.SetTextSize(0.065)
        #leg2.Draw()

        canvas.cd()

	
        #canvas.Write()
	canvas.SaveAs("plot_" + histo_key + ".pdf")


