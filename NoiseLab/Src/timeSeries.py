import lvm_read
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, rfft, rfftfreq, irfft
from scipy import signal
import noisereduce as nr
from Frequency import *



def frequencyTurbulenceTime_denoised(filename,plotFrequency=True,plotTurbulence=True,plotTimeseries=True):
    lvmBackground = lvm_read.read("micData_14.lvm", read_from_pickle=False)
    timeBackground = lvmBackground[0]['data'][:,0][-1]
    dataBackground = lvmBackground[0]['data'][:,1]

    if filename == "micData_16.lvm":

        lvm = lvm_read.read("micData_16.lvm", read_from_pickle=False)
        time = lvm[0]['data'][:,0][-1]-2 #2 seconds of higher turbulence flow was added to the set
        time_index = list(lvm[0]['data'][:,0]).index(time)
        times = lvm[0]['data'][:,0][:time_index]
        samplerate = lvm[0]['Samples'][0]
        dataNoised = lvm[0]['data'][:,1][:time_index]

        if time > timeBackground:
            data = data = dataNoised[:len(dataBackground)]-dataBackground
            times = times[:len(dataBackground)]


        else:
            data = dataNoised-dataBackground[:len(dataNoised)]


    else:

        lvm = lvm_read.read(filename, read_from_pickle=False)
        time = lvm[0]['data'][:,0][-1]
        times = lvm[0]['data'][:,0]
        dataNoised = lvm[0]['data'][:,1]
        samplerate = lvm[0]['Samples'][0]

        if time > timeBackground:
            data = dataNoised[:len(dataBackground)]-dataBackground
            times = times[:len(dataBackground)]

        else:
            data = data = dataNoised-dataBackground[:len(dataNoised)]


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
        plt.loglog(ffreq[int(len(ffreq)/9000):int(len(ffreq)/200)],10**(-7.5)*ffreq[int(len(ffreq)/9000):int(len(ffreq)/200)]**(-5/3),color="brown",label=r"$f^{(-5/3)}$")
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

    return data,times

def plotTimeseries(filename):

    dataNoised,timesNoised = frequencyTurbulenceTime(filename,plotFrequency=False,plotTurbulence=False,plotTimeseries=False)
    dataDenoised,timesDenoised = frequencyTurbulenceTime_denoised(filename,plotFrequency=False,plotTurbulence=False,plotTimeseries=False)

    plt.style.use('seaborn-v0_8')
    plt.subplot(211)
    plt.title("Noised")
    plt.plot(timesNoised,dataNoised)
    plt.ylabel("Amplitude[V]")

    plt.subplot(212)
    plt.plot(timesDenoised,dataDenoised)
    plt.title("Denoised")
    plt.xlabel("Time[s]")
    plt.ylabel("Amplitude[V]")
    plt.show()


frequencyTurbulenceTime_denoised("micData_18.lvm",plotFrequency=True,plotTurbulence=False,plotTimeseries=False)
