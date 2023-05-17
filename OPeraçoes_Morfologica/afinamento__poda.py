import cv2
import numpy as np
from skimage import morphology
import matplotlib.pyplot as plt

# Cria o objeto de captura de vídeo
captura = cv2.VideoCapture(0)

while True:
    # Lê o próximo frame da webcam
    ret, quadro = captura.read()
    
    # Converte o frame para tons de cinza
    cinza = cv2.cvtColor(quadro, cv2.COLOR_BGR2GRAY)
    
    # Aplica afinamento e poda na imagem em tons de cinza
    afinado = morphology.thin(cinza)
    
    # Mostra as imagens na tela
    cv2.imshow('Imagem original', quadro)
    plt.imshow(afinado, cmap='gray')
    plt.show()

    # Aguarda uma tecla ser pressionada para encerrar o programa
    if cv2.waitKey(1) == ord('q'):
        break

# Libera o objeto de captura e destroi as janelas
captura.release()
cv2.destroyAllWindows()
