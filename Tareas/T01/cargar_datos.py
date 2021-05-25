from deporte import Deportistas

def cargar_deportistas():

    lista_atributos = []

    deportistas = {}
    with open("deportistas.csv") as archivo:
        for row in archivo:
            row = row.strip().split(",")
            row[0] = row[0].strip()
            # Se crea una lista en la que cada posicion contiene 
            # el nombre de un atributo
            if lista_atributos == []:
                for i in range(len(row)):
                    row[i] = row[i].strip()
                    if row[i] == "nombre":
                        lista_atributos.append("nombre")
                        continue
                    elif row[i] == "flexibilidad":
                        lista_atributos.append("flexibilidad")
                        continue
                    elif row[i] == "moral":
                        lista_atributos.append("moral")
                        continue
                    elif row[i] == "precio":
                        lista_atributos.append("precio")
                        continue
                    elif row[i] == "velocidad":
                        lista_atributos.append("velocidad")
                        continue
                    elif row[i] == "lesionado":
                        lista_atributos.append("lesionado")
                        continue
                    elif row[i] == "resistencia":
                        lista_atributos.append("resistencia")
                        continue

            if row[i] in lista_atributos:
                continue
            else:
                for i in range(len(row)):
                    row[i] = row[i].strip()
                    if lista_atributos[i] == "nombre":
                        nom = row[i]
                    elif lista_atributos[i] == "flexibilidad":
                        flex = int(row[i])
                    elif lista_atributos[i] == "moral":
                        mor = int(row[i])
                    elif lista_atributos[i] == "precio":
                        pr = int(row[i])
                    elif lista_atributos[i] == "velocidad":
                        vel = int(row[i])
                    elif lista_atributos[i] == "lesionado":
                        les = row[i]
                    elif lista_atributos[i] == "resistencia":
                        res = int(row[i])
                    
            deportistas[nom] = (Deportistas(nom, vel, res, flex, mor, les, pr))

    return deportistas

def cargar_delegaciones():
    delegaciones = {}
    deportistas = cargar_deportistas()
    lista_atributos = []
    with open("delegaciones.csv") as archivo:
        
        for row in archivo:
            row = row.strip().split(",")
            
            if lista_atributos == []:
                for i in range(len(row)):
                    row[i] = row[i].strip()
                    if row[i] == "Moral":
                        lista_atributos.append("Moral")
                        continue
                    elif row[i] == "Delegacion":
                        lista_atributos.append("Delegacion")
                        continue
                    elif row[i] == "Equipo":
                        lista_atributos.append("Equipo")
                        continue
                    elif row[i] == "Medallas":
                        lista_atributos.append("Medallas")
                        continue
                    elif row[i] == "Dinero":
                        lista_atributos.append("Dinero")
                        continue
            if row[i] in lista_atributos:
                # para que no se metan los titulos de la tabla en las delegaciones
                continue
            else:
                for i in range(len(row)):
                    row[i] = row[i].strip()
                    if lista_atributos[i] == "Moral":
                        moral = float(row[i])
                    elif lista_atributos[i] == "Delegacion":
                        delegacion = row[i]
                    elif lista_atributos[i] == "Equipo":
                        row[i] = row[i].strip().split(";")
                        lista_deportistas = []
                        for deportista in row[i]:
                            lista_deportistas.append(deportistas[deportista])

                    elif lista_atributos[i] == "Medallas":
                        medallas = int(row[i])
                    elif lista_atributos[i] == "Dinero":
                        din = int(row[i])

                delegaciones[delegacion] = [lista_deportistas, medallas, moral, din]
        return delegaciones

