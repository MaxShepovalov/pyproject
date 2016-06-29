import pyaudio
import audioop

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

def fx_echo_init(delay_p, intense_p):
    global loop_frames
    global loop_times
    global time
    global setup
    global delay
    global intense
    loop_frames = []
    loop_times = []
    time = 0
    setup = True

    if  delay_p <= 0:
        print('[echo] delay should be > 0!')
        setup = False

    if  intense_p > 1:
        print('[echo] intense should be < 1!')
        setup = False

    if  intense_p < 0:
        print('[echo] intense should be > 0!')
        setup = False

    #delay_p is in seconds
    delay = int (delay_p * 43)
    intense = intense_p
    return


def fx_echo(chunk_p):
    global time
    global loop_frames
    global loop_times
    global delay
    global intense
    global setup

    if len(chunk_p) != 2 * CHUNK:
        print('[echo] chunk size is not %d but %d' % (2 * CHUNK, len(chunk_p)))
        return chunk_p

    if not setup:
        print('[echo] varibales are not set')
        return chunk_p

    #save data
    loop_times.append(time)    
    loop_frames.append(chunk_p)

    #count value
    i = 0
    while i < len(loop_frames):
        if (time - loop_times[i]) % delay == 0 and time != loop_times[i]:
            loop_frames[i] = audioop.mul(loop_frames[i], 2, intense)
            if audioop.rms(loop_frames[i], 2) < 1:
                del loop_frames[i]
                del loop_times[i]
                i = i - 1
            else:
                chunk_p = audioop.add(chunk_p, loop_frames[i], 2)
        i = i + 1
    del i

    time = time + 1
    return chunk_p