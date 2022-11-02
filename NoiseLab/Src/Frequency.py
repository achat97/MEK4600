import lvm_read
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, rfft, rfftfreq
from scipy import signal



def frequencyTurbulenceTime(filename,plotFrequency=True,plotTurbulence=True,plotTimeseries=True):

    if filename == "micData_16.lvm":
        lvm = lvm_read.read(filename, read_from_pickle=False)
        time = lvm[0]['data'][:,0][-1]-2 #2 seconds of higher turbulence flow was added to the set
        time_index = list(lvm[0]['data'][:,0]).index(time)
        times = lvm[0]['data'][:,0][:time_index]
        data = lvm[0]['data'][:,1][:time_index]

    else:
        lvm = lvm_read.read(filename, read_from_pickle=False)
        time = lvm[0]['data'][:,0][-1]
        times = lvm[0]['data'][:,0]
        data = lvm[0]['data'][:,1]

    samplerate = lvm[0]['Samples'][0]
    N = len(data)

    #frequency
    yf = rfft(data)
    xf = rfftfreq(N, 1 / samplerate)



    #turbulence
    ffreq, pxxw = signal.welch(data, nfft=len(times), fs = samplerate, nperseg = 100000, return_onesided=True)

    if plotFrequency == True:
        plt.style.use('seaborn-v0_8')
        plt.plot(xf, np.abs(yf))
        plt.xlabel("Frequency[Hz]")
        plt.ylabel("Amplitude[V]")
        plt.show()

    if plotTurbulence == True:
        plt.style.use('seaborn-v0_8')
        plt.loglog(ffreq,pxxw,label=r"$E(f)$")
        plt.loglog(ffreq[int(len(ffreq)/10000):int(len(ffreq)/100)],10**(-7.8)*ffreq[int(len(ffreq)/10000):int(len(ffreq)/100)]**(-5/3),color="brown",label=r"$f^{(-5/3)}$")
        plt.xlabel("frequency[Hz]")
        plt.ylabel("PSD")
        plt.legend()
        plt.show()

    if plotTimeseries == True:
        plt.style.use('seaborn-v0_8')
        plt.plot(times,data)
        plt.xlabel("Time[s]")
        plt.ylabel("Amplitude[V]")
        plt.show()

    return data, times
