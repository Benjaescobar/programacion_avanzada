import random
import time
from threading import Thread, Event, Lock, Timer

from parametros import (PROB_IMPOSTOR, PROB_ARREGLAR_SABOTAJE,
                        TIEMPO_ENTRE_TAREAS, TIEMPO_TAREAS, TIEMPO_SABOTAJE,
                        TIEMPO_ENTRE_ACCIONES, TIEMPO_ESCONDITE)

from funciones import (elegir_accion_impostor, print_progreso, print_anuncio,
                       print_sabotaje, cargar_sabotajes, print_explosión)


class Tripulante(Thread):

    def __init__(self, color, tareas, evento_sabotaje, diccionario_tareas):
        # No modificar
        super().__init__(daemon=True)
        self.color = color
        self.tareas = tareas
        self.esta_vivo = True
        self.diccionario_tareas = diccionario_tareas
        self.evento_sabotaje = evento_sabotaje
        # Si quieres agregar lineas, hazlo desde aca

    def run(self):
        # Completar
        while True:
            if not self.esta_vivo:
                break
            if len(self.tareas) == 0:
                break
            if not self.evento_sabotaje.is_set():
                self.hacer_tarea()
                time.sleep(TIEMPO_ENTRE_TAREAS)
                continue
            else:
                if random.uniform(0,1) <= PROB_ARREGLAR_SABOTAJE:
                    self.arreglar_sabotaje()
                else:
                    time.sleep(TIEMPO_ENTRE_TAREAS)

    def hacer_tarea(self):
        # Completar
        indice_tarea = random.randint(0,len(self.tareas)-1)
        tarea = self.diccionario_tareas[self.tareas[indice_tarea]]
        with tarea["lock"]:
            for i in range(5):
                if self.esta_vivo == False:
                    break
                tiempo = random.randint(TIEMPO_TAREAS[0],TIEMPO_TAREAS[1])
                time.sleep(tiempo)
                print_progreso(self.color, self.tareas[indice_tarea], i*25)
            tarea["realizado"] = True
            self.tareas.pop(indice_tarea)

    def arreglar_sabotaje(self):
        # Completar
        print_anuncio(self.color + ":", "Se empezo a reparar el sabotaje")
        for i in range(4):
            if self.esta_vivo == False:
                return
            tiempo = random.randint(TIEMPO_SABOTAJE[0],TIEMPO_SABOTAJE[1])
            time.sleep(tiempo)
            if self.esta_vivo == False:
                return
            print_progreso(self.color, "Arreglando Sabotaje...", i*25)
        print_anuncio(self.color, "Termine! nos salvamos :D")
        self.evento_sabotaje.clear()


class Impostor(Tripulante):

    def __init__(self, color, tareas, evento_sabotaje, diccionario_tareas, tripulantes, evento_termino):
        # No modificar
        super().__init__(color, tareas, evento_sabotaje, diccionario_tareas)
        self.tripulantes = tripulantes
        self.evento_termino = evento_termino
        self.sabotajes = cargar_sabotajes()
        # Si quieres agregar lineas, hazlo desde aca

    def run(self):
        # Completar
        while True:
            tripulantes_vivos = 0
            for tripulant in self.tripulantes:
                if tripulant.esta_vivo == True:
                    tripulantes_vivos += 1
                    break
                else:
                    continue
            if tripulantes_vivos == 0:
                self.join()
                return
            if not self.evento_termino.is_set:
                self.join()
                return
            
            accion = elegir_accion_impostor()
            if accion == "Matar":
                self.matar_jugador()
            elif accion == "Sabotear":
                self.sabotear()
            elif accion == "Esconderse":
                time.sleep(TIEMPO_ESCONDITE)
            time.sleep(TIEMPO_ENTRE_ACCIONES)
            continue

    def matar_jugador(self):
        # Completar
        indice_tripulante = random.randint(0, len(self.tripulantes)-1)
        self.tripulantes[indice_tripulante].esta_vivo == False
        color = self.tripulantes[indice_tripulante].color
        self.tripulantes.pop(indice_tripulante)
        print_anuncio(color, "Ha muerto" + color + ", quedan " + str(len(self.tripulantes)) + " Jugadores")
        

    def sabotear(self):
        # Completar
        if not self.evento_sabotaje.is_set():
            nombre_sabotaje = random.choice(self.sabotajes)
            tiempo = random.randint(TIEMPO_SABOTAJE[0],TIEMPO_SABOTAJE[1])
            el_timer = Timer(tiempo, self.terminar_sabotaje)
            self.evento_sabotaje.set()
            el_timer.start()
            
            print_sabotaje(nombre_sabotaje)


    def terminar_sabotaje(self):
        # Completar
        if self.evento_sabotaje.is_set:
            for tripulant in self.tripulantes:
                tripulant.esta_vivo = False
            print_explosión()
        else:
            return


if __name__ == "__main__":
    print("\n" + " INICIANDO PRUEBA DE TRIPULANTE ".center(80, "-") + "\n")
    # Se crea un diccionario de tareas y un evento sabotaje de ejemplos.
    ejemplo_tareas = {
            "Limpiar el filtro de oxigeno": {
                "lock": Lock(),
                "realizado": False,
                "nombre": "Limpiar el filtro de oxigeno"
            }, 
            "Botar la basura": {
                "lock": Lock(),
                "realizado": False,
                "nombre":  "Botar la basura"
            }
        }
    ejemplo_evento = Event()

    # Se intancia un tripulante de color ROJO
    rojo = Tripulante("Rojo", list(ejemplo_tareas.keys()), ejemplo_evento, ejemplo_tareas)

    rojo.start()

    time.sleep(5)
    # ==============================================================
    # Descomentar las siguientes lineas para probar el evento sabotaje.

    print(" HA COMENZADO UN SABOTAJE ".center(80, "*"))
    ejemplo_evento.set()

    rojo.join()

    print("\n-" + "="*80 + "\n")
    print(" PRUEBA DE TRIPULANTE TERMINADA ".center(80, "-"))
    if sum((0 if x["realizado"] else 1 for x in ejemplo_tareas.values())) > 0:
        print("El tripulante no logró completar todas sus tareas. ")
    elif ejemplo_evento.is_set():
        print("El tripulante no logró desactivar el sabotaje")
    else:
        print("El tripulante ha GANADO!!!")
