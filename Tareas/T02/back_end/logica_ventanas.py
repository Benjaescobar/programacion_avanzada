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
from back_end.flechas import Flecha, PinguirinBaila, PinguirinTienda
from back_end.funciones import crear_flechas_prob, cambiar_color_caja, chequear_teclas

class VentanaInicialLogica(QObject):
    pass

class VentanaResumenLogica(QObject):

    def escribir_ranking(self, puntaje, usuario):
        
        with open("ranking.txt", "a") as resultados:
            resultados.write(usuario + ", "+ str(puntaje) + "\n")

    def termino_juego(self, ventana_juego, ventana_termino):
        if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
            ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
        combo = ventana_juego.combo_mayor_valor
        # el contador de flechas ya cuenta el tipo de flecha con su respectivo ponderador.
        suma_flechas = ventana_juego.contador_flechas_atrapadas
        ventana_juego.puntaje = combo*suma_flechas*p.PUNTOS_FLECHA
        ventana_termino.puntaje_obtenido.setText(str(ventana_juego.puntaje))
        ventana_termino.puntaje_acumulado += ventana_juego.puntaje
        ventana_termino.puntaje_acumulado_label.setText(str(ventana_termino.puntaje_acumulado))
        ventana_termino.maximo_combo.setText(str(combo)+"X")
        ventana_termino.pasos_fallados.setText(str(ventana_juego.pasos_incorrectos))
        ventana_termino.porcentaje_aprobacion.setText(str(ventana_juego.aprobacion)+"%")
        ventana_juego.combo_mayor_valor = 0
        ventana_juego.combo_valor = 0
        if ventana_juego.aprobacion >= ventana_juego.aprobacion_necesaria:
            ventana_juego.dinero_jugador += int(ventana_juego.puntaje)
            ventana_juego.dinero_jugador_label.setText(str(ventana_juego.dinero_jugador))
            ventana_termino.texto_decision_jurado.setText("Pasaste! el jurado te aprobo :D")
            ventana_termino.ronda +=1
            ventana_termino.boton_continuar.show()
        else:
            texto = "El jurado decidio que no pasaras esta vez :(, chaooo"
            ventana_termino.texto_decision_jurado.setText(texto)
            ventana_juego.dinero_jugador = p.DINERO_INICIAL_JUGADOR
            ventana_juego.dinero_jugador_label.setText(str(ventana_juego.dinero_jugador))
            ventana_termino.boton_continuar.hide()

        ventana_juego.porcentaje_cancion = 0
        ventana_juego.progreso_cancion.setProperty("value", ventana_juego.porcentaje_cancion)
        ventana_juego.aprobacion = 0
        ventana_juego.porcentaje_aprobacion.setProperty("value", ventana_juego.aprobacion)
        ventana_juego.puntaje = 0

        ventana_juego.pinguirin_morado.habilitar_tienda(True)
        ventana_juego.pinguirin_rojo.habilitar_tienda(True)
        ventana_juego.pinguirin_verde.habilitar_tienda(True)
        ventana_juego.pinguirin_celeste.habilitar_tienda(True)
        ventana_juego.pinguirin_amarillo.habilitar_tienda(True)

        ventana_juego.pasos_correctos = 0 
        ventana_juego.pasos_incorrectos = 0
        ventana_termino.show()
        ventana_juego.hide()

class VentanaJuegoLogica(QObject):
    senal_reproducir_musica = pyqtSignal(str)
    senal_reproducir_flechas = pyqtSignal(int)
    senal_flecha_hielo = pyqtSignal(object)
    duracion_juego = 1

    def comenzar_juego(self, ventana_juego):
        cancion = ventana_juego.elegir_cancion_box.currentText()
        ventana_juego.elegir_cancion_box.setEnabled(False)
        ventana_juego.music_player.play_music(cancion)

        ventana_juego.pinguirin_morado.habilitar_tienda(False)
        ventana_juego.pinguirin_rojo.habilitar_tienda(False)
        ventana_juego.pinguirin_verde.habilitar_tienda(False)
        ventana_juego.pinguirin_celeste.habilitar_tienda(False)
        ventana_juego.pinguirin_amarillo.habilitar_tienda(False)

        dificultad = ventana_juego.elegir_dificultad_box.currentText()
        ventana_juego.elegir_dificultad_box.setEnabled(False)
        ventana_juego.boton_empezar.setEnabled(False)
        ventana_juego.boton_pausar.setEnabled(True)
        ventana_juego.ispausa = False

        self.dificultad = dificultad
        if dificultad == "Principiante":
            ventana_juego.aprobacion_necesaria = p.PRINCIPIANTE_APROBACION*100
            ventana_juego.timer_crea_flechas.setInterval(p.PRINCIPIANTE_GENERAFLECHAS)
            ventana_juego.timer_duracion_juego.setInterval(p.PRINCIPIANTE_DURACION)
            self.duracion_juego = ventana_juego.timer_duracion_juego.interval()

        elif dificultad == "Aficionado":
            ventana_juego.aprobacion_necesaria = p.AFICIONADO_APROBACION*100
            ventana_juego.timer_crea_flechas.setInterval(p.AFICIONADO_GENERAFLECHAS)
            ventana_juego.timer_duracion_juego.setInterval(p.AFICIONADO_DURACION)
            self.duracion_juego = ventana_juego.timer_duracion_juego.interval()
        
        elif dificultad == "Maestro Cumbia":
            ventana_juego.aprobacion_necesaria = p.MAESTRO_APROBACION*100
            ventana_juego.timer_crea_flechas.setInterval(p.MAESTRO_GENERAFLECHAS)
            ventana_juego.timer_duracion_juego.setInterval(p.MAESTRO_DURACION)
            self.duracion_juego = ventana_juego.timer_duracion_juego.interval()

        ventana_juego.crear_flechas()
        ventana_juego.timer_duracion_juego.start()
        ventana_juego.timer_crea_flechas.start()
        
    def actualizar_pantalla(self, padre):

        padre.flechas

    def crear_flechas(self, ventana_juego, especial):
        # LA FUNCION CREAR_FLECHAS_PROB ES DEL MODULO "funciones.py"   
        # el parametro especial sirve para identificar flechas cheatcode de los BONUS
        if especial != 10:
            crear_flechas_prob((0, 3), ventana_juego, especial)
            return
                 
        if self.dificultad == "Principiante":
            crear_flechas_prob((0, 3), ventana_juego, especial)

        elif self.dificultad == "Aficionado":
            crear_flechas_prob((0, 9), ventana_juego, especial)

        elif self.dificultad == "Maestro Cumbia":
            crear_flechas_prob((0, 13), ventana_juego, especial)
            
    def mover_flechas(self, flecha):
        sleep(0.01)
        nuevo_x = flecha.posicion[0]
        nuevo_y = flecha.posicion[1] + 1
        flecha.posicion = (nuevo_x, nuevo_y)

    def key_press_event(self, teclas, ventana_juego):
        a = teclas[65]
        s = teclas[83]
        d = teclas[68]
        w = teclas[87]
        # CHEAT CODES
        #  M + O + N "DINERO EXTRA"
        if teclas[77] == True and teclas[79] == True and teclas[71] == True:
            # Puedes encontrar esta funcion en "funciones.py"
            ventana_juego.dinero_jugador += p.DINERO_TRAMPA
            ventana_juego.dinero_jugador_label.setText(str(ventana_juego.dinero_jugador))
            teclas[77] = False
            teclas[79] = False
            teclas[71] = False
        
        # N + I + V (TERMINAR EL Juego instantaneamente)
        elif teclas[78] == True and teclas[73] == True and teclas[86] == True:
            # Solo si eljuego esta activo funciona, por eso corroboramos si pausa es falso,
            # es decir, si se esta jugando
            if ventana_juego.ispausa == False:
                ventana_juego.termino_juego()
        # F + T (flecha x2)
        elif teclas[70] == True and teclas[84] == True:
            self.crear_flechas(ventana_juego, 2)
        # F + G (flecha dorada)
        elif teclas[70] == True and teclas[71] == True:
            self.crear_flechas(ventana_juego, 0)    
        # F + H (flecha hielo)
        elif teclas[70] == True and teclas[72] == True:
            self.crear_flechas(ventana_juego, 3)
        
        if ventana_juego.ispausa == False:
            chequear_teclas(self, ventana_juego, a, s, d, w)

    def actualizar_info_pantalla(self, ventana_juego):
        ventana_juego.combo_valor_label.setText(str(ventana_juego.combo_valor))
        ventana_juego.combo_mayor_valor_label.setText(str(ventana_juego.combo_mayor_valor))
        self.tiempo_restante = ventana_juego.timer_duracion_juego.remainingTime()
        if ventana_juego.porcentaje_cancion < 100:
            ventana_juego.porcentaje_cancion = 100 - (self.tiempo_restante)*100/self.duracion_juego
            ventana_juego.progreso_cancion.setProperty("value", ventana_juego.porcentaje_cancion)
        elif ventana_juego.porcentaje_cancion == 100:
            pass
        pasos_totales = (ventana_juego.pasos_correctos +
        ventana_juego.pasos_incorrectos)
        if pasos_totales == 0:
            ventana_juego.aprobacion = 0
            ventana_juego.porcentaje_aprobacion.setProperty("value", ventana_juego.aprobacion)
        else:
            ventana_juego.aprobacion = 100*(ventana_juego.pasos_correctos - 
            ventana_juego.pasos_incorrectos)/pasos_totales
            ventana_juego.porcentaje_aprobacion.setProperty("value", ventana_juego.aprobacion)
        
    def actualizar_bailarines(self, paso_baile, objeto):
        def cambiar_pose_pinguirines(objeto, paso):
            for pinguirin in objeto.lista_pinguirines_bailando:
                if pinguirin.pixmap() == None:
                    pass
                else:
                    color_pinguirin = pinguirin.color_asignado
                    if paso == 10:
                        if color_pinguirin == QPixmap(p.pinguirin_celeste).toImage():
                            pinguirin.setPixmap(QPixmap(p.pinguirin_celeste))
                        elif color_pinguirin ==  QPixmap(p.pinguirin_amarillo).toImage():
                            pinguirin.setPixmap(QPixmap(p.pinguirin_amarillo))
                        elif color_pinguirin ==  QPixmap(p.pinguirin_rojo).toImage():
                            pinguirin.setPixmap(QPixmap(p.pinguirin_rojo))
                        elif color_pinguirin ==  QPixmap(p.pinguirin_morado).toImage():
                            pinguirin.setPixmap(QPixmap(p.pinguirin_morado))
                        elif color_pinguirin ==  QPixmap(p.pinguirin_verde).toImage():
                            pinguirin.setPixmap(QPixmap(p.pinguirin_verde))
                    else:
                        if color_pinguirin == QPixmap(p.pinguirin_amarillo).toImage():
                            pinguirin.hacer_paso(paso, p.pinguirin_amarillo_pasos)

                        elif color_pinguirin == QPixmap(p.pinguirin_celeste).toImage():
                            pinguirin.hacer_paso(paso, p.pinguirin_celeste_pasos)

                        elif color_pinguirin == QPixmap(p.pinguirin_rojo).toImage():
                            pinguirin.hacer_paso(paso, p.pinguirin_rojo_pasos)

                        elif color_pinguirin == QPixmap(p.pinguirin_morado).toImage():
                            pinguirin.hacer_paso(paso, p.pinguirin_morado_pasos)

                        elif color_pinguirin == QPixmap(p.pinguirin_verde).toImage():
                            pinguirin.hacer_paso(paso, p.pinguirin_verde_pasos)
        # 0 es izquierda
            # 1 es derecha
            # 2 es abajo
            # 3 es arriba
            # 4 es abajo izquierda
            # 5 es abajo derecha
            # 6 es arriba izquierda
            # 7 es arriba derecha
            # 8 es tres flechas
        if paso_baile == "neutro":
            cambiar_pose_pinguirines(objeto, 10)
        elif paso_baile == "izquierda":
            cambiar_pose_pinguirines(objeto, 0)
        elif paso_baile == "abajo":
            cambiar_pose_pinguirines(objeto, 2)
        elif paso_baile == "derecha":
            cambiar_pose_pinguirines(objeto, 1)
        elif paso_baile == "arriba":
            cambiar_pose_pinguirines(objeto, 3)
        if paso_baile == "izquierda_abajo":
            cambiar_pose_pinguirines(objeto, 4)
        elif paso_baile == "abajo_derecha":
            cambiar_pose_pinguirines(objeto, 5)
        elif paso_baile == "izquierda_arriba":
            cambiar_pose_pinguirines(objeto, 6)
        elif paso_baile == "derecha_arriba":
            cambiar_pose_pinguirines(objeto, 7)
        elif paso_baile == "tres_flechas":
            cambiar_pose_pinguirines(objeto, 8)

    def pausar_juego(self, ventana_juego):
        if ventana_juego.boton_pausar.isEnabled() == True:
            if ventana_juego.ispausa == False:
                ventana_juego.ispausa = True
                ventana_juego.boton_pausar.setText("&Continuar")
                ventana_juego.music_player.stop()
                self.tiempo_en_pausa = ventana_juego.timer_duracion_juego.remainingTime()
                ventana_juego.timer_duracion_juego.stop()
                ventana_juego.timer_crea_flechas.stop()
                for flecha in ventana_juego.lista_flechas:
                    flecha.mover = False
            elif ventana_juego.ispausa == True:
                ventana_juego.timer_crea_flechas.start()
                ventana_juego.ispausa = False
                ventana_juego.boton_pausar.setText("&Pausar")
                ventana_juego.timer_duracion_juego.setInterval(self.tiempo_en_pausa)
                ventana_juego.timer_duracion_juego.start()
                ventana_juego.music_player.play()
                for flecha in ventana_juego.lista_flechas:
                    flecha.mover = True
        else: 
            return
            
    def terminar_juego(self, ventana_juego):
        pass
        
    def flecha_hielo(self, ventana_juego):
        # for flecha in ventana_juego.lista_flechas:
        #     flecha.velocidad = flecha.velocidad*2

        # for flecha in ventana_juego.lista_flechas:
        #     flecha.velocidad = flecha.velocidad*2
        pass

