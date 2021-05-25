import os


def reparar_imagen(ruta_entrada, ruta_salida):
    #--- COMPLETAR ---#
    archivo = open(ruta_entrada, "rb")
    byte = archivo.read()
    array = bytearray(byte)
    TAMANO_CHUNK = 32

    for i in range(0, len(array), TAMANO_CHUNK):
        # Aqui obtenemos nuestro chunk
        # print(array[i])
        if array[i] == 1:
            print(array[i:i+15])
            seccion = array[i:i+15]
            seccion = seccion[::-1]
        



#--- NO MODIFICAR ---#
def reparar_imagenes(carpeta_entrada, carpeta_salida):
    for filename in os.listdir(os.path.join(os.getcwd(), carpeta_entrada)):
        reparar_imagen(
            os.path.join(os.getcwd(), carpeta_entrada, filename),
            os.path.join(os.getcwd(), carpeta_salida, filename)
        )


if __name__ == '__main__':
    try:
        reparar_imagenes('corruptas', 'caratulas')
        print("Imagenes reparadas (recuerda revisar que se carguen correctamente)")
    except Exception as error:
        print(f'Error: {error}')
        print("No has podido reparar las caratulas :'c")
