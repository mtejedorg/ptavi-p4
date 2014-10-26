#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        IP = self.client_address[0]
        PUERTO = str(self.client_address[1])
        print "IP: " + IP + " PUERTO: " + PUERTO
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line
            lista = line.split()

            #Guarda la información registrada y la IP en un diccionario
            if lista[0] == "REGISTER":
                usuario = lista[1][4:]
                expires = int(lista[4])
                if expires == 0:
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    if usuario in self.dicc:
                        del self.dicc[usuario]
                        #print self.dicc[usuario]
                if expires > 0:
                    self.dicc[usuario] = [IP, expires]
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    #print self.dicc[usuario]

            else:
                pass
            if not line or "[""]":
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
