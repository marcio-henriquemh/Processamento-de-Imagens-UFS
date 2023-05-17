# A operação de Dilatação no estudo de morfologia matwmática binária, consiste
#A(+)B , onde A é o conjunto ou a imagem , B é o elemento estruturante.



import matplotlib.pyplot as plt
import cv2
import numpy as np
import matplotlib.cm as cm
from skimage.morphology import binary_opening, binary_closing
from skimage.filters import sobel

#lendo uma imagem


img_gray = cv2.imread('/home/marciohenrique/UFS/Processamento de Imagens/OPeraçoes_Morfologica/rose.png.jpg')
plt.imshow(img_gray,cmap='gray')
plt.show()

