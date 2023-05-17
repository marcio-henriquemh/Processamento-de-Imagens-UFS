import os
import cv2
import numpy as np
from skimage import io


imagens_dataset_entrada = '/home/marciohenrique/UFS/Processamento de Imagens/Projeto Final/dataset/imagens_hsv'
imagens_dataset_saida = '/home/marciohenrique/UFS/Processamento de Imagens/Projeto Final/dataset//saida_imagens_cinza_sobel'

if not os.path.exists(imagens_dataset_saida):
    os.makedirs(imagens_dataset_saida)

# Cria um kernel Sobel para detecção de bordas
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

for nome_imagem in os.listdir(imagens_dataset_entrada):
    # Verifica se o arquivo é uma imagem
    if nome_imagem.endswith(".jpg") or nome_imagem.endswith(".jpeg") or nome_imagem.endswith(".png"):
        # Carrega a imagem em tons de cinza
        imagem = cv2.imread(os.path.join(imagens_dataset_entrada, nome_imagem), cv2.IMREAD_GRAYSCALE)

        # Aplica o operador Sobel nas direções x e y
        grad_x = cv2.Sobel(imagem, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(imagem, cv2.CV_64F, 0, 1, ksize=3)

        # Calcula o módulo do gradiente
        gradiente = np.sqrt(grad_x ** 2 + grad_y ** 2)

        # Converte para o tipo de dado de 8 bits sem sinal (0 a 255)
        gradiente = cv2.convertScaleAbs(gradiente)

        # Normaliza a imagem
        gradiente = gradiente.astype(np.float32)
        gradiente_norm = cv2.normalize(gradiente, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

        
        
        # Salva a imagem resultante no diretório de saída
        nome_imagem_saida = os.path.splitext(nome_imagem)[0] + '_sobel.png'
        io.imsave(os.path.join(imagens_dataset_saida, nome_imagem_saida), gradiente_norm)
