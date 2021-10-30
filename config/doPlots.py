#!/usr/bin/env python
import sys, os
import os.path
import ntpath
import importlib
import ROOT
import copy
import re

#__________________________________________________________
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

#__________________________________________________________
def mapHistos(var, label, sel, param):
    print ('run plots for var:{}     label:{}     selection:{}'.format(var,label,sel))
    signal=param.plots[label]['signal']
    backgrounds=param.plots[label]['backgrounds']

    hsignal = {}
    for s in signal:
        hsignal[s]=[]
        for f in signal[s]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                scaleSig=1.
                try:
                    scaleSig=param.scaleSig
                except AttributeError:
                    print ('no scale signal, using 1')
                    param.scaleSig=scaleSig
                print ('scaleSig ',scaleSig)
                hh.Scale(param.intLumi*scaleSig)

                if len(hsignal[s])==0:
                    hsignal[s].append(hh)
                else:
                    hh.Add(hsignal[s][0])
                    hsignal[s][0]=hh


    hbackgrounds = {}
    for b in backgrounds:
        hbackgrounds[b]=[]
        for f in backgrounds[b]:
            fin=param.inputDir+f+'_'+sel+'_histo.root'
            if not os.path.isfile(fin):
                print ('file {} does not exist, skip'.format(fin))
            else:
                tf=ROOT.TFile(fin)
                h=tf.Get(var)
                hh = copy.deepcopy(h)
                hh.Scale(param.intLumi)
                if len(hbackgrounds[b])==0:
                    hbackgrounds[b].append(hh)
                else:
                    hh.Add(hbackgrounds[b][0])
                    hbackgrounds[b][0]=hh

    for s in hsignal:
        if len(hsignal[s])==0:
            hsignal=removekey(hsignal,s)

    for b in hbackgrounds:
        if len(hbackgrounds[b])==0:
            hbackgrounds=removekey(hbackgrounds,b)

    return hsignal,hbackgrounds

#__________________________________________________________
def runPlots(var,sel,param,hsignal,hbackgrounds,extralab):
    legsize = 0.04*(len(hbackgrounds)+len(hsignal))
    legCoord=[0.68, 0.86-legsize, 0.96, 0.88]
    try:
        legCoord=param.legendCoord
    except AttributeError:
        print ('no legCoord, using default one...')
        legCoord=[0.68, 0.86-legsize, 0.96, 0.88]

    leg = ROOT.TLegend(legCoord[0],legCoord[1],legCoord[2],legCoord[3])
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetShadowColor(10)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    for s in hsignal:
        leg.AddEntry(hsignal[s][0],param.legend[s],"l")
    for b in hbackgrounds:
        leg.AddEntry(hbackgrounds[b][0],param.legend[b],"f")
 

    yields={}
    for s in hsignal:
        yields[s]=[param.legend[s],hsignal[s][0].Integral(0,-1), hsignal[s][0].GetEntries()]
    for b in hbackgrounds:
        yields[b]=[param.legend[b],hbackgrounds[b][0].Integral(0,-1), hbackgrounds[b][0].GetEntries()]

    histos=[]
    colors=[]

    nsig=len(hsignal)

    for s in hsignal:
        histos.append(hsignal[s][0])
        colors.append(param.colors[s])

    for b in hbackgrounds:
        histos.append(hbackgrounds[b][0])
        colors.append(param.colors[b])

    intLumiab = param.intLumi/1e+06 

    
    lt = "FCCAnalyses: FCC-hh Simulation (Delphes)"    
    rt = "#sqrt{{s}} = {:.1f} TeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    if 'ee' in param.collider:
        lt = "FCCAnalyses: FCC-ee Simulation (Delphes)"
        rt = "#sqrt{{s}} = {:.1f} GeV,   L = {:.0f} ab^{{-1}}".format(param.energy,intLumiab)

    customLabel=""
    try:
        customLabel=param.customLabel
    except AttributeError:
        print ('no customLable, using nothing...')

    if 'AAAyields' in var:
        drawStack(var, 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, False , True , histos, colors, param.ana_tex, extralab, param.scaleSig, customLabel, nsig, yields)
        return
        
    if 'stack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_stack_lin", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, False , True , histos, colors, param.ana_tex, extralab, param.scaleSig, customLabel, nsig)
        if 'log' in param.yaxis:
            drawStack(var+"_stack_log", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, True , True , histos, colors, param.ana_tex, extralab, param.scaleSig, customLabel, nsig)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))

    if 'nostack' in param.stacksig:
        if 'lin' in param.yaxis:
            drawStack(var+"_nostack_lin", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, False , False , histos, colors, param.ana_tex, extralab, param.scaleSig, customLabel, nsig)
        if 'log' in param.yaxis:
            drawStack(var+"_nostack_log", 'events', leg, lt, rt, param.formats, param.outdir+"/"+sel, True , False , histos, colors, param.ana_tex, extralab, param.scaleSig, customLabel, nsig)
        if 'lin' not in param.yaxis and 'log' not in param.yaxis:
            print ('unrecognised option in formats, should be [\'lin\',\'log\']'.format(param.formats))
    if 'stack' not in param.stacksig and 'nostack' not in param.stacksig:
        print ('unrecognised option in stacksig, should be [\'stack\',\'nostack\']'.format(param.formats))


#_____________________________________________________________________________________________________________
def drawStack(name, ylabel, legend, leftText, rightText, formats, directory, logY, stacksig, histos, colors, ana_tex, extralab, scaleSig, customLabel, nsig,  yields=None):

    canvas = ROOT.TCanvas(name, name, 600, 600) 
    canvas.SetLogy(logY)
    canvas.SetTicks(1,1)
    canvas.SetLeftMargin(0.14)
    canvas.SetRightMargin(0.08)
 

    # first retrieve maximum 
    sumhistos = histos[0].Clone()
    iterh = iter(histos)
    next(iterh)

    unit = 'GeV'
    if 'TeV' in str(histos[1].GetXaxis().GetTitle()):
        unit = 'TeV'
    
    if unit in str(histos[1].GetXaxis().GetTitle()):
        bwidth=sumhistos.GetBinWidth(1)
        if bwidth.is_integer():
            ylabel+=' / {} {}'.format(int(bwidth), unit)
        else:
            ylabel+=' / {:.2f} {}'.format(bwidth, unit)

    for h in iterh:
      sumhistos.Add(h)

    maxh = sumhistos.GetMaximum()
    minh = sumhistos.GetMinimum()

    if logY: 
       canvas.SetLogy(1)

    # define stacked histo
    hStack    = ROOT.THStack("hstack","")
    hStackBkg = ROOT.THStack("hstackbkg","")

    # first plot backgrounds
    histos[nsig].SetLineWidth(0)
    histos[nsig].SetLineColor(ROOT.kBlack)
    histos[nsig].SetFillColor(colors[nsig])
    hStack.Add(histos[nsig])
    hStackBkg.Add(histos[nsig])
    
    # now loop over other background (skipping first)
    iterh = iter(histos)
    for i in range(nsig):
        next(iterh)
    next(iterh)
    
    k = nsig+1
    for h in iterh:
       h.SetLineWidth(0)
       h.SetLineColor(ROOT.kBlack)
       h.SetFillColor(colors[k])
       hStack.Add(h)
       hStackBkg.Add(h)
       k += 1

    if not stacksig:
       hStack.Draw("hist")

    # define stacked signal histo
    hStackSig = ROOT.THStack("hstacksig","")

    # finally add signal on top
    for l in range(nsig):
      histos[l].SetLineWidth(3)
      histos[l].SetLineColor(colors[l])
      if stacksig:
        hStack.Add(histos[l])
      else:
        hStackSig.Add(histos[l])

    if stacksig:
        hStack.Draw("hist")

    xlabel = histos[1].GetXaxis().GetTitle()

    hStack.GetXaxis().SetTitle(xlabel)
    hStack.GetYaxis().SetTitle(ylabel)

    hStack.GetYaxis().SetTitleOffset(1.95)
    hStack.GetXaxis().SetTitleOffset(1.40)
    
    lowY=0.
    if logY:
        highY=200.*maxh/ROOT.gPad.GetUymax()
        threshold=0.5
        bin_width=hStack.GetXaxis().GetBinWidth(1)
        lowY=threshold*bin_width
        hStack.SetMaximum(highY)
        hStack.SetMinimum(lowY)
    else:
        hStack.SetMaximum(1.3*maxh)
        hStack.SetMinimum(0.)

    escape_scale_Xaxis=True    
    hStacklast = hStack.GetStack().Last()
    lowX_is0=True
    lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
    highX_ismax=False
    highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)

    if escape_scale_Xaxis==False:
      for i_bin in range( 1, hStacklast.GetNbinsX()+1 ):
         bkg_val=hStacklast.GetBinContent(i_bin)
         sig_val=histos[0].GetBinContent(i_bin)
         if bkg_val/maxh>0.1 and i_bin<15 and lowX_is0==True :
           lowX_is0=False
           lowX=hStacklast.GetBinCenter(i_bin)-(hStacklast.GetBinWidth(i_bin)/2.)

         val_to_compare=bkg_val
         if sig_val>bkg_val : val_to_compare=sig_val
         if val_to_compare<lowY and i_bin>15 and highX_ismax==False: 
           highX_ismax=True
           highX=hStacklast.GetBinCenter(i_bin)+(hStacklast.GetBinWidth(i_bin)/2.)
           highX*=1.1
    # protections
    if lowX<hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.) :
      lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
    if highX>hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.) :
      highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)
    if lowX>=highX :
      lowX=hStacklast.GetBinCenter(1)-(hStacklast.GetBinWidth(1)/2.)
      highX=hStacklast.GetBinCenter(hStacklast.GetNbinsX())+(hStacklast.GetBinWidth(1)/2.)
    hStack.GetXaxis().SetLimits(int(lowX),int(highX))

    if not stacksig:
        if 'AAAyields' not in name: hStackSig.Draw("same hist nostack")

    legend.Draw() 
                        
    Text = ROOT.TLatex()    
    Text.SetNDC() 
    Text.SetTextAlign(31);
    Text.SetTextSize(0.04) 

    text = '#it{' + leftText +'}'
    Text.DrawLatex(0.90, 0.94, text) 

    text = '#it{'+customLabel+'}'
    Text.SetTextAlign(12);
    Text.SetNDC(ROOT.kTRUE) 
    Text.SetTextSize(0.04) 
    Text.DrawLatex(0.18, 0.85, text)

    rightText = re.split(",", rightText)
    text = '#bf{#it{' + rightText[0] +'}}'
    
    Text.SetTextAlign(12);
    Text.SetNDC(ROOT.kTRUE) 
    Text.SetTextSize(0.04) 
    Text.DrawLatex(0.18, 0.81, text)

    rightText[1]=rightText[1].replace("   ","")    
    text = '#bf{#it{' + rightText[1] +'}}'
    Text.SetTextSize(0.035) 
    Text.DrawLatex(0.18, 0.76, text)

    text = '#bf{#it{' + ana_tex +'}}'
    Text.SetTextSize(0.04)
    Text.DrawLatex(0.18, 0.71, text)

    text = '#bf{#it{' + extralab +'}}'
    Text.SetTextSize(0.025)
    Text.DrawLatex(0.18, 0.66, text)

    text = '#bf{#it{' + 'Signal scale=' + str(scaleSig)+'}}'
    Text.SetTextSize(0.025)
    if scaleSig!=1:Text.DrawLatex(0.18, 0.63, text)

    canvas.RedrawAxis()
    canvas.GetFrame().SetBorderSize( 12 )
    canvas.Modified()
    canvas.Update()

    if 'AAAyields' in name:
        dummyh=ROOT.TH1F("","",1,0,1)
        dummyh.SetStats(0)
        dummyh.GetXaxis().SetLabelOffset(999)
        dummyh.GetXaxis().SetLabelSize(0)
        dummyh.GetYaxis().SetLabelOffset(999)
        dummyh.GetYaxis().SetLabelSize(0)
        dummyh.Draw("AH")
        legend.Draw()
        
        Text.SetNDC() 
        Text.SetTextAlign(31);
        Text.SetTextSize(0.04) 

        text = '#it{' + leftText +'}'
        Text.DrawLatex(0.90, 0.92, text)
        
        text = '#bf{#it{' + rightText[0] +'}}'
        Text.SetTextAlign(12);
        Text.SetNDC(ROOT.kTRUE) 
        Text.SetTextSize(0.04) 
        Text.DrawLatex(0.18, 0.83, text)

        text = '#bf{#it{' + rightText[1] +'}}'
        Text.SetTextSize(0.035) 
        Text.DrawLatex(0.18, 0.78, text)

        text = '#bf{#it{' + ana_tex +'}}'
        Text.SetTextSize(0.04)
        Text.DrawLatex(0.18, 0.73, text)
        
        text = '#bf{#it{' + extralab +'}}'
        Text.SetTextSize(0.025)
        Text.DrawLatex(0.18, 0.68, text)

        text = '#bf{#it{' + 'Signal scale=' + str(scaleSig)+'}}'
        Text.SetTextSize(0.04)
        Text.DrawLatex(0.18, 0.55, text)

        dy=0
        text = '#bf{#it{' + 'Process' +'}}'
        Text.SetTextSize(0.035)
        Text.DrawLatex(0.18, 0.45, text)
        
        text = '#bf{#it{' + 'Yields' +'}}'
        Text.SetTextSize(0.035)
        Text.DrawLatex(0.5, 0.45, text)
        
        text = '#bf{#it{' + 'Raw MC' +'}}'
        Text.SetTextSize(0.035)
        Text.DrawLatex(0.75, 0.45, text)

        for y in yields:
            text = '#bf{#it{' + yields[y][0] +'}}'
            Text.SetTextSize(0.035)
            Text.DrawLatex(0.18, 0.4-dy*0.05, text)

            stry=str(yields[y][1])
            stry=stry.split('.')[0]
            text = '#bf{#it{' + stry +'}}'
            Text.SetTextSize(0.035)
            Text.DrawLatex(0.5, 0.4-dy*0.05, text)
            
            stry=str(yields[y][2])
            stry=stry.split('.')[0]
            text = '#bf{#it{' + stry +'}}'
            Text.SetTextSize(0.035)
            Text.DrawLatex(0.75, 0.4-dy*0.05, text)

            
            dy+=1
        #canvas.Modified()
        #canvas.Update()
       
        
    printCanvas(canvas, name, formats, directory) 

    


#____________________________________________________
def printCanvas(canvas, name, formats, directory):

    if format != "":
        if not os.path.exists(directory) :
                os.system("mkdir -p "+directory)
        for f in formats:
            outFile = os.path.join(directory, name) + "." + f
            canvas.SaveAs(outFile)



#__________________________________________________________
if __name__=="__main__":
    ROOT.gROOT.SetBatch(True)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    # param file
    paramFile = sys.argv[1]

    module_path = os.path.abspath(paramFile)
    module_dir = os.path.dirname(module_path)
    base_name = os.path.splitext(ntpath.basename(paramFile))[0]

    sys.path.insert(0, module_dir)
    param = importlib.import_module(base_name)
        
    counter=0
    for var in param.variables:
        for label, sels in param.selections.items():
            for sel in sels:
                hsignal,hbackgrounds=mapHistos(var,label,sel, param)
                runPlots(var+"_"+label,sel,param,hsignal,hbackgrounds,param.extralabel[sel])
                if counter==0: runPlots("AAAyields_"+label,sel,param,hsignal,hbackgrounds,param.extralabel[sel])
        counter+=1
