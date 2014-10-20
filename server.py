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

    def handle(self):
        #Se ejecuta cada vez que recibimos una peticion del servidor
        # Escribe dirección y puerto del cliente (de tupla client_address)
 
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read() #saco lo que me llega en el mensaje 
            if not line: #miro primero si hay linea en blanco
                break  
            print "El cliente "+ str(self.client_address) + " nos manda " + line
            line = line.split() #troceo linea que me llega
            registro = {}
            registro[str(self.client_address[0])] = line[1]
            print registro
         
            
            if line [0] == "REGISTER" and line [2] == "SIP/1.0":
                self.wfile.write(" SIP/1.0 200 OK\r\n\r\n")
                   
            

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    SERVER = int(sys.argv[1]) 
    serv = SocketServer.UDPServer(("", SERVER), SIPRegisterHandler) #Instanciamos EchoHandler
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
