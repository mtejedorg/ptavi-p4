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
        self.wfile.write("Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            palabras = line.split(" ")
            if palabras[0] == "REGISTRAR":
                print "Recibido cliente nuevo"
                clients.append([palabras[1], self.client_address])
                print "Cliente agregado"
                self.wfile.write("Bienvenido!!!")
            else:
                print "El cliente nos manda " + line
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if len(sys.argv) == 2:
        serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
        print "Lanzando servidor UDP de eco..."
        serv.serve_forever()
    else:
        print "Usage: $python server.py <port>"
