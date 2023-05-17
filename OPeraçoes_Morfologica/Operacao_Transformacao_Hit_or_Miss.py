import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox
from PyQt5.QtCore import QTimer
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cria uma label para exibir a imagem da webcam
        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 640, 480)

        # Cria uma ComboBox para selecionar o tipo de imagem
        self.combo_box = QComboBox(self)
        self.combo_box.setGeometry(50, 10, 150, 30)
        self.combo_box.addItem("Normal")
        self.combo_box.addItem("Hit-or-Miss")

        # Conecta o evento de mudança de valor da ComboBox ao método correspondente
        self.combo_box.currentIndexChanged.connect(self.atualizar_imagem)

        # Inicia a captura de vídeo da webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Inicia o loop para exibir os quadros da webcam
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_imagem)
        self.timer.start(30)

    def atualizar_imagem(self):
        # Lê o último quadro da webcam
        ret, frame = self.cap.read()

        if ret:
            if self.combo_box.currentIndex() == 1:
                # Aplica a Transformação Hit-or-Miss na imagem
                img_tons_cinza= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                estruturante_positivo = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8)
                estruturante_negativo = np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]], dtype=np.uint8)
                erosao_positivo = cv2.erode(img_tons_cinza, estruturante_positivo)
                erosao_negativo = cv2.erode(cv2.bitwise_not(img_tons_cinza), estruturante_negativo)
                transformacao_hit_or_miss = cv2.bitwise_and(erosao_positivo, cv2.bitwise_not(erosao_negativo))
                img_rgb = cv2.cvtColor(transformacao_hit_or_miss, cv2.COLOR_GRAY2RGB)
            else:
                # Converte a imagem para tons de cinza
                img_tons_cinza= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Converte a imagem para RGB
                img_rgb = cv2.cvtColor(img_tons_cinza, cv2.COLOR_GRAY2RGB)
                # Binariza a imagem com um limite de intensidade de 127
            _, img_binarizacao = cv2.threshold(img_tons_cinza, 127, 255, cv2.THRESH_BINARY)

            # Converte a imagem binária para RGB
            img_rgb = cv2.cvtColor(img_binarizacao, cv2.COLOR_GRAY2RGB)

             # Cria um QImage a partir da imagem RGB
            altura, largura, canal = img_rgb.shape
            bytes_linha = 3 * largura
            q_img = QImage(img_rgb.data, largura,altura,bytes_linha, QImage.Format_RGB888)

            # Cria um QPixmap a partir do QImage
            pixmap = QPixmap(q_img)

            # Redimensiona o QPixmap para o tamanho da label
            pixmap = pixmap.scaled(self.label.largura(), self.label.height())

            # Exibe o QPixmap na label
            self.label.setPixmap(pixmap)

            

    def closeEvent(self, event):
        # Encerra a captura de vídeo da webcam
        self.cap.release()
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
