#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    dicc = {}

    def handle(self):

        def register2file():
            fichero = open("registered.txt", 'w')
            fichero.write("User \t IP \t Expires \n")
            lista = []
            for name in self.dicc:
                if time.time() > self.dicc[name][1]:
                    lista.append(name)
            for name in lista:
                del self.dicc[name]

            for clave in self.dicc:
                expire = time.strftime('%Y-­%m-­%d %H:%M:%S', time.gmtime
                                       (float((self.dicc[clave][1]))))
                fichero.write(clave)
                fichero.write("\t")
                fichero.write(self.dicc[clave][0])
                fichero.write(expire)
                fichero.write("\r\n")
            fichero.close()

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
                expires = time.time() + int(lista[4])
                if expires == 0:
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    if usuario in self.dicc:
                        del self.dicc[usuario]
                        register2file()
                if expires > 0:
                    self.dicc[usuario] = [IP, expires]
                    self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                    register2file()

            else:
                pass
            if not line or "[""]":
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
