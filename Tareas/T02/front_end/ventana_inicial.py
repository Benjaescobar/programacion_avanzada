import os
import sys
import parametros as p

from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox
)
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap

class MisSenales(QObject):

    senal_comenzar_juego = pyqtSignal()


class VentanaInicial(QWidget):

    ## SEÑALES
    senal_comenzar_juego = pyqtSignal()
    senal_nombre_usuario = pyqtSignal(str)
    senal_abrir_ranking = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.size = (p.ANCHO_VENTANA_INICIAL, p.ALTO_VENTANA_INICIAL)
        self.ruta_logo = p.RUTA_LOGO
        ## ALERTA
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("EL NOMBRE DEBE SER ALFANUMERICO")
        self.msg.setInformativeText("intentelo de nuevo")
        self.msg.setStandardButtons(QMessageBox.Ok)

        ## INICIALIZAR VENTANA
        self.init_gui()

    def init_gui(self):
        # Completar
        self.setGeometry(200, 100, self.size[0], self.size[1]+100)
        self.setWindowTitle('Baila pingüino')

        # IMAGEN
        self.imagen = QLabel(self)
        self.imagen.setGeometry(0, 0, self.size[0], self.size[1])

        pixeles = QPixmap(self.ruta_logo)

        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)
        ####
        #### input codigo
        self.texto = QLabel('Ingresa el nombre de tu bailarin', self)

        self.input_nombre = QLineEdit('', self)
        self.input_nombre.setGeometry(0, 0, 200, 20)
        self.input_nombre.setPlaceholderText("alfanumerico")

        self.boton1 = QPushButton('&Comenzar', self)
        self.boton1.resize(self.boton1.sizeHint())

        self.boton1.clicked.connect(self.comenzar_juego)

        self.boton2 = QPushButton('&Ver Ranking', self)
        self.boton2.resize(self.boton1.sizeHint())
        self.boton2.clicked.connect(self.abrir_ranking)


        ## ESTO PERMITE QUE LOS BOTONES ESTEN ALINEADOS
        botones_box = QHBoxLayout()
        botones_box.addStretch(1)
        botones_box.addWidget(self.boton1)
        botones_box.addWidget(self.boton2)
        botones_box.addStretch(1)

        ## ESTO PERMITE QUE TODOS LOS WIDGETS SE ORDENEN VERTICALMENTE

        vbox = QVBoxLayout()
        vbox.addStretch(5)
        vbox.addWidget(self.imagen)
        vbox.addWidget(self.texto)
        vbox.addWidget(self.input_nombre)
        vbox.addLayout(botones_box)
        vbox.addStretch(1)

        ## PARA QUE LOS WIDGETS NO SE ADAPTEN A TODA LA VENTANA SI ESTA CRECE

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

        self.show()

    def abrir_ranking(self):
        self.senal_abrir_ranking.emit()

    def comenzar_juego(self):
        ## CHECKEA Q EL NOMBRE SEA CORRECTO, SI LO ES, EMITE UNA SEÑAL.
        if self.input_nombre.text().isalnum():
            self.hide()
            self.senal_comenzar_juego.emit()
            self.senal_nombre_usuario.emit(self.input_nombre.text())
            self.input_nombre.setText("")
        else:
            self.input_nombre.setText("")
            self.msg.show()
        


if __name__ == '__main__':
    app = QApplication([])
    senales = MisSenales()
    senal = MisSenales.senal_comenzar_juego
    path = os.path.join("sprites", "logo.png")
    ventana = VentanaInicial()
    sys.exit(app.exec_())