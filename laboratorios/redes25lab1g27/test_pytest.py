import requests
import pytest
import requests_mock

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, 
               json={'id': 3, 'titulo': 'Pelicula de prueba', 
                     'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película 
        # específica
        m.get('http://localhost:5000/peliculas/1', 
              json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, 
              json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)
        
        # Simulamos la respuesta para que nos recomiende una pelicula segun un 
        # genero dado para ver en un feriado
        m.get('http://localhost:5000/peliculas/sugerir/Acción', 
              json={'feriado': {'fecha': '01/01/2023','motivo': 'Año Nuevo'},
                    'pelicula_sugerida': {'id': 1,
                                          'titulo': 'Indiana Jones',
                                          'genero': 'Acción'}})
        
        # Simulamos la respuesta para buscar una pelicula por el titulo 
        m.get('http://localhost:5000/peliculas/the', json=[
            {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
            {'id': 6, 'titulo': 'Back to the Future', 
             'genero': 'Ciencia ficción'}])
        
        # Simulamos la respuesta para buscar una pelicula para un feriado
        m.get('http://localhost:5000/peliculas/sugerir/Acción/Inolvidable', json={
            'feriado': {'fecha': {
                'dia': 1,
                'mes': 1,
                'año': 2023},'tipo': 'Inolvidable'},
            'pelicula_sugerida': {'id': 1,
                                  'titulo': 'IndianaJones',
                                  'genero': 'Acción'}})
        
        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', 
                             json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', 
                            json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_buscar_pelicula(mock_response):
    titulo = "the"
    response = requests.get(f'http://localhost:5000/peliculas/{titulo}')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200

def test_obtener_pelicula_para_feriado(mock_response):
    response = requests.get('http://localhost:5000/peliculas/sugerir/Acción')
    peli = response.json()['pelicula_sugerida']
    assert response.status_code == 200
    assert peli['genero'] == 'Acción'

def test_recomendar_feriado_por_tipo(mock_response):
    response = requests.get('http://localhost:5000/peliculas/sugerir/Acción/Inolvidable')
    feria = response.json()['feriado']
    peli = response.json()['pelicula_sugerida']
    assert response.status_code == 200
    assert peli['genero'] == 'Acción'
    assert feria['tipo'] == 'Inolvidable'