# Laboratorio 1: Desarrollo de una API #

* En este laboratorio creamos una API en el lenguaje de 
  programacion Python y el framework Flask. Esta dividido en
  cuatro partes:

  1. La configuracion del entorno de programacion
  en el que se desarrolla este laboratorio mediante la 
  creacion de un entorno virtual con virtualenv. 

  2. La construccion de la API principal, destinada a administrar una
  base de datos de peliculas que incluira un campo adicional
  para el genero de cada obra cinematografica.

  3. La integracion de nuestra API cinematografica con una
  API externa de feriados, utilizando la informacion sobre
  las proximas fechas festivas para recomendar peliculas que 
  se ajusten al genero solicitado para ese dia en particular.

  4. La evaluacion de la API, donde se consideraran aspectos
  cruciales como la respuesta de la API, codigos de estado 
  HTTP, escalabilidad y seguridad.

## Materiales del Laboratorio ##

*Link del Video*:
https://youtu.be/YGIoR565A7s?si=HpczvTTXQa-xWT-p

https://www.youtube.com/watch?v=YGIoR565A7s

**En teoria los dos links llevan al mismo video.**

*Power Point*:
Se encuentra en el repositorio.

## Requisitos ##

*Tener instalado*:
* Git
* Python

## Configuracion del entorno e instalacion de librerias ##

1. Clonar el repositorio.

2. Crear un entorno virtual de Python utilizando venv.
``` python3 -m venv .nombreDelEntornoVirtual ```
.venv es el nombre estandar.

3. Activar el entorno virtual.
``` source .venv/bin/activate ```

3Bis. Y para desactivarlo.
``` deactivate ```

4. Con venv activo instalamos las librerias de python
necesarias.
``` pip install -r requirements.txt ```

5. El servidor se levanta compilando el main.py:
``` python3 main.py ```

## Creacion de una API con Flask ##

*Implementaciones de funciones para*:
* Buscar una pelicula por su ID y devolver sus detalles.
* Buscar una pelicula por su ID y actualizar sus detalles.
* Buscar una pelicula por su ID y eliminarla.
* Devolver el listado de peliculas de un genero especifico.
* Busqueda de peliculas, devolviendo la listas de peliculas
  que tengan determinado string en el titulo.
* Sugerir una pelicula aleatoria.
* Sugerir una pelicula aleatoria segun genero.

## Consumo de una API externa ##

* Integramos nuestra API cinematografica con una API externa
  de feriados en Argentina.
* Implementamos una funcion que busca feriados por tipo.
  Sea Inamovible, Trasladable, No laborable y Puente.
* Implementamos en la API cinematografica utilizando la API 
  de feriados, una funcion que obtiene la proxima fecha de 
  feriado y recomienda una pelicula que se ajusta al genero
  solicitado para ese dia.

## Evaluacion de la API ##

* Ejecutamos y analizamos el test.py.
* Ejecutamos y analizamos con pytest el test_pytest.py.
* Agregamos los test para las funciones de ejercicios
  anteriores.
* Replicamos los request de test.py en Postman y analizamos 
  las respuestas.

## Decisiones de Diseño ##

1. La funcion para eliminar peliculas, no solo elimina la 
   pelicula del ID dado, sino que intercambia el nombre y 
   genero de la pelicula con la ubicada en la ultima posicion
   del diccionario (O la que tenga el ID mas alto), para 
   luego eliminar la ultima pelicula y seguir con los ID's 
   ordenados de menor a mayor. 

   Por ejemplo, si tenemos cinco peliculas y queremos 
   eliminar la tercera, primero intercambia los nombres y 
   generos de la quinta pelicula con la tercera para luego 
   eliminar la quinta pelicula. Que era la pelicula que 
   queriamos eliminar en un principio. 
   Esto nos deja siempre con los ID's ordenados.

   Esta decision se tomo para que no queden ID's inutilizados
   luego de eliminar una pelicula. 

2. Usamos una función privada que verifica la integridad de los datos 
    brindados en los JSON recibidos por parte del cliente.
    Dicha función verifica que sus los JSON no sean vacíos (Aunque Flask lo 
    maneja de forma automática) y, que en caso de darse un valor distinto de 0
    como segundo parámetro, también verificará que contenga los partes
    'titulo':'titulo de ejemplo' y 'genero':'genero de ejemplo'

### Made by ###

Santino Ponchiardi
Santos Facundo Adrian Farias 
Brandon Michel
Luca Alfredo Irrazabal

