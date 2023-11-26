import smtplib
import numpy as np
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# aumentar el parámetro figure.max_open_warning
import matplotlib
matplotlib.rcParams['figure.max_open_warning'] = 50

def datos():
    """
    Almacena el consumo diraio del vehiculo en un diccionario

    Parameter:
        none

    Returns:
        Diccionario con los datos de consumo del vehiculo
    """
    data = {
        'Lunes': 20,
        'Martes': 15,  
        'Miercoles': 30,
        'Jueves': 35,
        'Viernes': 20,
        'Sabado': 23,
        'Domingo': 14
    }
    return data 

def crear_grafico(data : dict) :
    """
    Crea un grafico en funcion del objeto data y lo guarda como imagen

    Parameter:
        data: Diccionario con informacion a graficar

    Returns:
        Imagen resultante
    """
    coloreslindos=('maroon','maroon','maroon','maroon','maroon','red', 'red') #lista de colores
    courses = list(data.keys()) #lista con los dias de semana en bse a las keys del diccionario
    values = list(data.values()) #lista con el consumo en base a los valores del diccionario
    fig = plt.figure(figsize = (15, 8))
    # Creando la bar
    plt.bar(courses, values, color =coloreslindos, width = 0.8)
    plt.xlabel("Dias de la semana")
    plt.ylabel("Consumo por día")
    plt.title("Consumo semanal")
    # plt.show()
    plt.savefig("imagen_grafico.png", dpi=150)
    plt.close(fig) # cerrar la figura para liberar memoria
    # Agregar imagen adjunta al mensaje
    with open('imagen_grafico.png', 'rb') as f:
        img_data = f.read()
        image = MIMEImage(img_data, name='imagen_grafico.png')
    # Devuelvo la imagen del grafico
    return image

def adjuntar_imagen(image, message : MIMEMultipart) -> MIMEMultipart:
    """
    Adjuntar la imagen creada a partit del grafico al mensaje

    Parameter:
        image: Imagen en formato png resultante del grafico
        message: Mensaje al que adjuntar la imagen

    Returns:
        Mensaje actualizado
    """
    message.attach(image)
    # devuelve el mensaje actualizado 
    enviar_mail(message)
    return message

def crear_mensaje():
    """
    Crea el mensaje, le agrega en asunto y el mensaje, y los pone el el mensaje

    Parameter:
        none

    Returns:
        Mensaje con asunto y cuerpo
    """
    mensaje="Hola, aqui el informe de esta semana"
    subject="Informe semanal Munay"
    # Crear objeto mensaje y configurar sus atributos
    message = MIMEMultipart()
    message['Subject'] = subject
     # Agregar cuerpo del correo
    body = MIMEText(mensaje)
    message.attach(body)
    adjuntar_imagen(crear_grafico(datos()), message) # ejecuta la adjuncion de la imagen
    return message

def enviar_mail(message):
    """
    Crea el mensaje, le agrega en asunto y el mensaje, y los pone el el mensaje

    Parameter:
        message: Mensaje con cuerpo asunto e imagen

    Returns:
        mensaje enviado
    """
    # Destinatario
    de = 'eeeeea1234567@gmail.com'
    para = 'sefatynet@gmail.com'
    # Configurar los atributos del objeto mensaje
    message['From'] = de
    message['To'] = para
    # Envio
    server=smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.starttls()
    server.login(user=de, password='yuejfolxfgkknmug') # de la autenticaion en dos pasos
    server.sendmail(from_addr=de, to_addrs=para, msg=message.as_string())
    server.quit()
    print("El mensaje fue enviado con exito")

crear_mensaje()