# -*- coding: utf-8 -*-
"""
Detector estatístico de imagens geradas por IA
Baseado em características de ruído, frequência, cor e textura
"""

import cv2
import numpy as np
from scipy.fftpack import fft2, fftshift
from scipy import stats
from skimage.feature import local_binary_pattern
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def extrair_residuos_ruido(imagem):
    """
    Extrai resíduos de ruído usando filtro bilateral
    Retorna estatísticas do resíduo
    """
    # Converter para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    # Aplicar filtro bilateral para remoção de ruído
    suavizada = cv2.bilateralFilter(cinza, d=9, sigmaColor=75, sigmaSpace=75)
    
    # Calcular resíduo absoluto
    residuo = cv2.absdiff(cinza, suavizada)
    
    # Calcar estatísticas do resíduo
    return [np.mean(residuo), np.var(residuo)]

def medir_estatisticas_frequencia(imagem, tamanho_bloco=32):
    """
    Calcula razão de energia entre altas e baixas frequências
    usando FFT em blocos da imagem
    """
    # Converter para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY).astype(float)
    
    razoes = []
    for y in range(0, cinza.shape[0], tamanho_bloco):
        for x in range(0, cinza.shape[1], tamanho_bloco):
            bloco = cinza[y:y+tamanho_bloco, x:x+tamanho_bloco]
            
            # Aplicar FFT e centralizar
            fft = fftshift(fft2(bloco))
            magnitude = np.log(np.abs(fft) + 1e-9)
            
            # Máscara para altas frequências (borda)
            mascara = np.ones_like(magnitude)
            centro = tamanho_bloco//2
            mascara[centro-3:centro+4, centro-3:centro+4] = 0
            
            # Calcular razão de energia
            energia_alta = np.sum(magnitude * mascara)
            energia_baixa = np.sum(magnitude * (1 - mascara))
            razoes.append(energia_alta / (energia_baixa + 1e-9))
    
    return [np.mean(razoes), np.std(razoes)]

def caracterizar_distribuicao_cores(imagem):
    """
    Calcula momentos estatísticos (média, variância, skewness, curtose)
    para cada canal de cor no espaço YCbCr
    """
    # Converter para YCbCr
    ycbcr = cv2.cvtColor(imagem, cv2.COLOR_BGR2YCrCb)
    
    caracteristicas = []
    for canal in range(3):
        dados = ycbcr[:, :, canal].flatten()
        caracteristicas.extend([
            np.mean(dados),
            np.var(dados),
            stats.skew(dados),
            stats.kurtosis(dados)
        ])
    
    return caracteristicas

def extrair_textura_local(imagem, raio=3, pontos=24):
    """
    Extrai histograma de padrões binários locais (LBP)
    para caracterização de textura
    """
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    lbp = local_binary_pattern(cinza, pontos, raio, method='uniform')
    hist, _ = np.histogram(lbp, bins=pontos+2, range=(0, pontos+2))
    return hist.tolist()

def extrair_caracteristicas(imagem):
    """
    Combina todas as características em um vetor único
    """
    features = []
    features += extrair_residuos_ruido(imagem)
    features += medir_estatisticas_frequencia(imagem)
    features += caracterizar_distribuicao_cores(imagem)
    features += extrair_textura_local(imagem)
    return features

# Exemplo de uso --------------------------------------------------------------
if __name__ == "__main__":
    # 1. Carregar dataset (substituir com seus próprios dados)
    # Formato esperado: lista de tuplas (caminho_imagem, rotulo)
    # Rotulo: 0 para real, 1 para IA
    dataset = [
        ("imagens/im1.jpg", 0),
        ("imagens/im2.jpg", 1),
        ("imagens/im3.jpg", 0),
        ("imagens/im4.jpg", 1),
        ("imagens/im5.jpg", 0),
        ("imagens/im6.jpg", 1),
        ("imagens/im7.jpg", 0),
        ("imagens/im8.jpg", 1),
        ("imagens/im9.jpg", 0),
        ("imagens/im10.jpg", 1),
        ("imagens/im11.jpg", 0),
        ("imagens/im12.jpg", 1),
        ("imagens/im13.jpg", 0),
        ("imagens/im14.jpg", 1),
        ("imagens/im15.jpg", 0),
        ("imagens/im16.jpg", 1),
        ("imagens/im17.jpg", 0),
        ("imagens/im18.jpg", 1),
        ("imagens/im19.jpg", 0),
        ("imagens/im20.jpg", 1),
        ("imagens/im21.jpg", 0),
        ("imagens/im22.jpg", 1),
    ]
    
    # 2. Extrair características
    X = []
    y = []
    for caminho, rotulo in dataset:
        imagem = cv2.imread(caminho)
        if imagem is None:
            continue
            
        features = extrair_caracteristicas(imagem)
        X.append(features)
        y.append(rotulo)
    
    # 3. Treinar classificador
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)
    
    # 4. Avaliar desempenho
    print("Acurácia:", modelo.score(X_test, y_test))
    
    # 5. Prever nova imagem
    nova_imagem = cv2.imread("imagens/real.jpg")
    features = extrair_caracteristicas(nova_imagem)
    proba = modelo.predict_proba([features])[0][1]
    print(f"Probabilidade de ser IA (real.jpg): {proba:.2%}")

    nova_imagem = cv2.imread("imagens/ia.jpg")
    features = extrair_caracteristicas(nova_imagem)
    proba = modelo.predict_proba([features])[0][1]
    print(f"Probabilidade de ser IA (ia.jpg): {proba:.2%}")

    nova_imagem = cv2.imread("imagens/real2.jpg")
    features = extrair_caracteristicas(nova_imagem)
    proba = modelo.predict_proba([features])[0][1]
    print(f"Probabilidade de ser IA (real2.jpg): {proba:.2%}")

    nova_imagem = cv2.imread("imagens/ia2.jpg")
    features = extrair_caracteristicas(nova_imagem)
    proba = modelo.predict_proba([features])[0][1]
    print(f"Probabilidade de ser IA (ia2.jpg): {proba:.2%}")