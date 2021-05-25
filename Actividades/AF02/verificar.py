from estudiante import cargar_datos, cargar_datos_corto


def verificar_numero_alumno(alumno):  # Levanta la excepción correspondiente
    numero_alumno = alumno.n_alumno
    if alumno.carrera == "Ingeneria":
        digito_carrera = "63"
    elif alumno.carrera == "College":
        digito_carrera = "61"
    
    if numero_alumno.isalnum:
        if numero_alumno[-1] == "J":
            pass
        else:
            raise ValueError("El numero de alumno es incorrecto")

    if numero_alumno[0] + numero_alumno[1] == str(alumno.generacion)[-2:]:
        if numero_alumno[2] + numero_alumno[3] == digito_carrera:
            pass
        else:
            raise ValueError("El numero de alumno es incorrecto")

    return True

def corregir_alumno(estudiante): # Captura la excepción anterior
    try:
        verificar_numero_alumno(estudiante)
    
    except ValueError as error:
        print(f"Error: {error}")
        print("El numero esta malo, arreglando...")
        if estudiante.carrera == "Ingeniería":
            digito_carrera = "63"
        elif estudiante.carrera == "College":
            digito_carrera = "61"
        elif estudiante.carrera == "Profesor":
            digito_carrera = "60"

        estudiante.n_alumno = str(estudiante.generacion)[2] + str(estudiante.generacion)[3] + digito_carrera
    
    else:
        print("El codigo esta correcto!")

    finally:
        print(estudiante.nombre + " esta correctamente inscrite en el curso, todo en orden \n")
        
# ************

def verificar_inscripcion_alumno(n_alumno, base_de_datos): # Levanta la excepción correspondiente
    if n_alumno not in base_de_datos:
        raise KeyError("El numero de alumno no se encuentra en la base de datos.")

    return base_de_datos[n_alumno]

def inscripcion_valida(estudiante, base_de_datos):  # Captura la excepción anterior
    try:
        verificar_inscripcion_alumno(estudiante.n_alumno,base_de_datos)
    except KeyError:
        print("¡Alerta! ¡Puede ser Dr. Pinto intentando atraparte!\n")

# ************

def verificar_nota(alumno):  # Levanta la excepción correspondiente
    if not isinstance(alumno.promedio, float):
        raise TypeError("El promedio no tiene el tipo correcto")
    return True


def corregir_nota(estudiante):  # Captura la excepción anterior
    try:
        verificar_nota(estudiante)
    except TypeError as error:
        print(f"Error: {error}")
        estudiante.promedio = str(estudiante.promedio).replace(",",".")
        estudiante.promedio = float(estudiante.promedio)
    finally:
        print("Procediendo a hacer git hack sobre " + str(estudiante.promedio) + "...\n")


if __name__ == "__main__":
    datos = cargar_datos_corto("alumnos.txt")  # Se cargan los datos
    for alumno in datos.values():
        if alumno.carrera != "Profesor":
            corregir_alumno(alumno)
            inscripcion_valida(alumno, datos)
            corregir_nota(alumno)
