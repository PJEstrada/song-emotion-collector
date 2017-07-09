# -*- coding: utf-8 -*-
from pyAudioAnalysis import audioFeatureExtraction
from pyAudioAnalysis import audioBasicIO
import matplotlib.pyplot as plt
from boto.s3.connection import S3Connection
from django.conf import settings
import scipy.io.wavfile as wav

def extract_features(song):
    # Init amazon S3 to get the songs.
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    # Connect to bucket
    bucket = conn.get_bucket('music-emotions')
    k = bucket.get_key(song.key)
    # Get the contents of the key into a file
    k.get_contents_to_filename("song-wavs/"+song.name)
    [Fs, x] = audioBasicIO.readAudioFile("song-wavs/"+song.name)
    x = audioBasicIO.stereo2mono(x)  # convert to MONO if required
    F = audioFeatureExtraction.stFeatureExtraction(x, Fs, round(0.050 * Fs), round(0.050 * Fs))
    F_M = a
    plt.subplot(2, 1, 1)
    plt.plot(F[0, :])
    plt.xlabel('Frame no')
    plt.ylabel('ZCR')
    plt.subplot(2, 1, 2)
    plt.plot(F[1, :])
    plt.xlabel('Frame no')
    plt.ylabel('Energy')
    plt.show()