#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

clients = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIP server class
    """
    
    def register2file(self):
        fich = open("registered.txt", 'w')
        info = "User \t IP \t Expires\r\n"
        print clients
        for client in clients:
            info += client + " \t "
            info += clients[client]["IP"] + " \t "
            tiempo = time.gmtime(clients[client]["time"])
            str_time = time.strftime('%Y-%m-%d %H:%M:%S', tiempo)
            info += str_time + " \t "
            info += "\r\n"
        print info
        fich.write(info)
        fich.close()

    def register(self, line):
        lineas = line.split("\r\n")
        palabras = lineas[0].split(" ") + lineas[1].split(" ")
        if palabras[0] == "REGISTER":
            cliente = palabras[1][4:]
            prot_ver = palabras[2].split("/")
            Data = prot_ver[0] + "/" + prot_ver[1] + " 200 OK\r\n\r\n"
            expires = int(palabras[4])

            print "Registrando cliente nuevo..."
            time_act = time.time() + expires
            valor = {"IP": self.client_address[0], "time": time_act}
            clients[cliente] = valor
            print "...cliente agregado: ",
            print cliente + ": ",
            print valor
            print clients

            if expires == 0:
                print "El tiempo de expiración es 0.",
                del clients[cliente]
                print "El cliente '" + cliente + "' ha sido borrado"

            self.wfile.write(Data)

    def update(self):
        lista_tmp = []
        for client in clients:
            if clients[client]["time"] < time.time():
                lista_tmp.append(client)
        for client in lista_tmp:
            del clients[client]


    def handle(self):
        print "Dirección del cliente: ",
        print self.client_address
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            # Asumo que el mensaje REGISTER estará bien construido
            line = self.rfile.read()
            if not line:
                break

            print line

            self.register(line)
            self.update()
            self.register2file()

            print "\r\n\r\n>> A la espera de nuevos clientes...\r\n\r\n"
            
if __name__ == "__main__":
    # Creamos servidor de register y escuchamos
    if len(sys.argv) == 2:
        serv = SocketServer.UDPServer(("", int(sys.argv[1])), SIPRegisterHandler)
        print "Lanzando servidor UDP de SIP Register...\r\n\r\n"
        serv.serve_forever()
    else:
        print "Usage: $python server.py <port>"
