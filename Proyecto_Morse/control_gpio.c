/*
Archivo: control_gpio.c
Creadores: Ian/Kerman
Fecha: 16/05/2024
Descripción: Archivo de configuración de los puertos GPIO
*/

//Importar librerías y archivos
#include <stdio.h>
#include <stdlib.h>
#include <pigpio.h>

//Definir pines GPIO a utilizar
#define GreenledPin 26
#define RedledPin 20
#define ButtonPin 12


void setup_gpio() {
    if (gpioInitialise() < 0) {
        printf("Error al inicializar pigpio\n");
        exit(1);
    }
    //Funciones de configuracion de los pines GPIO
    gpioSetMode(GreenledPin, PI_OUTPUT);
    gpioSetMode(RedledPin, PI_OUTPUT);
    gpioSetMode(ButtonPin, PI_INPUT);
    gpioSetPullUpDown(ButtonPin, PI_PUD_UP);
}

//Función de lectura del estado del botón
int read_button_state() {
    return gpioRead(ButtonPin);
}

//Función de escritura del estado del led verde
void set_green_led_state(int state) {
    gpioWrite(GreenledPin, state);
}

//Función de escritura del estado del led rojo
void set_red_led_state(int state) {
    gpioWrite(RedledPin, state);
}

//Reiniciar valores de los pines GPIO
void cleanup_gpio() {
    gpioTerminate();
}
