import os
from random import choice, sample

from bolsillo import BolsilloCriaturas
from entidades import Criatura, Entrenador


def cargar_criaturas(archivo_criaturas):
    # Completar
    diccionario = {}
    with open(archivo_criaturas) as archivo:
        for row in archivo:
            lista = row.split(",")
            if lista[0] == "Name":
                continue
            diccionario[lista[0]] = Criatura(lista[0],lista[1],lista[2],lista[3],lista[4],lista[5])

    return diccionario


def cargar_rivales(archivo_rivales):
    criaturas = cargar_criaturas("criaturas.csv")
    with open(archivo_rivales) as archivo:
        entrenadores = []
        bolsillo = BolsilloCriaturas()
        for row in archivo:
            lista = row.split(",")
            lista[1] = lista[1].strip().split(";")
            if lista[0] == 'entrenador':
                continue
            else:
                bolsillo.append(criaturas[lista[1][0]])
                bolsillo.append(criaturas[lista[1][1]])
                bolsillo.append(criaturas[lista[1][2]])
                bolsillo.append(criaturas[lista[1][3]])
                bolsillo.append(criaturas[lista[1][4]])
                bolsillo.append(criaturas[lista[1][5]])
                entrenadores.append(Entrenador(lista[0],BolsilloCriaturas))
                continue

    return entrenadores

def crear_jugador(nombre):
    criaturas = cargar_criaturas("criaturas.csv")
    nombres = criaturas.keys()
    bolsillo = BolsilloCriaturas()
    
    x = 0
    for i in nombres:
        bolsillo.append(criaturas[i])
        x += 1
        if x == 6:
            break
    entrena = Entrenador(nombre,bolsillo)
    return entrena
    # Completar


if __name__ == "__main__":
    # NO MODIFICAR
    # El siguiente codigo te ayudara a debugear este archivo.
    # Simplemente corre este archivo (cargar_datos.py)

    # Aquí revisamos si te encuentras en la ruta adecuada, para esto
    # vemos si el archivo criaturas.csv se encuentra dentro de la
    # carpera en la que estás trabajando
    if "criaturas.csv" not in list(os.walk(os.getcwd()))[0][2]:
        print(f"No estas en el directorio adecuado!")
    criaturas = cargar_criaturas("criaturas.csv")
    rivales = cargar_rivales("rivales.csv")
    jugador = crear_jugador("El Cracks")

    # Aquí revisamos si retornas lo adecuado, para esto se revisa si
    # lo retornado es una instancia de la clase correspondiente
    if (type(criaturas) is not dict or \
        not all(type(criatura) is Criatura for criatura in criaturas.values())):
            print("Recuerda: cargar_criaturas retorna un diccionario con Criatura")
    else:
        print("Lista de Criatura tiene formato correcto")
    if type(rivales) is not list or not all(type(rival) is Entrenador for rival in rivales):
        print("Recuerda: cargar_rivales retorna una lista de Entrenador")
    else:
        print("Lista de Entrenador tiene formato correcto")

    # Aquí revisamos que los datos que deben ser entregados como int
    # al __init__ de Criaturas se almacenen con el tipo correcto
    if type(criaturas) is dict:
        if not all(
            type(atributo) is int
            for criatura in criaturas.values()
            for atributo in [criatura.hp_base, criatura.atk, criatura.sp_atk, criatura.defense]
        ):
            print("Recuerda: los atributos de Criatura hp, atk, sp_atk y defensa deben ser int")
        else:
            print("Instancias de Criatura tienen atributos con tipo correcto")

    # Aquí revisamos que la cantidad de Criaturas en el Bolsillo del
    # Jugador sea la adecuada
    if type(jugador) is not Entrenador or len(jugador.bolsillo) < 6:
        print("Recuerda: debes agregar 6 Criaturas a tu bolsillo")
    else:
        print("Jugador tiene la cantidad correcta de Criatura en su Bolsillo")
