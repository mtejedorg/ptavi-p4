#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

if len(sys.argv) != 6:
    sys.exit("Usage: client.py ip puerto "
             "register sip_address expires_value")

# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
usuario = sys.argv[4]
expires = sys.argv[5]

# Contenido que vamos a enviar
LINE = "REGISTER sip:" + usuario + " SIP/2.0\r\n\r\n"
LINE1 = "Expires: " + expires + "\r\n\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print LINE
print LINE1
my_socket.send(LINE + LINE1 + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
