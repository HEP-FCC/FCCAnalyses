#Remove import statements for final version as this will only be used as a function...
import numpy as np
import sparse 
import h5py

def fullprint(*args, **kwargs):
  from pprint import pprint
  import numpy
  opt = numpy.get_printoptions()
  numpy.set_printoptions(threshold=numpy.inf)
  pprint(*args, **kwargs)
  numpy.set_printoptions(**opt)


def sparse2dense(f):
    #Here we load the file
    sparse_file = h5py.File(f, 'r')
    #Here we select every fourth element of the shape array, i.e. the number of non zero entries per batch, which usally follows the structure (dim1ofa1, dim2ofa1, ..., dimNofa1, dim1ofa2, ...)
    #file_lens = sparse_file['shape'][0::4]
    file_lens = sparse_file['data_len'][:]
    #Shorted number of batches to 3 for testing
    file_lens = file_lens[:]
    #print(len(sparse_file['data'][:file_lens[0]]))
    print('$$$$$$$$$$$$$$$$')
    print(sparse_file['shape'][:])
    print(sparse_file['coords'][:])
    print(sparse_file['data'][:10])
    print(len(sparse_file['shape'][:]))
    print(len(sparse_file['coords'][:]))
    print(len(sparse_file['data'][:]))
    print (file_lens) 
    index_old = 0
    index = file_lens[0]
    dense = sparse.COO(coords = (sparse_file['coords'][index_old:index]).T, data = sparse_file['data'][index_old:index], shape = tuple(sparse_file['shape'][:4])).todense()                  #, fill_value = sparse_file['fill_value'][0])
    '''
    print('USED INDICES')
    print(0)
    print(file_lens[0])
    print(file_lens[0]+file_lens[1])
    print(file_lens[0]+file_lens[1])
    for i in range(8000):
        print(i)
        print(sparse_file['coords'][:,0])
    '''
    for i in range(1, len(file_lens)):
        index_old = index
        index = index + file_lens[i]
        k=i-1
        '''
        print('CORDS')
        coords = (sparse_file['coords'][index_old:index])
        shape = tuple(sparse_file['shape'][(4*(k+1)):(4*(k+2))])
        print(max(coords[:-1,0]))
        print('SHAPE')
        print(shape)
        '''
        #print(sparse.COO(coords = (sparse_file['coords'][file_lens[i-1]:(file_lens[i-1]+file_lens[i])]).T, data = sparse_file['data'][file_lens[i-1]:(file_lens[i-1]+file_lens[i])], shape = tuple(sparse_file['shape'][(4*(k+1)):(4*(k+2))])).todense()[:,6,:])
        dense = np.append(dense, sparse.COO(coords = (sparse_file['coords'][index_old:index]).T, data = sparse_file['data'][index_old:index], shape = tuple(sparse_file['shape'][(4*(k+1)):(4*(k+2))])).todense(), axis=0)                  #, fill_value = sparse_file['fill_value'][0])
        #dense = np.append(dense, sparse.COO(coords = (sparse_file['coords'][file_lens[i-1]:(file_lens[i-1]+file_lens[i])]).T, data = sparse_file['data'][file_lens[i-1]:(file_lens[i-1]+file_lens[i])], shape = tuple(sparse_file['shape'][(4*(k+1)):(4*(k+2))])).todense(), axis=0)    #, fill_value = sparse_file['fill_value'][0])


    #for i in range(0, 200):
    #    print(i)
    #    print(np.sum(dense[i,6,:,:]))
    
    print(dense.shape)
    sparse_file.close()
    return dense

dense = sparse2dense('h5_output/Zuds_weighted_sparse_short.h5')[:]#[:,6,:]
dense_pure = h5py.File('h5_output/Zuds_weighted_short.h5', 'r')
dense_pure_histos = dense_pure['histos'][:]#[:,6,:]

print('................')
print(dense.shape)
print(dense_pure_histos.shape)
print('................')
'''
for i in range(20, 200):
    print(i)
    print(np.array_equal(dense[i].astype(np.float16), dense_pure_histos[i].astype(np.float16)))
    print('/')
first false at 25...
''' 

#print(len(sparse.COO(dense[:,6,:,:]).data))
print('->')
print(sparse.COO(dense_pure_histos).data[:10])
#for i in range(1):
#    if(np.sum(dense_pure_histos[11,0,:,:])>0):
#        print(i)
#        print(np.sum(dense_pure_histos[11,0,:,:]))
#        print('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVv')
#fullprint(dense_pure_histos[0,3,:,:])
'''
for i in range(5000, 6300):
    print(i)
    print(np.array_equal(dense[i].astype(np.float16), dense_pure_histos[i].astype(np.float16)))
    print(np.sum(dense[i,6,:,:]))
    print(np.sum(dense_pure_histos[i,6,:,:]))

print('xxxxxxxxxxxxxxx')
#print(dense_pure_histos[25])
'''

dense_pure.close()


'''
1. Fix tuple thing @
2. Generalize to loop and and append @
2.5 Compare to h5 files directly for a shorter set. Are they equivalent? if yes, what is going on with fill_value? @
3. Add to training code as a "preprocessing" step
4. Make ROC curves
'''



