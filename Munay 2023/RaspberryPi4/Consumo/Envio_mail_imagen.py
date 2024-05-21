import smtplib
import numpy as np
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import matplotlib
import time
import schedule
# sacables
import random
import math


class Mensaje ():
    def pepa(self):
        self.hora_semanal = "08:00"
        schedule.every().wednesday.at(self.hora_semanal).do(self.crear_mensaje) 
        print("acas")
    def datos_diarios(self): 
        self.data_minuto = []
        self.data_hora= []
        for a in range(60):
            for i in range(60):
                self.data_minuto.append(random.randint(0, 100))
            self.data_hora.append(sum(self.data_minuto) / len(self.data_minuto))
    def datos_semanales(self):
        """
        Almacena el consumo diraio del vehiculo en un diccionario
        """
        self.data = {
            'Lunes': 20,
            'Martes': 15,  
            'Miercoles': 30,
            'Jueves': 35,
            'Viernes': 20,
            'Sabado': 23,
            'Domingo': 14
        }
        return self.data

    def crear_grafico(self) :
        """
        Crea un grafico en funcion del objeto data y lo guarda como imagen

        Parameter:
            data: Diccionario con informacion a graficar

        Returns:
            Imagen resultante
        """
        # aumentar el parámetro figure.max_open_warning
        matplotlib.rcParams['figure.max_open_warning'] = 50
        coloreslindos=('maroon','maroon','maroon','maroon','maroon','red', 'red') #lista de colores
        courses = list(self.data.keys()) #lista con los dias de semana en bse a las keys del diccionario
        values = list(self.data.values()) #lista con el consumo en base a los valores del diccionario
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
            self.image = MIMEImage(img_data, name='imagen_grafico.png')
        # Devuelvo la imagen del grafico
        return self.image

    def adjuntar_imagen(self, image) -> MIMEMultipart:
        """
        Adjuntar la imagen creada a partit del grafico al mensaje

        Parameter:
            image: Imagen en formato png resultante del grafico
            message: Mensaje al que adjuntar la imagen

        Returns:
            Mensaje actualizado
        """
        self.message.attach(image)
        # devuelve el mensaje actualizado 
        self.enviar_mail(self.message)
        return self.message

    def crear_mensaje(self):
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
        self.message = MIMEMultipart()
        self.message['Subject'] = subject
        # Agregar cuerpo del correo
        body = MIMEText(mensaje)
        self.message.attach(body)
        self.adjuntar_imagen(self.crear_grafico()) # ejecuta la adjuncion de la imagen
        return self.message

    def enviar_mail(self, message):
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

informe_consumo = Mensaje()
informe_consumo.pepa()
informe_consumo.datos_semanales()

while True:
    print("aca gorda")
    schedule.run_pending()
    time.sleep(1)
