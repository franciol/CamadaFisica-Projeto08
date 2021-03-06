import sounddevice as sd
import signalTeste as st
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import math


chama = st.signalMeu()

timer = 1
fs = 44100
timeParser = 1000
sd.default.samplerate = fs
sd.default.channels= 2
duration = 5 #segundos

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = sp.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = sp.signal.lfilter(b, a, data)
    return y


def recebe_e_grava() :
    myrecording = sd.rec(int(duration*fs),channels=2)
    sd.wait()
    sf.write("received.wav",myrecording,fs)
    desmodula(myrecording)
   



def desmodula(myrecording):
    x, porter = chama.generateSin(200000,50,duration,fs)
  

    mList = []
    for i in range(0,len(x)):
        s = porter[i]*myrecording.T[0][i]
        mList.append(s)
    
    cutoff_hz = 20000
    filteredSound = butter_lowpass_filter(mList,cutoff_hz,fs)
    
    sd.play(filteredSound)
    sd.wait()

    plt.plot(myrecording.T[0])
    plt.title("Original")
    plt.figure()
    plt.plot(filteredSound)
    plt.title("Desmodulado")
    plt.show()

    chama.plotFFT(myrecording.T[0],fs)
    chama.plotFFT(filteredSound,fs)
    plt.show()
    #plt.plot(fourOr)


recebe_e_grava()
