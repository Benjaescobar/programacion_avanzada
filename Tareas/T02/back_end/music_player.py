import PyQt5
import parametros as p
import sys

from os.path import join
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep
#from back_end.logica_ventanas import VentanaJuegoLogica
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget
from PyQt5.QtCore import QRect, pyqtSignal, QObject, QTimer, QThread, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect


class MusicPlayer(QObject):

    def __init__(self):
        self.player = QSoundEffect()

    def play_music(self, cancion):
        if cancion == "onichan":
            sound_file = p.cancion1
            self.player.setSource(QtCore.QUrl.fromLocalFile(sound_file))
            self.player.setVolume(50)
        elif cancion == "cumbia":
            sound_file = p.cancion2
            self.player.setSource(QtCore.QUrl.fromLocalFile(sound_file))
            self.player.setVolume(50)
        else:
            sound_file = p.cancion2
            self.player.setSource(QtCore.QUrl.fromLocalFile(sound_file))
            self.player.setVolume(50)

        self.play()

    def stop(self):
        self.player.stop()
    
    def play(self):
        self.player.play()