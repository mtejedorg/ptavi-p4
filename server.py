#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time
registro = {}
class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def register2file(self):
        fich = open("registered.txt" ,"w") #abro fichero para escribir 
        fich.write("User" + "\t" + "IP" + "\t" + "Expires" + "\r\n")
        for clave in registro:            
            hora = time.strftime('%Y-%m-%d %H:%M:%S' , time.gmtime(time.time()))
            fich.write (clave + "\t" + registro[clave][0] + "\t" + hora +"\r\n")
        fich.close()

            
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
            print line

 
            if line [0] == "REGISTER" and line [2] == "SIP/1.0": #me llega un registrer mando 200 OK
                
                    self.wfile.write(" SIP/1.0 200 OK\r\n\r\n")
                    
            line[1] = line[1].split(":") #quiero el correo sin sip corto antes para poder usar line[1][1]
            if line[4] != "0" : #si el expires es 0 no le meto en el diccionario
                registro[line[1][1]] = [str(self.client_address[0]),line[4]] #tenemos un diccionario con valor una lsta/
                
                #llamada a la funcion para el FICHERO
                #llamo a la funcion y la creo arriba.
                self.register2file()

                print registro       
            if line[4] == "0":
                if line[1][1] in registro:
          
                    print line[1][1], "a"
                    del registro[line[1][1]] #borro del diccionario
                    self.wfile.write(" SIP/1.0 200 OK\r\n\r\n")
                    print registro
            

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    SERVER = int(sys.argv[1]) 
    serv = SocketServer.UDPServer(("", SERVER), SIPRegisterHandler) #Instanciamos EchoHandler
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
