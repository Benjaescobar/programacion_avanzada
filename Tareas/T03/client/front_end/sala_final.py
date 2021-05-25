from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox, QGridLayout
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QImage
from os.path import join
from time import sleep
from os.path import join

import json
with open(join("client", "parameters.json")) as file:
    parametros = json.load(file)

class SalaFinal(QWidget):

    senal_empezar_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widget_size = (parametros["dimensiones_sala_espera"][0],
            parametros["dimensiones_sala_espera"][1])
        self.__initgui__()
        

    def __initgui__(self):

        self.setGeometry(
            300, 
            300, 
            self.widget_size[0],
            self.widget_size[1])

        self.logo = QLabel(self)
        path_logo = parametros["path_logo"]
        pixmap = QPixmap(join(path_logo[0], path_logo[1], path_logo[2], path_logo[3]))
        self.logo.setPixmap(pixmap.scaled(
            self.widget_size[0]*0.9, self.widget_size[0]*0.3, 
            transformMode=Qt.SmoothTransformation))

        ## nombres usuarios

        self.usuario_ganador = QLabel(self)
        self.usuario_ganador.setGeometry(self.widget_size[0]/2 - 50, self.widget_size[1]/2, 100, 20)

    def mostrar_ventana(self, usuario_ganador):
        self.usuario_ganador.setText(usuario_ganador)
        self.show()
