import requests
import random

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Buscar peliculas por titulo
print("Busqueda de peliculas que tengan 'the' en el titulo:\n")
titulo = "the"
response = requests.get(f'http://localhost:5000/peliculas/{titulo}')
if response.status_code == 200:
    lista = response.json()
    for peli in lista:
        print(peli)
else: print("Error al buscar pelicula")

# Buscar dejando espacios y palabras incompletas
print("Buscar usando espacios:\n")
response = requests.get(f'http://localhost:5000/peliculas/ana%20jon')
if response.status_code == 200:
    lista = response.json()
    for peli in lista:
        print(peli)
else: print("Error al buscar pelicula")

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")


# Verificar si pelicula con ID = 1 fue reemplazada correctamente
print("Verificar si pelicula con ID = 1 fue reemplazada correctamente")
response = requests.get(f"http://localhost:5000/peliculas/1")
if response.status_code == 200:
    print("Película con id 1 encontrada!")
 

# Recomendar Pelicula segun genero dado para ver el proximo feriado
# Primero obtiene todos los generos de las peliculas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
listaGeneros = []
for peli in peliculas:
    listaGeneros.append(peli['genero'])


# Selecciona aleatoriamente un genero
generoRandom = random.choice(listaGeneros)
response = requests.get(f'http://localhost:5000/peliculas/sugerir/{generoRandom}')

if response.status_code == 200:
    data = response.json()
    feriado = data['feriado']
    pelicula = data['pelicula_sugerida']
    print()
    print("Pelicula segun genero para ver en el proximo feriado:")
    print(f"Para feriado del {feriado['fecha']}, con Motivo {feriado['motivo']}") 
    print("Pelicula encontrada segun el genero", generoRandom)
    print(f"Ver pelicula {pelicula['titulo']}")
else:
    print("Error al encontrar pelicula de genero random para ver el proximo feriado")

# Recomendar Pelicula segun genero dado y el tipo de feriado
listasFeriados = ['Inolvidable','Trasladable','NoLaborable','Puente']
generaFeriadoRandom = random.choice(listasFeriados)
response = requests.get(f'http://localhost:5000/peliculas/sugerir/{generoRandom}/{generaFeriadoRandom}')
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error al encontrar pelicula de genero: {generoRandom} o tipo de feriado: {generaFeriadoRandom}")