import parametros as p
import sys, os

from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox
)
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter
from PyQt5 import QtCore
# import parametros as p
from time import sleep
from back_end.logica_ventanas import VentanaJuegoLogica, Flecha
from back_end.music_player import MusicPlayer
from back_end.flechas import PinguirinBaila, PinguirinTienda

class VentanaRanking(QWidget):
    senal_volver_inicio = pyqtSignal()

    def __init__(self):
        # self.setGeometry(200, 100, p.ANCHO_VENTANA_TERMINO, p.ALTO_VENTANA_TERMINO)
        super().__init__()
        self.puntaje_acumulado = 0
        self.ronda = 0
        self.setGeometry(200, 100, 400, 400)
        
        self.titulo_ventana = QLabel(self)
        self.titulo_ventana.setText("Ranking de Puntajes")

        self.top_1 = QLabel(self)
        self.top_1.setText("")

        self.puntaje_1 = QLabel(self)
        self.puntaje_1.setText("")
    
        top_1 = QHBoxLayout()
        top_1.addWidget(self.top_1)
        top_1.addWidget(self.puntaje_1)

        self.top_2 = QLabel(self)
        self.top_2.setText("")

        self.puntaje_2 = QLabel(self)
        self.puntaje_2.setText("")
    
        top_2 = QHBoxLayout()
        top_2.addWidget(self.top_2)
        top_2.addWidget(self.puntaje_2)

        self.top_3 = QLabel(self)
        self.top_3.setText("")

        self.puntaje_3 = QLabel(self)
        self.puntaje_3.setText("")
    
        top_3 = QHBoxLayout()
        top_3.addWidget(self.top_3)
        top_3.addWidget(self.puntaje_3)

        self.top_4 = QLabel(self)
        self.top_4.setText("")

        self.puntaje_4 = QLabel(self)
        self.puntaje_4.setText("")
    
        top_4 = QHBoxLayout()
        top_4.addWidget(self.top_4)
        top_4.addWidget(self.puntaje_4)

        self.top_5 = QLabel(self)
        self.top_5.setText("")

        self.puntaje_5 = QLabel(self)
        self.puntaje_5.setText("")
    
        top_5 = QHBoxLayout()
        top_5.addWidget(self.top_5)
        top_5.addWidget(self.puntaje_5)
 
        box_texto_central = QVBoxLayout()
        box_texto_central.addStretch(1)
        box_texto_central.addLayout(top_1)
        box_texto_central.addLayout(top_2)
        box_texto_central.addLayout(top_3)
        box_texto_central.addLayout(top_4)
        box_texto_central.addLayout(top_5)
        box_texto_central.addStretch(1)

        self.boton_volver = QPushButton("&Volver")
        self.boton_volver.resize(self.boton_volver.sizeHint())

        self.boton_volver.clicked.connect(self.volver)

        botones_box = QHBoxLayout()
        botones_box.addStretch(1)
        botones_box.addWidget(self.boton_volver)
        botones_box.addStretch(1)


        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.titulo_ventana)
        vbox.addLayout(box_texto_central)
        vbox.addLayout(botones_box)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def volver(self):
        self.hide()
        self.senal_volver_inicio.emit()

    def mostrar_ranking(self):
        puntajes = {}
        with open("ranking.txt","rt") as lectura:
            leido = lectura.readlines()
            for linea in leido:
                fila = linea.strip().split(',')
                puntajes[fila[0]] = int(fila[1])


        # Ordenamiento de mayor a menor puntaje
        sort_orders = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
        rompe_loop = 0
        if len(puntajes) == 0:
            self.top_1.setText("No hay puntajes aun :/")
            return
        for jugador in sort_orders:
            rompe_loop += 1
            if rompe_loop > 5:
                break
            if rompe_loop == 1:
                self.top_1.setText(jugador[0])
                self.puntaje_1.setText(str(jugador[1]))
            elif rompe_loop == 2:
                self.top_2.setText(jugador[0])
                self.puntaje_2.setText(str(jugador[1]))
            elif rompe_loop == 3:
                self.top_3.setText(jugador[0])
                self.puntaje_3.setText(str(jugador[1]))
            elif rompe_loop == 4:
                self.top_4.setText(jugador[0])
                self.puntaje_4.setText(str(jugador[1]))
            elif rompe_loop == 5:
                self.top_5.setText(jugador[0])
                self.puntaje_5.setText(str(jugador[1]))

        self.show()
        

class TiendaPuffs(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(20, 200, 200, 200)
        self.pinguirin_morado = PinguirinTienda(self)
        self.pinguirin_morado.Geometry(10, 0, 51, 51)
        self.pinguirin_morado.Pixmap(QPixmap(p.puff_1))
        self.pinguirin_morado.setScaledContents(True)

        self.pinguirin_verde = PinguirinTienda(self)
        self.pinguirin_verde.Geometry(10, 100, 51, 51)
        self.pinguirin_verde.Pixmap(QPixmap(p.puff_2))
        self.pinguirin_verde.setScaledContents(True)

        self.pinguirin_rojo = PinguirinTienda(self)
        self.pinguirin_rojo.Geometry(90, 0, 51, 51)
        self.pinguirin_rojo.Pixmap(QPixmap(p.puff_3))
        self.pinguirin_rojo.setScaledContents(True)

        self.pinguirin_amarillo = PinguirinTienda(self)
        self.pinguirin_amarillo.Geometry(90, 100, 51, 51)
        self.pinguirin_amarillo.Pixmap(QPixmap(p.puff_4))
        self.pinguirin_amarillo.setScaledContents(True)