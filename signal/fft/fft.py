from numpy import fft
from math import pi, cos
import matplotlib.pyplot as plt

dfreq = 500
Srate = 15000
Sfreq = 1./Srate

N = 20000/dfreq

for j in range(0,N):
	cfreq = dfreq*j
	print 'Freq=',cfreq,' start'
	inp = []
	for i in range(500):
		inp.append(cos(2*pi*100*i*Sfreq)+cos(2*pi*cfreq*i*Sfreq))
	
	Hraw = fft.fft(inp)
	H = fft.fftshift(Hraw)
	Wraw = []
	for w in range(len(H)):
		Wraw.append(float(w)/len(H) - 0.5)
	W = fft.fftshift(Wraw)
	print 'Freq=',cfreq,' saving'

	y = fft.ifft(H)
	
	plt.subplot(311)
	plt.plot(inp)
	plt.subplot(312)
	plt.plot(W, Hraw)
	plt.subplot(313)
	plt.plot(y)
	plt.savefig('fftplot_'+str(cfreq)+'.png')
	plt.close()

