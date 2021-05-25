import os

from cargar_archivos import cargar_aeropuertos, cargar_conexiones
from entidades import Aeropuerto, Conexion


UMBRAL = 40000


class RedesMundiales:

    def __init__(self):
        # Estructura donde se guardaran los aeropuertos
        # Cada llave es un id y el valor es una instancia de Aeropuerto
        self.aeropuertos = {}

    def agregar_aeropuerto(self, aeropuerto_id, nombre):
        # Agregar un aeropuerto a la estructura
        if not aeropuerto_id in list(self.aeropuertos.keys()):
            self.aeropuertos[aeropuerto_id] = Aeropuerto(aeropuerto_id, nombre)

    def agregar_conexion(self, aeropuerto_id_partida, aeropuerto_id_llegada, infectados):
        # Crear la conexion de partida-llegada para el par de aeropuertos
        if aeropuerto_id_partida in list(self.aeropuertos.keys()) and aeropuerto_id_llegada in list(self.aeropuertos.keys()):
            conexion = Conexion(aeropuerto_id_partida, aeropuerto_id_llegada, infectados)
            if conexion in self.aeropuertos[aeropuerto_id_partida].conexiones:
                pass
            else:
                self.aeropuertos[aeropuerto_id_partida].conexiones.append(conexion)
        else:
            pass

    def cargar_red(self, ruta_aeropuertos, ruta_conexiones):

        # Primero se crean todos los aeropuertos
        for aeropuerto_id, nombre in cargar_aeropuertos(ruta_aeropuertos):
            self.agregar_aeropuerto(aeropuerto_id, nombre)

        # Después generamos las conexiones
        for id_partida, id_salida, infectados in cargar_conexiones(ruta_conexiones):
            self.agregar_conexion(id_partida, id_salida, infectados)

    def eliminar_conexion(self, conexion):
        id_partida = conexion.aeropuerto_inicio_id
        id_llegada = conexion.aeropuerto_llegada_id
        aeropuerto_inicio = self.aeropuertos.get(id_partida)
        for c in aeropuerto_inicio.conexiones:
            if c.aeropuerto_llegada_id == id_llegada:
                aeropuerto_inicio.conexiones.remove(c)
                break

    def eliminar_aeropuerto(self, aeropuerto_id):
        if aeropuerto_id not in self.aeropuertos:
            raise ValueError(f"No puedes eliminar un aeropuerto que no existe ({aeropuerto_id})")
        if self.aeropuertos[aeropuerto_id].conexiones:
            raise ValueError(f"No puedes eliminar un aeropuerto con conexiones ({aeropuerto_id})")
        del self.aeropuertos[aeropuerto_id]

    def infectados_generados_desde_aeropuerto(self, aeropuerto_id):
        # Muestra la cantidad de infectados generados por un aeropuerto
        def recorrer_conexiones(lista_conexiones, aeropuertos_visitados):
            infectados_conexion = 0
            # Esta funcion se llama a si misma en el caso de que el aeropuerto de llegada tenga mas conexiones
            # de esa forma puede recorrer la rama completa.
            for conexion in lista_conexiones:
                if self.aeropuertos[conexion.aeropuerto_llegada_id] in aeropuertos_visitados:
                    pass
                else:
                    aeropuertos_visitados.append(self.aeropuertos[conexion.aeropuerto_llegada_id])
                    if len(self.aeropuertos[conexion.aeropuerto_llegada_id].conexiones) > 0:
                        infectados_conexion += recorrer_conexiones(self.aeropuertos[conexion.aeropuerto_llegada_id].conexiones, aeropuertos_visitados)
                        
                    infectados_conexion += conexion.infectados

            return infectados_conexion
        
        aeropuertos_visitados = []
        numero_infectados = recorrer_conexiones(self.aeropuertos[aeropuerto_id].conexiones, aeropuertos_visitados)
        print(f"La cantidad estimada de infectados generados por el aeropuerto {self.aeropuertos[aeropuerto_id].nombre} es de {numero_infectados}")
        return numero_infectados

    def verificar_candidatos(self, ruta_aeropuertos_candidatos, ruta_conexiones_candidatas):
        # Se revisa cada aeropuerto candidato con las agregars conexiones candidatas.
        # Se elimina el aeropuerto en caso de que este genere muchos infectados

        # Primero se crean todos los aeropuertos
        for aeropuerto_id, nombre in cargar_aeropuertos(ruta_aeropuertos_candidatos):
            self.agregar_aeropuerto(aeropuerto_id, nombre)

        # Después generamos las conexiones
        for id_partida, id_salida, infectados in cargar_conexiones(ruta_conexiones_candidatas):
            self.agregar_conexion(id_partida, id_salida, infectados)

        for aeropuerto_id, nombre in cargar_aeropuertos(ruta_aeropuertos_candidatos):
            if self.infectados_generados_desde_aeropuerto(aeropuerto_id) > UMBRAL:
                print(f"La conexion {id_partida} -> {id_salida} rompe las normas de seguridad")
                self.eliminar_conexion(Conexion(id_partida, id_salida, infectados))

    def escala_mas_corta(self, id_aeropuerto_1, id_aeropuerto_2):
        def recorrer_conexiones(lista_conexiones, aeropuertos_visitados):
            largo_ruta = 0
            # Esta funcion se llama a si misma en el caso de que el aeropuerto de llegada tenga mas conexiones
            # de esa forma puede recorrer la rama completa.
            for conexion in lista_conexiones:
                if len(self.aeropuertos[conexion.aeropuerto_llegada_id].conexiones) > 0 and not self.aeropuertos[conexion.aeropuerto_llegada_id] in aeropuertos_visitados:
                    aeropuertos_visitados.append(self.aeropuertos[conexion.aeropuerto_llegada_id])
                    largo_ruta += recorrer_conexiones(self.aeropuertos[conexion.aeropuerto_llegada_id].conexiones, aeropuertos_visitados)
                largo_ruta += 1
                if id_aeropuerto_2 == conexion.aeropuerto_llegada_id:
                    return "stop"

            return largo_ruta
    


if __name__ == "__main__":
    # I: Construcción de la red
    # Instanciación de la red de aeropuertos
    redmundial = RedesMundiales()
    # Carga de datos (utiliza agregar_aeropuerto y agregar_conexion)
    redmundial.cargar_red(
        os.path.join("datos", "aeropuertos.txt"),
        os.path.join("datos", "conexiones.txt"),
    )

    # II: Consultas sobre la red
    # Verificar si conteo de infectados funciona
    # Para el aeropuerto 8 debería ser 2677
    redmundial.infectados_generados_desde_aeropuerto(8)
    # Para el aeropuerto 7 debería ser 10055
    redmundial.infectados_generados_desde_aeropuerto(7)
    # Para el aeropuerto 12 debería ser 30000
    redmundial.infectados_generados_desde_aeropuerto(12)

    # III: Simulación sobre la red
    # Utilizamos lo que hemos hecho para aplicar los cambios sobre la red
    redmundial.verificar_candidatos(
        os.path.join("datos", "aeropuertos_candidatos.txt"),
        os.path.join("datos", "conexiones_candidatas.txt")
    )
