import parametros as p
import sys, os
from os.path import join

from random import randint, uniform
from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox, QMainWindow
)
from time import sleep
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QImage
from PyQt5.QtMultimedia import QMediaPlayer
from back_end.music_player import MusicPlayer

class Flecha(QThread):
    actualizar = pyqtSignal(QLabel, int, int)
    senal_mover_flecha = pyqtSignal(object)
    def __init__(self, label, pos_x, pos_y, tipo_flecha, ruta_flecha, lista_flechas):
        super().__init__()
        # LABEL DE LA FLECHA
        self.velocidad = 0
        self.mover = True
        self.lista_flechas = lista_flechas
        self.flecha = label
        self.flecha.setScaledContents(True)
        self.tipo_flecha = tipo_flecha
        # Estos limites sirven para no pasarse del widget
        self.limite_x = p.ANCHO_VENTANA_JUEGO
        self.limite_y = p.ALTO_VENTANA_JUEGO
        # Seteamos la posición inicial y la guardamos para usarla como una property
        self.__posicion = (0, 0)
        self.posicion = (pos_x, pos_y)
  
        self.flecha.setPixmap(QPixmap(ruta_flecha))
        self.flecha.resize(30, 30)
        self.start()

        self.flecha.show()

    @property
    def posicion(self):
        return self.__posicion

    # Cada vez que se actualicé la posición,
    # se actualiza la posición de la etiqueta
    @posicion.setter
    def posicion(self, valor):
        self.__posicion = valor
        #esta señal permite que se actualize la pantalla
        if self.posicion[1] <= self.limite_y - 30:   
            self.actualizar.emit(self.flecha, *self.posicion)
        else:
            self.flecha.hide()
            if self.flecha in self.lista_flechas:
                self.lista_flechas.remove(self.flecha)
                
    def run(self):
        if self.tipo_flecha == 0: # FLECHA NORMAL
                self.velocidad = p.velocidad_flecha_dorada
        else:
            self.velocidad = p.velocidad_flecha_normal

        while self.posicion[0] < self.limite_x and self.posicion[1] < self.limite_y:
            # self.senal_mover_flecha.emit(self.flecha)
            if self.mover == True:
                sleep(self.velocidad)
                nuevo_x = self.posicion[0]
                nuevo_y = self.posicion[1] + 1
                self.posicion = (nuevo_x, nuevo_y)
            else:
                continue


class PinguirinTienda(QLabel):
    ## ESTO CODIGO ESTA INSPIRADO EN EL TUTOTIAL DE 
    ## https://learndataanalysis.org/create-label-to-label-drag-and-drop-effect-pyqt5-tutorial/
    def Pixmap(self, pixmap):
        self.setPixmap(pixmap)
    
    def Geometry(self, px, py, w, h):
        self.setGeometry(px, py, w, h)
    
    def habilitar_tienda(self, bool):
        self.tienda_habilitada = bool

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() and Qt.LeftButton) and self.tienda_habilitada == True:
            return
        else:
            drag = QDrag(self)
            mimedata = QMimeData()
            mimedata.setImageData(self.pixmap())
            drag.setMimeData(mimedata)
            ## Dragging effect
            pixmap = QPixmap(self.size()) # label size
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
            self.show()

class PinguirinBaila(QLabel):
    def __init__(self, parent, ventana_juego):
        super().__init__(parent)
        self.ventana_juego = ventana_juego
        self.setAcceptDrops(True)
        self.color_asignado = QPixmap(p.pinguirin_amarillo).toImage()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.ventana_juego.dinero_jugador >= p.PRECIO_PINGUIRINES:
            if self.pixmap() == None:
                self.ventana_juego.dinero_jugador -= p.PRECIO_PINGUIRINES
                self.ventana_juego.dinero_jugador_label.setText(
                    str(self.ventana_juego.dinero_jugador))
                self.ventana_juego.lista_pinguirines_bailando.append(self)
                image = event.mimeData().imageData()
                self.setPixmap(image)
                event.acceptProposedAction()
                self.color_asignado = self.pixmap().toImage()
                if self.color_asignado == QPixmap(p.puff_4).toImage():
                    self.resize(50, 50)
                elif self.color_asignado == QPixmap(p.puff_3).toImage():
                    self.resize(50, 50)
                elif self.color_asignado == QPixmap(p.puff_2).toImage():
                    self.resize(50, 50)
                elif self.color_asignado == QPixmap(p.puff_1).toImage():
                    self.resize(50, 50)
            else:
                return
        else:
            return
    def hacer_paso(self, paso, lista_pasos):
        self.setPixmap(QPixmap(lista_pasos[paso]))