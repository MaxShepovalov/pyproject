import pyaudio
import audioop

CHUNK = 1024

def fx_distortion(chunk_p, gain_p, tres_p):
    if len(chunk_p) != 2 * CHUNK:
        print('[distortion] chunk size is not %d but %d' % (2 * CHUNK, len(chunk_p)))
        return chunk_p
    if  tres_p<= 0:
        print('[distortion] threshold should be > 0!')
        return chunk_p

    if  tres_p > 1:
        print('[distortion] threshold should be < 1!')
        return chunk_p
    
    if  gain_p < 1:
        print('[distortion] gain should be > 1!')
        return chunk_p

    #do distortion
    temp1 = audioop.mul(chunk_p, 2, 1 / tres_p)
    temp2 = audioop.mul(temp1, 2, tres_p)

    #do gain
    chunk_p = audioop.mul(temp2, 2, gain_p)
    del temp1
    del temp2
    return chunk_p