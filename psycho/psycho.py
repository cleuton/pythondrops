import pygame
import numpy as np
import math
import sys

# Inicialização do Pygame
def iniciar_pygame(largura, altura):
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Caleidoscópio Psicodélico - Túnel")
    return tela

# Gera a malha de coordenadas normalizadas
def gerar_malha(largura, altura):
    x = np.linspace(-1, 1, largura)
    y = np.linspace(-1, 1, altura)
    X, Y = np.meshgrid(x, y)
    return X, Y

# Atualiza cada frame desenhando o túnel caleidoscópico
def atualizar_frame(tela, X, Y, tempo, segmentos=12):
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    
    angulo_segmento = 2 * math.pi / segmentos
    Theta_mod = np.mod(Theta, angulo_segmento)
    Theta_dobrado = np.abs(Theta_mod - angulo_segmento / 2)
    
    padrao_radial = np.sin(10 * R - tempo * 4)
    padrao_angular = np.sin(segmentos * Theta_dobrado + tempo * 6)
    
    padrao = (padrao_radial + padrao_angular) / 2
    padrao_norm = ((padrao + 1) / 2 * 255).astype(np.uint8)
    
    canal_r = padrao_norm
    canal_g = ((np.sin(10 * R - tempo * 4 + 2) + 1) / 2 * 255).astype(np.uint8)
    canal_b = ((np.sin(10 * R - tempo * 4 + 4) + 1) / 2 * 255).astype(np.uint8)
    
    imagem = np.dstack((canal_r, canal_g, canal_b))  # (altura, largura, 3)
    
    # Transpõe para (largura, altura, 3) para casar com a Surface
    imagem_corrigida = np.transpose(imagem, (1, 0, 2))
    
    pygame.surfarray.blit_array(tela, imagem_corrigida)
    pygame.display.flip()

# Laço principal
def main():
    largura, altura = 800, 600
    tela = iniciar_pygame(largura, altura)
    X, Y = gerar_malha(largura, altura)
    relogio = pygame.time.Clock()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        tempo = pygame.time.get_ticks() / 1000.0
        atualizar_frame(tela, X, Y, tempo, segmentos=16)
        relogio.tick(30)

if __name__ == "__main__":
    main()
