# Voice Command Recognition Without AI Models

[**Cleuton Sampaio**](https://linkedin.com/in/cleutonsampaio).

See the [**repository**](https://github.com/cleuton/pythondrops/tree/master/audio_fft).

Understanding the problem and the algorithm (Clean Code’s G-21) is essential to create an effective solution. Many people run after AI, either to use pre-trained models or to generate source code, without understanding what is actually required. You need to analyze the problem and look for appropriate techniques, tools, and algorithms.

Imagine the following problem:

> We have an **edge computing SoC** that needs to recognize voice commands and take actions. These commands are short words within a sentence. If they are present, it must trigger some device.

Simple problem, right? We could use a **speech recognition AI** model and everything would be solved. But there’s a catch:

> The system must work **offline**.

And now?

Here are some interesting techniques:

1. **Time-domain cross-correlation**
   It directly calculates similarity between the reference segment and all displacements of the input signal, summing pointwise products. It is simple but costs O(N·M) time (where N and M are signal lengths).

2. **FFT-based cross-correlation**
   Uses FFT/IFFT to convert signals to the frequency domain, multiply spectra (with conjugate) and return to time, reducing cost to O((N+M)·log(N+M)).

3. **Template matching with DTW (Dynamic Time Warping)**
   Extracts features (e.g., MFCC) from both signals and applies DTW to align sequences of different lengths, tolerating timing variations in pronunciation.

4. **Hidden Markov Models (HMM)**
   Trains an HMM for the word pattern using acoustic features (typically MFCC), then uses the Viterbi algorithm to verify its likelihood in the input audio.

5. **MFCC + GMM (Gaussian Mixture Models)**
   Represents the distribution of cepstral coefficients with Gaussian mixtures and evaluates the probability of each frame belonging to the word model, detecting windows of high probability.

6. **Neural networks (CNN/RNN/LSTM)**
   Feed spectrograms or MFCC sequences into deep networks trained for keyword spotting, obtaining classifiers capable of handling noise and voice variation.

7. **Wavelet transform**
   Decomposes the signal into multiple time–frequency scales, allowing detection of local patterns more robust to non-stationary noise.

In our case, we will combine band-pass filtering (to isolate the speech band and reduce noise), FFT-based cross-correlation (for computational efficiency), and local energy normalization (Normalized Correlation Coefficient), followed by thresholding. This approach is simple to implement, runs fast even on long audio, and is resistant to volume variation and out-of-band noise.

Oh, and very important: We will use **Python** and common libraries such as **numpy** and **scipy**, which exist on multiple architectures and platforms.

## What is FFT?

First, we must understand what the **Fourier transform** is. It is a mathematical tool that converts a signal from the time (or space) domain into the frequency domain. Instead of looking at how a waveform changes over time, it tells us which frequencies (and with what intensity) make up that waveform. In the continuous form, the Fourier transform of a function (x(t)) is defined as

![](im2.png)

and returns a function (X(f)) that indicates “how much” of each frequency (f) exists in (x(t)).

FFT (Fast Fourier Transform) is not a different transform: it is a family of algorithms that numerically and much more efficiently compute the Discrete Fourier Transform (DFT). The DFT is the Fourier transform applied to sampled signals of finite size (N), defined as

![](im3.png)

Computing that sum directly costs (O(N^2)) operations. The FFT reorganizes operations using “divide-and-conquer,” reducing the cost to (O(N\log N)), making it feasible to process long signals in real time.

In short, FFT is simply the efficient implementation (in computational time) of the Discrete Fourier Transform, allowing extraction of a sampled signal’s frequency content without the high cost of the naïve DFT.

## Implementation

I created a **Python** script to test the concept, with the following dependency list (requirements.txt):

```text
numpy
scipy
```

Here is the script:

```python
#!/usr/bin/env python3
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

def filtro_passa_banda(sinal, sr, lowcut=300, highcut=3400, ordem=4):
    """
    Applies a Butterworth band-pass filter to the vector 'sinal'.
    - lowcut/highcut define the frequency band of interest (Hz).
    - ordem controls the filter slope.
    """
    nyq = 0.5 * sr
    wn = [lowcut/nyq, highcut/nyq]
    sos = butter(ordem, wn, btype='band', output='sos')
    return sosfilt(sos, sinal)

def correlacao_fft(sinal, ref):
    """
    Computes the valid cross-correlation of 'sinal' with 'ref' via FFT.
    Returns only the portion where the reference fits inside the signal.
    """
    n_corr = len(sinal) + len(ref) - 1
    N = 1 << (n_corr - 1).bit_length()
    S = np.fft.fft(sinal, n=N)
    R = np.fft.fft(ref,   n=N)
    corr = np.fft.ifft(S * np.conj(R)).real
    return corr[len(ref)-1 : len(sinal)]

def detecta_palavra(entrada_wav, ref_wav, limiar=0.6):
    """
    Returns True if the segment in 'ref_wav' is detected in 'entrada_wav'.
      1) Load both WAVs (mono or stereo → convert to mono)
      2) Apply band-pass filtering to reduce out-of-speech noise
      3) Remove DC offset (mean)
      4) Compute FFT-based correlation
      5) Normalize locally by energy
      6) Check if the largest coefficient ≥ threshold
    """
    # 1) reading
    sr_e, entrada = wavfile.read(entrada_wav)
    sr_r, ref    = wavfile.read(ref_wav)
    if sr_e != sr_r:
        raise ValueError("Different sampling rates")

    # stereo → average channels; float
    if entrada.ndim == 2: entrada = entrada.mean(axis=1)
    if ref.ndim     == 2: ref     = ref.mean(axis=1)
    entrada = entrada.astype(float)
    ref     = ref.astype(float)

    # 2) filtering
    entrada_f = filtro_passa_banda(entrada, sr_e)
    ref_f     = filtro_passa_banda(ref,     sr_e)

    # 3) remove DC offset
    entrada_f -= np.mean(entrada_f)
    ref_f     -= np.mean(ref_f)

    # 4) correlation via FFT
    corr = correlacao_fft(entrada_f, ref_f)

    # 5) local normalization
    energia_local = np.sqrt(
        np.convolve(entrada_f**2, np.ones(len(ref_f)), mode='valid')
    )
    energia_ref = np.linalg.norm(ref_f)
    ncc = corr / (energia_local * energia_ref + 1e-10)

    # 6) decision
    pico = np.max(np.abs(ncc))
    return pico >= limiar

if __name__ == "__main__":
    if len(sys.argv) not in (3,4):
        print("Usage: python analisador.py <input.wav> <ref.wav> [threshold]")
        sys.exit(1)

    entrada = sys.argv[1]
    ref     = sys.argv[2]
    limiar  = float(sys.argv[3]) if len(sys.argv)==4 else 0.6

    presente = detecta_palavra(entrada, ref, limiar=limiar)
    print("PRESENT" if presente else "ABSENT")
```

I have some example audios:

* `entrada.wav`: Contains the speech “Eu peguei o meu carro e fui passear na praia.”
* `entrada_sem_nada.wav`: Contains the speech “Fui no supermercado, mas esqueci a lista de compra.”
* `carro.wav`: Contains the word “carro.”
* `bola.wav`: Contains the word “bola.”
* `praia.wav`: Contains the word “praia.”

To run:

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analisador.py <input file> <word file> <threshold>
```

The threshold can be a value between 0.4 (very bad audio) and 0.8 (good audio). Very small values tend to generate false positives.

Execution examples:

```shell
$ python analisador.py entrada.wav praia.wav 0.8
PRESENT
$ python analisador.py entrada.wav carro.wav 0.8
PRESENT
$ python analisador.py entrada.wav bola.wav 0.8
ABSENT
$ python analisador.py entrada_sem_nada.wav bola.wav 0.8
ABSENT
$ python analisador.py entrada_sem_nada.wav carro.wav 0.8
ABSENT
$ python analisador.py entrada_sem_nada.wav praia.wav 0.8
ABSENT
```

## Code Analysis

The code is like a simple **pipeline** for detecting an audio segment (the “reference word”) inside a larger file. At a high level, the stages and techniques are:

1. **Reading and pre-processing**

   * Loads both WAV files (input and reference), ensuring they have the same sampling rate.
   * Converts to mono (channel average) and floating-point, preparing the signal for numerical processing.

2. **Band-pass filtering (Butterworth)**

   * Applies an adjustable-order filter (default 4) that passes only frequencies between 300 Hz and 3400 Hz, the typical speech band.

   * By removing low and high frequencies outside that range, it reduces noise and interference that do not help speech identification.

   > The Butterworth filter was designed to provide the smoothest possible frequency response in the passband, avoiding ripples, and to show monotonic attenuation outside this region, such that frequencies above the cutoff are progressively suppressed. The attenuation strength increases as filter order increases, yielding a steeper transition between bands. Mathematically, its gain follows 1/√(1+(ω/ωc)²ⁿ), giving –3 dB at the cutoff point, and the uniform distribution of poles along a semicircle in the complex plane ensures stability and flat behavior. Even in its digital version, obtained via transformations such as the bilinear transform, the Butterworth preserves these qualities, making it the natural choice when isolating a frequency band without introducing unwanted amplitude distortion.

3. **DC offset removal**

   * Subtracts the mean of each filtered signal, centering it at zero.

   * This prevents constant low-frequency components (offset) from influencing correlation later.

   > Non-zero mean value that shifts a signal’s baseline; must be removed to avoid bias in operations such as correlation.

4. **FFT-based cross-correlation**

   * Instead of sliding directly (which is slow), it uses the Fast Fourier Transform to convert signals to the frequency domain, multiplies spectra (with complex conjugate), and returns to time with the IFFT.

   * This technique quickly computes correlation between input and reference, showing where they match best.

   > **FFT**: Fast algorithm to compute the Discrete Fourier Transform (DFT), converting time-domain signals to frequency in O(N log N).

   > **IFFT**: Inverse FFT to reconstruct the time-domain signal from its frequency representation.

   > **Cross-correlation**: Measure of similarity between two signals as a function of their relative shift; detects when a pattern appears within another.

5. **Energy normalization (NCC)**

   * Divides the raw correlation by the square-root of the product of local input energy (sum of squares in a window equal to the reference length) and total reference energy.

   * Produces a dimensionless coefficient ranging from –1 to 1, indicating similarity independent of signal volume.

   > **NCC**: Cross-correlation divided by the product of signal energies, yielding a coefficient between –1 and 1, independent of amplitude.

6. **Threshold decision**

   * Finds the highest absolute normalized coefficient (the “peak”).
   * If that peak reaches or exceeds a threshold (e.g., 0.6), the code considers the reference word present in the input audio.

In short, the algorithm combines filtering to isolate speech, fast frequency-domain correlation to measure temporal similarity, and normalization to make detection robust to intensity variations, finishing with a simple threshold comparison to decide “present” or “absent.”

## Did you like it?

For more articles like this, follow me [**here**](https://linkedin.com/in/cleutonsampaio), or subscribe to my [**channel**](https://www.youtube.com/@CleutonSampaio), and visit my [**courses page**](https://www.cleutonsampaio.com/).
