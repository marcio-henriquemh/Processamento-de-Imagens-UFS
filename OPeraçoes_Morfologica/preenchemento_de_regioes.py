import cv2
import numpy as np

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
    cinza = cv2.cvtColor(quadro, cv2.COLOR_BGR2GRAY)
    
    # Aplica um filtro Gaussiano para suavizar a imagem
    suave = cv2.GaussianBlur(cinza, (5, 5), 0)
    
    # Detecta as bordas da imagem usando o algoritmo de Canny
    bordas = cv2.Canny(suave, 100, 200)

    # Encontra os contornos das formas presentes na imagem
    contornos, hierarquia = cv2.findContours(bordas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop sobre todos os contornos encontrados
    for cnt in contornos:
        # Calcula a área do contorno
        area = cv2.contourArea(cnt)
        
        # Desenha e preenche apenas os contornos com área maior que 500 pixels
        if area > 500:
            # Desenha e preenche o contorno externo em vermelho
            cv2.drawContours(quadro, [cnt], 0, (0, 0, 255), cv2.FILLED)
            
            # Encontra o casco convexo do contorno externo para extrair o contorno interno
            casco = cv2.convexHull(cnt)
            
            # Desenha e preenche o contorno interno em azul
            cv2.drawContours(quadro, [casco], 0, (255, 0, 0), cv2.FILLED)
    
    # Mostra o quadro com os contornos preenchidos na janela de visualização
    cv2.imshow('quadro', quadro)
    
    # Aguarda uma tecla ser pressionada para verificar se deve encerrar o programa
    if cv2.waitKey(1) == ord('q'):
        break

# Encerra a captura de vídeo e fecha a janela de visualização
captura.release()
cv2.destroyAllWindows()
