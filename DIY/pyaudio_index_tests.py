#sound libraries
import pyaudio
import audioop
import math

#global variables
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 60
D_INDEX = 0
FILENAME = 'volume.csv'

def printDB(piece):
    db = 10.0 * audioop.rms(piece, 2) / math.pow(2,15)
    str_mark1 = '.'
    str_mark2 = '#'
    str_start = '['
    str_end = ']%f' % db
    if db > 8:
        str_end = ']LIMIT %f' % db
    output = str_start
    for i in range(0,int(db)):
        if i > 6:
            output = output + str_mark2
        else:
            output = output + str_mark1
    output = output + str_end
    print(output)
    return db


p = pyaudio.PyAudio()

volume = []

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = D_INDEX,
                frames_per_buffer=CHUNK)

print('using device #%d' % D_INDEX)
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    data = audioop.mul(data, 2, 10)
    volume.append(printDB(data))

stream.stop_stream()
stream.close()
p.terminate()

print('writing %d volume samples to file' % len(volume))
target = open(FILENAME, 'w')
target.truncate()
for i in volume:
    target.write('%f' % i)
    target.write(';')
target.close()