#sound libraries
import pyaudio
import audioop
import wave
import math
from FX.FX_distortion import fx_distortion
from FX.FX_echo import fx_echo
from FX.FX_echo import fx_echo_init
from FX.FX_noise_filter import fx_noise_cancel

def printDB(piece):
    db = int(100 * audioop.rms(piece, 2) / math.pow(2,15))
    str_mark1 = '*'
    str_mark2 = '#'
    str_start = '['
    str_end = ']%f' % db
    if db > 80:
        str_end = ']LIMIT %f' % db
    output = str_start
    for i in range(0,db):
        if i > 60:
            output = output + str_mark2
        else:
            output = output + str_mark1
    output = output + str_end
    print(output)
    return
    

#DISTORTION PARAMS
#Threshold (0 - 1)
#post gain (1 - inf)
tres = 0.05
gain = 2

#ECHO PARAMS
#delay > 0 [seconds]
#intense 0< i < 1
delay = 0.5
intense = 0.3
fx_echo_init(delay, intense)

#NOISE CANCEL PARAMS
#Threshold (0 - 1)
noise_tres = 0.1

#global variables
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = 'output.wav'

p = pyaudio.PyAudio()

#streams
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

ostream = p.open(format = FORMAT,
                 channels = CHANNELS,
                 rate = RATE,
                 output = True,
                 frames_per_buffer = CHUNK)

print("* recording")

#frames = []
file_frames = []
processed_file_frames = []

#learn noise
print('noise auto read')
powers = []
for i in range(0,20):
    data = stream.read(CHUNK)
    powers.append(audioop.rms(data, 2) / float(math.pow(2, 15)))

noise_tres = max(powers) / 10.0

print('noise set: %f. RECORDING %d seconds' % (noise_tres, RECORD_SECONDS))
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #pregain
    data = fx_noise_cancel(data, noise_tres)
    data = audioop.mul(data, 2, 3)

    #record
    printDB(data)
    file_frames.append(data)

    #distortion
    data = fx_distortion(data, gain, tres)

    #echo
    #data = fx_echo(data)

    #record output
    processed_file_frames.append(data)

print("\n* done recording")

stream.stop_stream()
stream.close()

#frite out original sound
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(file_frames))
wf.close()

#play gained sound
print('\n* playing')
for i in processed_file_frames:
    #output gain
    gained = audioop.mul(i, 2, 5)
    ostream.write(gained)
    printDB(gained)
print('\n* done playing')

ostream.stop_stream()
ostream.close()
p.terminate()

#frite out modified sound
wf = wave.open('mod_'+WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(processed_file_frames))
wf.close()