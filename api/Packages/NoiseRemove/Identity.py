import secrets
from flask_restful import Resource
import numpy as np
from scipy import signal
from scipy.io import wavfile
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import wave
import sys
import math
import contextlib

cutOffFrequencyMax = 1200.0
cutOffFrequencyMin = 200.0


class Identity(Resource):
    @staticmethod
    def noise_identity_and_remove(filename):
        if filename != "":
            res = split_file("uploads/" + filename, filename)
            return res

        else:
            return {'status': 'Request Failed..!',
                    'response_code': 1005,
                    'Application': 'Research 2020-159-speech_recognition_system',
                    'version': '1.0.0'}


def running_mean(x, windowSize):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize


def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved=True):
    if sample_width == 1:
        dtype = np.uint8  # unsigned char
    elif sample_width == 2:
        dtype = np.int16  # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)

    return channels


def split_file(filepath, filename):
    # sample_rate, samples = wavfile.read(filepath)
    # frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    # index = 0
    f_token = secrets.token_hex(5)
    with contextlib.closing(wave.open(filepath, 'rb')) as spf:
        sampleRate = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()

        # Extract Raw Audio from multi-channel Wav File
        _signal = spf.readframes(nFrames * nChannels)
        spf.close()
        channels = interpret_wav(_signal, nFrames, nChannels, ampWidth, True)

        # get window size
        freqRatioMax = (cutOffFrequencyMax / sampleRate)
        N_min = int(math.sqrt(0.196196 + freqRatioMax ** 2) / freqRatioMax)
        # Use moviung average (only on first channel)
        # Get minimum frequency data_set
        filteredMin = running_mean(channels[0], N_min).astype(channels.dtype)

        # Adding Additional data into array
        i = 0
        while i < N_min - 1:
            filteredMin = np.insert(filteredMin, 1, 0)
            i = i + 1

        freqRatioMin = (cutOffFrequencyMin / sampleRate)
        N_max = int(math.sqrt(0.196196 + freqRatioMin ** 2) / freqRatioMin)
        # Use moviung average (only on first channel)
        # Get maximum frequency data_set
        filteredMax = running_mean(filteredMin, N_max).astype(channels.dtype)

        j = 0
        while j < N_max - 1:
            filteredMax = np.insert(filteredMax, 1, 0)
            j = j + 1

        low_pass = filteredMin
        low_pass_max = filteredMax
        high_pass = np.subtract(channels[0], filteredMin)
        medium = np.subtract(channels[0], low_pass_max)

        low_pass_name = 'out/' + f_token + '_low_pass.wav'
        wav_file = wave.open(low_pass_name, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(low_pass.tobytes('C'))
        wav_file.close()

        high_pass_name = 'out/' + f_token + '_high_pass.wav'
        wav_file = wave.open(high_pass_name, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(high_pass.tobytes('C'))
        wav_file.close()
        out_name = f_token + '_mid.wav'
        mid_name = 'out/' + out_name
        wav_file = wave.open(mid_name, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(medium.tobytes('C'))
        wav_file.close()

    res = {'status': 'Request success..!',
           'data': {
               'file': filename,
               'out_name': out_name,
               'sample_rate': str(sampleRate),
               'channels': str(nChannels),
               'ampWidth': str(ampWidth)
           },
           'response_code': 1004,
           'Application': 'Research 2020-159-speech_recognition_system',
           'version': '1.0.0'}
    return res
