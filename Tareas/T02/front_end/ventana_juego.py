import parametros as p
import sys, os

from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox
)
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QImage
from PyQt5 import QtCore
# import parametros as p
from time import sleep
from back_end.logica_ventanas import VentanaJuegoLogica, Flecha
from back_end.music_player import MusicPlayer
from back_end.flechas import PinguirinBaila, PinguirinTienda
from front_end.ventana_ranking import TiendaPuffs

class VentanaJuego(QWidget):
    senal_inicio_juego = pyqtSignal(object)
    senal_key_press = pyqtSignal(dict, object)
    senal_reproducir_musica = pyqtSignal(str)
    senal_actualizar_bailarines = pyqtSignal(str, object)
    senal_pausa = pyqtSignal(object)
    senal_termino_juego = pyqtSignal(object)
    senal_crear_flechas = pyqtSignal(object, int)
    senal_actualizar_info = pyqtSignal(object)
    senal_volver_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        ## INICIALIZAR VENTANA
        self.nombre_usuario = ""
        self.porcentaje_cancion = 0
        self.contador_flechas_atrapadas = 0
        self.pasos_incorrectos = 0
        self.pasos_correctos = 0
        self.puntaje = 0
        self.contador_pasos_totales = 0
        self.combo_valor = 0
        self.combo_mayor_valor = 0
       
        self.ispausa = True
        self.aprobacion_necesaria = 0
        
        self.dinero_jugador = p.DINERO_INICIAL_JUGADOR
        self.init_gui()
    def init_gui(self):
        # Completar
        self.setGeometry(200, 100, p.ANCHO_VENTANA_JUEGO, p.ALTO_VENTANA_JUEGO)
        self.setWindowTitle('Baila pingüino')
        self.lista_pinguirines_bailando = []
        self.teclas_presionadas = {65: False, 83: False, 68: False, 87: False, 77: False,
            79: False, 71: False, 78: False, 73: False, 86: False, 70: False, 84: False,
            72: False}
        self.tienda_puffs = TiendaPuffs()
    #   ## VENTANA FLECHAS
        self.zona_flechas = QWidget(self)
        self.zona_flechas.setGeometry(QRect(20, 140, 171, 451))
        self.zona_flechas.setObjectName("flechas")
        self.zona_flechas.setStyleSheet("background-color:pink;")

        self.caja_left = QLabel(self.zona_flechas)
        self.caja_left.setGeometry(QRect(
            p.pos_x_caja_left, p.pos_y_cajas, 31, 31))
        self.caja_left.setPixmap(QPixmap(p.color_azul))
        self.caja_left.setObjectName("caja_left")

        self.caja_up = QLabel(self.zona_flechas)
        self.caja_up.setGeometry(QRect(
            p.pos_x_caja_up, p.pos_y_cajas, 31, 31))
        self.caja_up.setPixmap(QPixmap(p.color_azul))
        self.caja_up.setObjectName("caja_up")

        self.caja_down = QLabel(self.zona_flechas)
        self.caja_down.setGeometry(QRect(
            p.pos_x_caja_down, p.pos_y_cajas, 31, 31))
        self.caja_down.setPixmap(QPixmap(p.color_azul))
        self.caja_down.setObjectName("caja_down")

        self.caja_right = QLabel(self.zona_flechas)
        self.caja_right.setGeometry(QRect(
            p.pos_x_caja_right, p.pos_y_cajas, 31, 31))
        self.caja_right.setPixmap(QPixmap(p.color_azul))
        self.caja_right.setObjectName("caja_right")

    #   ## PISTA BAILE
        self.pista_baile = QWidget(self)
        self.pista_baile.setGeometry(QRect(200, 140, 511, 451))

        self.fondo = QLabel(self.pista_baile)
        self.fondo.setGeometry(QRect(0, 0, p.ANCHO_PISTA_BAILE, p.ALTO_PISTA_BAILE))
        self.fondo.setPixmap(QPixmap(p.RUTA_PISTA_BAILE))
        self.fondo.setScaledContents(True)

        self.pinguirin_inicial = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_inicial.setGeometry(QRect(170, 260, 91, 91))
        self.pinguirin_inicial.setPixmap(QPixmap(p.pinguirin_amarillo))
        self.pinguirin_inicial.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_inicial)

        ## estos labels son para el drag and drop :D ##
        self.pinguirin_medio = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_medio.setGeometry(QRect(230, 260, 91, 91))
        self.pinguirin_medio.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_medio)

        self.pinguirin_derecha_medio = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_derecha_medio.setGeometry(QRect(320, 260, 91, 91))
        self.pinguirin_derecha_medio.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_derecha_medio)

        self.pinguirin_derecha_atras = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_derecha_atras.setGeometry(QRect(295, 195, 91, 91))
        self.pinguirin_derecha_atras.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_derecha_medio)

        self.pinguirin_medioderecha_adelante = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_medioderecha_adelante.setGeometry(QRect(235, 340, 91, 91))
        self.pinguirin_medioderecha_adelante.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_medioderecha_adelante)

        self.pinguirin_medioizquierda_adelante = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_medioizquierda_adelante.setGeometry(QRect(170, 340, 91, 91))
        self.pinguirin_medioizquierda_adelante.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_medioizquierda_adelante)

        self.pinguirin_izquierda_adelante = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_izquierda_adelante.setGeometry(QRect(65, 340, 91, 91))
        self.pinguirin_izquierda_adelante.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_izquierda_adelante)

        self.pinguirin_derecha_adelante = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_derecha_adelante.setGeometry(QRect(336, 340, 91, 91))
        self.pinguirin_derecha_adelante.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_derecha_adelante)

        self.pinguirin_izquierda_medio = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_izquierda_medio.setGeometry(QRect(80, 260, 91, 91))
        self.pinguirin_izquierda_medio.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_izquierda_medio)

        self.pinguirin_izquierda_atras = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_izquierda_atras.setGeometry(QRect(105, 195, 91, 91))
        self.pinguirin_izquierda_atras.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_izquierda_atras)

        self.pinguirin_medioizquierda_atras = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_medioizquierda_atras.setGeometry(QRect(178, 195, 91, 91))
        self.pinguirin_medioizquierda_atras.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_medioizquierda_atras)

        self.pinguirin_medioderecha_atras = PinguirinBaila(self.pista_baile, self)
        self.pinguirin_medioderecha_atras.setGeometry(QRect(223, 195, 91, 91))
        self.pinguirin_medioderecha_atras.setScaledContents(True)
        self.lista_pinguirines_bailando.append(self.pinguirin_medioderecha_atras)

    #   ## TIENDA
        self.tienda = QWidget(self)
        self.tienda.setGeometry(QRect(720, 140, 161, 451))
        self.tienda.setObjectName("tienda")
        self.tienda.setStyleSheet("background-color:pink;")
        self.titulo_ventana = QLabel(self.tienda)
        self.titulo_ventana.setGeometry(QRect(30, 10, 101, 21))
        self.titulo_ventana.setTextFormat(QtCore.Qt.PlainText)
        self.titulo_ventana.setAlignment(QtCore.Qt.AlignCenter)
        self.titulo_ventana.setText("TIENDA")

        self.pinguirin_morado = PinguirinTienda(self.tienda)
        self.pinguirin_morado.Geometry(10, 150, 71, 71)
        self.pinguirin_morado.Pixmap(QPixmap(p.pinguirin_morado))
        self.pinguirin_morado.setScaledContents(True)

        self.pinguirin_verde = PinguirinTienda(self.tienda)
        self.pinguirin_verde.Geometry(10, 230, 71, 71)
        self.pinguirin_verde.Pixmap(QPixmap(p.pinguirin_verde))
        self.pinguirin_verde.setScaledContents(True)

        self.pinguirin_rojo = PinguirinTienda(self.tienda)
        self.pinguirin_rojo.Geometry(90, 150, 71, 71)
        self.pinguirin_rojo.Pixmap(QPixmap(p.pinguirin_rojo))
        self.pinguirin_rojo.setScaledContents(True)

        self.pinguirin_amarillo = PinguirinTienda(self.tienda)
        self.pinguirin_amarillo.Geometry(90, 230, 71, 71)
        self.pinguirin_amarillo.Pixmap(QPixmap(p.pinguirin_amarillo))
        self.pinguirin_amarillo.setScaledContents(True)

        self.pinguirin_celeste = PinguirinTienda(self.tienda)
        self.pinguirin_celeste.Geometry(50, 310, 71, 71)
        self.pinguirin_celeste.Pixmap(QPixmap(p.pinguirin_celeste))
        self.pinguirin_celeste.setScaledContents(True)

        self.texto_dinero = QLabel(self.tienda)
        self.texto_dinero.setGeometry(QRect(10, 40, 51, 21))
        self.texto_dinero.setText("DINERO:")
        self.dinero_jugador_label = QLabel(self.tienda)
        self.dinero_jugador_label.setGeometry(QRect(70, 40, 41, 21))
        self.dinero_jugador_label.setText(str(self.dinero_jugador))
        self.texto_valor_pinguirin = QLabel(self.tienda)
        self.texto_valor_pinguirin.setGeometry(QRect(10, 120, 91, 21))
        self.texto_valor_pinguirin.setText("Valor Pingüino:")

        self.valor_pinguirin = QLabel(self.tienda)
        self.valor_pinguirin.setGeometry(QRect(110, 120, 41, 21))
        self.valor_pinguirin.setText("$500")

        self.boton_tienda_puffs = QPushButton(self.tienda)
        self.boton_tienda_puffs.setGeometry(QRect(40, 400, 91, 20))
        self.boton_tienda_puffs.setText("Puffs")
        self.boton_tienda_puffs.clicked.connect(self.abrir_tienda_puffs)

    #   ## MENUBAR
        self.menu_bar = QWidget(self)
        self.menu_bar.setGeometry(QRect(20, 20, 861, 101))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_bar.setStyleSheet("background-color:pink;")

        ## BOTON SALIR
        self.boton_salir = QtWidgets.QPushButton(self.menu_bar)
        self.boton_salir.setGeometry(QRect(740, 51, 91, 20))
        self.boton_salir.setText("Salir")
        self.boton_salir.clicked.connect(self.salir)

        ## Boton pausa
        self.boton_pausar = QtWidgets.QPushButton(self.menu_bar)
        self.boton_pausar.setGeometry(QRect(740, 11, 91, 20))
        self.boton_pausar.setText("Pausar")
        self.boton_pausar.clicked.connect(self.pausar)
        self.boton_pausar.setEnabled(False)

        ## BOTON EMPEZAR
        self.boton_empezar = QtWidgets.QPushButton(self.menu_bar)
        self.boton_empezar.setGeometry(QRect(590, 77, 120, 20))
        self.boton_empezar.setText("Empezar Juego")
        self.boton_empezar.clicked.connect(self.comenzar_juego)

        ## PROGRESO CANCION
        self.progreso_cancion = QtWidgets.QProgressBar(self.menu_bar)
        self.progreso_cancion.setGeometry(QRect(350, 10, 101, 20))
        self.progreso_cancion.setProperty("value", 0)
        self.progreso_cancion.setObjectName("progreso_cancion")
        self.texto_progreso = QLabel(self.menu_bar)
        self.texto_progreso.setGeometry(QRect(260, 10, 71, 16))
        self.texto_progreso.setText("Progreso")

        ## CANCION
        self.texto_cancion = QLabel(self.menu_bar)
        self.texto_cancion.setGeometry(QRect(510, 10, 60, 16))
        self.texto_cancion.setText("Cancion:")

        self.elegir_cancion_box = QtWidgets.QComboBox(self.menu_bar)
        self.elegir_cancion_box.setGeometry(QRect(590, 10, 111, 21))
        self.elegir_cancion_box.addItem("onichan")
        self.elegir_cancion_box.addItem("cumbia")
        self.elegir_cancion_box.setObjectName("elegir_cancion_box")

        ## DIFICULTAD
        self.texto_dificutlad = QLabel(self.menu_bar)
        self.texto_dificutlad.setGeometry(QRect(510, 50, 60, 16))
        self.texto_dificutlad.setText("Dificultad:")
        self.elegir_dificultad_box = QtWidgets.QComboBox(self.menu_bar)
        self.elegir_dificultad_box.setGeometry(QRect(590, 50, 111, 21))
        self.elegir_dificultad_box.setObjectName("elegir_dificultad_box")
        self.elegir_dificultad_box.addItem("Principiante")
        self.elegir_dificultad_box.addItem("Aficionado")
        self.elegir_dificultad_box.addItem("Maestro Cumbia")

        ## LOGO
        self.logo = QLabel(self.menu_bar)
        self.logo.setGeometry(QRect(0, 8, 91, 91))
        self.logo.setPixmap(QPixmap(p.RUTA_LOGO))
        self.logo.setScaledContents(True)

        ## APROBACION
        self.porcentaje_aprobacion = QtWidgets.QProgressBar(self.menu_bar)
        self.porcentaje_aprobacion.setGeometry(QRect(350, 50, 101, 20))
        self.porcentaje_aprobacion.setProperty("value", 0)
        self.texto_aprobacion = QLabel(self.menu_bar)
        self.texto_aprobacion.setGeometry(QRect(260, 50, 81, 16))
        self.texto_aprobacion.setText("Aprobacion")

        ## COMBOS 
        self.texto_combo = QLabel(self.menu_bar)
        self.texto_combo.setGeometry(QRect(140, 10, 51, 16))
        self.texto_combo.setText("Combo:")
        self.texto_combo_mayor = QLabel(self.menu_bar)
        self.texto_combo_mayor.setGeometry(QRect(100, 50, 91, 16))
        self.texto_combo_mayor.setText("Combo Mayor:")
        self.combo_valor_label = QLabel(self.menu_bar)
        self.combo_valor_label.setGeometry(QRect(200, 10, 21, 16))
        self.combo_valor_label.setObjectName("label")
        self.combo_mayor_valor_label = QLabel(self.menu_bar)
        self.combo_mayor_valor_label.setGeometry(QRect(200, 50, 21, 16))
        self.combo_mayor_valor_label.setObjectName("label_2")

    #
        self.timer_duracion_juego = QTimer(self)
        self.timer_duracion_juego.timeout.connect(self.termino_juego)

        self.timer_crea_flechas = QTimer(self)
        self.timer_crea_flechas.timeout.connect(self.crear_flechas)

        self.timer_emitir_teclas = QTimer(self)
        self.timer_emitir_teclas.timeout.connect(self.enviar_teclas_presionadas)
        self.timer_emitir_teclas.setInterval(100)
        self.timer_emitir_teclas.start()

        self.music_player = MusicPlayer()
        self.lista_flechas = []
        # self.show()

    def enviar_teclas_presionadas(self):
        self.senal_actualizar_bailarines.emit("neutro", self)
        self.senal_key_press.emit(self.teclas_presionadas, self)

    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            return
        else:
            if e.text() == "p":
                self.pausar()
            tecla = e.key()
            self.teclas_presionadas[tecla] = True
            
    def keyReleaseEvent(self, e):
        self.caja_left.setPixmap(QPixmap(p.color_azul))
        self.caja_up.setPixmap(QPixmap(p.color_azul))
        self.caja_right.setPixmap(QPixmap(p.color_azul))
        self.caja_down.setPixmap(QPixmap(p.color_azul))
        for tecla in list(self.teclas_presionadas.keys()):
            self.teclas_presionadas[tecla] = False

    def comenzar_juego(self):
        self.senal_inicio_juego.emit(self)

    def crear_flechas(self):
        self.senal_crear_flechas.emit(self, 10)

    def actualizar_label(self, label, x, y):
        label.move(x, y)
        self.senal_actualizar_info.emit(self)

    def pausar(self):
        self.senal_pausa.emit(self)

    def reset_settings(self):
        self.music_player.stop()
        self.timer_crea_flechas.stop()
        self.boton_pausar.setEnabled(False)
        self.boton_empezar.setEnabled(True)
        self.elegir_cancion_box.setEnabled(True)
        self.elegir_dificultad_box.setEnabled(True)
        for flecha in self.lista_flechas:
            flecha.flecha.hide()
        self.porcentaje_cancion = 0

    def salir(self):
        self.timer_duracion_juego.stop()
        self.reset_settings()
        self.hide()
        self.porcentaje_aprobacion = 0
        self.senal_volver_inicio.emit()
        
    def termino_juego(self):
        self.timer_crea_flechas.stop()
        self.timer_duracion_juego.setInterval(200)
        self.timer_duracion_juego.start()
        if self.lista_flechas[len(self.lista_flechas) - 1].isFinished() == True:
            self.timer_duracion_juego.stop()
            self.reset_settings()
            self.senal_termino_juego.emit(self)

    def abrir_tienda_puffs(self):
        self.tienda_puffs.show()