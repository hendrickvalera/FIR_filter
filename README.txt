FIR Filter (Windowed-Sinc Lowpass and Highpass)

A command-line tool that loads a WAV file, applies a linear-phase FIR filter, plots the frequency response, and saves the result.

The lowpass is a sinc kernel with a Hamming window, normalized so DC gain is 1. The highpass is spectral inversion: delta - lowpass, i.e. the original minus the lows. Kernels are odd-length (M = 4001) so the center tap lines up with the delta.

How to use:

python FIR_filter.py path/to/file.wav
