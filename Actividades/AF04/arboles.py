class Nodo:
    def __init__(self, tipo, valor, padre):
        self.tipo = tipo
        self.valor = valor
        self.padre = padre

        self.hijos = []


class PlataformaMusical:
    def __init__(self, nombre_plataforma):
        self.raiz = Nodo("plataforma", nombre_plataforma, None)

    def agregar_cancion(self, info_cancion):
        # Completar
        genero = Nodo("genero", info_cancion["genero"], self.raiz)
        artista = Nodo("artista", info_cancion["artista"], genero)
        album = Nodo("album", info_cancion["album"], artista)
        cancion = Nodo("cancion", info_cancion["nombre"], album)
        self.raiz.hijos.append(genero)
        genero.hijos.append(artista)
        artista.hijos.append(album)
        album.hijos.append(cancion)

    def armar_arbol(self, informacion_canciones):
        print(f" Armando plataforma {self.raiz.valor} ".center(80, "*"))

        for cancion in informacion_canciones:
            self.agregar_cancion(cancion)

    def visualizar_arbol(self, nodo, margen=0):
        print(f'{"  " * margen}{nodo.valor}')
        if len(nodo.hijos) > 0:
            margen += 1
            for hijo in nodo.hijos:
                self.visualizar_arbol(hijo, margen)