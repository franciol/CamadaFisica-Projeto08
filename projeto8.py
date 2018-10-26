import sounddevice as sd
import signalTeste as st
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp


chama = st.signalMeu()

timer = 1
fs = 44100
timeParser = 1000
sd.default.samplerate = fs
sd.default.channels= 2
duration = 5 #segundos

def grava_e_salva():
    myrecording = sd.rec(int(duration*fs),channels=2)
    sd.wait()
    sf.write("myrecording.wav",myrecording,fs)
    chama.plotFFT(myrecording.T[0],fs)
    plt.show()
    print("Teste")
    sd.play(myrecording,fs)
    sd.wait()
    print("Done")    
    plt.plot(myrecording.T[0])
    plt.show()
    print(myrecording.T[0]/np.argmax(myrecording.T[0]))
    
def importa_e_converte(nomeArquivo):
    arquivo, fs = sf.read(nomeArquivo)
    preparedSound = arquivo.T
    plt.plot(preparedSound[1])
    plt.show()
    nyq_rate = fs/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = sp.signal.kaiserord(ripple_db, width)
    cutoff_hz = 4000.0
    taps = sp.signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    plt.plot(taps)
    plt.show()  
    yFiltrado = sp.signal.lfilter(taps, 1.0, arquivo)
    plt.plot(yFiltrado)

