#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        #Se ejecuta cada vez que recibimos una peticion del servidor
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion") #escribe esto cuando le llega algo
        #print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente "+ str(self.client_address) + " nos manda " + line
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    SERVER = int(sys.argv[1]) 
    serv = SocketServer.UDPServer(("", SERVER), EchoHandler) #Instanciamos EchoHandler
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
