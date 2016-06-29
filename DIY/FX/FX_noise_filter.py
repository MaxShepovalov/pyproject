import pyaudio
import audioop
import math

CHUNK = 1024

#fragments
loop_frames = []
#time when fragment occured
loop_times = []
#current chunk
time = 0
#effect parameters
delay = 1
intense = 0
setup = False

def fx_noise_cancel(chunk_p, tres_p):
    if len(chunk_p) != 2 * CHUNK:
        print('[echo] chunk size is not %d but %d' % (2 * CHUNK, len(chunk_p)))
        return chunk_p

    power = audioop.rms(chunk_p, 2) / float(math.pow(2, 15))
    if power < tres_p:
        chunk_p = audioop.mul(chunk_p, 2, 0)
    return chunk_p