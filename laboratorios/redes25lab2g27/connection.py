# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import os
import socket
import base64
from constants import *

class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket: socket.socket, directory):
        self.socket = socket
        self.directory = directory
        self.connected = True
        self.data_acc = ''
        self.send_buffer = b''
        self.peername = self.socket.getpeername()
        print(f"Connected to {self.peername[0]}:{self.peername[1]}")

    def send(self, msg: bytes):
        """
        Envia datos, manejando envios parciales.
        """
        self.send_buffer += msg

        try:
            while self.send_buffer:
                bytes_send = self.socket.send(self.send_buffer)
                self.send_buffer = self.send_buffer[bytes_send:]
        except BlockingIOError:
            pass

    def recv_line(self):
        """
        Lee datos hasta encontrar un EOL. Y retorna el comando o None si hay errores.
        """
        while True:
            try:
                data = self.socket.recv(1024).decode('ascii')
            except UnicodeDecodeError:
                self.send(f"{BAD_REQUEST} Non-ASCII characters{EOL}".encode())
                return None

            if not data: return None

            self.data_acc += data
            eol_index = self.data_acc.find(EOL)
            if eol_index != -1:
                command = self.data_acc[:eol_index + len(EOL)]
                self.data_acc = self.data_acc[eol_index + len(EOL):]
                return command

    def quit_handler(self, command):
        """
        Maneja el comando quit y sus errores.
        """
        parts = command.strip().split()
        if parts[0] == "quit" and len(parts) == 1:
            self.send(f"{CODE_OK} OK{EOL}".encode())
            self.connected = False
        elif len(parts[0]) > len("quit"):
            self.send(f"{INVALID_COMMAND} Invalid Command{EOL}".encode())
        else:
            self.send(f"{INVALID_ARGUMENTS} Invalid Arguments{EOL}".encode())

    def listing_handler(self, command):
        """
        Maneja el comando get_file_listing y sus errores.
        """
        parts = command.strip().split()
        if parts[0] == "get_file_listing" and len(parts) == 1:
            files = os.listdir(self.directory)
            self.send(f"{CODE_OK} OK{EOL}".encode())
            for file in files:
                self.send(f"{file}{EOL}".encode())
            self.send(f"{EOL}".encode())
        elif len(parts[0]) > len("get_file_listing"):
            self.send(f"{INVALID_COMMAND} Invalid Command{EOL}".encode())
        else:
            self.send(f"{INVALID_ARGUMENTS} Invalid Arguments{EOL}".encode())

    def metadata_handler(self, command):
        """
        Maneja el comando get_metadata y sus errores.
        """
        parts = command.strip().split()
        if parts[0] == "get_metadata" and len(parts) == 2 and len(parts[1]) < 255:
            try:
                filepath = os.path.join(self.directory, parts[1])
                stats = os.stat(filepath)
                size = stats.st_size
                self.send(f"{CODE_OK} OK{EOL}".encode())
                self.send(f"{size}{EOL}".encode())
            except FileNotFoundError:
                self.send(f"{FILE_NOT_FOUND} File Not Found{EOL}".encode())
        elif len(parts[0]) > len("get_metadata"):
            self.send(f"{INVALID_COMMAND} Invalid Command{EOL}".encode())
        elif len(parts) == 2 and len(parts[1]) >= 255:
            self.send(f"{FILE_NOT_FOUND} Exceded the 255 Bytes of name max length{EOL}".encode())
        else:
            self.send(f"{INVALID_ARGUMENTS} Invalid Arguments{EOL}".encode())

    def slice_handler(self, command):
        """
        Maneja el comando get_slice y sus errores.
        """
        parts = command.strip().split()
        if parts[0] == "get_slice" and len(parts) == 4 and len(parts[1]) < 255:
            try:
                filename = parts[1]
                offset = int(parts[2])
                size = int(parts[3])
                filepath = os.path.join(self.directory, filename)
                file = open(filepath, 'rb')
                text = file.read()
                textito = text[offset:offset+size]
                textoBase64 = base64.b64encode(textito).decode()
                self.socket.send(f"{CODE_OK} OK{EOL}".encode())
                self.socket.send(f"{textoBase64}{EOL}".encode())
            except FileNotFoundError:
                self.send(f"{FILE_NOT_FOUND} File Not Found{EOL}".encode())
            except:
                self.send(f"{INVALID_ARGUMENTS} Invalid Arguments{EOL}".encode())
        elif len(parts[0]) > len("get_slice"):
            self.send(f"{INVALID_COMMAND} Invalid Command{EOL}".encode())
        elif len(parts) == 2 and len(parts[1]) >= 255:
            self.send(f"{FILE_NOT_FOUND} Exceded the 255 Bytes of name max length{EOL}".encode())
        else:
            self.send(f"{INVALID_ARGUMENTS} Invalid Arguments{EOL}".encode())

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        try:
            while(self.connected):
                command = self.recv_line()
                if command is None:
                    break
                print("Request:", command)

                if command.startswith("quit"):
                    self.quit_handler(command)
                elif command.startswith("get_file_listing"):
                    self.listing_handler(command)
                elif command.startswith("get_metadata"):
                    self.metadata_handler(command)
                elif command.startswith("get_slice"):
                    self.slice_handler(command)
                else:
                    part = command.split(EOL, 1)
                    if "\n" in part[0]:
                        self.send(f"{BAD_EOL} Bad Eol{EOL}".encode())
                    else:
                        self.send(f"{INVALID_COMMAND} Invalid Command{EOL}".encode())

        except KeyboardInterrupt:
            self.connected = False
        except Exception as e:
            self.send(f"{INTERNAL_ERROR} Internal Error: {e}{EOL}".encode())
        finally:
            self.socket.close()
            print(f"\nClient {self.peername[0]}:{self.peername[1]} Disconnected")

