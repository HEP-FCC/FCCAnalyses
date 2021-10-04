import h5py
import numpy as np
import sparse

# This file is a bit wasteful, literally only splits data into train+test vs eval set. The train vs test split is done in the training file. I wanted the eval set to be independent of the input set (for later comparisons).

# Ideally, I would convert these files to dense matrices just to shuffle them event wise. Given the associated RAM issues, I decided instead to select the data by batches. As I have been running the analysis code in batches of size 20, I will randomly select two batches to use as the eval sets. 

fname = 'Zuds_weighted_sparse'
sparse_file = h5py.File('{0}.h5'.format(fname), 'r')

# Could draw two ints at once but that risks repetition...
first_eval_batch = np.random.randint(0,20)
second_eval_batch = np.random.randint(0,20)

while(second_eval_batch==first_eval_batch):
    second_eval_batch = np.random.randint(0,20)
   
print(first_eval_batch)
print(second_eval_batch)

pid = sparse_file['pid'][:]
pid_lens = sparse_file['shape'][::4]
p4 = sparse_file['p4'][:]
shape = sparse_file['shape'][:]
data = sparse_file['data'][:]
coords = sparse_file['coords'][:]
data_lens = sparse_file['data_len'][:]

sparse_file.close()

first_pid_index = np.array([np.sum(pid_lens[:first_eval_batch]), (np.sum(pid_lens[:first_eval_batch])+pid_lens[first_eval_batch])])
second_pid_index = np.array([np.sum(pid_lens[:second_eval_batch]), (np.sum(pid_lens[:second_eval_batch])+pid_lens[second_eval_batch])])


eval_pid_mask = np.arange(len(pid))
eval_pid_mask = ((eval_pid_mask>=first_pid_index[0])&(eval_pid_mask<first_pid_index[1]))|((eval_pid_mask>=second_pid_index[0])&(eval_pid_mask<second_pid_index[1]))


first_data_index = np.array([np.sum(data_lens[:first_eval_batch]), (np.sum(data_lens[:first_eval_batch])+data_lens[first_eval_batch])])
second_data_index = np.array([np.sum(data_lens[:second_eval_batch]), (np.sum(data_lens[:second_eval_batch])+data_lens[second_eval_batch])])

eval_data_mask = np.arange(len(data))
eval_data_mask = ((eval_data_mask>=first_data_index[0])&(eval_data_mask<first_data_index[1]))|((eval_data_mask>=second_data_index[0])&(eval_data_mask<second_data_index[1]))



eval_lens_mask = np.arange(len(data_lens))
eval_lens_mask = (eval_lens_mask==first_eval_batch)|(eval_lens_mask==second_eval_batch)

eval_shape_mask = np.repeat(np.arange(len(data_lens)), 4)
eval_shape_mask = (eval_shape_mask==first_eval_batch)|(eval_shape_mask==second_eval_batch)



pid_eval = pid[eval_pid_mask]
pid_train = pid[~eval_pid_mask]

p4_eval = p4[eval_pid_mask]
p4_train = p4[~eval_pid_mask]

data_eval = data[eval_data_mask]
data_train = data[~eval_data_mask]

coords_eval = coords[eval_data_mask]
coords_train = coords[~eval_data_mask]

data_lens_eval = data_lens[eval_lens_mask]
data_lens_train = data_lens[~eval_lens_mask]

shape_eval = shape[eval_shape_mask]
shape_train = shape[~eval_shape_mask]

f_eval = h5py.File('{0}_eval.h5'.format(fname), 'w')
f_train = h5py.File('{0}_train.h5'.format(fname), 'w')

f_eval['pid'] = pid_eval
f_eval['p4'] = p4_eval
f_eval['shape'] = shape_eval
f_eval['data'] = data_eval
f_eval['coords'] = coords_eval
f_eval['data_len'] = data_lens_eval

f_train['pid'] = pid_train
f_train['p4'] = p4_train
f_train['shape'] = shape_train
f_train['data'] = data_train
f_train['coords'] = coords_train
f_train['data_len'] = data_lens_train

f_eval.close()
f_train.close()















