"""
This module contains all the necessary methods for data pre-processing.
"""
import os
import random
import numpy as np

import librosa
from sklearn.utils import shuffle


def get_audio_mfccs(wave, sample_rate):
    """
    Function to crop an audio waveform and extract MFCCs features.
    For more information please refer to https://gloria-m.github.io/unimodal.html#s0

    :param wave: waveform of an audio
    :param sample_rate: the rate the audio was sampled at
    :return: MFCCs features of size 20x1200
    """

    # The initial duration of the waveform is 45sec.
    # The features are extracted from an excerpt of 36sec duration.
    full_length = 45 * sample_rate
    crop_length = 36 * sample_rate

    # The windows length is 30ms
    sr_ms = sample_rate / 1000
    win_length = int(30 * sr_ms)

    diff_length = full_length - crop_length

    # Select a random point in the wave duration to represent the cropped sample start time
    # Crop 36sec starting from the selected point
    crop_start = np.random.randint(diff_length, size=1)[0]
    crop_end = crop_start + crop_length
    sample = wave[crop_start:crop_end]

    # Extract MFCCs features from non-overlapping windows of 30ms length
    sample_mfcc = librosa.feature.mfcc(sample, sr=sample_rate, n_mfcc=20,
                                       n_fft=win_length, hop_length=win_length)

    return sample_mfcc


class DataPreprocessor:
    """
    Methods for dataset preprocessing are defined in this class.
    """
    def __init__(self, args):

        self._data_dir = args.data_dir
        self._deam_dir = args.deam_dir
        self._audio_dir = args.data_pt
        #self._audio_dir = os.path.join(self._deam_dir, 'Audio')
        self._annotations_path = os.path.join(self._deam_dir, 'static_annotations.csv')

        self._waves_dir = os.path.join(self._deam_dir, 'Waveforms')

        self._audio_extension = args.audio_extension
        self._sample_rate = args.sample_rate

        self.audio_names = []
        self.annotations = []
        self.quadrants = []

        self.train_audio_names = []
        self.train_annotations = []
        self.test_audio_names = []
        self.test_annotations = []

        self.train_mfccs = []
        self.test_mfccs = []


    def get_test_data_info(self):
        folder_list = self._audio_dir
        #folder_path = data_pt
        #file_list = [os.path.splitext(f)[0] for f in sorted(os.listdir(folder_path)) if f.endswith('.mp3')]
        #self.audio_names = file_list
        self.audio_names = folder_list
        #print(file_list)

    def get_waveforms(self):
        """
        Method to get and save waveforms from audio resampled at 44,100Hz/sec and extended or shortened
        to 45sec duration.
        """
        #print("hello")
        sr_ms = self._sample_rate / 1000
        for idx, audio_name in enumerate(self.audio_names):
            #print(audio_name)#修改
            # Load and resample the audio sample
            audio_path = audio_name
            #audio_path = os.path.join(self._audio_dir, '{:s}.{:s}'.format(audio_name, self._audio_extension))
            wave, _ = librosa.load(audio_path, sr = self._sample_rate)

            # Get the duration in miliseconds
            duration = len(wave) / sr_ms
            # If the duration is smaller than 45000ms, extend the sample by appending the last portion of the
            # waveform to the end.
            if duration < 45000:
                diff = int((duration - 45000) * sr_ms)
                wave = np.concatenate([wave, wave[diff:]])

            # If the duration is llarger than 45000ms, keep only the first 45000ms and drop the
            # last portion of the waveform
            else:
                wave = wave[:45*self._sample_rate]
            # Save the waveform as numpy array with the audio sample name
            #修改
            mfcc = get_audio_mfccs(wave, self._sample_rate)
            self.test_mfccs.append(mfcc)
        return self.test_mfccs    

            #wave_path = os.path.join(self._waves_dir, '{:s}.npy'.format(audio_name))
            #np.save(wave_path, wave)

