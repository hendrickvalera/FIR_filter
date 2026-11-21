import numpy as np
from scipy.signal import fftconvolve
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from smstools.models import utilFunctions as UF

def printplot(h, fs):

    Nfft = 2 ** int(np.ceil(np.log2(len(h))))                               # Nfft ≥ M
    Hresp = np.fft.rfft(h, Nfft)
    freqs = np.fft.rfftfreq(Nfft, 1/fs)
    plt.plot(freqs, np.abs(Hresp))
    plt.xlim(0, 20000)

def lowpass(fc_hz, fs, M):

    cutOffValue = fc_hz * 2 / fs
    n = np.arange(-((M-1)//2),(M-1)//2+1)
    h = np.sinc(n * cutOffValue)         
    h = h * np.hamming(M)
    # normalization
    h = h / h.sum()

    return h


def highpass(fc_hz, fs, M):

    delta = np.zeros(M)
    delta[(M-1)//2] = 1

    hp = delta - lowpass(fc_hz, fs, M)
    
    return hp

def get_filter(fs, M):
    filterType = int(input("type 1 for low pass or 2 for high pass "))

    if filterType == 1:
        lpFreq = int(input("in what freq between 20Hz and 20kHz do you want to apply the low pass filter? "))
        h = lowpass(lpFreq, fs, M)
    elif filterType == 2:
        hpFreq = int(input("in what freq between 20Hz and 20kHz do you want to apply the high pass filter? "))
        h = highpass(hpFreq, fs, M)
    else:
        sys.exit("pick 1 or 2 ")

    return h


def main():
    if len(sys.argv) < 2:
        sys.exit("I need an audio file to filter")

    f_name = Path(sys.argv[1])

    if not f_name.exists():
        sys.exit(f"can't find {f_name}")

    input_file = f_name

    M = 4001

    fs, x = UF.wavread(input_file)

    h = get_filter(fs, M)
    
    y = fftconvolve(x, h, mode="same")

    UF.wavwrite(y, fs, "filtered.wav")
    printplot(h, fs)
    plt.show()

if __name__ == "__main__":
    main()