
from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox, QGridLayout
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QImage
from os.path import join
from time import sleep
from generador_grilla import GeneradorGrillaHexagonal
from os.path import join

import json

with open(join("client", "grafo.json")) as file:
    grafos = json.load(file)

with open(join("client", "parameters.json")) as file:
    p = json.load(file)


class Hexagono(QLabel):

    def __init__(self, padre, id_hexagono):
        super().__init__(parent = padre)
        self.padre = padre
        self.id_hexagono = id_hexagono
        self.nodos_adyacentes = grafos["hexagonos"][str(self.id_hexagono)]
        self.setScaledContents(True)

    def geometria(self, width_hexagonos, height_hexagonos):
        self.posicion = (p["posiciones hexagonos"][self.id_hexagono][0],
            p["posiciones hexagonos"][self.id_hexagono][1])
        self.tamano = (width_hexagonos, height_hexagonos)
        self.setGeometry(
            self.posicion[0],
            self.posicion[1],
            width_hexagonos,
            height_hexagonos
            )

    def set_material(self, lista_ficha_material):
        self.numero_ficha = lista_ficha_material[1]
        self.material = lista_ficha_material[0]
        self.padre.label_fichas_numeros[self.id_hexagono].setText(str(self.numero_ficha))
        path = p["paths"]["Materias_primas"]
        if self.material == "ARCILLA":
            self.setPixmap(QPixmap(join(
                path[0], path[1], path[2] ,"hexagono_arcilla.png")))
        elif self.material == "TRIGO":
            self.setPixmap(QPixmap(join(
                path[0], path[1], path[2], "hexagono_trigo.png")))
        elif self.material == "MADERA":
            self.setPixmap(QPixmap(join(
                path[0], path[1], path[2], "hexagono_madera.png")))

class Nodo(QLabel):

    # senal_construir_casa = pyqtSignal(str)
    def __init__(self, padre, nombre):
        super().__init__(parent = padre)
        self.padre = padre
        self.nombre_nodo = nombre
        self.habilita_compras = False
        self.setScaledContents(True)
    
    def mousePressEvent(self, event):
        if self.habilita_compras == True:
            if self.pixmap() == None:
                #HACER ALGO
                self.padre.senal_construir_casa.emit(self.nombre_nodo)
            else:
                print("usado")
        else:
            print(f"hola, soy el nodo numero {self.nombre_nodo}")

class Camino(QLabel):

    def __init__(self, padre, valor, nodos_adyacentes, tipo_camino):
        super().__init__(parent = padre)
        self.dim = p["posicion_caminos"]
        self.padre = padre
        self.nombre_nodo = valor
        self.habilita_compras = False
        self.setScaledContents(True)
        self.nodo1 = nodos_adyacentes[0]
        self.nodo2 = nodos_adyacentes[1]
        self.tipo_camino = tipo_camino
        if self.tipo_camino == 1:
            self.setGeometry(
            self.dim[self.nodo2][0] + 20,
            self.dim[self.nodo2][1] - 7,
            41, 16)
        elif self.tipo_camino == 2: 
            self.setGeometry(
            self.dim[self.nodo2][0] + 10,
            self.dim[self.nodo2][1] + 20,
            31, 41)
        elif self.tipo_camino == 3: 
            self.setGeometry(
            self.dim[self.nodo2][0] - 35,
            self.dim[self.nodo2][1] + 20,
            31, 41)
    
    def construir(self, color):
        path = p["paths"]["Construcciones"]
        if self.tipo_camino == 1:
            self.setPixmap(QPixmap(
                join(join(path[0], path[1], path[2], f"camino_{color}_0.png"))))
        elif self.tipo_camino == 2:
            self.setPixmap(QPixmap(
                join(join(path[0], path[1], path[2], f"camino_{color}_120.png"))))
        elif self.tipo_camino == 3:
            self.setPixmap(QPixmap(
                join(join(path[0], path[1], path[2], f"camino_{color}_60.png"))))

    def mousePressEvent(self, event):
        if self.habilita_compras == True:
            if self.pixmap() == None:
                print("enviando mensaje...")
                self.padre.senal_construir_camino.emit(self.nombre_nodo)
            else:
                print("usado")
        else:
            print(f"hola, soy el camino numero {self.nombre_nodo}")

class Mapa(QWidget):
    
    senal_construir_casa = pyqtSignal(str)
    senal_construir_camino = pyqtSignal(str)

    def __init__(self, parent, lista_nodos):
        super().__init__(parent)

        grilla = GeneradorGrillaHexagonal(p["arista mapa"])
        self.dimensiones = grilla.generar_grilla(
            p["dimensiones mapa"], p["padding x"], p["padding y"])
        self.info_caminos = grafos["caminos"]

        # dimensiones es un dict con llaves = "nodos" y valores una lista de la forma (x, y)
        self.posicion_hexagonos = p["posiciones hexagonos"]
        self.label_nodos = {}
        self.label_caminos = {}

        self.label_hexagonos = {}
        self.label_fichas = {}
        self.label_fichas_numeros = {}

        self.lista_nodos = lista_nodos
        self.crear_label_hexagonos()
        self.crear_labels_nodos()
        self.crear_labels_caminos()

    def crear_label_hexagonos(self):
        # 0  es x y 1 es y
        # esta resta corresponde al ancho de un hexagono
        self.width_hexagonos = self.dimensiones["5"][0] - self.dimensiones["4"][0]
        # y esta al ancho
        self.height_hexagonos = self.dimensiones["9"][1] - self.dimensiones["0"][1]
        
        for i in range(0, 10):
            label_hexagono = Hexagono(self, str(i))
            label_hexagono.geometria(self.width_hexagonos, self.height_hexagonos)
            self.label_hexagonos[str(i)] = label_hexagono
        self.crear_labels_fichas()

    def crear_labels_nodos(self):
        for nodo in self.lista_nodos:
            label = Nodo(self, nodo)
            label_width = 30
            label_height = 30
            label.setGeometry(0, 0, label_width, label_height)
            # con la resta logramos que los objetos sobre los labels se vean centrados
            label.move(
                self.dimensiones[nodo][0] - label_width/2, 
                self.dimensiones[nodo][1] - label_height/2
                )
            label.setScaledContents(True)
            
            self.label_nodos[nodo] = label

    def crear_labels_caminos(self):
        for id_camino in list(self.info_caminos.keys()):
            camino = Camino(self,
            id_camino, self.info_caminos[id_camino][:2], 
            self.info_caminos[id_camino][2])
            self.label_caminos[id_camino] = camino

    def crear_labels_fichas(self):
        for i in range(0, 10):
            label_ficha = QLabel(parent = self)
            label_ficha.setGeometry(
                self.posicion_hexagonos[str(i)][0] + self.width_hexagonos/2 - 15, 
                self.posicion_hexagonos[str(i)][1] + self.height_hexagonos/2 - 15, 
                30, 
                30)
            path = p["paths"]["Materias_primas"]
            label_ficha.setPixmap(QPixmap(
                join(path[0], path[1], path[2], "ficha_numero.png")))
            label_ficha.setScaledContents(True)
            self.label_fichas[str(i)] = label_ficha

        for i in range(0, 10):
            label_ficha_numero = QLabel(parent = self)
            label_ficha_numero.setGeometry(
                self.posicion_hexagonos[str(i)][0] + self.width_hexagonos/2 - 5, 
                self.posicion_hexagonos[str(i)][1] + self.height_hexagonos/2 - 15, 
                30, 
                30)
            self.label_fichas_numeros[str(i)] = label_ficha_numero

    def cargar_materiales(self, lista_material_y_ficha):
        for hexagon in list(self.label_hexagonos.values()):
            hexagon.set_material(lista_material_y_ficha.pop(0))


class Boton(QWidget):
    '''
        Esta clase sirve para los labels con los que el usuario debe interactuar
    '''
    senal_comprar_objeto = pyqtSignal(str)
    def __init__(self, padre, compra):
        super().__init__(parent = padre)
        self.padre = padre
        self.compra = compra
        self.label_imagen = QLabel(self)
        if self.compra == "CHOZA":
            self.label_imagen.setGeometry(QRect(20, 20, 61, 61))
            path = p["paths"]["Construcciones"]
            self.label_imagen.setPixmap(QPixmap(
                join(path[0], path[1], path[2], "choza_azul.png")))
        elif self.compra == "CARTA_DESARROLLO":
            self.label_imagen.setGeometry(QRect(10, 10, 61, 81))
            path = p["paths"]["carta_reverso"]
            self.label_imagen.setPixmap(QPixmap(
                join(path[0], path[1], path[2], path[3])))
        elif self.compra == "CAMINO":
            self.label_imagen.setGeometry(QRect(10, 40, 81, 21))
            path = p["paths"]["Construcciones"]
            self.label_imagen.setPixmap(QPixmap(
                join(path[0], path[1], path[2], "camino_azul_0.png")))
        self.label_imagen.setScaledContents(True)

    def mousePressEvent(self, event):
        self.senal_comprar_objeto.emit(self.compra)

class WidgetInfo(QWidget):

    def __init__(self, padre, dim, tipo):
        super().__init__(parent = padre)
        if tipo == 0:
            self.setGeometry(dim[0], dim[1], dim[2], dim[3])
            self.nombre = QLabel(self)
            self.nombre.setGeometry(QRect(10, 10, 100, 16))
            self.nombre.setText("")
            self.puntos = QLabel(self)
            self.puntos.setGeometry(QRect(80, 50, 81, 16))
            self.puntos.setText(f"Puntos: {2}")
            self.carta_desarrolo = QLabel(self)
            self.carta_desarrolo.setGeometry(QRect(10, 40, 31, 41))
            path = p["paths"]["carta_reverso"]
            self.carta_desarrolo.setPixmap(QPixmap(
                join(path[0], path[1], path[2], path[3])
            ))
            self.carta_desarrolo.setScaledContents(True)

        elif tipo == 1:
            self.usuario = None
            self.setGeometry(dim[0], dim[1], dim[2], dim[3])    
            self.nombre = QLabel(self)
            self.nombre.setGeometry(QRect(10, 10, 100, 16))
            self.nombre.setText("no hay jugador")
            self.puntos = QLabel(self)
            self.puntos.setGeometry(QRect(100, 10, 60, 16))
            self.puntos.setText(f"Puntos: {2}")
            self.widget_cartas = QWidget(self)
            self.widget_cartas.setGeometry(QRect(0, 40, 191, 61))
            self.arcilla = QLabel(self.widget_cartas)
            self.arcilla.setGeometry(QRect(10, 10, 31, 41))
            path = p["paths"]["arcilla"]
            self.arcilla.setPixmap(QPixmap(
                join(path[0], path[1], path[2], path[3])
            ))
            self.arcilla.setScaledContents(True)
            self.madera = QLabel(self.widget_cartas)
            self.madera.setGeometry(QRect(130, 10, 31, 41))
            path = p["paths"]["madera"]
            self.madera.setPixmap(QPixmap(
                join(path[0], path[1], path[2], path[3])
            ))
            self.madera.setScaledContents(True)
            self.trigo = QLabel(self.widget_cartas)
            self.trigo.setGeometry(QRect(70, 10, 31, 41))
            path = p["paths"]["trigo"]
            self.madera.setPixmap(QPixmap(
                join(path[0], path[1], path[2], path[3])
            ))
            self.trigo.setScaledContents(True)
            self.cantidad_arcilla = QLabel(self.widget_cartas)
            self.cantidad_arcilla.setGeometry(QRect(50, 20, 21, 16))
            self.cantidad_arcilla.setText("0")
            self.cantidad_madera = QLabel(self.widget_cartas)
            self.cantidad_madera.setGeometry(QRect(110, 20, 21, 16))
            self.cantidad_madera.setText("0")
            self.cantidad_trigo = QLabel(self.widget_cartas)
            self.cantidad_trigo.setGeometry(QRect(170, 20, 21, 16))
            self.cantidad_trigo.setText("0")

    def definir_usuario(self, usuario):
        self.usuario = usuario
        self.nombre.setText(usuario)

    def actualizar_cantidades(self, estado_usuario):
        pass