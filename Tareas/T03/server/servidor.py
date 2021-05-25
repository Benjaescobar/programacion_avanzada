
import threading
import socket
import random
import json
import time
from os.path import join

from logica_servidor import AdminJuego
from nodos import Tablero

with open(join("server", "parameters.json")) as file:
    parametros = json.load(file)

# codigo inspirado en la ayudantia 11 de @lucasvsj, @tocococa & @SugarFreeManatee

class Servidor():


    def __init__(self, port, host):
        self.max_recv = 2**16
        self.host = host
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.back_end = AdminJuego()
        self.sala_actual = "sala de espera"

        # CLIENTES
        self.sockets = {}
        self.usuarios_skt = {}
        self.bind_listen()
        self.accept_connections()
        self.colores = ["0", "1", "2", "3"]

        self.estado_usuarios = {}
        # el turno_actual parte asi dado al funcionamiento de la funcion cambia turnos, de esta
        # forma logramos que se parta el jugador 0.
        self.turno_actual = parametros["CANTIDAD_JUGADORES_PARTIDA"] - 1

        # FLUJO PROGRAMA
        self.lock_send = threading.Lock()
        # MAPA
        self.tablero = Tablero()

        self.info_caminos = {}    
        for camino in self.tablero.caminos.values():
            nodos_valor = []
            for nodo in camino.nodos_adyacentes:
                nodos_valor.append(nodo.valor)
            self.info_caminos[camino.valor] = nodos_valor

        self.logica_servidor = AdminJuego()

        self.informacion_hexagonos = {}
        
        self.informacion_nodos = {}

        self.online()
        

    def bind_listen(self):
        try:
            self.socket_server.bind((self.host, self.port))
            self.socket_server.listen(250)
            print(f'Servidor escuchando en {self.host} : {self.port}')

        except OSError as e:
            print("HUBO UN ERROR")
            self.port += 1
        
    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        while True:
            if len(self.sockets) == parametros["CANTIDAD_JUGADORES_PARTIDA"]:
                print("-"*20)
                print("Iniciando Partida")
                print("-"*20)
                time.sleep(1)
                with self.lock_send:
                    print("Enviando senal para partir juego...")
                    for sock in self.sockets:
                        self.send("empezar juego", "empezar juego", sock)
                with self.lock_send:
                    print("Enviando caminos")
                    for sock in self.sockets:
                        self.send("empezar juego", "empezar juego", sock)


                self.sala_actual = "sala de juego"
                self.crear_mapa()
            client_socket, address = self.socket_server.accept()
            # añadimos en socket del cliente aceptado a nuestro diccionario
            self.sockets[client_socket] = address
            escuchar_cliente_thread = threading.Thread(
                target= self.listen_client_thread,
                args=(client_socket, ),
                daemon=True
            )
            escuchar_cliente_thread.start()
            print(len(self.sockets))            

    # El metodo "listen_client_thread" y "procesar_mensaje" tienen como funcion escuchar a los
    # clientes y ver a que accion corresponde cada mensaje

    def listen_client_thread(self, client_socket):
        while True:
            largo_archivo = int.from_bytes(
                client_socket.recv(4), byteorder='big')
            print("Recibiendo mensaje de Cliente")
            if largo_archivo > self.max_recv:
                largo_archivo = self.max_recv
            bytes_leidos = bytearray()
            while len(bytes_leidos) < largo_archivo:
                modulo = int.from_bytes(
                client_socket.recv(4), byteorder='little')

                respuesta = client_socket.recv(60)
                bytes_leidos += respuesta

            print("Limpiando bytes...")

            bytes_leidos_importantes = bytes_leidos[:largo_archivo]

            self.procesar_mensaje(bytes_leidos_importantes, client_socket)

        # try:
            # # Si se elimina el usuario, el servidor recibe un mensaje vacío y no logra
            # # deserializarlo.
            #     print("No se a procesado aun...")
            #     msg = bytes_leidos.decode()
            #     print(msg)
            #     self.procesar_mensaje(msg)
            # except json.decoder.JSONDecodeError as e:
            #     print('Usuario eliminado')
            # # Eliminamos al cliente del diccionario de sockets
            #     del self.sockets[client_socket]
            #     break

    def procesar_mensaje(self, msg_bytes, client_socket):
        msg = msg_bytes.decode()
        msg = json.loads(msg)
        usuario = msg["user"]
        data = msg["data"]
        accion = msg["accion"]

        if self.sala_actual == "sala de espera":
            # mensaje_decoded = json.loads(msg)
            # En este caso el mensaje es el nombre de usuario, ya que estamos en el lobby
            # es por eso que anadimos el mensaje a nuestra lista de usuarios.
            self.usuarios_skt[data] = self.sockets[client_socket]
            cant_init = parametros["cantidades_iniciales"]
            self.estado_usuarios[data] = {
                "MATERIALES": {
                    "ARCILLA": cant_init["ARCILLA"],
                     "TRIGO": cant_init["TRIGO"],
                      "MADERA": cant_init["MADERA"]},
                "COLOR": parametros["colores"][self.colores.pop(0)],
                "CHOZAS": 0,
                "CAMINOS": 0,
                "PUNTOS_VICTORIA": 0,
                "CAMINO_MAS_LARGO": 1,
                "CAMINO_MAS_LARGO_BOOL": False
            }
            with self.lock_send:
                print("Enviando usuarios conectados...")
                for skt in self.sockets:
                    self.send(self.usuarios_skt, "CARGAR USUARIOS", skt)
            
            print("--- Datos Enviados ---")

        elif self.sala_actual == "sala de juego":
            if accion == 'LANZAR DADO':
                self.lanzar_dados(client_socket)
            if accion == "TERMINAR TURNO":
                ganador = self.logica_servidor.terminar_turno(self.estado_usuarios)
                if ganador == True:
                    print(f"ha ganado {usuario}")
                    with self.lock_send:
                        for skt in self.sockets:
                            self.send(usuario, "TERMINAR JUEGO", skt)
                else:
                    self.cambiar_turno()
            elif accion == "COMPRAR CHOZA":
                # construir_vivienda retorna true si es que se puede
                precio = parametros["precios"]["CHOZA"]
                materiales = self.estado_usuarios[usuario]["MATERIALES"]
                aceptado = self.logica_servidor.aprobar_construccion("CHOZA", materiales, precio)
                if aceptado == True:
                    # chequeamos si el usuario tiene los recursos
                    construir = self.tablero.nodos[data].construir_vivienda(usuario)
                    if construir == True:
                        self.logica_servidor.cobrar_materiales("CHOZA", materiales, precio)
                        print("COMPRA DE CHOZA APROBADA")
                        self.estado_usuarios[usuario]["CHOZAS"] += 1
                        with self.lock_send:
                            for skt in self.sockets:
                                self.send(
                                    [self.estado_usuarios[usuario]["COLOR"], data],
                                    "AGREGAR CHOZA", skt)

                        with self.lock_send:
                            for skt in self.sockets:
                                self.send(
                                    self.estado_usuarios, 
                                    "NUEVO MATERIAL", 
                                    skt)
                    else:
                        print("POSICION INVALIDA")
            elif accion == "COMPRAR CAMINO":
                precio = parametros["precios"]["CAMINO"]
                materiales = self.estado_usuarios[usuario]["MATERIALES"]
                aceptado = self.logica_servidor.aprobar_construccion("CAMINO", materiales, precio)
                if aceptado == True:
                    # chequeamos si el usuario tiene los recursos
                    print(f"se puede construir en {data}?")
                    construir = self.tablero.caminos[data].construir_camino(usuario, False)
                    if construir == True:
                        self.logica_servidor.cobrar_materiales("CAMINO", materiales, precio)
                        print("COMPRA DE CAMINO APROBADA")
                        self.estado_usuarios[usuario]["CAMINOS"] += 1
                        with self.lock_send:
                            for skt in self.sockets:
                                self.send(
                                    [self.estado_usuarios[usuario]["COLOR"], data],
                                    "AGREGAR CAMINO", skt)
                        self.estado_usuarios[usuario]["CAMINO_MAS_LARGO"] = (
                            self.logica_servidor.carretera_mas_larga(self.tablero.nodos, usuario))
                        self.logica_servidor.carretera_mas_larga_definir(self.estado_usuarios)
                        with self.lock_send:
                            for skt in self.sockets:
                                self.send(
                                    self.estado_usuarios, 
                                    "NUEVO MATERIAL", 
                                    skt)

        elif self.sala_actual == "fin del juego":
            pass
    
    ## El metodo send se encarga de enviar mensajes a los clientes
    def send(self, data, accion, sock):
        mensaje = {
            "ventana": self.sala_actual,
            "data": data, 
            "accion": accion
            }
        json_msg = json.dumps(mensaje)
        msg_in_bytes = json_msg.encode()
        msg_to_read = bytearray(msg_in_bytes)

        largo = len(msg_to_read)

        mensaje_entero = bytearray()
        mensaje_entero += largo.to_bytes(4, byteorder='big')

        for modulo in range(largo//60 + 1):
            mensaje_entero += modulo.to_bytes(4, byteorder='little')
            largo_restante = len(msg_to_read)
            if largo_restante >= 60:
                mensaje_entero += msg_to_read[:60]
                msg_to_read = msg_to_read[60:]
            else:
                mensaje_entero += msg_to_read[:largo_restante]
                bytes_cero_restantes = bytearray(60 - largo_restante)
                mensaje_entero += bytes_cero_restantes
                break
        
        sock.send(mensaje_entero)

    def lanzar_dados(self, skt):
        self.dado_1 = random.randint(1, 6)
        self.dado_2 = random.randint(1, 6)

        with self.lock_send:
            for skt in self.sockets:
                self.send([self.dado_1, self.dado_2], "DADO", skt)

        self.suma_dados = self.dado_1 + self.dado_2

        self.repartir_materiales(self.suma_dados)

    def repartir_materiales(self, dados):
        '''
            Buscamos todos los hexagonos que tengan el numero que salio en el dado y luego enviamos
            esa informacion a otro lado
        '''
        print("Analizando dados con hexagonos...")
        if dados == 7:
            #SACAR CARTAS A LOS QUE TENGAN MAS DE 8
            pass
        else:
            verificador_igualdad = False
            for i in range(len(self.informacion_hexagonos)):
                llave = str(i)
                if self.informacion_hexagonos[llave][1] == dados:
                    verificador_igualdad = True
                    break
            if verificador_igualdad == False:
                print("no existe ficha con aquellos dados")
                return
            material = self.informacion_hexagonos[llave][0]
            print(f"Repartiendo {self.informacion_hexagonos[llave][0]}")
            with self.lock_send:
                for nodo_adyacente in self.informacion_hexagonos[llave][2]:
                    nodo = self.tablero.nodos[nodo_adyacente]
                    if nodo.usado == True:
                        # AGREGAMOS 1 A LA CANTIDAD DEL MATERIAL 
                        # DEL USUARIO CORRESPONDIENTE A ESE NODO
                        self.estado_usuarios[nodo.usuario]["MATERIALES"][material] += 1
                        for skt in self.sockets:
                            self.send(
                                self.estado_usuarios, 
                                "NUEVO MATERIAL", 
                                skt)

    def crear_mapa(self):
        print("CREANDO MAPA...")
        time.sleep(0.1)
        with self.lock_send:
            lista_orden_hexagonos = self.logica_servidor.crear_lista_hexagonos()
            self.informacion_hexagonos = self.logica_servidor.crear_dict_hexagonos(
                lista_orden_hexagonos)
            print("MAPA CREADO")        
            for skt in self.sockets:
                self.send(lista_orden_hexagonos, "CARGAR MAPA", skt)
        # ESTA PARTE SIRVE PARA ASIGNAR 2 CHOZAS A LOS JUGADORES
        while True:
            nombres = list(self.usuarios_skt.keys())
            for usuario in nombres:
                contador = 0
                while contador < 2:
                    nodo = str(random.randint(0, 30))
                    self.tablero.nodos[nodo].caminos_adyacentes[0].construir_camino(
                        usuario, True)
                    construir = self.tablero.nodos[nodo].construir_vivienda(usuario)
                    if construir == True:
                        contador += 1
                        with self.lock_send:
                            for skt in self.sockets:
                                self.send(
                                    [self.estado_usuarios[usuario]["COLOR"], nodo],
                                    "AGREGAR CHOZA", skt)
                                self.estado_usuarios[usuario]["CHOZAS"] += 1
                        with self.lock_send:
                            for skt in self.sockets:
                                self.send(
                                    [self.estado_usuarios[usuario]["COLOR"], 
                                    self.tablero.nodos[nodo].caminos_adyacentes[0].valor],
                                    "AGREGAR CAMINO", skt)
                    else:
                        continue
            break
        with self.lock_send:
            for skt in self.sockets:
                self.send(
                    self.estado_usuarios,
                    "NUEVO MATERIAL",
                    skt)
        self.cambiar_turno()

    def cambiar_turno(self):
        '''
            Esta funcion funciona brinda el turno a el siguiente skt de manera circular,
            de forma que si ya se llego a el numero de usuarios vuelve a 0 ciclicamente.
            self.turno_actual parte con el numero mas grande de manera que el juego parta en 0.
        '''
        nombres = list(self.usuarios_skt.keys())
        self.turno_actual = self.logica_servidor.cambiar_turno(
            nombres, self.turno_actual, self.usuarios_skt)
            
        usuario_turno = nombres[self.turno_actual].replace('"', '')
        with self.lock_send:
            for skt in self.sockets:
                self.send(
                [usuario_turno, 
                self.estado_usuarios[usuario_turno]["COLOR"]], 
                "TURNO", skt)

    def online(self):
        while True:
            pass

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 47365

    Servidor(PORT, HOST)