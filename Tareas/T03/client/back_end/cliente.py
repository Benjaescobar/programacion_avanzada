from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox, QGridLayout
)
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QRect, QThread, QTimer, QMimeData
from PyQt5.QtGui import QPixmap, QDrag, QPainter, QImage
from os.path import join

import string
import random
import threading
import socket
import json

with open(join("client", "parameters.json")) as file:
    parametros = json.load(file)

class Cliente(QObject):

    update_screen = pyqtSignal(str)
    senal_nombres_usuario = pyqtSignal(list, str)
    senal_empezar_juego = pyqtSignal()
    senal_actualizar_dados = pyqtSignal(int, int)
    senal_cargar_mapa = pyqtSignal(list)
    senal_turno = pyqtSignal(bool, list)
    senal_actualizar_mapa = pyqtSignal(list, str)
    senal_cargar_usuarios = pyqtSignal(list)
    senal_terminar_juego = pyqtSignal(str)

    senal_actualizar_usuarios = pyqtSignal(dict, list, str)

    def __init__(self, port, host):
        super().__init__()

        print('Creando cliente')
        self.port = port
        self.host = host
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = 'User' + ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6))
        self.turno = True
        try:
            self.connect_to_server()
            self.initBackend()
            self.listen()
        except ConnectionError:
            print('Conexion terminada')
            self.socket_cliente.close()
            self.isConnected = False
            exit()

    def initBackend(self):
        self.isConnected = True
        self.send(self.username, "AGREGAR USUARIO")

    def send(self, data, accion):
        if self.turno == True:
            msg = {
                "user": self.username,
                "data": data, 
                "accion": accion
                }

            json_msg = json.dumps(msg)
            msg_in_bytes = json_msg.encode()

            largo = len(msg_in_bytes)

            mensaje_entero = bytearray()
            mensaje_entero += largo.to_bytes(4, byteorder='big')

            for modulo in range(largo//60 + 1):
                mensaje_entero += modulo.to_bytes(4, byteorder='little')
                largo_restante = len(msg_in_bytes)
                if largo_restante >= 60:
                    mensaje_entero += msg_in_bytes[:60]
                    msg_in_bytes = msg_in_bytes[60:]
                else:
                    mensaje_entero += msg_in_bytes[:largo_restante]
                    bytes_cero_restantes = bytearray(60 - largo_restante)
                    mensaje_entero += bytes_cero_restantes
                    break

            print("Enviando mensaje a servidor...")
            self.socket_cliente.send(mensaje_entero)

    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print('Cliente conectado a servidor')

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        self.max_recv = 2**16
        while True:
            largo_archivo = int.from_bytes(
                self.socket_cliente.recv(4), byteorder='big')
            if largo_archivo > self.max_recv:
                largo_archivo = self.max_recv
            bytes_leidos = bytearray()
            while len(bytes_leidos) < largo_archivo:
                modulo = int.from_bytes(
                self.socket_cliente.recv(4), byteorder='little')
                respuesta = self.socket_cliente.recv(60)
                bytes_leidos += respuesta
            
            bytes_importantes = bytes_leidos[:largo_archivo]
            self.decode_data(bytes_importantes)

    def decode_data(self, data_bytes):
        # data = json.loads(data_bytes)
        data_decode = data_bytes.decode()
        data = json.loads(data_decode)
        print("Decodificando data...")
        sala_actual = data["ventana"]
        data_recibida = data["data"]
        accion = data["accion"]

        if sala_actual == "sala de espera":
            if accion == "CARGAR USUARIOS":
                self.usuarios = list(data_recibida.keys())
                self.senal_nombres_usuario.emit(self.usuarios, self.username)

            elif accion == "empezar juego":
                
                print("INICIANDO JUEGO")
                self.senal_empezar_juego.emit()
                self.senal_cargar_usuarios.emit(self.usuarios)

        elif sala_actual == "sala de juego":
            if accion == "DADO":
                self.senal_actualizar_dados.emit(data_recibida[0], data_recibida[1])
            
            if accion == "TURNO":
                if data_recibida[0] == self.username:
                    self.turno = True
                else:
                    self.turno = False
                    
                self.senal_turno.emit(self.turno, data_recibida)

            elif accion == "CARGAR MAPA":
                self.senal_cargar_mapa.emit(data_recibida)

            elif accion == "NUEVO MATERIAL":
                self.senal_actualizar_usuarios.emit(data_recibida, self.usuarios, self.username)

            elif accion == "AGREGAR CHOZA":
                self.senal_actualizar_mapa.emit(data_recibida, "CHOZA")

            elif accion == "AGREGAR CAMINO":
                self.senal_actualizar_mapa.emit(data_recibida, "CAMINO")

            elif accion == "TERMINAR JUEGO":
                self.senal_terminar_juego.emit(data_recibida)

    def request_construir_casa(self, nodo):
        if self.turno == True:
            self.send(nodo, "COMPRAR CHOZA")
        else:
            print("no es tu turno")
    
    def request_construir_camino(self, nodo):
        if self.turno == True:
            self.send(nodo, "COMPRAR CAMINO")
        else:
            print("no es tu turno")

    def terminar_turno(self):
        self.send(None, "TERMINAR TURNO")

    def lanzar_dado(self):
        # esta funcion se activa con un boton de sala_de_juego.py y el dado se lanza en el servidor
        # por lo que simplemente no pasara nada si no es tu turno
        if self.turno == True:
            self.send(self.username, "LANZAR DADO")
        else:
            print("NO ES TU TURNO")

        