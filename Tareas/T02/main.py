import os
import sys
import parametros as p

from back_end.logica_ventanas import VentanaJuegoLogica, Flecha, VentanaResumenLogica
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter
from PyQt5 import QtCore
from front_end.ventana_inicial import VentanaInicial
# from front_end.ventana_juego_qt import VentanaJuego, Flecha
from front_end.ventana_juego import VentanaJuego, PinguirinBaila, PinguirinTienda
from front_end.ventana_termino_juego import VentanaResumen
from front_end.ventana_ranking import VentanaRanking
#from back_end.logica_ventanas import MusicPlayer
from PyQt5.QtWidgets import QApplication, QMainWindow
from back_end.music_player import MusicPlayer
from back_end.flechas import Flecha, PinguirinTienda, PinguirinBaila
from time import sleep

if __name__ == "__main__":
    app = QApplication([])

    ventana_ranking = VentanaRanking()
    ventana_resumen = VentanaResumen()
    logica_juego = VentanaJuegoLogica()
    logica_ranking = VentanaResumenLogica()
    ventana_inicial = VentanaInicial()
    ventana_juego = VentanaJuego()
    music_player = MusicPlayer()

    ## SENALES
    ventana_inicial.senal_abrir_ranking.connect(ventana_ranking.mostrar_ranking)
    ventana_inicial.senal_comenzar_juego.connect(ventana_juego.show)
    ventana_inicial.senal_nombre_usuario.connect(ventana_resumen.definir_nombre)
    ventana_ranking.senal_volver_inicio.connect(ventana_inicial.show)
    logica_juego.senal_flecha_hielo.connect(logica_juego.flecha_hielo)    
    ventana_juego.senal_volver_inicio.connect(ventana_inicial.show)
    ventana_juego.senal_termino_juego.connect(ventana_resumen.termino_juego)
    ventana_juego.senal_crear_flechas.connect(logica_juego.crear_flechas)
    ventana_juego.senal_key_press.connect(logica_juego.key_press_event)
    ventana_juego.senal_inicio_juego.connect(logica_juego.comenzar_juego)
    ventana_juego.senal_reproducir_musica.connect(music_player.play_music)
    ventana_juego.senal_actualizar_bailarines.connect(logica_juego.actualizar_bailarines)
    ventana_juego.senal_pausa.connect(logica_juego.pausar_juego)
    ventana_juego.senal_actualizar_info.connect(logica_juego.actualizar_info_pantalla)
    ventana_resumen.senal_registrar_puntaje.connect(logica_ranking.escribir_ranking)
    ventana_resumen.senal_ventana_incial.connect(ventana_inicial.show)
    ventana_resumen.senal_volver_juego.connect(ventana_juego.show)
    ventana_resumen.senal_termino_nivel.connect(logica_ranking.termino_juego)

    sys.exit(app.exec_())