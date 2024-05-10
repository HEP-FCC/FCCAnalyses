
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor, TLorentzVector, TH1D, TH2D
import math
import sys
import string
import numpy as np

gROOT.SetBatch(True)

class ttEvent:
	def __init__(self, event):
		self.pidlist = []
		self.TLVecs = []
		for iPart in range(6,16):
			self.pidlist.append(event.pid[iPart])
			tmpLV = TLorentzVector(0,0,0,0)
			tmpLV.SetPxPyPzE( event.px[iPart] , event.py[iPart] , event.pz[iPart], event.energy[iPart])
			self.TLVecs.append(tmpLV)
		self.lep1 = TLorentzVector(0,0,0,0)
		self.antilep1 = TLorentzVector(0,0,0,0) 
		self.nu1 = TLorentzVector(0,0,0,0)
		self.antinu1 = TLorentzVector(0,0,0,0)  
		self.lep2 = TLorentzVector(0,0,0,0)
		self.antilep2 = TLorentzVector(0,0,0,0) 
		self.nu2 = TLorentzVector(0,0,0,0)
		self.antinu2 = TLorentzVector(0,0,0,0)  
		self.q1 = TLorentzVector(0,0,0,0)
		self.qbar1 = TLorentzVector(0,0,0,0) 
		self.q2 = TLorentzVector(0,0,0,0)
		self.qbar2 = TLorentzVector(0,0,0,0)
		self.Wlepp = TLorentzVector(0,0,0,0)
		self.Wlepn = TLorentzVector(0,0,0,0) 
		self.Whadp = TLorentzVector(0,0,0,0)
		self.Whadn = TLorentzVector(0,0,0,0)
		self.tlepp = TLorentzVector(0,0,0,0)
		self.tlepn = TLorentzVector(0,0,0,0) 
		self.thadp = TLorentzVector(0,0,0,0)
		self.thadn = TLorentzVector(0,0,0,0)
		self.b = TLorentzVector(0,0,0,0)
		self.bbar = TLorentzVector(0,0,0,0)
		self.channel = ""		            
	def consistency(self):
		pidlist = np.asarray(self.pidlist)
		if len(np.where(pidlist == 11)[0]) > 0 and len(np.where(pidlist == -12)[0]) == 0: return False
		if len(np.where(pidlist == 13)[0]) > 0 and len(np.where(pidlist == -14)[0]) == 0: return False
		if len(np.where(pidlist == 15)[0]) > 0 and len(np.where(pidlist == -16)[0]) == 0: return False
		if len(np.where(pidlist == -11)[0]) > 0 and len(np.where(pidlist == 12)[0]) == 0: return False
		if len(np.where(pidlist == -13)[0]) > 0 and len(np.where(pidlist == 14)[0]) == 0: return False
		if len(np.where(pidlist == -15)[0]) > 0 and len(np.where(pidlist == 16)[0]) == 0: return False
		if len(np.where(pidlist == 1)[0]) > 0 and len(np.where(pidlist == -2)[0]) == 0 and len(np.where(pidlist == -4)[0]) == 0: return False
		if len(np.where(pidlist == 2)[0]) > 0 and len(np.where(pidlist == -1)[0]) == 0 and len(np.where(pidlist == -3)[0]) == 0 and len(np.where(pidlist == -5)[0]) == 0: return False
		if len(np.where(pidlist == 3)[0]) > 0 and len(np.where(pidlist == -4)[0]) == 0 and len(np.where(pidlist == -2)[0]) == 0: return False
		if len(np.where(pidlist == 4)[0]) > 0 and len(np.where(pidlist == -3)[0]) == 0 and len(np.where(pidlist == -1)[0]) == 0 and len(np.where(pidlist == -5)[0]) == 0: return False
		if len(np.where(pidlist == -1)[0]) > 0 and len(np.where(pidlist == 2)[0]) == 0 and len(np.where(pidlist == 4)[0]) == 0: return False
		if len(np.where(pidlist == -2)[0]) > 0 and len(np.where(pidlist == 1)[0]) == 0 and len(np.where(pidlist == 3)[0]) == 0 and len(np.where(pidlist == 5)[0]) == 0: return False
		if len(np.where(pidlist == -3)[0]) > 0 and len(np.where(pidlist == 4)[0]) == 0 and len(np.where(pidlist == 2)[0]) == 0: return False
		if len(np.where(pidlist == -4)[0]) > 0 and len(np.where(pidlist == 3)[0]) == 0 and len(np.where(pidlist == 1)[0]) == 0 and len(np.where(pidlist == 5)[0]) == 0: return False
		return True
		
	def setParticles(self):
		if self.pidlist[6] in [11,13,15]:
			self.lep1 = self.TLVecs[6]
			self.antinu1 = self.TLVecs[7]
			self.Wlepn = self.lep1+self.antinu1
		if self.pidlist[6] in [-11,-13,-15]:
			self.antilep1 = self.TLVecs[6]
			self.nu1 = self.TLVecs[7]
			self.Wlepp = self.antilep1+self.nu1
		if self.pidlist[6] in [1,3,5]:		
			self.q1 = self.TLVecs[6]
			self.qbar1 = self.TLVecs[7]
			self.Whadn = self.q1+self.qbar1
		if self.pidlist[6] in [-1,-3,-5]:		
			self.qbar1 = self.TLVecs[6]
			self.q1 = self.TLVecs[7]
			self.Whadp = self.q1+self.qbar1
		if self.pidlist[6] in [2,4]:		
			self.q1 = self.TLVecs[6]
			self.qbar1 = self.TLVecs[7]
			self.Whadp = self.q1+self.qbar1	
		if self.pidlist[6] in [-2,-4]:		
			self.qbar1 = self.TLVecs[6]
			self.q1 = self.TLVecs[7]
			self.Whadn = self.q1+self.qbar1
			
		if self.pidlist[8] in [11,13,15]:
			self.lep2 = self.TLVecs[8]
			self.antinu2 = self.TLVecs[9]
			self.Wlepn = self.lep2+self.antinu2
		if self.pidlist[8] in [-11,-13,-15]:
			self.antilep2 = self.TLVecs[8]
			self.nu2 = self.TLVecs[9]
			self.Wlepp = self.antilep2+self.nu2
		if self.pidlist[8] in [1,3,5]:		
			self.q2 = self.TLVecs[8]
			self.qbar2 = self.TLVecs[9]
			self.Whadn = self.q2+self.qbar2
		if self.pidlist[8] in [-1,-3,-5]:		
			self.qbar2 = self.TLVecs[8]
			self.q2 = self.TLVecs[9]
			self.Whadp = self.q2+self.qbar2
		if self.pidlist[8] in [2,4]:		
			self.q2 = self.TLVecs[8]
			self.qbar2 = self.TLVecs[9]
			self.Whadp = self.q2+self.qbar2	
		if self.pidlist[8] in [-2,-4]:		
			self.qbar2 = self.TLVecs[8]
			self.q2 = self.TLVecs[9]
			self.Whadn = self.q2+self.qbar2
		self.b = self.TLVecs[4]
		self.bbar = self.TLVecs[5]
		self.tlepp = self.Wlepp + self.b
		self.thadp = self.Whadp + self.b
		self.thadn = self.Whadn + self.bbar
		self.tlepn = self.Wlepn + self.bbar
			
	def setChannel(self):
		pidlist = np.asarray(self.pidlist)
		if len(np.where(abs(pidlist) == 11)[0]) == 2: self.channel = "ee"
		elif len(np.where(abs(pidlist) == 13)[0]) == 2: self.channel = "mumu"
		elif len(np.where(abs(pidlist) == 15)[0]) == 2: self.channel = "tautau"
		elif len(np.where(abs(pidlist) == 11)[0]) == 1 and len(np.where(abs(pidlist) == 13)[0]) == 1: self.channel = "emu"
		elif len(np.where(abs(pidlist) == 11)[0]) == 1 and len(np.where(abs(pidlist) == 15)[0]) == 1: self.channel = "etau"
		elif len(np.where(abs(pidlist) == 15)[0]) == 1 and len(np.where(abs(pidlist) == 13)[0]) == 1: self.channel = "mutau"
		elif len(np.where(abs(pidlist) == 11)[0]) == 1 and len(np.where(abs(pidlist) < 6)[0]) > 2: self.channel = "eh"
		elif len(np.where(abs(pidlist) == 13)[0]) == 1 and len(np.where(abs(pidlist) < 6)[0]) > 2: self.channel = "muh"
		elif len(np.where(abs(pidlist) == 15)[0]) == 1 and len(np.where(abs(pidlist) < 6)[0]) > 2: self.channel = "tauh"
		else: self.channel = "hh"

channel = TH1D("channel","channel",10,-0.5,9.5)
names = ["ee","mumu","tautau", "emu", "etau", "mutau", "eh", "muh", "tauh", "hh"]
for label, i in zip(names, range(len(names))):
	channel.GetXaxis().SetBinLabel(i+1,label)
tPt = TH1D("tPt","top Pt",100,0,1000) 
antitPt = TH1D("antitPt","antitop Pt",100,0,1000)
lepPt = TH1D("lepPt","lepton Pt",1000,0,1000) 
nuPt = TH1D("nuPt","neutrino Pt",1000,0,1000)
qPt = TH1D("qPt","q Pt",100,0,1000)
bPt = TH1D("bPt","b Pt",100,0,1000) 
mtt = TH1D("mtt","m_{tt}",200,0,1000) 

listNfermion=[ "ne1", "nmu1", "ntau1",  "ne2", "nmu2", "ntau2", "nb", "nh1","nh2"]
nhists = []

for i in range(len(listNfermion)):
	nhists.append(TH1D(listNfermion[i],listNfermion[i],50,0,50) )
	
 #[ee,mumu.tautau, emu, etua, mutau, eh, muh, tauh, hh]

f = TFile.Open("test_output.root")
events = f.Get("events")

for ievt in events:
	print ("----------------------------")	
	mytt = ttEvent(ievt)
	if not mytt.consistency():
		print ("Fatal error")
		sys.exit(0)
		
	mytt.setParticles()
	mytt.setChannel()
	channel.Fill(np.where(np.asarray(names) == mytt.channel)[0][0])
	bPt.Fill(mytt.b.Pt())
	bPt.Fill(mytt.bbar.Pt())
	if mytt.channel in ["ee","mumu","tautau","emu","mumu","etau"]:
		lepPt.Fill(mytt.lep1.Pt())
		lepPt.Fill(mytt.lep2.Pt())
		nuPt.Fill(mytt.nu1.Pt())
		nuPt.Fill(mytt.nu2.Pt())
		mtt.Fill((mytt.tlepn+mytt.tlepp).M())
		tPt.Fill(mytt.tlepp.Pt())
		antitPt.Fill(mytt.tlepn.Pt())		
		
	elif mytt.channel in ["eh","muh","tauh"]:
		if mytt.lep1.Pt() == 0:
			lepPt.Fill(mytt.lep2.Pt())
			nuPt.Fill(mytt.nu2.Pt())
			qPt.Fill(mytt.q1.Pt())
			qPt.Fill(mytt.qbar1.Pt())
		else:
			lepPt.Fill(mytt.lep1.Pt())
			nuPt.Fill(mytt.nu1.Pt())
			qPt.Fill(mytt.q2.Pt())
			qPt.Fill(mytt.qbar2.Pt())
		if mytt.Wlepp.Pt() == 0:
			mtt.Fill((mytt.thadp+mytt.tlepn).M())
			tPt.Fill(mytt.thadp.Pt())
			antitPt.Fill(mytt.tlepn.Pt())
		else:
			mtt.Fill((mytt.thadn+mytt.tlepp).M())
			tPt.Fill(mytt.tlepp.Pt())
			antitPt.Fill(mytt.thadn.Pt())
	else:
		qPt.Fill(mytt.q2.Pt())
		qPt.Fill(mytt.qbar2.Pt())		
		qPt.Fill(mytt.q1.Pt())
		qPt.Fill(mytt.qbar1.Pt())
		mtt.Fill((mytt.thadn+mytt.thadp).M())
		tPt.Fill(mytt.thadp.Pt())
		antitPt.Fill(mytt.thadn.Pt())
	
	
	
out = TFile("validation.root","recreate")	
out.cd()
channel.Write()
tPt.Write() # TH1D("tPt","top Pt",100,0,1000) 
antitPt.Write() # TH1D("antitPt","antitop Pt",100,0,1000)
lepPt.Write() # TH1D("lepPt","lepton Pt",1000,0,1000) 
nuPt.Write() # TH1D("nuPt","neutrino Pt",1000,0,1000)
qPt.Write() # TH1D("qPt","q Pt",100,0,1000)
bPt.Write() # TH1D("bPt","b Pt",100,0,1000) 
mtt.Write() # TH1D("mtt","m_{tt}",200,0,1000) 
for i in range(len(listNfermion)):
	nhists[i].Write()
out.Close()
	
