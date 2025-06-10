from flask import Flask, jsonify, request
import random
from proximo_feriado import NextHoliday

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'},
    {'id': 13, 'titulo': 'Cars 1', 'genero': 'Binario'}
]


def _obtener_nuevo_id():
    """ Returns last movie's id + 1 """
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    return 1


def _pelicula_aleatoria_segun_genero(genero: str):
    """ Returns a random movie based on requested 'genero' """
    lista = _peliculas_por_genero(genero)
    peli = random.choice(lista)
    return peli


def _peliculas_por_genero(genero: str):
    """ Returns an array with all matching movies given a 'genero' """
    lista_por_genero = []
    for peli in peliculas:
        if peli['genero'].lower() == genero.lower():
            lista_por_genero.append(peli)
    return lista_por_genero


def _verificar_json(data: str | None, movie = 0):
    if data == None: 
        return jsonify({'error': 'Pelicula no agregada', 
                        'reason': 'JSON vacio'})
    if movie:
        if 'titulo' not in data:
            return jsonify({'error': 'Pelicula no agregada', 
                            'reason': 'Titulo no otorgado'}), 400
        if 'genero' not in data:
            return jsonify({'error': 'Pelicula no agregada', 
                            'reason': 'Genero no otorgado'}), 400 
    return None 


def obtener_peliculas():
    """ Returns every movie on the server """
    return jsonify(peliculas), 200


def obtener_pelicula_title(titulo:str):
    """ Returns every movie on server that matches 'titulo' from given url.
        
        Args:
            titulo (string): Movie name filter.
        
        Returns:
            tuple[dict,HTTP]: Contains all matching movies in JSON format.
                              Empty if no movie was found.
    """
    lista = []
    for peli in peliculas:
        if titulo.lower() in peli['titulo'].lower():
            lista.append(peli)
    return jsonify(lista), 200 


def obtener_pelicula_id(id):
    """ Returns a movie given an id. 
        Returns instantly if id is out of range.
    """
    # Verificar si id está en rango
    maxId = _obtener_nuevo_id()
    if id > maxId: return jsonify({'message':'Pelicula no encontrada'}), 400 

    # Lógica para buscar la película por su ID y devolver sus detalles
    for pelicula in peliculas:
        if pelicula['id'] == id:
            return jsonify(pelicula), 200
    return jsonify({'message':'Pelicula no encontrada'}), 400 


def pelicula_aleatoria():
    """ Returns a random movie """
    peli = random.choice(peliculas)
    return jsonify(peli['titulo']), 200


def agregar_pelicula():
    """ 
        Adds a movie given a JSON with correct values. 
        Automatically gives id based on server disponiblity.
        Extra JSON values are ignored.
        
        Requires (At least):
            {'titulo':'movieTitle','genero':'movieGender'}
    """
    data = request.json
    # Manage bad requests
    error = _verificar_json(data,1)
    if error: return error

    nueva_pelicula = {
            'id': _obtener_nuevo_id(), 
            'titulo': data['titulo'],
            'genero': data['genero']
            }
    peliculas.append(nueva_pelicula)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id: int):
    """ 
        Replaces a movie's title and gender given correct JSON.
        Extra JSON values are ignored.
        
        Requires (At least):
            {'titulo':'movieTitle','genero':'movieGender'}
    """
    data = request.json

    # Manage bad requests
    error = _verificar_json(data,1)
    if error: return error

    # Lógica para buscar la película por su ID y actualizar sus detalles
    for peli in peliculas:
        if peli['id'] == id:
            peli['titulo'] = data['titulo']
            peli['genero'] = data['genero']
            pelicula_actualizada = peli
            return jsonify(pelicula_actualizada) 
    return jsonify({'message':"No se pudo actualizar la pelicula!",
                    'reason': 'id no encontrado'}), 400


def eliminar_pelicula(id: int):
    """
        "Deletes" a movie given id.
        Instead of deleting, the server moves the last movie to the (now) free
        place, also updating that movie's id with the requested one.

        Returns: 
            If OK, a message informing that movie was updated.
            If movie is not found or its id is out of range, 
            a message indicating error with no changes.
    """
    if 0 < id < _obtener_nuevo_id():
        # Lógica para buscar la película por su ID y eliminarla
        for pelicula in peliculas:
            if pelicula['id'] == id:
                pelicula['titulo'] = peliculas[-1]['titulo']
                pelicula['genero'] = peliculas[-1]['genero']
                peliculas.pop()
                return jsonify({'message': (f'Pelicula con id {id} eliminada '
                                'correctamente')}), 200

    return jsonify({'message': ('Pelicula no encontrada. '
                    'No se han realizado cambios')}), 400 


def recomendar_pelicula_feriado(genero):
    """
       Returns a movie given a 'genero'. Also indicating next holiday's date. 
    """
    # Crea instancia de la clase
    next_holiday = NextHoliday()
    # Llama la funcion que devuelve los feriados para guardarla en 
    # next_holiday.holiday
    next_holiday.fetch_holidays()

    # Guarda el proximo feriado
    proximo_feriado = next_holiday.holiday
    day = proximo_feriado['dia']
    month = proximo_feriado['mes']
    year = next_holiday.year
    motivo = proximo_feriado['motivo']
    # Busca una pelicula aleatoria del genero pedido
    pelicula_encontrada = _pelicula_aleatoria_segun_genero(genero)

    return jsonify({'feriado': {'fecha': f"{day}/{month}/{year}",
                                'motivo': motivo},
                    'pelicula_sugerida': pelicula_encontrada},), 200


def recomendar_feriado_por_tipo(genero, tipo):
    next_holiday = NextHoliday()
    next_holiday.buscar_feriado(tipo)

    pelicula_encontrada = _pelicula_aleatoria_segun_genero(genero)

    proximo_feriado = next_holiday.holiday
    day = proximo_feriado['dia']
    month = proximo_feriado['mes']
    year = next_holiday.year
    tipo_feriado = proximo_feriado['tipo']

    return jsonify({'feriado': {'fecha': f"{day}/{month}/{year}",
                                'tipo': tipo_feriado},
                    'pelicula_sugerida': pelicula_encontrada},), 200


# GET rules
app.add_url_rule('/peliculas', 'obtener_peliculas', 
                 obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula_id', 
                 obtener_pelicula_id, methods=['GET'])
app.add_url_rule('/peliculas/<string:titulo>', 'obtener_peliculas_title', 
                 obtener_pelicula_title, methods=['GET'])
app.add_url_rule('/peliculas/random', 'pelicula_aleatoria', 
                 pelicula_aleatoria, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/<string:genero>', 'recomendar_pelicula', 
                 recomendar_pelicula_feriado, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/<string:genero>/<string:tipo>', 'recomendar_feriado_por_tipo', recomendar_feriado_por_tipo, methods=['GET'])


# POST rules
app.add_url_rule('/peliculas', 'agregar_pelicula', 
                 agregar_pelicula, methods=['POST'])

# PUT rules
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', 
                 actualizar_pelicula, methods=['PUT'])

# DELETE rules
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', 
                 eliminar_pelicula, methods=['DELETE'])

if __name__ == '__main__':
    app.run()
