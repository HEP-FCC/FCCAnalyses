import numpy as np
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

f = np.load('eval_filesplitter.npz')

pid = f['arr_1']
DNN = f['arr_0']
pred_DNN = np.argmax(DNN, axis=1)
#QGL = f['arr_2']
#data = f['arr_3']
#glob = f['arr_4']
#DeepFlavQG = f['arr_5']
'''
data = f['arr_3'][:]
print(data.shape)
print(data[:10])
E = data[:,:,3]
E_mask = (E>0)
n = [np.sum(x) for x in E_mask]
pt = np.exp(glob[:,0])

mask = (pt>=20) & (n>=3)

pid = pid[mask]
DNN = DNN[mask]
pred_DNN = pred_DNN[mask]
QGL = QGL[mask]
DeepFlavQG = DeepFlavQG[mask]
'''

#pt = np.exp(glob[:,0])
#eta = np.abs(glob[:,1])

cmatrix = metrics.confusion_matrix(pid, pred_DNN, normalize='true') #already the same structure as Vini matrix
cmatrix_col = metrics.confusion_matrix(pid, pred_DNN, normalize='pred')

cmatrix = cmatrix.round(2)
cmatrix_col = cmatrix_col.round(2)

np.savetxt('cmatrix.txt', cmatrix)

print(pid[:20])

DNN_d = DNN[:,0]
pid_d = (np.abs(pid)==0)
DNN_u = DNN[:,1]
pid_u = (np.abs(pid)==1)
DNN_s = DNN[:,2]
pid_s = (np.abs(pid)==2)
#DNN_g = DNN[:,3]
#pid_g = (np.abs(pid)==3)
#pid_q = (np.abs(pid)==0)|(np.abs(pid)==1)|(np.abs(pid)==2)

print('length of pid_u = '+str(np.sum(pid_u)))
print('length of pid_d = '+str(np.sum(pid_d)))
print('length of pid_s = '+str(np.sum(pid_s)))
#print('length of pid_g = '+str(np.sum(pid_g)))
'''
nan_mask = (~(np.isnan(QGL)))&(QGL!=-1)
#phase_mask = (pt>80)&(eta<2.5)
#phase_mask = (pt<=80)&(eta>=2.5)
phase_mask = (pt>=0)
tot_mask = (nan_mask)&(phase_mask)


DNN_u = DNN_u[tot_mask]
DNN_d = DNN_d[tot_mask]
DNN_s = DNN_s[tot_mask]
DNN_g = DNN_g[tot_mask]
pid_u = pid_u[tot_mask]
pid_d = pid_d[tot_mask]
pid_s = pid_s[tot_mask]
pid_g = pid_g[tot_mask]
QGL = QGL[tot_mask]
DeepFlavQG = DeepFlavQG[tot_mask]
pid_q = pid_q[tot_mask]

print("tot selects: "+str(np.sum(tot_mask)/len(tot_mask)))
'''

fpr_u, tpr_u, thresholds = metrics.roc_curve(pid_u, DNN_u)
fpr_d, tpr_d, thresholds = metrics.roc_curve(pid_d, DNN_d)
fpr_s, tpr_s, thresholds = metrics.roc_curve(pid_s, DNN_s)
#fpr_g, tpr_g, thresholds = metrics.roc_curve(pid_g, DNN_g)
#fpr_qgl, tpr_qgl, thresholds_qgl = metrics.roc_curve(pid_q, QGL)
#fpr_DFQG, tpr_DFQG, thresholds_DFQG = metrics.roc_curve(pid_g, DeepFlavQG)
print("roc done: 1")

                       

ftr_u = 1 - fpr_u
ftr_d = 1 - fpr_d
ftr_s = 1 - fpr_s
#ftr_g = 1 - fpr_g
#ftr_qgl = 1-fpr_qgl
#ftr_DFQG = 1-fpr_DFQG

AUC_u = metrics.auc(ftr_u, tpr_u)
AUC_d = metrics.auc(ftr_d, tpr_d)
AUC_s = metrics.auc(ftr_s, tpr_s)
#AUC_g = metrics.auc(ftr_g, tpr_g)
#AUC_q = metrics.auc(ftr_qgl, tpr_qgl)
#AUC_DFQG = metrics.auc(ftr_DFQG, tpr_DFQG)

##plt.plot([], [], ' ', label=r'$20 \leq p_{T} \leq 80$ GeV, $|\eta| \geq 2.5$')
##plt.plot([], [], ' ', label=r'$p_{T} > 80$ GeV, $|\eta| < 2.5$')
##plt.plot([], [], ' ', label=r'$p_{T} \geq 20$ GeV')
plt.plot(ftr_u, tpr_u, label='up quarks (AUC='+str(round(AUC_u, 4))+')', linestyle='-', color='b')
plt.plot(ftr_d, tpr_d, label='down quarks (AUC='+str(round(AUC_d, 4))+')', linestyle='-', color='r')
plt.plot(ftr_s, tpr_s, label='strange quarks (AUC='+str(round(AUC_s, 4))+')', linestyle='-', color='c')
##plt.plot(ftr_g, tpr_g, label='gluons (AUC='+str(round(AUC_g, 4))+')', linestyle='-', color='g')
##plt.plot(ftr_g, tpr_g, label='ABCNet gluon (Small) (AUC='+str(round(AUC_g, 4))+')', linestyle='-', color='g')
##plt.plot(ftr_qgl, tpr_qgl, label='QGL (AUC='+str(round(AUC_q, 4))+')', linestyle='-.', color='r')
##plt.plot(ftr_DFQG, tpr_DFQG, label='DeepFlavQG (AUC='+str(round(AUC_DFQG, 4))+')', linestyle='-.', color='b')
plt.plot(1-np.linspace(0, 1, 40), np.linspace(0, 1, 40), linestyle='-', color='k')
plt.xlabel(r'Background Rejection ($\mathbf{1- \varepsilon_{bkg}}$)')
plt.ylabel(r'Signal Efficiency ($\mathbf{\varepsilon_{sig}}$)')
plt.title(r'$\mathbf{FCCee}$ Delphes Sim. - (LodeNet on $\mathbf{Zuds}$ Jets), $\sqrt{s}$ = 91 GeV')
plt.xticks(np.linspace(0, 1, 11))
plt.yticks(np.linspace(0, 1, 11))
plt.grid()
#plt.annotate('Something', xy=(0.05, 0.95), xycoords='axes fraction')
plt.xlim([0,1])
plt.ylim([0,1])
##plt.title(r'ROC for different Jet Flavours, $\sqrt{s}$ = 13 TeV')
#plt.title(r'ROC for Jets, 300 GeV $< p_{T} \leq$ 600 GeV, $\sqrt{s}$ = 13 TeV')
plt.legend(loc="lower left")
#plt.savefig('thesis_standard/ROCJetFlavours_Zjets_2306_cut_mixed_noL_1705_comp.png')
#plt.savefig('thesis_standard/ref_QCD.png')
plt.savefig('plots/LodeNet_filesplitter.png')
























