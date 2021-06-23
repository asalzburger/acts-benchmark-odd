import ROOT
import numpy as np
import matplotlib.pyplot as plt

parameters = {'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12,
          'legend.fontsize': 12,
          'lines.linewidth' : 2,
          'lines.markersize' : 7}
plt.rcParams.update(parameters)


ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetStatX(0.90)                
ROOT.gStyle.SetStatY(0.45)                
ROOT.gStyle.SetStatW(0.25)                
ROOT.gStyle.SetStatH(0.15)

def getEff(fileName, effName, lbin, hbin, x, y, yerr):
  f = ROOT.TFile.Open(fileName)
  tefficiency = f.Get(effName)
  htotal = tefficiency.GetTotalHistogram()
  for xbin in range(lbin,hbin): 
    binContent = htotal.GetXaxis().GetBinCenter(xbin)
    eff = tefficiency.GetEfficiency(xbin)*100
    err_low = tefficiency.GetEfficiencyErrorLow(xbin)*100
    err_up = tefficiency.GetEfficiencyErrorUp(xbin)*100
    x.append(binContent)
    y.append(eff)
    yerr.append(err_up)

# open file
# 100 ttbar, constant field
#fileName1 = "../data/reco_generic_const2Tesla_truthEstimatedSeeds_e100/ttbar_mu200_bothpT1GeV_nHits6_deltaRMin10_deltaRMax100_nSeedsMax1_bestSeed/performance_ckf.root"
#fileName2 = "../data/reco_generic_const2Tesla_e100/ttbar_mu200_bothpT1GeV_nHits6/performance_ckf.root"
#detector = "Generic_const2Tesla"

#Below are solenoidal field
# 100 ttbar events
#fileName1 = "../data/reco_generic_sole2Tesla_truthEstimatedSeeds_e100/ttbar_mu200_bothpT1GeV_nHits6_deltaRMin10_deltaRMax100_nSeedsMax1_bestSeed/performance_ckf.root"
#fileName2 = "../data/reco_generic_sole2Tesla_e100/ttbar_mu200_bothpT1GeV_nHits6/performance_ckf.root"

# 1000 ttbar events. Removing fake tracks in eta = [0.8, 1.0] for reco tracks
# 1) real truth seeds
fileName1 = "../data/reco_generic_sole2Tesla_truthEstimatedSeeds/ttbar_mu200_bothpT1GeV_nHits6_realTruth_resTime1ns_eta0p8_OR3/performance_ckf.root"
# 2) truth estimated seeds
#fileName1 = "../data/reco_generic_sole2Tesla_truthEstimatedSeeds/ttbar_mu200_bothpT1GeV_nHits6_deltaRMin10_deltaRMax100_nSeedsMax1_bestSeed_resTheta0p02_resPhi0p02/performance_ckf.root"
# reco seeds
fileName2 = "../data/reco_generic_sole2Tesla/ttbar_mu200_bothpT1GeV_nHits6_resTheta0p02_resPhi0p02_eta0p8_OR3_HR2/performance_ckf.root"

# 1000 ttbar events. Removing fake tracks in eta = [0.8, 1.0] for reco tracks and those in eta>1.8 region for truth and reco tracks
#fileName1 = "../data/reco_generic_sole2Tesla_truthEstimatedSeeds/ttbar_mu200_bothpT1GeV_nHits6_deltaRMin10_deltaRMax100_nSeedsMax1_bestSeed_resTheta0p02_resPhi0p02_eta1p8_OR6/performance_ckf.root"
#fileName2 = "../data/reco_generic_sole2Tesla/ttbar_mu200_bothpT1GeV_nHits6_resTheta0p02_resPhi0p02_eta0p8_OR3_HR2_eta1p8_OR5_eta2_OR6/performance_ckf.root"

detector = "Generic_sole2Tesla"

effNames = ["trackeff_vs_eta", "fakerate_vs_eta", "duplicationRate_vs_eta"] 

xlables = ["Truth $\eta$", "$\eta$", "$\eta$"]
ylables = ["Tracking efficiency (%)", "Fake rate (%)", "Duplication rate (%)"]

ylimits = [ [70, 110], [0, 0.08], [0, 140]]
#ylimits = [ [0.7, 1.1], [0, 0.0008], [0, 1.4]]

#old: ylimits = [ [0.7, 1.1], [0, 0.0005], [0, 1.4]]

x = [[], [], [], [], [], []] 
y = [[], [], [], [], [], []] 
yerr = [[], [], [], [], [], []] 

i=0
while i < 3:
  getEff(fileName1, effNames[i],  8, 34, x[i*2], y[i*2], yerr[i*2])
  getEff(fileName2, effNames[i],  8, 34, x[i*2+1], y[i*2+1], yerr[i*2+1])

  ax = plt.subplot(111)
  plt.errorbar(x[i*2], y[i*2], yerr=yerr[i*2], label='Truth seeds',  marker="o", ls='none')
  plt.errorbar(x[i*2+1], y[i*2+1], yerr=yerr[i*2+1], label='Reco seeds',  marker="^", ls='none')
  plt.legend()
  ylimit = ylimits[i]
  ax.set_ylim((ylimit[0],ylimit[1]))
  ax.set_xlabel(xlables[i])
  ax.set_ylabel(ylables[i])
#  if i == 1:
#    plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))

  if i == 0:
    figName ="./plots/python/" + effNames[i] + "_ttbar_e1000_mu200_" + detector + "_bothpT1GeV.eps"
  else:
    figName ="./plots/python/" + effNames[i] + "_ttbar_e1000_mu200_" + detector + "_pT1GeV.eps"

  plt.savefig(figName, format='eps')
  plt.show()

  i += 1

