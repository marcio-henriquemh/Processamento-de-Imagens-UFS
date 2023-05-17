import os
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np



# Define o caminho para o diretório de entrada
imagens_dataset_entrada = ('/home/marciohenrique/UFS/Processamento de Imagens/Projeto Final/dataset/images')

# Define o caminho para o diretório de imagens tons de cinza
imagens_dataset_saida = ('/home/marciohenrique/UFS/Processamento de Imagens/Projeto Final/dataset/imagens_hsv')


# Cria o diretório de saída, caso não exista
if not os.path.exists(imagens_dataset_saida):
    os.makedirs(imagens_dataset_saida)

# Loop para processar todas as imagens do diretório de entrada
for lendo_imagens in os.listdir(imagens_dataset_entrada):

    # Verifica se o arquivo é uma imagem
    if lendo_imagens.endswith(".jpg") or lendo_imagens.endswith("j.peg") or lendo_imagens.endswith(".png"):

        #carregar imagens
        imagem=cv2.imread(os.path.join(imagens_dataset_entrada,lendo_imagens))
        #converter para espaços de cores HSV

        imagem_hsv=cv2.cvtColor(imagem,cv2.COLOR_BGR2HSV)

        #Separar o componente da matriz vermelha
        min_cor_vermelha=np.array([150,100,100],np.uint8)
        max_cor_vermelho=np.array([180,255,255],np.uint8)
        kernel_vermelho=cv2.inRange(imagem_hsv,min_cor_vermelha,max_cor_vermelho)
        

        #definindo o diretório de saída
        caminho_imagem_hsv_saida=os.path.join(imagens_dataset_saida,lendo_imagens)
           
        #salvando imagem na cor vermelha

        cv2.imwrite(caminho_imagem_hsv_saida,kernel_vermelho)






