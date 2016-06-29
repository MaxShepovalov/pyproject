import pyaudio
import audioop
import numpy as np

CHUNK = 1024
RATE = 44100
setup = False

#parameters borders
BASS_MID = 250  #Hz
MID_TREB = 4000 #Hz

p_bss = 1
p_mid = 1
p_tre = 1

def fx_filter_init(bass, middle, treble):
    global setup
    global p_bss
    global p_mid
    global p_tre

    setup = True

    if bass < 0:
        print('[filter] bass should be > 0')
        setup = False

    if middle < 0:
        print('[filter] bass should be > 0')
        setup = False

    if treble < 0:
        print('[filter] bass should be > 0')
        setup = False

    if setup:
        p_bss = bass
        p_mid = middle
        p_tre = treble

    return


def fx_filter(chunk_p):
    if len(chunk_p) != 2 * CHUNK:
        print('[filter] chunk size is not %d but %d' % (2 * CHUNK, len(chunk_p)))
        return chunk_p

    if not setup:
        print('[filter] varibales are not set')
        return chunk_p

    spectr = np.fft.rfft(np.fromstring(data, dtype = np.int16))
    freq = np.fft.rfftfreq(spectr.shape[-1], 1.0/RATE)
    for i in range(0,freq.shape[-1]):
        #bass
        if freq[i] < BASS_MID:
            spectr = spectr[i] * p_bss
        #middle
        elif freq[i] < MID_TREB:
            spectr[i] = spectr[i] * p_mid
        #treble
        else:
            spectr[i] = spectr[i] * p_tre

    chunk_p = np.fft.irfft(spectr)
    chunk_p = np.array_str(chunk_p)
    return chunk_p

