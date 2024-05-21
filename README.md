# Proyecto ADE: Traductor Morse
<p align="center"><img src="https://github.com/perezADEolazar/Proyecto-ADE-Traductor-Morse/assets/167235174/30f20dfd-2916-4669-a746-93aa4d9f1696"/></p>

## Tabla de contenidos:
---
- [Introducción](#introducción-🚀)
- [Configuración software](#configuración-software)
- [Configuración hardware](#configuración-hardware)
- [Modo de uso](#modo-de-uso)
  
## Introducción 🚀

Este repositorio contiene el código fuente para la implementación de un traductor de código Morse en una Raspberry Pi. El proyecto se encuentra diseñado para escribir caracteres en Morse mediante un botón y/o la terminal del celular e imprimir en una pantalla LCD la traducción en alfabeto latino. Además, las dos luces LED incluidas en el proyecto permiten al usuario monitorizar el estado de la traducción/envio de caracteres, proporcionando una interfaz simple e intuitiva para dar los primeros pasos en el aprendizaje del código Morse.

A continuación, se encuentran descritos los requisitos y el proceso a seguir para configurar el proyecto.

## Configuración software 📄

Los archivos necesarios para configurar el proyecto se encuentran divididos en tres grupos: configuración de periféricos, función de traducción y arranque automático. 

### Configuración de periféricos 💡

Algunos dispositivos externos utilizados en este proyecto requieren la configuración mediante software de varios puertos de la Raspberry Pi. Concretamente, las dos luces LED y el botón se comunican mediante los puertos GPIO y la pantalla LCD utiliza el protocolo I2C con los canales SDA y SCL. Además, el envio de los mensajes traducidos al celular se realiza mediante protocolo UDP. 

*El control de los puertos GPIO se realiza en código C mediante las librerias **pigpio**, **stdlib** y **stdio** y requiere la compilación para su ejecución:*

```
//Importar librerias y archivos
#include <stdio.h>
#include <stdlib.h>
#include <pigpio.h>

//Definir pines GPIO a utilizar
#define GreenledPin 26
#define RedledPin 20
#define ButtonPin 12
```

Comando de compilación en Linux:
```
gcc -o control_gpio control_gpio.c
```

*La comunicación con la pantalla se realiza en código Python utilizando la libreria **smbus** y define una dirección de memoria para el dispositivo:*

```
#Importar librerías y archivos
import smbus
from time import sleep

#Configuración del bus para la pantalla LCD
I2CBUS = 1
ADDRESS = 0x27
```

*La comunicación con el celular se realiza en código Python utilizando la libreria **socket** para configurar el UDP y require la conexión del dispositivo a la red IP de la Raspberry Pi:*

```
#Importar librerias y archivos
import socket

#Configuracion del servidor
HOST = '0.0.0.0'
PORT = 5002  # Puerto arbitrario
```

### Función de traducción 📚

El archivo principal del proyecto consta de varias funciones que traducen el mensaje, encienden las luces de envio e imprimen la información final en la pantalla. Además, el bucle principal muestrea en intervalos concretos de tiempo el estado del botón/terminal del celular para seleccionar cual de los caracteres pretende escribir el usuario y distinguir entre el envio de cada letra y la palabra entera.

El código se encuentra en lenguaje Python e incluye los archivos de configuración de periféricos:

```
#Importar librerias y archivos
import ctypes
import time
import I2C_LCD_driver

#Cargar archivo de configuración GPIO
lib = ctypes.CDLL('/home/ADE-MASTER/Desktop/morse/proyecto/control_gpio.so')
```

```
button_press_time0 = time.time() #Hora de la primera pulsacion guardada para escribir letras
button_press_time1 = time.time() #Hora de la primera pulsacion guardada para enviar la palabra
```

```
if (time.time()-button_press_time0>1.5): #1.5 segundos sin pulsar significa guardar letra
```

```
if (time.time()-button_press_time1>6): #6 segundos sin pulsar significa guardar y traducir palabra
```

### Arranque automático 🔌

Los archivos **boot** incluidos en el repositorio tienen como objetivo configurar la ejecución automática del proyecto en cada arranque de la Raspberry Pi. Para ello, es necesario generar un *servicio* con el archivo boot.service el cual ejecuta un código Python del mismo nombre. Este archivo importa todos los programas de configuración y traducción mencionados anteriormente y lanza un mensaje de inicialización en la pantalla y las luces LED. 

```
#Importar librerias y archivos
import I2C_LCD_driver
import udp_socket
import ctypes
import time
import funcionalidad_morse

#Cargar archivo de configuración GPIO
lib = ctypes.CDLL('/home/ADE-MASTER/Desktop/morse/proyecto/control_gpio.so')
```

Comandos en Linux:
```
sudo cp udp-server.service /etc/systemd/system/
systemctl enable udp-server
sudo reboot
```

## Configuración hardware
## Modo de uso

