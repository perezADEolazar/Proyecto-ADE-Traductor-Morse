"""
Archivo: udp_socket.py
Creadores: Ian/Kerman
Fecha: 16/05/2024
Descripción: Archivo de configuracion para comunicación entre el celular y la Raspberry Pi
"""

#Importar librerías y archivos
import socket
import funcionalidad_morse

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 5002  # Puerto arbitrario

# Creación de un socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Enlazar el socket al host y puerto especificados
server_socket.bind((HOST, PORT))


# Bucle para recibir mensajes y mostrarlos en la terminal
def udp_socket():
    while True:
        # Recibir datos desde el cliente
        data, addr = server_socket.recvfrom(1024)  # Recibir hasta 1024 bytes de datos
        message = data.decode('utf-8')
        
        # Decodificar y mostrar los datos recibidos en la terminal
        print(message)
        funcionalidad_morse.print_message(funcionalidad_morse.morse_udp_traduction(message))
        # print("Mensaje recibido de {}: {}".format(addr, message))