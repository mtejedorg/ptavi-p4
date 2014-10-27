#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

clients = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """

    def handle(self):
        print "Dirección del cliente: ",
        print self.client_address
        Data = "Hemos recibido tu peticion"
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            palabras = line.split(" ")
            if palabras[0] == "REGISTER":
                print "Registrando cliente nuevo..."
                clients[palabras[1]] = self.client_address[0]
                print "...cliente agregado: ",
                print self.client_address
                Data += "\r\nSIP/1.0 200 OK\r\n\r\n    Bienvenido!!!"
            else:
                print "Un cliente nos manda " + line
                self.wfile.write(Data)
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if len(sys.argv) == 2:
        serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
        print "Lanzando servidor UDP de SIP Register..."
        serv.serve_forever()
    else:
        print "Usage: $python server.py <port>"
