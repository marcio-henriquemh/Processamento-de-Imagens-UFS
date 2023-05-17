from ctypes import *
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np

# Carrega a biblioteca compartilhada contendo a função de filtro de mediana em C
mediana_lib = CDLL("./filtro_mediana.so")

# Define os tipos de argumentos e retorno para a função de filtro de mediana em C
mediana_lib.filtro_mediana.argtypes = [c_int, c_int, POINTER(c_ubyte), POINTER(c_ubyte)]
mediana_lib.filtro_mediana.restype = None

# Função de filtro de mediana em Python que chama a função de filtro de mediana em C
def filtro_mediana_c(image):
    width, height = image.shape[:2]
    data_in = image.ctypes.data_as(POINTER(c_ubyte))
    data_out = (c_ubyte * (width * height * 3))()
    mediana_lib.filtro_mediana(width, height, data_in, data_out)
    return np.ctypeslib.as_array(data_out, shape=(height, width, 3))

# Função de filtro de mediana em Python que aplica o filtro usando o OpenCV
def filtro_mediana_python(image):
    return cv2.medianBlur(image, 5)



#bibliotcas
#cv2 (OpenCV) é uma biblioteca de visão computacional muito utilizada em processamento de imagens e vídeos;
#PyQt5 é uma biblioteca que fornece uma interface gráfica para aplicações em Python;
#numpy é uma biblioteca de computação numérica utilizada em diversas aplicações, incluindo processamento de imagens.



#O método __init__ é chamado quando uma instância da classe é criada. Ele define o título da janela (self.setWindowTitle), o tamanho do vídeo (self.video_size) 
# e chama o método setup_ui para configurar a interface gráfica.
#
#
class Interface(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Filtro da Mediana")
        self.video_size = QtCore.QSize(640, 480)
        self.setup_ui()
        
        

    def setup_ui(self):
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.quit_button = QtWidgets.QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)

        self.filter_dropdown = QtWidgets.QComboBox()
        self.filter_dropdown.addItems(["Imagem_normal", "Imagem_sal_e_pimenta", "Filtro_mediana"])
        self.filter_dropdown.currentIndexChanged.connect(self.aplicando_filtro)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.filter_dropdown)
        layout.addWidget(self.quit_button)


        #pode ser uma função que recebe uma imagem como entrada e um filtro (kernel) para aplicar na imagem. Essa função usa a técnica de convolução para aplicar o filtro na imagem.

    def aplicando_filtro(self):
        filter_name = self.filter_dropdown.currentText()
        if filter_name == "Imagem_sal_e_pimenta":
            self.filtro_imagem(sal_e_pimenta)
        elif filter_name == "Filtro_mediana":
            self.filtro_imagem(filtro_mediana)
        else:
            self.filtro_imagem(lambda x: x)

    def filtro_imagem(self, filter_function):
        pixmap = self.image_label.pixmap()
        if pixmap is None:
            return

        image = pixmap.toImage()
        width, height = image.width(), image.height()
        image = image.convertToFormat(QtGui.QImage.Format_RGB888)
        ptr = image.constBits()
        ptr.setsize(image.byteCount())

        np_array = np.array(ptr).reshape(height, width, 3)

        np_array = filter_function(np_array)

        qt_image = QtGui.QImage(np_array.data, width, height, np_array.strides[0], QtGui.QImage.Format_RGB888)

        pixmap = QtGui.QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

#sta função aplica um efeito de sal e pimenta aleatório à imagem. Isso é feito selecionando aleatoriamente alguns pixels e definindo seus valores de pixel para preto ou branco.
def sal_e_pimenta(image):
    probability = 0.08
    rand = np.random.rand(*image.shape[:2])
    mask = rand < probability / 2.
    image[mask, :] = 0
    out = np.copy(image)
    mask = rand > 1 - probability / 2.
    out[mask, :] = 255
    return out

def filtro_mediana(image):
    return cv2.medianBlur(image, 5)
#ste método é chamado quando uma instância da classe MainWindow é criada
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.camera_widget = Interface()
        self.setCentralWidget(self.camera_widget)
        self._capture = None
        self.start_webcam()

    def start_webcam(self):
        self._capture = cv2.VideoCapture(0)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_widget.video_size.width())
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_widget.video_size.height())

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(5)

    def update_frames(self):
        ret, frame = self._capture.read()
        if ret:
            filter_name = self.camera_widget.filter_dropdown.currentText()
            if filter_name == "Imagem_sal_e_pimenta":
                frame = sal_e_pimenta(frame)
            self.camera_widget.image_label.setPixmap(QtGui.QPixmap.fromImage(
                QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            ))

    def closeEvent(self, event):
        self._capture.release()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
