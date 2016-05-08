from python_speech_features.features.base import mfcc
from python_speech_features.features.base import logfbank

import scipy.io.wavfile as wav
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

import sys
import os
from time import time
import warnings

# actually, we're not computing the cross-dot=products, just the diagonals (sampling_window_length sums)... so maybe we can try doing that 
# Should take an audio file, compute the mfcc (which is basically a feature vector), then computes the similarity matrix with square dimensions (dim(mfcc)/sampling_window_length)-squared by averaging over every cross=dot=product for a window of size sampling_window_length
# thus, there are sampling_window_length*sampling_window_length sums


sampling_window_length = 10
file_head_length = 10 # in seconds
warnings.filterwarnings("ignore", category=wav.WavFileWarning)

def compute_mfcc(audio_file):
    print("\tComputing MFCCs...")
    t0 = time()
    print audio_file
    (rate,sig) = wav.read(audio_file)
    if file_head_length != 0: # just take the first file_head_length seconds of the audio file
        sig = sig[0:rate*file_head_length,:] # delete this after testing
    mfcc_feat = mfcc(sig,rate)
    #fbank_feat = logfbank(sig,rate) # potentially look at this later?
    print("\tDone in %0.3fs." % (time() - t0))
    return mfcc_feat

def standardize_mfcc_features(mfcc_features):
    print("\tStandardizing MFCC Features...")
    t0 = time()
    feature_means = mean(mfcc_features)
    feature_stds = std(mfcc_features)
    standardized_features = (mfcc_features-feature_means)/feature_stds
    print("\tDone in %0.3fs." % (time() - t0))
    return standardized_features

'''
Inputs: audio_file_path - path to the audio file
standardize_flag - True (default) to standardize the mfccs

Outputs the generated mfcc .npz file to the output path 
'''
def generate_mfcc(input_file_path, output_file_path, standardize_flag):
    mfcc = compute_mfcc(input_file_path)
    if standardize_flag:
        mfcc = standardize_mfcc_features(mfcc)
    np.savez(output_file_path, mfcc)
    
    

def generate_all_mfccs(input_dir_path, output_dir_path,standardize_flag):
    for target_file in os.listdir(input_dir_path):
       input_file_path = os.path.join(input_dir_path,target_file)
       output_file_path = os.path.join(output_dir_path,"npz","mfcc",target_file[:-4]+".npz")
       generate_mfcc(input_file_path,output_file_path,standardize_flag)

'''
Inputs: source_path
output_path
standardize_flag - t/f for true/false

Writes .npz files to output_path/npz/mfcc/*, completely copying the directory layout
'''
if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("usage: python scripts/{} source_path output_path standardize_flag".format(os.path.basename(__file__)))
        sys.exit(1)

    source_path = sys.argv[1]
    output_path = sys.argv[2]
        
    if len(sys.argv) == 4:
        standardize_flag = (sys.argv[3] == 't')
        generate_all_mfccs(source_path,output_path,standardize_flag)
    else:
        generate_all_mfccs(source_path,output_path)


        
