import os

from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication
)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap


class VentanaInicial(QWidget):

    senal_comparar_codigo = pyqtSignal(str)
    senal_abrir_menu_principal = pyqtSignal()

    def __init__(self, ancho, alto, ruta_logo):
        """Es el init de la ventana del menú de inicio. Puedes ignorarlo."""
        super().__init__()
        self.size = (ancho, alto)
        self.resize(ancho, alto)
        self.init_gui(ruta_logo)

    def init_gui(self, ruta_logo):
        # Completar
        self.setGeometry(200, 100, self.size[0], self.size[1]+100)
        self.setWindowTitle('Among us')

        # IMAGEN
        self.imagen = QLabel(self)
        self.imagen.setGeometry(0, 0, self.size[0], self.size[1])

        pixeles = QPixmap(ruta_logo)

        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)
        
        ####
        #### input codigo
        self.texto = QLabel('Ingrese un codigo:', self)
        self.texto.move(self.size[0] - int(2*self.size[0]/3), self.size[1]+20)

        self.input_codigo = QLineEdit('', self)
        self.input_codigo.setGeometry(self.size[0] - int(3*self.size[0]/7), self.size[1]+20, 200, 20)
        self.input_codigo.setPlaceholderText("debe ser uno existente")

        self.boton1 = QPushButton('&Ingresar', self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.move(self.size[0] - int(self.size[0]/2) - 50, self.size[1]+40)
        self.boton1.clicked.connect(self.comparar_codigo)
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.texto)
        hbox.addWidget(self.input_codigo)
        hbox.addWidget(self.boton1)
        hbox.addStretch(1)

        self.show()

    def comparar_codigo(self):
        """Método que emite la señal para comparar el código. Puedes ignorarlo.
        Recuerda que el QLineEdit debe llamarse 'input_codigo'"""
        codigo = self.input_codigo.text()
        self.senal_comparar_codigo.emit(codigo)

    def recibir_comparacion(self, son_iguales):
        """Método que recibe el resultado de la comparación. Puedes ignorarlo.
        Recuerda que el QLineEdit debe llamarse 'input_codigo'"""
        if not son_iguales:
            self.input_codigo.clear()
            self.input_codigo.setPlaceholderText("¡Inválido! Debe ser un código existente.")
        else:
            self.hide()
            self.senal_abrir_menu_principal.emit()