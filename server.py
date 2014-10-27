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
        """Escribe en un fichero los usuarios registrados o dados de baja
           con sus valores."""

        fich = open("registered.txt" ,"w")  
        fich.write("User" + "\t" + "IP" + "\t" + "Expires" + "\r\n")
        for clave in registro:
            hora = time.strftime('%Y-%m-%d %H:%M:%S' , time.gmtime(registro[clave][2]))
            fich.write (clave + "\t" + registro[clave][0] + "\t" + hora +"\r\n")
        fich.close()
    
    def borrar_caducados(self,registro):
        """Gestiona la caducidad de los usuarios registrados"""
   
        list_caducados =[]
        for clave in registro:
            hora_entrada=registro[clave][2]
            expires = registro[clave][1]
            tiemp_a =time.time()
            if int(hora_entrada) + int(expires) <= tiemp_a :
                list_caducados.append(clave)
        for clave in list_caducados:
            del registro[clave]
    
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
                #guardo la hora en la que me conecto en segundos con time.time y la meto en el diccionario
                hora_s= time.time()
                registro[line[1][1]] = [str(self.client_address[0]),line[4],hora_s] #tenemos un diccionario con valor una lsta/
                
                #llamada a la funcion para el FICHERO y caducidad
               
                

                print registro       
            if line[4] == "0":
                if line[1][1] in registro:
          
                    print line[1][1], "a"
                    del registro[line[1][1]] #borro del diccionario
                    #self.register2file(registro) #para borrar del fichero si el usuario ya no esta
                    self.wfile.write(" SIP/1.0 200 OK\r\n\r\n")
                    print registro
            self.borrar_caducados(registro)
            self.register2file()

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    SERVER = int(sys.argv[1]) 
    serv = SocketServer.UDPServer(("", SERVER), SIPRegisterHandler) #Instanciamos EchoHandler
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
