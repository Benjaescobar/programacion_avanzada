
import threading
import socket
import random
from os.path import join
import json
with open(join("server", "parameters.json")) as file:
    parametros = json.load(file)


class AdminJuego():

#     def __init__(self):


#         # CLIENTES
#         # el turno_actual parte asi dado al funcionamiento de la funcion cambia turnos, de esta
#         # forma logramos que se parta el jugador 0.
#         self.turno_actual = parametros["CANTIDAD_JUGADORES_PARTIDA"]

#         # FLUJO PROGRAMA
#         self.sala_actual = "sala de espera"
#         self.lock_send = threading.Lock()

#         # MAPA
#         self.informacion_hexagonos = {}


    def aprobar_construccion(self, compra, materiales, precio):
        if materiales["ARCILLA"] >= precio[f"CANTIDAD_ARCILLA_{compra}"]:
            if materiales["TRIGO"] >= precio[f"CANTIDAD_TRIGO_{compra}"]:
                if materiales["MADERA"] >= precio[f"CANTIDAD_MADERA_{compra}"]:
                    return True
        return False

    def cobrar_materiales(self, compra, materiales, precio):
        materiales["ARCILLA"] -= precio[f"CANTIDAD_ARCILLA_{compra}"]
        materiales["TRIGO"] -= precio[f"CANTIDAD_TRIGO_{compra}"]
        materiales["MADERA"] -= precio[f"CANTIDAD_MADERA_{compra}"]

    def crear_lista_hexagonos(self):
        numeros_fichas = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        random.shuffle(numeros_fichas)
        lista_orden_hexagonos = []
        contador_1 = 0
        contador_2 = 0
        contador_3 = 0
        print("CREANDO MAPA...")
        while True:
            eleccion = random.randint(0, 2)
            if (contador_1 + contador_2 + contador_3) == 9:
                break
            else:
                if contador_1 < 3 and eleccion == 0:
                    lista_orden_hexagonos.append(["ARCILLA", numeros_fichas.pop(0)])
                    contador_1 += 1
                elif contador_2 < 3 and eleccion == 1:
                    lista_orden_hexagonos.append(["TRIGO", numeros_fichas.pop(0)])
                    contador_2 += 1
                elif contador_3 < 3 and eleccion == 2:
                    lista_orden_hexagonos.append(["MADERA", numeros_fichas.pop(0)])
                    contador_3 += 1
        if eleccion == 0:
            lista_orden_hexagonos.append(["ARCILLA", numeros_fichas.pop(0)])
            contador_1 += 1
        elif eleccion == 1:
            lista_orden_hexagonos.append(["TRIGO", numeros_fichas.pop(0)])
            contador_2 += 1
        elif eleccion == 2:
            lista_orden_hexagonos.append(["MADERA", numeros_fichas.pop(0)])
            contador_3 += 1

        return lista_orden_hexagonos

    def crear_dict_hexagonos(self, lista_orden_hexagonos):
        informacion_hexagonos = {}
        for i in range(len(lista_orden_hexagonos)):
            informacion_hexagonos[str(i)] = lista_orden_hexagonos[i]
            informacion_hexagonos[str(i)].append(
                parametros["hexagonos"][str(i)]
            )
        return informacion_hexagonos

    def terminar_turno(self, estado_usuarios):
        
        for estado in estado_usuarios.values():
            bonus_carretera = 0
            if estado["CAMINO_MAS_LARGO_BOOL"] == True:
                bonus_carretera = 2
            estado["PUNTOS_VICTORIA"] = estado["CHOZAS"] + estado["CAMINOS"]  + bonus_carretera
            if estado["PUNTOS_VICTORIA"] >= 10:
                return True
        return False

    def cambiar_turno(self, nombres, turno_actual, usuarios_totales):
        nombres = list(usuarios_totales.keys())
        if turno_actual < len(nombres) - 1:
            turno_actual += 1

        elif turno_actual == len(nombres) - 1:
            turno_actual = 0

        return turno_actual

    def carretera_mas_larga(self, nodos, usuario):
        def recorrer_caminos(nodo_inicial, camino, caminos_visitados):
            contador = 0
            for nodo in camino.nodos_adyacentes:
                if nodo == nodo_inicial:
                    continue
                for camino_adyacente in nodo.caminos_adyacentes:
                    if camino_adyacente is camino:
                        continue
                    else:
                        if camino_adyacente.usuario == usuario and not camino_adyacente in caminos_visitados:
                            caminos_visitados.append(camino_adyacente)
                            contador += 1
                            contador += recorrer_caminos(nodo, camino_adyacente, caminos_visitados)
            return contador

        caminos_visitados = []

        contador_1 = 1
        contador_2 = 1
        contador_3 = 1
        contador_4 = 1
        camino_contado = 0
        for nodo in nodos.values():
            if nodo.usado == True and nodo.usuario == usuario:
                for camino in nodo.caminos_adyacentes:
                    if camino_contado == 0:
                        contador_1 = recorrer_caminos(nodo, camino, caminos_visitados)
                        camino_contado += 1
                    if camino_contado == 1:
                        contador_2 = recorrer_caminos(nodo, camino, caminos_visitados)
                        camino_contado += 1
                    if camino_contado == 2:
                        contador_3 = recorrer_caminos(nodo, camino, caminos_visitados)
                        camino_contado += 1
                    if camino_contado == 3:
                        contador_4 = recorrer_caminos(nodo, camino, caminos_visitados)
        return max(contador_1, contador_2, contador_3, contador_4)


    def carretera_mas_larga_definir(self, estado_usuarios):
        usuarios = list(estado_usuarios.keys())
        camino_usuario1 = estado_usuarios[usuarios[0]]["CAMINO_MAS_LARGO"]
        camino_usuario2 = estado_usuarios[usuarios[1]]["CAMINO_MAS_LARGO"]
        # camino_usuario3 = estado_usuarios[usuarios[2]]["CAMINO_MAS_LARGO"]
        # camino_usuario4 = estado_usuarios[usuarios[3]]["CAMINO_MAS_LARGO"]
        camino_mas_largo = max(camino_usuario1, camino_usuario2)

        for usuario in usuarios:
            if estado_usuarios[usuario]["CAMINO_MAS_LARGO"] == camino_mas_largo:
                estado_usuarios[usuario]["CAMINO_MAS_LARGO_BOOL"] = True
            else:
                estado_usuarios[usuario]["CAMINO_MAS_LARGO_BOOL"] = False
        return