from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox, QGridLayout
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QImage
from os.path import join
from front_end.tablero import Mapa, Boton, WidgetInfo
from os.path import join

import json
with open(join("client", "parameters.json")) as file:
    parametros = json.load(file)

class SalaJuego(QWidget):

    senal_lanzar_dado = pyqtSignal()
    senal_terminar_turno = pyqtSignal()
    senal_terminar_juego = pyqtSignal(str)

    def __init__(self, lista_nodos):
        super().__init__()
        self.widget_size = (parametros["dimensiones_sala_juego"][0],
            parametros["dimensiones_sala_juego"][1])
        self.lista_nodos = lista_nodos
        self.__initgui__()
        
    def __initgui__(self):
        self.resize(1073, 649)

        self.widget_principal = QWidget(self)

        self.widget_principal.setGeometry(QRect(10, 10, 1051, 631))
        self.widget_principal.setObjectName("widget_principal")

        self.widget_mapa = Mapa(self.widget_principal, self.lista_nodos)
        self.widget_mapa.setGeometry(QRect(10, 10, 661, 501))

    ## CARTAS
        self.widget_cartas = QWidget(self.widget_principal)
        self.widget_cartas.setGeometry(QRect(10, 520, 371, 101))
        self.widget_cartas.setStyleSheet("background-color: grey;")

        self.arcilla = QLabel(self.widget_cartas)
        self.arcilla.setGeometry(QRect(10, 10, 61, 81))
        path = parametros["paths"]["arcilla"]
        self.arcilla.setPixmap(QPixmap(join(
            path[0], path[1], path[2], path[3])))
        self.arcilla.setScaledContents(True)
        self.cantidad_arcilla = QLabel(self.widget_cartas)
        self.cantidad_arcilla.setGeometry(QRect(80, 40, 31, 16))
        self.cantidad_arcilla.setText("0")
        self.madera = QLabel(self.widget_cartas)
        self.madera.setGeometry(QRect(130, 10, 61, 81))
        path = parametros["paths"]["madera"]
        self.madera.setPixmap(QPixmap(join(
            path[0], path[1], path[2], path[3])))
        self.madera.setScaledContents(True)
        self.cantidad_madera = QLabel(self.widget_cartas)
        self.cantidad_madera.setGeometry(QRect(200, 40, 31, 16))
        self.cantidad_madera.setText("0")
        self.trigo = QLabel(self.widget_cartas)
        self.trigo.setGeometry(QRect(250, 10, 61, 81))
        path = parametros["paths"]["trigo"]
        self.trigo.setPixmap(QPixmap(join(path[0], path[1], path[2], path[3])))
        self.trigo.setScaledContents(True)
        self.cantidad_trigo = QLabel(self.widget_cartas)
        self.cantidad_trigo.setGeometry(QRect(320, 40, 31, 16))
        self.cantidad_trigo.setText("0")

    ## Cosas para comprar

        self.widget_intercambio = QWidget(self.widget_principal)
        self.widget_intercambio.setGeometry(QRect(720, 520, 101, 101))
        self.widget_intercambio.setStyleSheet("background-color: grey;")
        self.intercambio = QLabel(self.widget_intercambio)
        self.intercambio.setGeometry(QRect(20, 20, 61, 61))
        path = parametros["paths"]["intercambio"]
        self.intercambio.setPixmap(QPixmap(join(
            path[0], path[1], path[2], path[3])))
        self.intercambio.setScaledContents(True)

        self.widget_camino = Boton(self.widget_principal, "CAMINO")
        self.widget_camino.setGeometry(QRect(500, 520, 101, 101))
        self.widget_camino.setStyleSheet("background-color: grey;")
        self.widget_camino.senal_comprar_objeto.connect(self.modo_comprar)
        
        self.widget_carta_desarrollo = Boton(self.widget_principal, "CARTA_DESARROLLO")
        self.widget_carta_desarrollo.setGeometry(QRect(610, 520, 101, 101))
        self.widget_carta_desarrollo.setStyleSheet("background-color: grey;")
        self.widget_carta_desarrollo.senal_comprar_objeto.connect(self.modo_comprar)

        self.widget_choza = Boton(self.widget_principal, "CHOZA")
        self.widget_choza.setGeometry(QRect(390, 520, 101, 101))
        self.widget_choza.setStyleSheet("background-color: grey;")
        self.widget_choza.senal_comprar_objeto.connect(self.modo_comprar)

    ## INFO PARTIDA
        self.widget_informacion_partida = QWidget(self.widget_principal)
        self.widget_informacion_partida.setGeometry(QRect(830, 10, 211, 611))
        self.widget_informacion_partida.setObjectName("widget_informacion_partida")
        self.widget_informacion_partida.setStyleSheet("background-color: grey;")
        self.turno_actual_texto = QLabel(self.widget_informacion_partida)
        self.turno_actual_texto.setGeometry(QRect(20, 20, 61, 21))
        self.turno_actual_texto.setText("Turno de")
        self.turno_actual = QLabel(self.widget_informacion_partida)
        self.turno_actual.setGeometry(QRect(85, 20, 110, 21))
        self.turno_actual.setText("")

        self.carretera_larga_texto = QLabel(self.widget_informacion_partida)
        self.carretera_larga_texto.setGeometry(10, 430, 191, 16)
        self.carretera_larga_texto.setText("Carretera mas larga:")

        self.carretera_mas_larga = QLabel(self.widget_informacion_partida)
        self.carretera_mas_larga.setGeometry(10, 450, 191, 16)
        self.carretera_mas_larga.setText("")

        dim = [20, 490, 191, 91]
        self.widget_propio = WidgetInfo(self.widget_informacion_partida, dim, 0)

        dim = parametros["posicion informacion jugadores"]["0"]
        self.widget_jugador_1 = WidgetInfo(self.widget_informacion_partida, dim, 1)
        dim = parametros["posicion informacion jugadores"]["1"]
        self.widget_jugador_2 = WidgetInfo(self.widget_informacion_partida, dim, 1)
        dim = parametros["posicion informacion jugadores"]["2"]
        self.widget_jugador_3 = WidgetInfo(self.widget_informacion_partida, dim, 1)
        
        self.info_jugadores = {
            "0": self.widget_jugador_1,
            "1": self.widget_jugador_2,
            "3": self.widget_jugador_3
        }

    ## DADOS
        self.widget_dados = QWidget(self.widget_principal)
        self.widget_dados.setGeometry(QRect(680, 390, 141, 121))
        self.dado_1 = QLabel(self.widget_dados)
        self.dado_1.setGeometry(QRect(10, 60, 51, 51))
        path = parametros["paths"]["dado_1"]
        self.dado_1.setPixmap(QPixmap(join(path[0], path[1], path[2], path[3])))
        self.dado_1.setScaledContents(True)
        self.dado_2 = QLabel(self.widget_dados)
        self.dado_2.setGeometry(QRect(80, 60, 51, 51))
        path = parametros["paths"]["dado_2"]
        self.dado_2.setPixmap(QPixmap(join(path[0], path[1], path[2], path[3])))
        self.dado_2.setScaledContents(True)
        self.boton_lanzar_dado = QPushButton(self.widget_dados)
        self.boton_lanzar_dado.setGeometry(QRect(10, 10, 121, 32))
        self.boton_lanzar_dado.setText("Lanzar dado")
        self.boton_lanzar_dado.clicked.connect(self.lanzar_dado)

        self.widget_terminar_turno = QWidget(self.widget_principal)
        self.widget_terminar_turno.setGeometry(QRect(680, 330, 141, 34))
        self.boton_terminar_turno = QPushButton(self.widget_terminar_turno)
        self.boton_terminar_turno.setGeometry(QRect(10, 10, 121, 32))
        self.boton_terminar_turno.setText("Terminar Turno")
        self.boton_terminar_turno.clicked.connect(self.terminar_turno)
        self.boton_terminar_turno.setEnabled(False)

    def modo_comprar(self, compra):
        if compra == "CHOZA":
            for nodo in list(self.widget_mapa.label_nodos.values()):
                nodo.habilita_compras = True
        elif compra == "CAMINO":
            for nodo in list(self.widget_mapa.label_caminos.values()):
                nodo.habilita_compras = True
        elif compra == "CARTA_DESARROLLO":
            pass
    
    def crear_usuarios(self, usuarios):
        pass
        # for i in range(2):
        #     widget = QWidget(self.widget_informacion_partida)
        #     dim = parametros["posicion informacion jugadores"][str(i)]
        #     widget.setGeometry(dim[0], dim[1], dim[2], dim[3])
        #     nombre = QLabel(widget)
        #     nombre.setGeometry(QRect(10, 10, 100, 16))
        #     nombre.setText(usuarios[i])
        #     puntos = QLabel(widget)
        #     puntos.setGeometry(QRect(100, 10, 60, 16))
        #     puntos.setText(f"Puntos: {2}")
        #     widget_cartas = QWidget(widget)
        #     widget_cartas.setGeometry(QRect(0, 40, 191, 61))
        #     arcilla = QLabel(widget_cartas)
        #     arcilla.setGeometry(QRect(10, 10, 31, 41))
        #     arcilla.setPixmap(QPixmap("client/sprites/Materias_primas/carta_arcilla.png"))
        #     arcilla.setScaledContents(True)
        #     madera = QLabel(widget_cartas)
        #     madera.setGeometry(QRect(130, 10, 31, 41))
        #     madera.setPixmap(QPixmap("client/sprites/Materias_primas/carta_madera.png"))
        #     madera.setScaledContents(True)
        #     trigo = QLabel(widget_cartas)
        #     trigo.setGeometry(QRect(70, 10, 31, 41))
        #     trigo.setPixmap(QPixmap("client/sprites/Materias_primas/carta_trigo.png"))
        #     trigo.setScaledContents(True)
        #     cantidad_arcilla = QLabel(widget_cartas)
        #     cantidad_arcilla.setGeometry(QRect(50, 20, 21, 16))
        #     cantidad_arcilla.setText("0")
        #     cantidad_madera = QLabel(widget_cartas)
        #     cantidad_madera.setGeometry(QRect(110, 20, 21, 16))
        #     cantidad_madera.setText("0")
        #     cantidad_trigo = QLabel(widget_cartas)
        #     cantidad_trigo.setGeometry(QRect(170, 20, 21, 16))
        #     cantidad_trigo.setText("0")
        #     self.info_jugadores[usuarios[i]] = {
        #         "WIDGET": widget,
        #         "NOMBRE": nombre,
        #         "PUNTOS": puntos,
        #         "WIDGET CARTAS": widget_cartas,
        #         "LABELS": [arcilla, madera, trigo],
        #         "CANTIDAD ARCILLA": cantidad_arcilla,
        #         "CANTIDAD MADERA": cantidad_madera,
        #         "CANTIDAD TRIGO": cantidad_trigo
        #     }
        # self.show()

    def terminar_turno(self):
        self.senal_terminar_turno.emit()
        self.boton_terminar_turno.setEnabled(False)

    def lanzar_dado(self):
        self.senal_lanzar_dado.emit()
        self.boton_lanzar_dado.setEnabled(False)
        self.boton_terminar_turno.setEnabled(True)

    ## ACTUALIZAR INTERFAZ
    def comprar(self):
        pass

    def actualizar_usuarios(self, estado_usuarios, usuarios, self_user):
        self.usuario = self_user
        
        self.cantidad_arcilla.setText(
            str(estado_usuarios[self_user]["MATERIALES"]["ARCILLA"]))
        self.cantidad_madera.setText(
            str(estado_usuarios[self_user]["MATERIALES"]["MADERA"]))
        self.cantidad_trigo.setText(
            str(estado_usuarios[self_user]["MATERIALES"]["TRIGO"]))
        self.widget_propio.nombre.setText(self_user)
        self.widget_propio.puntos.setText(
            "Puntos: " + str(estado_usuarios[self_user]["PUNTOS_VICTORIA"]))
        contador = 0
        for i in range(len(usuarios)):
            if estado_usuarios[usuarios[i]]["CAMINO_MAS_LARGO_BOOL"] == True:
                self.carretera_mas_larga.setText(usuarios[i])
            if self_user == usuarios[i]:
                continue
            else:
                jugador = self.info_jugadores[str(contador)]
                jugador.nombre.setText(usuarios[i])
                jugador.puntos.setText(
                    str(estado_usuarios[usuarios[i]]["PUNTOS_VICTORIA"]))
                jugador.cantidad_arcilla.setText(
                    str(estado_usuarios[usuarios[i]]["MATERIALES"]["ARCILLA"]))
                jugador.cantidad_madera.setText(
                    str(estado_usuarios[usuarios[i]]["MATERIALES"]["MADERA"]))
                jugador.cantidad_trigo.setText(
                    str(estado_usuarios[usuarios[i]]["MATERIALES"]["TRIGO"]))

    def actualizar_mapa(self, dato, accion):
        # La accion es lo que se debe agregar, y el dato es una lista con el color (indice 0) y
        # la llave de la compra a realizar (indice 1)
        if accion == "CHOZA":
            print("agregando choza")
            path = parametros["paths"]["Construcciones"]
            self.widget_mapa.label_nodos[dato[1]].setPixmap(QPixmap(
                join(path[0], path[1], path[2], f"choza_{dato[0]}")))
            for nodo in list(self.widget_mapa.label_nodos.values()):
                nodo.habilita_compras = False
        elif accion == "CAMINO":
            print("agregando camino")
            self.widget_mapa.label_caminos[dato[1]].construir(dato[0])
            for nodo in list(self.widget_mapa.label_caminos.values()):
                nodo.habilita_compras = False

    def actualizar_dados(self, dado1, dado2):
        path = parametros["paths"][f"dado_{dado1}"]
        self.dado_1.setPixmap(QPixmap(join(path[0], path[1], path[2], path[3])))
        path = parametros["paths"][f"dado_{dado2}"]
        self.dado_2.setPixmap(QPixmap(join(path[0], path[1], path[2], path[3])))

    def cargar_mapa(self, material_hexagonos):
        print("Cargando mapa...")
        self.widget_mapa.cargar_materiales(material_hexagonos)

    def usar_turno(self, turno, nombre_color):
        self.turno = turno
        self.boton_lanzar_dado.setEnabled(turno)
        if nombre_color[0] == self.usuario:
            self.turno_actual.setText(nombre_color[0] + " (Tú)")
        else:
            self.turno_actual.setText(nombre_color[0])
        if nombre_color[1] == "azul":
            self.turno_actual.setStyleSheet("color: blue;")
        elif nombre_color[1] == "verde":
            self.turno_actual.setStyleSheet("color: green;")
        elif nombre_color[1] == "roja":
            self.turno_actual.setStyleSheet("color: red;")

    def terminar_juego(self, usuario_ganador):
        self.senal_terminar_juego.emit(usuario_ganador)
        self.hide()