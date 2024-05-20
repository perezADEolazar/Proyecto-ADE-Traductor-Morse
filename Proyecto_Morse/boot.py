"""
Archivo: boot.py
Creadores: Ian/Kerman
Fecha: 16/05/2024
Descripción: Archivo de incialización para configurar los puertos GPIO y lanzar el proyecto Morse en la Raspberry Pi desde el arranque
"""

#Importar librerías y archivos
import I2C_LCD_driver
import udp_socket
import ctypes
import time
import funcionalidad_morse

#Cargar archivo de configuración GPIO
lib = ctypes.CDLL('/home/ADE-MASTER/Desktop/morse/proyecto/control_gpio.so')

#Configuración de los puertos GPIO
lib.setup_gpio.argtypes = []
lib.setup_gpio.restype = None

#Configuración del puerto del botón
lib.read_button_state.argtypes = []
lib.read_button_state.restype = ctypes.c_int

#Configuración del puerto del led verde
lib.set_green_led_state.argtypes = [ctypes.c_int]
lib.set_green_led_state.restype = None

#Configuración del puerto del led rojo
lib.set_red_led_state.argtypes = [ctypes.c_int]
lib.set_red_led_state.restype = None

lib.cleanup_gpio.argtypes = []
lib.cleanup_gpio.restype = None

lib.setup_gpio()

lib.cleanup_gpio.argtypes = []
lib.cleanup_gpio.restype = None

#Función para seleccionar el uso del botón o del Celular (servidor UDP) para introducir los caracteres en Morse
def boot():
    I2C_LCD_driver.lcd().lcd_display_string("BOTON / CELULAR")
    init_time = time.time()
    while True:
        if lib.read_button_state() == 0:
            I2C_LCD_driver.lcd().lcd_display_string("BOTON")
            time.sleep(2)
            I2C_LCD_driver.lcd().lcd_clear()
            hello_message()
            funcionalidad_morse.loop()
        elif (time.time()-init_time>5):
            I2C_LCD_driver.lcd().lcd_display_string("CELULAR")
            time.sleep(2)
            I2C_LCD_driver.lcd().lcd_clear()
            hello_message()
            udp_socket.udp_socket()
            
#Función para ejecutar la secuencia de incialización en el LED y el display
def hello_message():
    I2C_LCD_driver.lcd().lcd_display_string("")
    lib.set_red_led_state(0)
    lib.set_green_led_state(0)
    time.sleep(0.1)
    for _ in range(4):
        I2C_LCD_driver.lcd().lcd_display_string("Escribe Morse!")
        lib.set_red_led_state(1)
        lib.set_green_led_state(0)
        time.sleep(0.1)
        lib.set_red_led_state(0)
        lib.set_green_led_state(1)
        time.sleep(0.1)  
    lib.set_red_led_state(1)
    lib.set_green_led_state(1)  
    I2C_LCD_driver.lcd().lcd_display_string("Escribe Morse!")
    time.sleep(1)
    lib.set_red_led_state(0)
    lib.set_green_led_state(0)
    I2C_LCD_driver.lcd().lcd_clear()


 # Ejecución del programa principal
if __name__ == "__main__":
    try:
        boot()
    except KeyboardInterrupt:
        pass