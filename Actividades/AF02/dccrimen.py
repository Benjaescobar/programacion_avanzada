from estudiante import cargar_datos
from verificar import corregir_alumno, corregir_nota, inscripcion_valida


class GymPro(Exception): 
    #Completar
    pass
    def __init__(self, estudiante):
        self.profesor = estudiante.nombre
        self.carrera = estudiante.carrera
        print("Wait a minute... Who are you?")

    def evitar_sospechas(self):

        print("¡Cuidado, viene " + self.profesor + "! Solo estaba haciendo mi último push...")
    
    def detectar_profe(self):
        # Cree este metodo para derectar profes en el try, 
        # de esta forma si existe un profe se levanta un value error :D
        if self.carrera == "Profesor":
            raise ValueError("Chuta")


if __name__ == "__main__":
    datos = cargar_datos("alumnos.txt")
    nueva_base = dict()
    for alumno in datos.values():
        corregir_alumno(alumno)
        corregir_nota(alumno)
        nueva_base[alumno.n_alumno] = alumno
    for alumno in nueva_base.values():
        estudiante = GymPro(alumno)
        try:
            estudiante.detectar_profe()
            alumno.promedio = 7.0
            print("Hackeando nota...")

        except ValueError as error:  # Recuerda especificar el tipo de excepción que vas a capturar
            print(f"Error: {error}")
            estudiante.evitar_sospechas()

