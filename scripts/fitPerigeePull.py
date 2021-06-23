import ROOT
import numpy as np
import matplotlib.pyplot as plt
from ROOT import TF1
import sys

parameters = {'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12,
          'legend.fontsize': 12,
          'lines.linewidth' : 2.5,
          'lines.markersize' : 5}
plt.rcParams.update(parameters)

ROOT.TH1.SetDefaultSumw2()
ROOT.gROOT.SetBatch(True)

ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetStatX(0.90)                
ROOT.gStyle.SetStatY(0.45)                
ROOT.gStyle.SetStatW(0.25)                
ROOT.gStyle.SetStatH(0.15)

def gauss(x, A, x0, sigma):
    return A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


func = TF1('func', 'gaus', -5, 5)

def reorderLegend(ax=None,order=None,unique=False):
    if ax is None: ax=plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0])) # sort both labels and handles by labels
    if order is not None: # Sort according to a given list (not necessarily complete)
        keys=dict(zip(order,range(len(order))))
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t,keys=keys: keys.get(t[0],np.inf)))
    if unique:  labels, handles= zip(*unique_everseen(zip(labels,handles), key = labels)) # Keep only the first of each handle
    ax.legend(handles, labels)
    return(handles, labels)


#https://matplotlib.org/stable/gallery/statistics/errorbar_features.html
def getHist(fileName, name, x, y, yerr, fitPars, fitParErrs):
  f = ROOT.TFile.Open(fileName)
  hist = f.Get(name)
  hist.Fit("func")
  # extract the fit parameters 
  pars = [0, 1, 2]
  for ip in pars:
    fitPars.append(func.GetParameter(ip)); 
    fitParErrs.append(func.GetParError(ip)); 

  nbins = hist.GetXaxis().GetNbins()
  for xbin in range(1, nbins+1): 
   binCenter  = hist.GetBinCenter(xbin)
   binCont = hist.GetBinContent(xbin)
   binErr =  hist.GetBinError(xbin)
   x.append(binCenter)
   y.append(binCont)
   yerr.append(binErr)

# open file
fileName = str(sys.argv[1])
f = ROOT.TFile.Open(fileName)

paramsIn = ["d0", "z0", "phi", "theta", "qop", "t"] 
params = ["$d_{0}$", "$z_{0}$", "$\phi$", "$\\theta$", "$q/p$", "t"] 

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
#fig.tight_layout()
left  = 0.08    # the left side of the subplots of the figure
right = 0.98    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9      # the top of the subplots of the figure
wspace = 0.3   # the amount of width reserved for blank space between subplots
hspace = 0.2   # the amount of height reserved for white space between subplots
plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

i=0
for param in paramsIn:
  name = "pull_" + param
  x = []
  y = []
  yerr = []
  fitPars = []
  fitParErrs = []
  getHist(fileName, name, x, y, yerr, fitPars, fitParErrs)

  if i < 3:
    irow = 0 
    icol = i 
  else:
    irow = 1 
    icol = i -3

  ax[irow, icol].errorbar(x, y, yerr=yerr, marker="o", ls='none', label = 'Data')
  print(fitPars)
  #0.01 is the sampling granularity 
  xr = np.arange(-5, 5., 0.01)
  #fitlabel = "'Gauss fit: $\mu$ = {0:0.2f} $\pm$ {1:0.2f}, $\sigma$ = {2:0.2f} $\pm$ {3:0.2f}".format(fitPars[1], fitParErrs[1], fitPars[2], fitParErrs[2]) 
  fitlabel = "Gaussian fit: $\mu$ = {0:0.2f}, $\sigma$ = {1:0.2f}".format(fitPars[1], fitPars[2]) 
  ax[irow, icol].plot(xr, gauss(xr, *fitPars), label=fitlabel)
  bottom, top = ax[irow, icol].get_ylim() 
  ax[irow, icol].set_ylim(bottom, top=top*1.3)

  xtitle = "pull(" + params[i] + ")"
  ax[irow, icol].set_xlabel(xtitle)
  ax[irow, icol].set_ylabel("Events/ 0.1")
  ax[irow, icol].legend()
  reorderLegend(ax[irow, icol],["Data", fitlabel]) 

  i += 1

figName=str(sys.argv[2])
plt.savefig(figName, format='png')

plt.show()

