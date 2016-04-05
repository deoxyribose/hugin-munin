import numpy as np
import scipy as sp
from scipy.io import loadmat
import scipy.signal as signal
import os
from fnmatch import fnmatch
import matplotlib.pylab as plt
import cPickle as pickle

def load_one_hour(path):
    data = loadmat(path, squeeze_me=False)
    return data['eeg']

def detrend(EEG):
    window_size = 207*10
    filt = np.ones((window_size,))/float(window_size)
    trend0 = signal.fftconvolve(EEG[:,0], filt, 'same')
    trend1 = signal.fftconvolve(EEG[:,1], filt, 'same')
    trend = np.vstack([trend0,trend1]).T
    return EEG-trend

def spectrograms(EEG, nfft):
    (spec1,f,_,_) = plt.specgram(EEG[:,0], NFFT=nfft, Fs=207,noverlap=nfft/2,mode='magnitude')
    (spec2,f,_,_) = plt.specgram(EEG[:,1], NFFT=nfft, Fs=207,noverlap=nfft/2,mode='magnitude')
    fs_below_40 = f < 40
    return (np.stack((np.log10(spec1[fs_below_40,:]),np.log10(spec2[fs_below_40,:]))).astype(np.float32),f[fs_below_40])

# load .mat files
root = "/home/ben/Documents/HypoSafe/20151005_D_07/"
pattern = "*00.mat"
paths = [os.path.join(path, name) for path, subdirs, files in os.walk(root) for name in files if fnmatch(name, pattern)]
paths = [path for path in paths if path[-13:-11] == '10']
days, hours = zip(*[(int(path[-11:-9]), int(path[-8:-6])) for path in paths])

paired_sorted = sorted(zip(paths,days,hours),key = lambda x: (x[0],-x[1]))
paths,days,hours = zip(*paired_sorted)

#nhours = np.unique(hours[:36]).shape[0]
#ndays = np.unique(days[:36]).shape[0]

# generate spectrograms
c = 0
for path in paths[:155]:
    EEG = detrend(load_one_hour(path))
    (S,freq) = spectrograms(EEG,nfft=512) 
    # 198 frequency intervals, each ~.4 Hz
    # 2909 time intervals, each 74.25 sec 
    Ss = S.reshape(-1,S.shape[2])
    pickle.dump(Ss,open('pickled_specs/'+str(days[c])+'_'+str(hours[c])+'_'+'07'+'spectrogram.p','wb'))
    c += 1
# pickle it

# unpickle all spectrograms

