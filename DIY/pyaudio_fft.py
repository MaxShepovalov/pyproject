#sound libraries
import pyaudio
import audioop
import math
import matplotlib.pyplot as plt
import numpy as np

#change plot to interactive mode
plt.ion()

#global variables
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
D_INDEX = 0

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

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = D_INDEX,
                frames_per_buffer=CHUNK)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_ylim(-math.pow(2,17),math.pow(2,17))
fig.canvas.draw()
plt.show(block=False)

data = stream.read(CHUNK)
data = np.fromstring(data, dtype = np.int16)
data = np.fft.rfft(data)
t = np.arange(len(data))
freq = np.fft.rfftfreq(t.shape[-1], 1.0/RATE)
#ax.set_xlim(0,)
line1, = ax.plot(freq, data.real)

frames = []

#read fft
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    stream.start_stream()
    data = stream.read(CHUNK)
    stream.stop_stream()
    data = audioop.mul(data, 2, 5)

    data = np.fft.rfft(np.fromstring(data, dtype = np.int16))
    line1.set_ydata(data.real)
    fig.canvas.draw()

#apply filter


stream.stop_stream()
stream.close()
p.terminate()

