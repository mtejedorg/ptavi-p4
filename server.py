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
            #Asumo que el mensaje REGISTER estará bien construido
            line = self.rfile.read()
            if not line:
                break

            print line
            lineas = line.split("\r\n")
            palabras = lineas[0].split(" ") + lineas[1].split(" ")
            if palabras[0] == "REGISTER":
                cliente = palabras[1][4:]
                print "Registrando cliente nuevo..."
                clients[cliente] = self.client_address[0]
                print "...cliente agregado: ",
                print self.client_address
                prot_ver = palabras[2].split("/")
                Data += "\r\n\r\n" + prot_ver[0] + "/" + prot_ver[1] + " 200 OK\r\n\r\n    Bienvenido!!!"
                exp = int(palabras[4])
                if exp == 0:
                    print "El tiempo de expiración es 0.",
                    del clients[cliente]
                    print "El cliente '" + cliente + "' ha sido borrado"
            self.wfile.write(Data)
            print "\r\n\r\n>> A la espera de nuevos clientes...\r\n\r\n"
            
if __name__ == "__main__":
    # Creamos servidor de register y escuchamos
    if len(sys.argv) == 2:
        serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
        print "Lanzando servidor UDP de SIP Register..."
        serv.serve_forever()
    else:
        print "Usage: $python server.py <port>"
