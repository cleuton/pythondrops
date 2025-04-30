#!/usr/bin/env python3
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

def filtro_passa_banda(sinal, sr, lowcut=300, highcut=3400, ordem=4):
    """
    Aplica filtro Butterworth passa-banda ao vetor 'sinal'.
    - lowcut/highcut definem a faixa de interesse (Hz).
    - ordem controla a inclinação do filtro.
    """
    nyq = 0.5 * sr
    wn = [lowcut/nyq, highcut/nyq]
    sos = butter(ordem, wn, btype='band', output='sos')
    return sosfilt(sos, sinal)

def correlacao_fft(sinal, ref):
    """
    Calcula a correlação cruzada válida de 'sinal' com 'ref' via FFT.
    Retorna apenas a parte em que a referência cabe no sinal.
    """
    n_corr = len(sinal) + len(ref) - 1
    N = 1 << (n_corr - 1).bit_length()
    S = np.fft.fft(sinal, n=N)
    R = np.fft.fft(ref,   n=N)
    corr = np.fft.ifft(S * np.conj(R)).real
    return corr[len(ref)-1 : len(sinal)]

def detecta_palavra(entrada_wav, ref_wav, limiar=0.6):
    """
    Retorna True se o trecho em 'ref_wav' for detectado em 'entrada_wav'.
      1) Carrega ambos os WAVs (mono ou stereo → converte pra mono)
      2) Filtra passa-banda para reduzir ruído fora da fala
      3) Remove offset DC (média)
      4) Calcula correlação via FFT
      5) Normaliza localmente pelo produto de energias
      6) Verifica se o maior coeficiente ≥ limiar
    """
    # 1) leitura
    sr_e, entrada = wavfile.read(entrada_wav)
    sr_r, ref    = wavfile.read(ref_wav)
    if sr_e != sr_r:
        raise ValueError("Taxas de amostragem diferentes")

    # mono → média dos canais; float
    if entrada.ndim == 2: entrada = entrada.mean(axis=1)
    if ref.ndim     == 2: ref     = ref.mean(axis=1)
    entrada = entrada.astype(float)
    ref     = ref.astype(float)

    # 2) filtragem
    entrada_f = filtro_passa_banda(entrada, sr_e)
    ref_f     = filtro_passa_banda(ref,     sr_e)

    # 3) remove offset DC
    entrada_f -= np.mean(entrada_f)
    ref_f     -= np.mean(ref_f)

    # 4) correlação via FFT
    corr = correlacao_fft(entrada_f, ref_f)

    # 5) normalização local
    energia_local = np.sqrt(
        np.convolve(entrada_f**2, np.ones(len(ref_f)), mode='valid')
    )
    energia_ref = np.linalg.norm(ref_f)
    ncc = corr / (energia_local * energia_ref + 1e-10)

    # 6) decisão
    pico = np.max(np.abs(ncc))
    return pico >= limiar

if __name__ == "__main__":
    if len(sys.argv) not in (3,4):
        print("Uso: python analisador.py <entrada.wav> <ref.wav> [limiar]")
        sys.exit(1)

    entrada = sys.argv[1]
    ref     = sys.argv[2]
    limiar  = float(sys.argv[3]) if len(sys.argv)==4 else 0.6

    presente = detecta_palavra(entrada, ref, limiar=limiar)
    print("PRESENTE" if presente else "AUSENTE")
