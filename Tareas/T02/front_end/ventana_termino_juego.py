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
from time import sleep
# from back_end.logica_ventanas import VentanaJuegoLogica, Flecha
# from back_end.music_player import MusicPlayer

class VentanaResumen(QWidget):
    senal_ventana_incial = pyqtSignal()
    senal_registrar_puntaje = pyqtSignal(int, str)
    senal_volver_juego = pyqtSignal()
    senal_termino_nivel = pyqtSignal(object, object)
    def __init__(self):
        # self.setGeometry(200, 100, p.ANCHO_VENTANA_TERMINO, p.ALTO_VENTANA_TERMINO)
        super().__init__()
        self.puntaje_acumulado = 0
        self.ronda = 0
        self.setGeometry(200, 100, 400, 400)
        
        self.titulo_ventana = QLabel(self)
        self.titulo_ventana.setText("RESUMEN DE LA RONDA")

        self.texto_decision_jurado = QLabel(self)

        self.texto_puntaje_obtenido = QLabel(self)
        self.texto_puntaje_obtenido.setText("Puntaje Obtenido:")

        self.puntaje_obtenido = QLabel(self)
        self.puntaje_obtenido.setText("100000")
    
        puntaje_obtenido = QHBoxLayout()
        puntaje_obtenido.addWidget(self.texto_puntaje_obtenido)
        puntaje_obtenido.addWidget(self.puntaje_obtenido)

        self.texto_puntaje_acumulado = QLabel(self)
        self.texto_puntaje_acumulado.setText("Puntaje Acumulado")
        self.puntaje_acumulado_label = QLabel(self)

        puntaje_acumulado = QHBoxLayout()
        puntaje_acumulado.addWidget(self.texto_puntaje_acumulado)
        puntaje_acumulado.addWidget(self.puntaje_acumulado_label)

        self.texto_maximo_combo = QLabel(self)
        self.texto_maximo_combo.setText("Mayor Combo")
        self.maximo_combo = QLabel(self)

        maximo_combo = QHBoxLayout()
        maximo_combo.addWidget(self.texto_maximo_combo)
        maximo_combo.addWidget(self.maximo_combo)

        self.texto_pasos_fallados = QLabel(self)
        self.texto_pasos_fallados.setText("Pasos Fallados")
        self.pasos_fallados = QLabel(self)

        pasos_fallados = QHBoxLayout()
        pasos_fallados.addWidget(self.texto_pasos_fallados)
        pasos_fallados.addWidget(self.pasos_fallados)

        self.texto_porc_aprobacion = QLabel(self)
        self.texto_porc_aprobacion.setText("Porcentaje Aprobacion")
        self.porcentaje_aprobacion = QLabel(self)

        porcentaje_aprobacion = QHBoxLayout()
        porcentaje_aprobacion.addWidget(self.texto_porc_aprobacion)
        porcentaje_aprobacion.addWidget(self.porcentaje_aprobacion)

        box_texto_central = QVBoxLayout()
        box_texto_central.addLayout(puntaje_obtenido)
        box_texto_central.addLayout(puntaje_acumulado)
        box_texto_central.addLayout(maximo_combo)
        box_texto_central.addLayout(pasos_fallados)
        box_texto_central.addLayout(porcentaje_aprobacion)

        self.boton_volver = QPushButton("&Volver")
        self.boton_volver.resize(self.boton_volver.sizeHint())

        self.boton_volver.clicked.connect(self.volver)

        self.boton_continuar = QPushButton("&Continuar")
        self.boton_continuar.resize(self.boton_continuar.sizeHint())

        self.boton_continuar.clicked.connect(self.continuar)

        botones_box = QHBoxLayout()
        botones_box.addStretch(1)
        botones_box.addWidget(self.boton_volver)
        botones_box.addWidget(self.boton_continuar)
        botones_box.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.titulo_ventana)
        vbox.addLayout(box_texto_central)
        vbox.addWidget(self.texto_decision_jurado)
        vbox.addLayout(botones_box)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def definir_nombre(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario

    def termino_juego(self, ventana_juego):
        self.senal_termino_nivel.emit(ventana_juego, self)

    def volver(self):
        self.senal_registrar_puntaje.emit(self.puntaje_acumulado, self.nombre_usuario)
        self.senal_ventana_incial.emit()
        self.puntaje_acumulado = 0
        self.hide()
    
    def continuar(self):
        self.senal_volver_juego.emit()
        self.hide()