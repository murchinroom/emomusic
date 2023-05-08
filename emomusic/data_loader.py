"""
This module contains all the necessary functions to create data loaders
"""
import os
import numpy as np
import torch


def normalize_mfccs(sample_mfcc, mfcc_mean, mfcc_std):
    """
    Function to normalize MFCCs data, according to mean and variance in train set
    :param sample_mfcc: MFCC data to be normalized
    :param mfcc_mean: train set MFCC mean
    :param mfcc_std: train set MFCC stadard deviation
    :return: normalized MFCC data
    """
    return (sample_mfcc - mfcc_mean) / mfcc_std


