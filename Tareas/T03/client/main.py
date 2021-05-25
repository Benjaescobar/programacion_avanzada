from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QImage
from os.path import join
from front_end.sala_espera import SalaEspera, parametros
from front_end.sala_de_juego import SalaJuego
from front_end.sala_final import SalaFinal
from back_end.cliente import Cliente

import json
import sys
from os.path import join

with open(join("client", "grafo.json")) as file:
    grafo = json.load(file)


if __name__ == "__main__":
    app = QApplication([])
    HOST = "localhost"
    PORT = 47365

    cliente = Cliente(PORT, HOST)
    sala_espera = SalaEspera()
    sala_juego = SalaJuego(list(grafo["nodos"].keys()))
    sala_final = SalaFinal()
    ## SENALES

    cliente.senal_nombres_usuario.connect(sala_espera.anadir_usuarios)
    cliente.senal_empezar_juego.connect(sala_espera.cargar_sala_juego)
    cliente.senal_actualizar_dados.connect(sala_juego.actualizar_dados)
    cliente.senal_cargar_mapa.connect(sala_juego.cargar_mapa)
    cliente.senal_actualizar_usuarios.connect(sala_juego.actualizar_usuarios)
    cliente.senal_turno.connect(sala_juego.usar_turno)
    cliente.senal_actualizar_mapa.connect(sala_juego.actualizar_mapa)
    cliente.senal_cargar_usuarios.connect(sala_juego.crear_usuarios)
    cliente.senal_terminar_juego.connect(sala_juego.terminar_juego)
    sala_juego.senal_terminar_juego.connect(sala_final.mostrar_ventana)
    sala_juego.widget_mapa.senal_construir_casa.connect(cliente.request_construir_casa)
    sala_juego.widget_mapa.senal_construir_camino.connect(cliente.request_construir_camino)
    sala_juego.senal_lanzar_dado.connect(cliente.lanzar_dado)
    sala_juego.senal_terminar_turno.connect(cliente.terminar_turno)
    sala_espera.senal_empezar_juego.connect(sala_juego.show)
    
    sala_juego.senal_lanzar_dado.connect(cliente.lanzar_dado)

    sys.exit(app.exec_())