import cv2
import numpy as np
from skimage import color, feature, filters, measure

# Inicia a captura de vídeo pela webcam
captura = cv2.VideoCapture(0)

# Define o tamanho da janela de visualização
captura.set(3, 640) # largura da janela
captura.set(4, 480) # altura da janela

# Loop infinito para capturar e processar os quadros da webcam
while True:
    # Lê um quadro da webcam
    ret, quadro = captura.read()

    # Converte o quadro para escala de cinza
    cinza = color.rgb2gray(quadro)

    # Aplica um filtro Gaussiano para suavizar a imagem
    suave = filters.gaussian(cinza, sigma=2)

    # Detecta as bordas da imagem usando o algoritmo de Canny
    bordas = feature.canny(suave, sigma=2)

    # Encontra os contornos das formas presentes na imagem
    contornos = measure.find_contours(bordas, level=0.8)

    # Loop sobre todos os contornos encontrados
    for cnt in contornos:
        # Calcula a área do contorno
        area = measure.contour_area(cnt)

        # Desenha apenas os contornos com área maior que 500 pixels
        if area > 500:
            # Desenha o contorno externo em verde
            vertices = cnt.astype(np.int32)
            cv2.polylines(quadro, [vertices], True, (0, 255, 0), 2)

            # Encontra o casco convexo do contorno externo para extrair o contorno interno
            casco = measure.convex_hull_object(cnt)

            # Desenha o contorno interno em vermelho
            vertices = casco.coords.astype(np.int32)
            cv2.polylines(quadro, [vertices], True, (0, 0, 255), 2)

    # Mostra o quadro com os contornos na janela de visualização
    cv2.imshow('quadro', quadro)

    # Aguarda uma tecla ser pressionada para verificar se deve encerrar o programa
    if cv2.waitKey(1) == ord('q'):
        break

# Encerra a captura de vídeo e fecha a janela de visualização
captura.release()
cv2.destroyAllWindows()
