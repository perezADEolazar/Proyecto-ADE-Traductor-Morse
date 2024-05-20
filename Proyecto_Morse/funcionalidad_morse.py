"""
Archivo: funcionalidad_morse.py
Creadores: Ian/Kerman
Fecha: 16/05/2024
Descripción: Archivo principal con las funcionalidades de la traducción de Morse a alfabeto latino,
             además de la lógica principal de entrada y salida de los periféricos
"""

#Importar librerías y archivos
import ctypes
import time
import I2C_LCD_driver

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

#Función principal
def loop():
    letter_array = [] #Array de caracteres en Morse
    word_array=[] #Array de letras en morse
    button_press_time0 = None
    button_press_time1 = None
    while True:
        if lib.read_button_state() == 0: #Muestreo del boton
            time.sleep(0.1)
            if lib.read_button_state() == 0: 
                time.sleep(0.7)
                if lib.read_button_state() == 0:
                    character = "-" #Pulsación larga en el muestreo es una raya
                    print_message(character)
                    letter_array.append(character)
                    time.sleep(0.7)
                elif lib.read_button_state() == 1:
                    character = "." #Pulsación corta en el muestreo es un punto
                    print_message(character)
                    letter_array.append(character)
                    time.sleep(0.7)
            button_press_time0 = time.time() #Tiempo de la primera pulsación guardada para escribir letras
            button_press_time1 = time.time() #Tiempo de la primera pulsación guardada para enviar la palabra
        elif (button_press_time1 is not None):
            if (button_press_time0 is not None):
                if (time.time()-button_press_time0>1.5): #1.5 segundos sin pulsar significa guardar letra
                    word_array.append(letter_array) 
                    letter = "".join(letter_array)
                    letter_array=[]
                    print_message(letter)
                    lib.set_green_led_state(1) #LED verde indica guardar letra escrita
                    time.sleep(1)
                    lib.set_green_led_state(0)
                    button_press_time0 = None #Reiniciar tiempo de escritura de letras
            elif (button_press_time0 is None):
                if (time.time()-button_press_time1>6): #6 segundos sin pulsar significa guardar y traducir palabra
                    blink_fast() #LED rojo indica envío de la palabra
                    button_press_time1 = None #Reiniciar tiempo de escritura de la palabra
                    print_message(morse_array_traduction(word_array))
                    word_array=[]
                    
#Función para imprimir en la pantalla LCD
def print_message(message):
    I2C_LCD_driver.lcd().lcd_display_string(message)

#Función para ejecutar el aviso de envío de la palabra
def blink_fast():    
    lib.set_red_led_state(1)
    time.sleep(0.4)
    lib.set_red_led_state(0)
    time.sleep(0.4)
    I2C_LCD_driver.lcd().lcd_display_string("Enviando...")
    
    for i in range(18):
        if lib.read_button_state() == 0:
            time.sleep(2)
            loop()
            break
        delay = 1 / (i + 1)
        lib.set_red_led_state(1)
        time.sleep(delay)
        lib.set_red_led_state(0)
        time.sleep(delay)
        
    lib.set_red_led_state(1)
    time.sleep(1.5)
    lib.set_red_led_state(0)

#Función de traducción del mensaje enviado con el celular
def morse_udp_traduction(message):
    traduction = []
    #Diccionario con valores en morse y alfabeto latino
    morse_code= {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D',
                '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
                '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
                '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
                '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
                '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
                '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2',
                '...--': '3', '....-': '4', '.....': '5', '-....': '6',
                '--...': '7', '---..': '8', '----.': '9', '-----': '0',
                '.-.-': ' '}
    message_array = message.split()
    for char in message_array:
        for key, value in morse_code.items():
            if char==key:
                traduction.append(value)
    traduction="".join(traduction)
    return traduction

#Función de traducción del mensaje enviado con el botón
def morse_array_traduction(word_array):
    traduction = []
    #Diccionario con valores en morse y alfabeto latino
    morse_code= {'.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D',
                '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H',
                '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
                '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P',
                '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
                '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
                '-.--': 'Y', '--..': 'Z', '.----': '1', '..---': '2',
                '...--': '3', '....-': '4', '.....': '5', '-....': '6',
                '--...': '7', '---..': '8', '----.': '9', '-----': '0',
                '.-.-': ' '}
    for letter in word_array:
        letter = "".join(letter)
        for key, value in morse_code.items():
            if letter==key:
                traduction.append(value)
    traduction="".join(traduction)
    return traduction



