def buscar_info_artista(plataforma, artista_seleccionado):
    # Completar
    for genero in plataforma.raiz.hijos:
        for artista in genero.hijos:
            if artista.valor == artista_seleccionado:
                print(artista.valor)
                for album in artista.hijos:
                    print("Album: " + album.valor)
        
def buscar_mejor_plataforma(genero, plataformas):
    contador_amazon = 0
    contador_spotify = 0
    contador_youtube = 0
    for plataforma in plataformas:
        for genero_buscado in plataforma.raiz.hijos:
            if genero_buscado.valor == genero:
                for artistas in genero_buscado.hijos:
                    for albumes in artistas.hijos:
                        for canciones in albumes.hijos:
                            if plataforma.raiz.valor == "Spotify":
                                contador_spotify += 1
                            elif plataforma.raiz.valor == "Amazon Music":
                                contador_amazon += 1
                            elif plataforma.raiz.valor == "YouTube Music":
                                contador_youtube += 1

    if contador_spotify > contador_amazon and contador_spotify > contador_youtube:          
        return plataformas[0]
        # plataforma_escogida = "Spotify"
    elif contador_amazon > contador_spotify and contador_amazon > contador_youtube:  
        return plataformas[1]
    elif contador_youtube > contador_spotify and contador_amazon < contador_youtube:  
        # plataforma_escogida = "Youtube Music"
        return plataformas[2]
    else:
        return plataformas[2]
        # plataforma_escogida = "cualquiera"
    
    # print("para escuchar", genero, "te recomendamos que lo hagas en", plataforma_escogida)
        
def buscar_artistas_parecidos(nombre_cancion, plataforma):
    # Completar
    encontrado = False
    genero_cancion_solicitada = ""
    artista_cancion = ""
    lista_artistas_similares = []
    for genero in plataforma.hijos:
        if encontrado == False:
            for artista in genero.hijos:
                if encontrado == False:
                    for album in artista.hijos:
                        if encontrado == False:
                            for cancion in album.hijos:
                                if cancion.valor == nombre_cancion:
                                    encontrado = True
                                    genero_cancion_solicitada = genero.valor
                                    artista_cancion = artista.valor
    for genero in plataforma.hijos:
        if genero.valor == genero_cancion_solicitada:
            for artista in genero.hijos:
                if artista.valor == artista_cancion:
                    continue
                else:
                    lista_artistas_similares.append(artista.valor)

    return lista_artistas_similares

def crear_playlist(plataforma, genero_seleccionado, conceptos_canciones):
    # Completar
    playlist = []
    for genero in plataforma.hijos:
        if genero.valor == genero_seleccionado:
            for artista in genero.hijos:
                for album in artista.hijos:
                    for cancion in album.hijos:
                        for concepto in conceptos_canciones:
                            if concepto.upper() in cancion.valor.upper():
                                if not cancion.valor in playlist:
                                    playlist.append(cancion.valor)
    return playlist
                    
