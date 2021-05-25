
import json
from os.path import join

# with open("client/grafo.json") as file:
#     grafos = json.load(file)

with open(join("server", "parameters.json")) as file:
    grafos = json.load(file)

class Nodo():
    
    def __init__(self, valor):
        self.valor = valor
        self.usado = False
        self.vecinos = []
        self.caminos_adyacentes = []
        self.usuario = None
        
    def agregar_vecino(self, nodo):
        self.vecinos.append(nodo)

    def agregar_camino(self, camino):
        self.caminos_adyacentes.append(camino)

    def construir_vivienda(self, usuario):
        habilitar_construccion = True
        for vecino in self.vecinos:
            if vecino.usado == True:
                habilitar_construccion = False
                return False
            else:
                continue
        if habilitar_construccion == True:
            # Se puede construir
            for camino in self.caminos_adyacentes:
                if camino.usuario == usuario:
                    self.usado = True
                    self.usuario = usuario
                    return True

    def definir_posicion(self, x, y):
        self.posicion = (x, y)
        
    def __repr__(self):
        texto = f"[{self.valor}]"
        if len(self.vecinos) > 0:
            textos_vecinos = [f"[{vecino.valor}]" for vecino in self.vecinos]
            texto += " -> " + ", ".join(textos_vecinos)
        return texto

class Camino():
    
    def __init__(self, valor, nodo1, nodo2):
        self.valor = valor
        self.usado = False
        self.usuario = None
        self.nodos_adyacentes = [nodo1, nodo2]

    def construir_camino(self, usuario, inicio):
        # primero checkeamos si hay una choza
        if inicio == True:
            self.usado = True
            self.usuario = usuario
            return True
        for nodo in self.nodos_adyacentes:
            if nodo.usado == True:
                print("-"*20)
                print("Construyendo camino al lado de una casa")
                print("-"*20)
                if nodo.usuario == usuario:
                    self.usado = True
                    self.usuario = usuario
                    return True
            else:
                continue
        # Si no habia, chequeamos si existe algun camino adyacente
        for nodo in self.nodos_adyacentes:
            for camino in nodo.caminos_adyacentes:
                if camino == self:
                    continue
                else:
                    if camino.usado == True:
                        if camino.usuario == usuario:
                            print("-"*20)
                            print("Construyendo camino al lado de otro camino")
                            print("-"*20)
                            self.usado = True
                            self.usuario = usuario
                            return True
                        else:
                            continue
        # Si ninguno funciono, retornamos diciendo que no es valido
        return False

class Tablero():
    def __init__(self):
        # nodos es un dict con una instancia de cada nodo
        self.nodos = {}
        self.caminos = {}
        self.info_nodos_vecinos = grafos["nodos"]
        for valor in list(self.info_nodos_vecinos.keys()):
            self.nodos[valor] = Nodo(valor)

        for valor in list(self.info_nodos_vecinos.keys()):
            lista_nodos_vecinos = self.info_nodos_vecinos[valor]
            for nodo_vecino in lista_nodos_vecinos:
                self.nodos[valor].agregar_vecino(self.nodos[nodo_vecino])

        for nodo in list(self.nodos.values()):
            for vecino in nodo.vecinos:
                if int(vecino.valor) < int(nodo.valor):
                    camino = Camino(str(len(self.caminos)), nodo, vecino)
                    nodo.caminos_adyacentes.append(camino)
                    vecino.caminos_adyacentes.append(camino)
                    self.caminos[str(len(self.caminos))] = camino
        

if __name__ == "__main__":
    
    tablero = Tablero()
    print(tablero.nodos["11"])
    print(tablero.nodos["11"].vecinos)
    print(tablero.nodos)
    info_caminos = {}    
    for camino in tablero.caminos.values():
        nodos_valor = []
        for nodo in camino.nodos_adyacentes:
            nodos_valor.append(nodo.valor)
        info_caminos[camino.valor] = nodos_valor

    json_dict = json.dumps(info_caminos)
    print(json_dict)