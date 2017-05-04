from numpy import fft,convolve,absolute,angle
import math
import matplotlib.pyplot as plt

BITLEN = 8

def shrink(v, bt):
    sign = 1
    if v!=0:
        sign = v/abs(v)
    val = v%pow(2,bt-1)
    step = pow(2,-bt-1)
    return round((val+(sign-1)*pow(2,bt-2))/step)*step

def garmonic(f,t,p=0):
    # f - frequency
    # t - moment of time
    # p - phase as p*pi
    return shrink(math.cos(2*math.pi*f*t+p*math.pi), BITLEN)

#    96kHz
Fs = 9600. #Hz
Ts = 1./Fs

#input
T = 0.01 #seconds
x = []
t = []
N = int(T/Ts)
print 'generate',N,'samples'
for i in range(N):
    if i in range(10,50):
        x.append(garmonic(100,i*Ts)+garmonic(1000,i*Ts)+garmonic(9000,i*Ts))
    else:
        x.append(0)
    t.append(i*Ts)
FFT_L = 512
X = fft.fft(x,n=FFT_L)

#filter
def sinc(t):
    if t==0:
        return 1.0
    else:
        return math.sin(t)/t

L = 16 #filter length
h = []
for i in range(L):
    h.append(shrink(sinc(2*math.pi*i/L), BITLEN))

H = fft.fft(h,n=FFT_L)

#apply filter
y = []
for i in convolve(x,h):
    y.append(shrink(i, BITLEN))

freq = fft.fftfreq(FFT_L)
Y = fft.fft(y, n=FFT_L)

frame = (len(X)/2)*2
Y = Y[:frame]
X = X[:frame]
H = H[:frame]
freq = freq[:frame]

plt.subplot(3,2,1)
plt.plot(x)
plt.subplot(3,2,2)
plt.plot(freq, absolute(X))
plt.subplot(3,2,3)
plt.plot(y)
plt.subplot(3,2,4)
plt.plot(freq, absolute(Y))
plt.subplot(3,2,5)
plt.plot(h)
plt.subplot(3,2,6)
plt.plot(freq, angle(H))
plt.show()