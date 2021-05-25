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

class SalaEspera(QWidget):

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
        self.esperando_usuarios_mensaje = QLabel(self)
        self.esperando_usuarios_mensaje.setGeometry(170, 0, 100, 20)

        self.nombres = QWidget(self)

        self.usuario1 = QLabel(self.nombres)
        self.usuario2 = QLabel(self.nombres)
        self.usuario3 = QLabel(self.nombres)
        self.usuario4 = QLabel(self.nombres)
        self.usuario5 = QLabel(self.nombres)

        grid_layout_nombre_usuarios = QGridLayout(self.nombres)
        grid_layout_nombre_usuarios.addWidget(self.usuario1, 0, 0)
        grid_layout_nombre_usuarios.addWidget(self.usuario2, 0, 2)
        grid_layout_nombre_usuarios.addWidget(self.usuario3, 1, 0)
        grid_layout_nombre_usuarios.addWidget(self.usuario4, 1, 2)
        grid_layout_nombre_usuarios.addWidget(self.usuario5, 2, 1)

        # self.nombres.setLayout(grid_layout_nombre_usuarios)

        vbox = QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(self.logo)
        vbox.addWidget(self.esperando_usuarios_mensaje)
        vbox.addWidget(self.nombres)
        vbox.addStretch(1)

        hbox = QHBoxLayout(self)
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

        self.show()

    def anadir_usuarios(self, usuarios):
        print("agregando usuario")
        self.esperando_usuarios_mensaje.setText(f"Esperando a {5 - len(usuarios)} usuarios")
        for i in range(len(usuarios)):
            if i == 0:
                self.usuario1.setText(str(usuarios[0].replace('"', "")))
            elif i == 1:
                self.usuario2.setText(str(usuarios[1].replace('"', "")))
            elif i == 2:
                self.usuario3.setText(str(usuarios[2].replace('"', "")))
            elif i == 3:
                self.usuario4.setText(str(usuarios[3].replace('"', "")))
            elif i == 4:
                self.usuario5.setText(str(usuarios[4].replace('"', "")))
    
    def cargar_sala_juego(self):
        self.senal_empezar_juego.emit()
        self.hide()
