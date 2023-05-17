import numpy as np
import cv2
from skimage import morphology, measure

# Cria o objeto de captura de vídeo
captura = cv2.VideoCapture(0)

while True:
    # Lê um frame da webcam
    ret, quadro = captura.read()

    # Converte o quadro para escala de cinza
    cinza = cv2.cvtColor(quadro, cv2.COLOR_BGR2GRAY)

    # Aplica uma operação de limiarização para obter uma imagem binária
    limiar = np.uint8(0.5 * (cinza.max() + cinza.min()))
    binaria = np.uint8(cinza > limiar)

    # Aplica uma operação de abertura para remover ruídos e desconexões
    kernel = np.ones((5, 5))
    abertura = morphology.opening(binaria, kernel)

    # Extrai os componentes conexos da imagem binária usando a função measure.label
    rotulos = measure.label(abertura)

    # Cria uma paleta de cores para os rótulos
    cores = np.zeros((np.max(rotulos) + 1, 3), dtype=np.uint8)
    cores[1:] = np.random.randint(0, 255, (np.max(rotulos), 3))

    # Cria uma imagem colorida com os componentes conexos rotulados
    imagem_colorida = np.zeros((quadro.shape[0], quadro.shape[1], 3), dtype=np.uint8)
    for i in range(1, np.max(rotulos) + 1):
        imagem_colorida[rotulos == i] = cores[i]

    # Mostra a imagem colorida com os componentes conexos rotulados
    cv2.imshow('Componentes Conexos', imagem_colorida)

    # Aguarda uma tecla ser pressionada para encerrar o programa
    if cv2.waitKey(1) == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()
