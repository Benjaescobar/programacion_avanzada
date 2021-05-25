from os.path import join

## FOTOS PNG

RUTA_LOGO = join("sprites", "logo.png")

## PISTA BAILE

ANCHO_PISTA_BAILE = 511
ALTO_PISTA_BAILE = 451
RUTA_PISTA_BAILE = join("sprites", "fondos", "fondo.png")

## VENTANAS
ANCHO_VENTANA_TERMINO = 400
ALTO_VENTANA_TERMINO = 400

ANCHO_VENTANA_JUEGO = 895
ALTO_VENTANA_JUEGO = 612

ANCHO_VENTANA_INICIAL = 400
ALTO_VENTANA_INICIAL = 400


## PINGUINOS
# 0 es izquierda
# 1 es derecha
# 2 es abajo
# 3 es arriba
# 4 es abajo izquierda
# 5 es abajo derecha
# 6 es arriba izquierda
# 7 es arriba drecha
# 8 es tres flechas
pinguirin_amarillo = join("sprites", "pinguirin_amarillo", "amarillo_neutro.png")
pinguirin_amarillo_pasos =[
    join("sprites", "pinguirin_amarillo", "amarillo_izquierda.png")
, join("sprites", "pinguirin_amarillo", "amarillo_derecha.png")
, join("sprites", "pinguirin_amarillo", "amarillo_abajo.png")
, join("sprites", "pinguirin_amarillo", "amarillo_arriba.png")
, join("sprites", "pinguirin_amarillo", "amarillo_abajo_izquierda.png")
, join("sprites", "pinguirin_amarillo", "amarillo_abajo_derecha.png")
, join("sprites", "pinguirin_amarillo", "amarillo_arriba_izquierda.png")
, join("sprites", "pinguirin_amarillo", "amarillo_arriba_derecha.png")
, join("sprites", "pinguirin_amarillo", "amarillo_tres_flechas.png")
]
pinguirin_morado = join("sprites", "pinguirin_morado", "morado_neutro.png")
pinguirin_morado_pasos = [
    join("sprites", "pinguirin_morado", "morado_izquierda.png")
, join("sprites", "pinguirin_morado", "morado_derecha.png")
, join("sprites", "pinguirin_morado", "morado_abajo.png")
, join("sprites", "pinguirin_morado", "morado_arriba.png")
, join("sprites", "pinguirin_morado", "morado_abajo_izquierda.png")
, join("sprites", "pinguirin_morado", "morado_abajo_derecha.png")
, join("sprites", "pinguirin_morado", "morado_arriba_izquierda.png")
, join("sprites", "pinguirin_morado", "morado_arriba_derecha.png")
, join("sprites", "pinguirin_morado", "morado_tres_flechas.png")
]
pinguirin_rojo = join("sprites", "pinguirin_rojo", "rojo_neutro.png")
pinguirin_rojo_pasos = [
    join("sprites", "pinguirin_rojo", "rojo_izquierda.png")
, join("sprites", "pinguirin_rojo", "rojo_derecha.png")
, join("sprites", "pinguirin_rojo", "rojo_abajo.png")
, join("sprites", "pinguirin_rojo", "rojo_arriba.png")
, join("sprites", "pinguirin_rojo", "rojo_abajo_izquierda.png")
, join("sprites", "pinguirin_rojo", "rojo_abajo_derecha.png")
, join("sprites", "pinguirin_rojo", "rojo_arriba_izquierda.png")
, join("sprites", "pinguirin_rojo", "rojo_arriba_derecha.png")
, join("sprites", "pinguirin_rojo", "rojo_tres_flechas.png")
]
pinguirin_verde = join("sprites", "pinguirin_verde", "verde_neutro.png")
pinguirin_verde_pasos = [
    join("sprites", "pinguirin_verde", "verde_izquierda.png")
, join("sprites", "pinguirin_verde", "verde_derecha.png")
, join("sprites", "pinguirin_verde", "verde_abajo.png")
, join("sprites", "pinguirin_verde", "verde_arriba.png")
, join("sprites", "pinguirin_verde", "verde_abajo_izquierda.png")
, join("sprites", "pinguirin_verde", "verde_abajo_derecha.png")
, join("sprites", "pinguirin_verde", "verde_arriba_izquierda.png")
, join("sprites", "pinguirin_verde", "verde_arriba_derecha.png")
, join("sprites", "pinguirin_verde", "verde_tres_flechas.png")
]
pinguirin_celeste = join("sprites", "pinguirin_celeste", "celeste_neutro.png")
pinguirin_celeste_pasos = [
    join("sprites", "pinguirin_celeste", "celeste_izquierda.png")
, join("sprites", "pinguirin_celeste", "celeste_derecha.png")
, join("sprites", "pinguirin_celeste", "celeste_abajo.png")
, join("sprites", "pinguirin_celeste", "celeste_arriba.png")
, join("sprites", "pinguirin_celeste", "celeste_abajo_izquierda.png")
, join("sprites", "pinguirin_celeste", "celeste_abajo_derecha.png")
, join("sprites", "pinguirin_celeste", "celeste_arriba_izquierda.png")
, join("sprites", "pinguirin_celeste", "celeste_arriba_derecha.png")
, join("sprites", "pinguirin_celeste", "celeste_tres_flechas.png")
]

puff_1 = join("sprites", "puffles", "puffle_01.png")
puff_2 = join("sprites", "puffles", "puffle_02.png")
puff_3 = join("sprites", "puffles", "puffle_03.png")
puff_4 = join("sprites", "puffles", "puffle_04.png")


## COLORES PNG

color_azul = join("sprites", "colores", "azul.png")
color_morado = join("sprites", "colores", "morado.png")

## CANCIONES 

cancion1 = join("songs", "cancion_1.wav")
cancion2 = join("songs", "cancion_2.wav")

## DIFICULTADES

PRINCIPIANTE_DURACION = 30000
PRINCIPIANTE_GENERAFLECHAS = 1000
PRINCIPIANTE_APROBACION = 0.3

AFICIONADO_DURACION = 45000
AFICIONADO_GENERAFLECHAS = 750
AFICIONADO_APROBACION = 0.5

MAESTRO_DURACION = 60000
MAESTRO_GENERAFLECHAS = 500
MAESTRO_APROBACION = 0.7


## FLECHAS
flecha_left_normal = join("sprites", "flechas", "left_1.png")
flecha_left_dorada = join("sprites", "flechas", "left_2.png")
flecha_left_x2 = join("sprites", "flechas", "left_3.png")
flecha_left_hielo = join("sprites", "flechas", "left_4.png")
flechas_left = [
    flecha_left_dorada, flecha_left_normal, flecha_left_x2, flecha_left_hielo
    ]

flecha_up_normal = join("sprites", "flechas", "up_1.png")
flecha_up_dorada = join("sprites", "flechas", "up_2.png")
flecha_up_x2 = join("sprites", "flechas", "up_3.png")
flecha_up_hielo = join("sprites", "flechas", "up_4.png")
flechas_up = [
    flecha_up_dorada, flecha_up_normal, flecha_up_x2, flecha_up_hielo
    ]

flecha_down_normal = join("sprites", "flechas", "down_1.png")
flecha_down_dorada = join("sprites", "flechas", "down_2.png")
flecha_down_x2 = join("sprites", "flechas", "down_3.png")
flecha_down_hielo = join("sprites", "flechas", "down_4.png")
flechas_down = [
    flecha_down_dorada, flecha_down_normal, flecha_down_x2, flecha_down_hielo
    ]

flecha_right_normal = join("sprites", "flechas", "right_1.png")
flecha_right_dorada = join("sprites", "flechas", "right_2.png")
flecha_right_x2 = join("sprites", "flechas", "right_3.png")
flecha_right_hielo = join("sprites", "flechas", "right_4.png")
flechas_right = [
    flecha_right_dorada, flecha_right_normal, flecha_right_x2, flecha_right_hielo
    ]


PROB_FLECHA_NORMAL = 0.8
PROB_FLECHA_X2 = 0.17
PROB_FLECHA_DORADA = 0.02
PROB_FLECHA_HIELO = 0.01

velocidad_flecha_normal = 0.008
velocidad_flecha_dorada = 0.006

PUNTOS_FLECHA = 1

ancho_alto_cajas = 31

pos_x_flecha_left = 30
pos_x_flecha_up = 70
pos_x_flecha_down = 110
pos_x_flecha_right = 150

pos_x_caja_left = 10
pos_x_caja_up = 50
pos_x_caja_down = 90
pos_x_caja_right = 130

pos_y_cajas = 400


## TIENDA

DINERO_INICIAL_JUGADOR = 1000
PRECIO_PINGUIRINES = 500

## CHEATCODES

DINERO_TRAMPA = 1000

