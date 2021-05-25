
import parametros as p
import sys, os
from os.path import join

from random import randint, uniform
from PyQt5.QtWidgets import (
    QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QApplication,
    QMessageBox, QMainWindow
)
from time import sleep
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QSize, QRect, QThread
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer
from back_end.music_player import MusicPlayer
from back_end.flechas import Flecha


def tipo_flecha():
    prob = uniform(0, 1)
    prob_2 = p.PROB_FLECHA_NORMAL + p.PROB_FLECHA_X2
    if prob <= p.PROB_FLECHA_NORMAL:
        return 1 # FLECHA NORMAL
    elif p.PROB_FLECHA_NORMAL < prob <= prob_2:
        return 2 # FLECHA x2
    elif prob_2 < prob <= prob_2 + p.PROB_FLECHA_HIELO:   
        return 3 # FLECHA hielo
    elif prob_2 + p.PROB_FLECHA_HIELO < prob <= 1:
        return 0 # FLECHA DORADA

def crear_flecha(flechas, ventana_juego, tipo):
    if tipo == 10: # Normal
        flecha = tipo_flecha()
    else: # cheatcode
        flecha = tipo
    nueva_flecha = Flecha(
        QLabel(ventana_juego), flechas[0], 140, flecha, flechas[1][flecha],
            ventana_juego.lista_flechas)
    nueva_flecha.actualizar.connect(ventana_juego.actualizar_label)
    ventana_juego.lista_flechas.append(nueva_flecha)

def cambiar_color_caja(cajas): 
     # el parametro es una lista de 
    if len(cajas) == 1:
        cajas[0].setPixmap(QPixmap(p.color_morado))
    elif len(cajas) == 2:
        cajas[0].setPixmap(QPixmap(p.color_morado))
        cajas[1].setPixmap(QPixmap(p.color_morado))
    elif len(cajas) == 3:
        cajas[0].setPixmap(QPixmap(p.color_morado))
        cajas[1].setPixmap(QPixmap(p.color_morado))
        cajas[2].setPixmap(QPixmap(p.color_morado))

def crear_flechas_prob(rango, ventana_juego, especial):
    ## Esta funcion sirve para crear flechas en las distintas dificultades
    ## Lo hace de forma que en cada dificultad se ingresa un rango de numeros,
    ## que generan cierto tipo de secuencia, e.x-> si esta en Principiante
    ## solo se hace del 0 al 3 (crear una flecha).
    combinacion_flecha = randint(rango[0], rango[1])
    flecha_derecha = [p.pos_x_flecha_right, p.flechas_right]
    flecha_izquierda = [p.pos_x_flecha_left, p.flechas_left]
    flecha_down = [p.pos_x_flecha_down, p.flechas_down]
    flecha_up = [p.pos_x_flecha_up, p.flechas_up]
    ventana_juego.contador_pasos_totales += 1
    if combinacion_flecha == 0: # flecha izquierda
        crear_flecha(flecha_izquierda, ventana_juego, especial)

    elif combinacion_flecha == 1: # flecha up
        crear_flecha(flecha_up, ventana_juego, especial)

    elif combinacion_flecha == 2: # flecha down
        crear_flecha(flecha_down, ventana_juego, especial)
    
    elif combinacion_flecha == 3: # flecha right
        crear_flecha(flecha_derecha, ventana_juego, especial)

    elif combinacion_flecha == 4: # flecha right - left
        crear_flecha(flecha_derecha, ventana_juego, especial)
        crear_flecha(flecha_izquierda, ventana_juego, especial)
        
    elif combinacion_flecha == 5: # flecha right - down
        crear_flecha(flecha_derecha, ventana_juego, especial)
        crear_flecha(flecha_down, ventana_juego, especial)

    elif combinacion_flecha == 6: # flecha right - up
        crear_flecha(flecha_derecha, ventana_juego, especial)
        crear_flecha(flecha_up, ventana_juego, especial)
    
    elif combinacion_flecha == 7: # flecha left - down
        crear_flecha(flecha_izquierda, ventana_juego, especial)
        crear_flecha(flecha_down, ventana_juego, especial)

    elif combinacion_flecha == 8: # flecha left - up
        crear_flecha(flecha_izquierda, ventana_juego, especial)
        crear_flecha(flecha_up, ventana_juego, especial)

    elif combinacion_flecha == 9: # flecha down - up
        crear_flecha(flecha_down, ventana_juego, especial)
        crear_flecha(flecha_up, ventana_juego, especial)
        
    elif combinacion_flecha == 10:# flecha right - down - left
        crear_flecha(flecha_derecha, ventana_juego, especial)
        crear_flecha(flecha_izquierda, ventana_juego, especial)
        crear_flecha(flecha_down, ventana_juego, especial)
    
    elif combinacion_flecha == 11: # flecha right - up - left
        crear_flecha(flecha_derecha, ventana_juego, especial)
        crear_flecha(flecha_izquierda, ventana_juego, especial)
        crear_flecha(flecha_up, ventana_juego, especial)

    elif combinacion_flecha == 12: # flecha right - up - down
        crear_flecha(flecha_derecha, ventana_juego, especial)
        crear_flecha(flecha_down, ventana_juego, especial)
        crear_flecha(flecha_up, ventana_juego, especial)

    elif combinacion_flecha == 13: # flecha left - up - down
        crear_flecha(flecha_izquierda, ventana_juego, especial)
        crear_flecha(flecha_down, ventana_juego, especial)
        crear_flecha(flecha_up, ventana_juego, especial)

def chequear_teclas(self, ventana_juego, a, s, d, w):
    def sacar_flechas(pos_x, tecla):
        ## Esta funcion primero nos pregunta si es que la tecla ingresada es verdadera,
        # si eso se cumple, entonces procede a ver si hay una flecha en la posicion x,
        # y si eso pasa, se suma puntaje y se retorna True.
        verificado_paso_correcto = False
        if tecla == True:
            for flecha in ventana_juego.lista_flechas:
                pos_fl_y = flecha.posicion[1]
                pos_fl_x = flecha.posicion[0]
                limite_inferior_y = p.pos_y_cajas + 140
                limite_superior_y = p.pos_y_cajas + p.ancho_alto_cajas + 140
                c1 = limite_inferior_y < pos_fl_y < limite_superior_y
                c2 = limite_inferior_y < pos_fl_y + p.ancho_alto_cajas < limite_superior_y
                c3 = pos_x + 20 <= pos_fl_x <= pos_x + 51
                if c1 and c3 or c2 and c3:
                    if flecha.tipo_flecha == 0:
                        ventana_juego.contador_flechas_atrapadas += 10
                    elif flecha.tipo_flecha == 1:
                        ventana_juego.contador_flechas_atrapadas += 1
                    elif flecha.tipo_flecha == 2:
                        ventana_juego.contador_flechas_atrapadas += 2
                    elif flecha.tipo_flecha == 3:
                        ventana_juego.contador_flechas_atrapadas += 1
                        self.senal_flecha_hielo.emit(ventana_juego)    
                    verificado_paso_correcto = True        
                    flecha.flecha.hide()

        ## Si esque se atrapo una flecha, se retornara True, si no, False
        if verificado_paso_correcto == True:
            return True
        else:
            return False

    # EXPLICACION :
    # En esta parte, para asegurarnos de cual es el comando, se piden condiciones
    # que incluyen que las teclas que buscamos que sean presionadas sean True y 
    # que las que no esten False.

    # De la misma forma, la funcion "sacar_flecha" nos retorna True si en esa posicion
    # habia una flecha, y False en el caso contrario, esta forma podemos comprobar si los
    # pasos fueron correctos, pues un paso correcto es solo si en las teclas presionadas
    # habian flechas
    # Asi, si se presiono una combinacion de teclas , se comprobara que SOLO en esas cajas 
    # hayan habido flechas

    # Esta parte esta muy acoplada, pero entendiendo la logica de un if, todos hacen sentido.

    fl_iz = sacar_flechas(p.pos_x_caja_left, a) # flecha izquierda
    fl_de = sacar_flechas(p.pos_x_caja_right, d) # flecha derecha
    fl_ab = sacar_flechas(p.pos_x_caja_down, s) # flecha abajo
    fl_ar = sacar_flechas(p.pos_x_caja_up, w) # flecha arriba

    #   # SOLO UNA TECLA
    if a == True and s == False and d == False and w == False:
        cambiar_color_caja([ventana_juego.caja_left])
        if fl_iz == True and fl_de == False and fl_ab == False and fl_ar == False:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("izquierda", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif s == True and a == False and d == False and w == False:
        cambiar_color_caja([ventana_juego.caja_down])
        if fl_iz == False and fl_de == False and fl_ab == True and fl_ar == False:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("abajo", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif d == True and a == False and s == False and w == False:
        cambiar_color_caja([ventana_juego.caja_right])
        if fl_iz == False and fl_de == True and fl_ab == False and fl_ar == False:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("derecha", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif w == True and a == False and d == False and s == False:
        cambiar_color_caja([ventana_juego.caja_up])
        if fl_iz == False and fl_de == False and fl_ab == False and fl_ar == True:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("arriba", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1

    # DOS TECLAS
    elif a == True and s == True and d == False and w == False: # left - down
        cambiar_color_caja([ventana_juego.caja_down, ventana_juego.caja_left])
        if fl_iz == True and fl_de == False and fl_ab == True and fl_ar == False:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("izquierda_abajo", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == True and s == False and d == True and w == False: # left - right
        cambiar_color_caja([ventana_juego.caja_left, ventana_juego.caja_right])
        if fl_iz == True and fl_de == True and fl_ab == False and fl_ar == False:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("izquierda_derecha", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == True and s == False and d == False and w == True: # left - up
        cambiar_color_caja([ventana_juego.caja_left, ventana_juego.caja_up])
        if fl_iz == True and fl_de == False and fl_ab == False and fl_ar == True:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("izquierda_arriba", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == False and s == True and d == True and w == False: # down - right
        cambiar_color_caja([ventana_juego.caja_down, ventana_juego.caja_right])
        if fl_iz == False and fl_de == True and fl_ab == True and fl_ar == False:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("abajo_derecha", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == False and s == True and d == False and w == True: # down - up
        cambiar_color_caja([ventana_juego.caja_down, ventana_juego.caja_up])
        if fl_iz == False and fl_de == False and fl_ab == True and fl_ar == True:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("arriba_abajo", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == False and s == False and d == True and w == True: # up - right
        cambiar_color_caja([ventana_juego.caja_up, ventana_juego.caja_right])
        if fl_iz == False and fl_de == True and fl_ab == False and fl_ar == True:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("derecha_arriba", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1

    # TRES TECLAS
    elif a == True and s == True and d  == True and w == False: # left - down - right
        cambiar_color_caja([ventana_juego.caja_left, ventana_juego.caja_down, ventana_juego.caja_right])
        if fl_iz == True and fl_de == True and fl_ab == True and fl_ar == False:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("tres_flechas", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == True and s == False and d  == True and w == True: # left - up - right
        cambiar_color_caja([ventana_juego.caja_left, ventana_juego.caja_up, ventana_juego.caja_right])
        if fl_iz == True and fl_de == True and fl_ab == False and fl_ar == True:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("tres_flechas", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == True and s == True and d  == False and w == True: # left - down - up
        cambiar_color_caja([ventana_juego.caja_left, ventana_juego.caja_down, ventana_juego.caja_up])
        if fl_iz == True and fl_de == False and fl_ab == True and fl_ar == True:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("tres_flechas", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1
    elif a == False and s == True and d  == True and w == True: # up - down - right
        cambiar_color_caja([ventana_juego.caja_right, ventana_juego.caja_down, ventana_juego.caja_up])
        if fl_iz == False and fl_de == True and fl_ab == True and fl_ar == True:
            ventana_juego.pasos_correctos += 1
            self.actualizar_bailarines("tres_flechas", ventana_juego)
            ventana_juego.combo_valor += 1
        else:
            if ventana_juego.combo_mayor_valor < ventana_juego.combo_valor:
                ventana_juego.combo_mayor_valor = ventana_juego.combo_valor
            ventana_juego.combo_valor = 0
            ventana_juego.pasos_incorrectos += 1