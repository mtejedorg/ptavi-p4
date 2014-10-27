#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
coms = sys.argv
try:
    SERVER = coms[1]
    PORT = int(coms[2])

    if coms[3] != "register":
        # Contenido que vamos a enviar
        LINE = ""
        for com in coms[3:]:
            LINE += com + " "
    else:
        LINE = "REGISTER sip:" + coms[4] + "SIP/1.0\r\n\r\n"
except IndexError:
    print "Usage: $python client.py <ip> <puerto> <linea>"
    sys.exit()

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."



       
