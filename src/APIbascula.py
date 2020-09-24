import serial
import io
import requests
import time
import json
import traceback, sys
from datetime import datetime


class APIbascula:
    """
    Clase controladora de la bascula.
    Permite leer el peso, el estado de esta y enviarle comandos.

    Dependiendo del sistema, es posible que requiera
    ejecutarse con privilegios (sudo).
    """

    def __init__(self):
        # costantes
        self.DP = False #enable Debug Prints
        self.SERIAL_PORT = "/dev/ttyUSB0"
        self.SER = None #
        self.LAST_ERR = "Aun no hay errores :)"


    def comprobarConexion(self):
        """
        Comprueba que la conexion con la bascula es correcta y esta lista.

        Return:
            True  -> la conexion es correcta y esta lista para usarse
            False -> hay un fallo en la conexion. No deberia usarse
        """
        return self.iniciarConexion()


    def iniciarConexion(self):
        """ Inicia la conexion con el puerto serie de la bascula"""
        try:
            self.SER = serial.Serial(self.SERIAL_PORT)
            if(self.DP):print(self.SER.name,"USB Correcto")
            return True
        except:
            if(self.DP):print("USB desconectado.")
            self.SER = None
            self.LAST_ERR = sys.exc_info()
            return False


    def iniciarConexionLoop(self):
        """ Llamada bloqueante que entra en bucle hasta que la conexion esta lista. """
        while True:
            try:
                self.SER = serial.Serial(self.SERIAL_PORT)
                if(self.DP):print(self.SER.name,"\rUSB Correcto                                        \n\n")
                break
            except:
                self.LAST_ERR = sys.exc_info()
                if(self.DP):print("USB desconectado.       Esperando conexion...", end='\r')


    def enviarComando(self, comando):
        """
        Funcion que envia un comando a la bascula.

        El comando debe self.SER un string y, a menos que lo especifique,
        debe terminar en CR (retorno de carro ó /r con la otra barra)


        comandos:
        A    Petición de peso en formato F4
        G    Equivalente a las teclas EXIT + TARA
        P    Petición de peso con respuesta según el formato seleccionado (estado + peso)
        Q    Equivalente a la tecla PRINT
        R    Reinicialización del equipo
        T    Equivalente a la tecla TARA
        Z    Equivalente a la tecla ZERO
        S    Equivalente a la tecla E
        E    Equivalente a la tecla EXIT + E
        $    Petición de peso: El comando no requiere <CR>
        STX, ENQ, ETX Petición de peso: El comando no requiere <CR>
        SYN Petición de peso con estabilidad. Si el peso no es estable, espera a mandarlo.
        El comando no requiere <CR>

        """
        # enviamos la peticion
        peticion = comando.encode()
        if(self.DP):print("Enviando peticion ", peticion)
        try:
            self.SER.write(peticion)
            if(self.DP):print("Comando ", peticion, " enviado correctamente.")
        except:
            self.LAST_ERR = sys.exc_info()
            if(self.DP):print("Error al enviar el comando")



    def obtenerPeso(self):
        """
        Funcion que pide por comando el peso y su estado y los devuelve.

        Return:
            devuelve (estado, peso)

            estado (string):
                +  -> El peso es estable
                -  -> El peso es negativo
                ?  -> El peso NO es estable

            peso (float) en Kg

        Inicia la conexion automaticamente si no esta iniciada
        Si la conexion falla, devuelve (None, None)

        [!] Esta funcion podria self.SER bloqueante y quedar atascada.

        """

        if self.comprobarConexion():
            # realizamos la peticion del Peso
            self.enviarComando("P\r")

            # obtenemos los datos
            if(self.DP):print("obteniendo Datos:")
            data = self.SER.readline()
            if(self.DP):print("Datos: ", data)

            estado = str(data.decode("utf-8"))[1:2]
            peso = float(str(data.decode("utf-8"))[2:9])

            if(self.DP):print("Estado: " + estado)
            if(self.DP):print("Peso: " + str(peso) + " Kg\n")

            return peso, estado

        else:
            if(self.DP):print("Fallo en la obtencion del peso")
            return None, None


    def leerDatos(self):
        """
        Funcion que lee los datos que ofrezca la bascula hasta un salto de linea.
        Devuelve un String con los datos decodificados

        Si la conexion falla, devuelve None

        [!] Esta funcion podria self.SER bloqueante y quedar atascada.

        """
        if self.comprobarConexion():
            # obtenemos los datos
            if(self.DP):print("obteniendo datos:\n")
            data = self.SER.readline()
            if(self.DP):print("Datos: ", data)

            return data.decode("utf-8")

        else:
            if(self.DP):print("Fallo en la obtencion de datos")
            return None


    def ultimoError(self):
        """ Devuelve el ultimo error que se ha producido en un string. """
        return str(self.LAST_ERR)



##########  TESTING AREA  ##########

test = False

if test:
    B = APIbascula()


    # prueba de peticion rapida
    print("Prueba de peso rapido")
    ret = B.obtenerPeso()
    print("Peso: ",  ret[0])
    print("Estado ", ret[1])
    print(B.ultimoError())


    # prueba de peticion personalizada
    pet = "$"
    print("\n\nPrueba de peticion independiente (", pet[0], ")")
    B.enviarComando(pet)
    dat = B.leerDatos()
    print("datos: ", dat)
    print(B.ultimoError())
