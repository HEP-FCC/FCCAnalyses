import numpy as np
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText

f = np.load('../ConvNet/eval_filesplitter.npz')

pid = f['arr_1']
DNN = f['arr_0']
pred_DNN = np.argmax(DNN, axis=1)

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

print('length of pid_u = '+str(np.sum(pid_u)))
print('length of pid_d = '+str(np.sum(pid_d)))
print('length of pid_s = '+str(np.sum(pid_s)))

fpr_u, tpr_u, thresholds_s = metrics.roc_curve(pid_u, DNN_u)
fpr_d, tpr_d, thresholds_d = metrics.roc_curve(pid_d, DNN_d)
fpr_s, tpr_s, thresholds_u = metrics.roc_curve(pid_s, DNN_s)
print("roc done: 1")

ftr_u = 1 - fpr_u
ftr_d = 1 - fpr_d
ftr_s = 1 - fpr_s

AUC_u = metrics.auc(ftr_u, tpr_u)
AUC_d = metrics.auc(ftr_d, tpr_d)
AUC_s = metrics.auc(ftr_s, tpr_s)

plt.plot(fpr_u, tpr_u, label='up quarks (AUC='+str(round(AUC_u, 4))+')', linestyle='-', color='b')
plt.plot(fpr_d, tpr_d, label='down quarks (AUC='+str(round(AUC_d, 4))+')', linestyle='-', color='r')
plt.plot(fpr_s, tpr_s, label='strange quarks (AUC='+str(round(AUC_s, 4))+')', linestyle='-', color='c')
#plt.plot(1-np.linspace(0, 1, 40), np.linspace(0, 1, 40), linestyle='-', color='k')
plt.xlabel(r'Background Efficiency ($\mathbf{\varepsilon_{bkg}}$)')
plt.ylabel(r'Signal Efficiency ($\mathbf{\varepsilon_{sig}}$)')
plt.title(r'$\mathbf{FCCee}$ Delphes Sim. - (LodeNet on $\mathbf{Zuds}$ Jets), $\sqrt{s}$ = 91 GeV')
plt.xticks(np.linspace(0, 1, 6))
#plt.yticks(np.linspace(0, 1, 11))
plt.grid()
plt.xlim([0,1])
#plt.ylim([0,1])
plt.yscale('log')
plt.legend(loc='lower right')
plt.savefig('../ConvNet/plots/LodeNet_filesplitter_log.png')
