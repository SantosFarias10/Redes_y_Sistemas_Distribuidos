**Video del laboratorio**
https://youtu.be/vPdigJxBrJk

# Laboratorio 2: **Aplicación Servidor**  
**Cátedra de Redes y Sistemas Distribuidos**  

## Objetivos  
- Aplicar la comunicación cliente/servidor mediante programación de sockets  
- Familiarizarse con protocolos de aplicación personalizados  
- Implementar un servidor de archivos en Python usando el protocolo HFTP  

## Protocolo HFTP  
### Características principales  
- **Protocolo**: Home-made File Transfer Protocol (HFTP)  
- **Capa de transporte**: TCP (puerto 19500 por defecto)  
- **Formato**: ASCII (todos los mensajes son legibles por humanos)  
- **Flujo**:  
  1. Cliente envía comando terminado en `\r\n`  
  2. Servidor responde antes de procesar siguiente comando  
  3. Conexión persiste hasta comando `quit`  

## Comandos HFTP  

### `get_file_listing`  
**Función**: Listar archivos disponibles  
**Formato**: 
get_file_listing\r\n
0 OK\r\n
archivo1.txt\r\n
archivo2.jpg\r\n
\r\n

### `get_metadata`  
**Función**:   Obtener tamaño de archivo (bytes)  
**Formato**:   
get_metadata <FILENAME>\r\n
0 OK\r\n
24576\r\n

### `get_slice`  
**Función**: Obtener fragmento de archivo (base64)  
**Parámetros**:  
- `OFFSET`: Byte inicial (≥0)  
- `SIZE`: Cantidad de bytes (≥0)  
**Formato**:  
get_slice <FILENAME> <OFFSET> <SIZE>\r\n
0 OK\r\n
VGhpcyBpcyB1biB... (base64)\r\n

### `quit`  
**Función**:   Terminar conexión  
**Formato**:   
quit\r\n
0 OK\r\n

## Manejo de Errores  

| Código | Categoría         | Descripción                                 | Acción del Servidor |
|--------|-------------------|---------------------------------------------|---------------------|
| 0      | Exito             | Operación completada                        | Continúa conexión   |
| 1XX    | Error fatal       | Problema grave (ej. formato inválido)       | Cierra conexión     |
| 2XX    | Error recuperable | Problema específico (ej. archivo no existe) | Permite nuevos comandos |

## Implementación del Servidor  

### Requisitos técnicos  
- Python 3.6+  
- Módulos esenciales:  
  ```python
  import socket
  import threading
  import base64
  import os
  ```

### Ejecución  
**Servidor**:  
```bash
python3 server.py -d ~/Documents/Redes/lab2/ -p 19500
```  

**Cliente**:  
```bash
python3 client.py -a 127.0.0.1 -p 19500
```  

### 1. Concurrencia en servidores  
¿Qué estrategias existen para poder implementar este mismo servidor pero con 
capacidad de atender múltiples clientes simultáneamente? Investigue y responda 
brevemente qué cambios serían necesarios en el diseño del código.

**Estrategias**:  
1. **Threading**:  
2. **Polling**:  

**Ventajas comparativas**:  
- Threading: Más simple para conexiones persistentes  
- Polling: Más eficiente para muchas conexiones cortas  

### 2. Comportamiento de direcciones IP  
Pruebe ejecutar el servidor en una máquina del laboratorio, mientras utiliza 
el cliente desde otra, hacia la ip de la máquina servidor. ¿Qué diferencia 
hay si se corre el servidor desde la IP "localhost", "127.0.0.1" o la ip "0.0.0.0"?

| Dirección   | Alcance              | Uso típico            |
|-------------|----------------------|-----------------------|
| 127.0.0.1   | Solo máquina local   | Pruebas desarrollo    |
| 0.0.0.0     | Todas las interfaces | Servidores en red     |

## Material de Apoyo  
### Video explicativo  
1. Introducción  
2. Demostración protocolo  
3. Explicación código clave  
4. Pruebas de robustez  

## Integrantes  
- Santino Ponchiardi  
- Luca Irrazabal  
- Brandon Michel  
- Santos Farias  

