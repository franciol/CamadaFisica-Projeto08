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

def modulaAM(sinal):
    x, porter = chama.generateSin(200000,50,duration,fs)
    mList = []
    
    for i in range(0,len(x)):
        mList.append(porter[i]*sinal[i])
    
        
    sf.write("receiveds.wav",mList,fs)
    sf.write("received.wav",mList,fs)
    return(mList)

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = sp.signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = sp.signal.filtfilt(b, a, data)
    return y


def prints(original,normalizado,filtrado,modulado):
    fig = plt.figure()
    timers = fig.canvas.new_timer(interval=20000)
    timers.add_callback(close_event)
    plt.plot(original)
    plt.title("Original")
    plt.figure() 
    plt.plot(normalizado)
    plt.title("Normalizado")
    plt.figure() 
    plt.plot(filtrado)
    plt.title("Filtrado")
    plt.figure() 
    plt.plot(modulado)
    plt.title("Modulado")
    timers.start()
    plt.show()


    plt.plot(modulado)
    plt.plot(original)
    plt.title("Modulado x Original")
    plt.legend(["Modulado","Original"])
    plt.show()

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = sp.signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = sp.signal.lfilter(b, a, data)
    return y

def close_event():
    plt.close()

def grava_e_salva():
    myrecording = sd.rec(int(duration*fs),channels=2)
    sd.wait()
    sf.write("myrecording.wav",myrecording,fs)
    plt.figure()
    plt.plot(myrecording.T[0])
    plt.show()

def importa_e_converte(nomeArquivo):
    arquivo,fs = sf.read(nomeArquivo)
    preparedSound = arquivo.T[0]
    normalizedSound = preparedSound/np.linalg.norm(preparedSound)
    print("PREPARA")
    filteredSound1 = butter_highpass_filter(normalizedSound,1000,fs)
    filteredSound = butter_lowpass_filter(filteredSound1,4000,fs)
    modulatedSound = modulaAM(filteredSound)
    print("VAI")
    sd.play(modulatedSound,fs)    
    sd.wait()
    prints(preparedSound,normalizedSound,filteredSound,modulatedSound)


#grava_e_salva()
importa_e_converte("myrecording.wav")