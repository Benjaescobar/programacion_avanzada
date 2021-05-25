from collections import namedtuple, defaultdict


# Para esta parte necesitarás los contenidos de la semana 0
def cargar_datos(path):
    # Para esta función te puede servir el cuaderno 3 de la semana 0
    datos = []
    with open(path,"rt") as archivo:
        lineas = archivo.readlines()
        for l in lineas:
            linea = l.strip().split(",")
            if linea[0] == "Nombre":
                continue
            datos.append(linea)

    if datos is None:
        return None
    else:
        return datos
        

# De aquí en adelante necesitarás los contenidos de la semana 1
def crear_ayudantes(datos):
    # Completar función
    Ayudantes = namedtuple("Ayudantes",["nombre","cargo","usuario"])
    lista = []
    for dato in datos:
        lista.append(Ayudantes(dato[0],dato[1],dato[2]))

    return lista

def encontrar_cargos(ayudantes):
    # Completar función
    todos_cargos = []
    for tupla in ayudantes:
        todos_cargos.append(tupla[1])
    lista = set(todos_cargos)

    return lista

def ayudantes_por_cargo(ayudantes):
    # Completar función
    hibrido_docencia = []
    full_tareas = []
    full_docencia = []
    hibrido_tareas = []
    

    for ayudante in ayudantes:
        if ayudante[1] == " Híbrido Docencia":
            hibrido_docencia.append(ayudante)
        elif ayudante[1] == " Full Tareas":
            full_tareas.append(ayudante)
        elif ayudante[1] == " Full Docencia":
            full_docencia.append(ayudante)
        elif ayudante[1] == " Híbrido Tareas":
            hibrido_tareas.append(ayudante)

    dictionary = {}

    dictionary["Híbrido Docencia"] = hibrido_docencia
    dictionary["Full Tareas"] = full_tareas
    dictionary["Full Docencia"] = full_docencia
    dictionary["Híbrido Tareas"] = hibrido_tareas


    return dictionary


if __name__ == '__main__':
    datos = cargar_datos('ayudantes.csv')
    if datos is not None:
        print('Se lograron leer los datos')
    else:
        print('Debes completar la carga de datos')

    ayudantes = crear_ayudantes(datos)
    if ayudantes is not None:
        print('\nLos ayudantes son:')
        for ayudante in ayudantes:
            print(ayudante)
    else:
        print('\nDebes completar la creación de Ayudantes')

    cargos = encontrar_cargos(ayudantes)
    if cargos is not None:
        print('\nLos cargos son:')
        for cargo in cargos:
            print(cargo)
    else:
        print('\nDebes completar la búsqueda de Cargos')

    clasificados = ayudantes_por_cargo(ayudantes)
    print(clasificados)
    if clasificados is not None:
        print('\nLos ayudantes por cargos son:')
        for cargo in clasificados:
            print(f'\n{cargo}')
            for ayudante in clasificados[cargo]:
                print(ayudante)
    else:
        print('\nDebes completar la clasificación de Ayudantes')
        