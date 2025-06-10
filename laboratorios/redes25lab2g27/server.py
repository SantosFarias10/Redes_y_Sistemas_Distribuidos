#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
import sys
import threading
from connection import Connection
from constants import *

class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):

        print("Serving %s on %s:%s." % (directory, addr, port))

        # Set server address family for IPv4
        # "AF_INET sockets use IP addresses and port numbers
        # for communication."
        self.s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.addr = addr
        self.port = port
        self.directory = directory
        self.s.bind((self.addr, self.port))
        self.s.listen(5) # 5 Porque somos 4 en el grupo mas el profe

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez, creando
        un thread para tratar cada conexion.
        """
        try:
            while True:
                # Acepta la conexion, devolviendo un socket nuevo y la
                # direccion del cliente.
                connSocket, addrClient = self.s.accept()

                # Conecta al socket que recibió y lo posiciona en el
                # directorio aclarado.
                connection = Connection(connSocket, self.directory)
                
                # Crea un hilo con nombre único.
                # Este hilo llamará a la función handle del objeto creado
                # previamente.
                myThread = threading.Thread(target=connection.handle,
                                            name=f"Thread-{addrClient[1]}",
                                            daemon=True)
                myThread.start()

        except KeyboardInterrupt:
            print(f"\nShutting Down Server...")
        except Exception as e:
            print(f"{INTERNAL_ERROR} Internal Server Error: {e}")
        finally:
            self.s.close()


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)

    server.serve()


if __name__ == '__main__':
    main()
