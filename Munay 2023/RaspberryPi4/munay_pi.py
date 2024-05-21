import datetime
import smtplib
import numpy as np
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import matplotlib
import time
import socket
import threading 
import serial

#https://mega.nz/file/EWMVlLrR#lV5s_R7rRDGS2ZtGT4ZJvDcT2gsYQyOQiek71ZtkCT4

class Pi_Munay():
    def __init__(self) -> None:
        pass

    class Gps():
        def __init__(self) -> None:
            # Abre el puerto serial (ajusta el puerto según tu configuración)
            self.ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
        
        def posición(self):
            data = self.ser.readline().decode('utf-8').strip()
            if data.startswith('$GPRMC'):
                parts = data.split(',')
                if len(parts) >= 10 and parts[2] == 'A':
                    latitude = float(parts[3][:2]) + float(parts[3][2:]) / 60.0
                    if parts[4] == 'S':
                        latitude = -latitude  # Convierte a valor negativo para el sur
                    longitude = float(parts[5][:3]) + float(parts[5][3:]) / 60.0
                    if parts[6] == 'W':
                        longitude = -longitude  # Convierte a valor negativo para el oeste
                    google_maps_link = f'https://www.google.com/maps?q={latitude},{longitude}'
                    return google_maps_link
        
        def cerrar(self):
            self.ser.close()

    class Dashboard():
        def __init__(self) -> None:
            pass

    class Informe():
        def init(self) -> None:
            self.voltaje = [0] * 1440  # Crear una lista de 1440 elementos, todos inicializados a 0
            return self.voltaje
        
        def lista_tiempo(self):
            self.tiempo = []
            for hora in range(24):
                for minuto in range(0, 60, 5):
                    tiempo.append(f'{hora:02d}:{minuto:02d}')
            return self.tiempo

        def volaje_grafico(self, vol, p):
            self.voltaje[p] = vol
       
        def crear_grafico(self):
            # aumentar el parámetro figure.max_open_warning
            matplotlib.rcParams['figure.max_open_warning'] = 50
                   # Crear una figura y un eje
            fig, ax = plt.subplots(figsize=(13,8))
            # Ajustar los márgenes de la figura
            fig.subplots_adjust(top=1, bottom=0.1, left=0.1, right=0.9)
            # Graficar la curva de carga sin marcadores
            ax.plot(self.tiempo[:16], self.voltaje[:16], label='Carga', linestyle='-')

            # Graficar la curva de descarga sin marcadores
            ax.plot(self.tiempo[15:], self.voltaje[15:], label='Descarga', linestyle='-')

            # Etiquetas de ejes y leyenda
            ax.set_xlabel('Tiempo (horas)')
            ax.set_ylabel('Voltaje (V)')
            ax.set_title('Curva de Carga y Descarga de la Batería')
            ax.legend()

            # Mostrar el gráfico
            plt.xticks(tiempo[::6], rotation=45)  # Mostrar etiquetas cada 30 minutos (cada 6 valores)
            plt.grid(True)
            plt.title("Recta de carga y descarga")
            plt.savefig('grafico0.png', dpi=300)
            plt.close(fig) # cerrar la figura para liberar memoria
            # Agregar imagen adjunta al mensaje
            with open('grafico0.png', 'rb') as f:
                img_data = f.read()
                self.image = MIMEImage(img_data, name='grafico0.png')
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
            self.voltaje=[]

    class Bateria():
        def __init__(self, voltage_divider_ratio=15, battery_capacity=100, battery_voltage_min=0.0, battery_voltage_max=4.0):
            # self.i2c = busio.I2C(board.SCL, board.SDA)
            # self.ads = ADS.ADS1115(self.i2c)
            # self.chan = AnalogIn(self.ads, ADS.P0)
            self.voltage_divider_ratio = voltage_divider_ratio
            self.battery_capacity = battery_capacity
            self.battery_voltage_min = battery_voltage_min * 12  # Adjust for a 12-cell battery
            self.battery_voltage_max = battery_voltage_max * 12  # Adjust for a 12-cell battery

        def measure_adc_voltage(self):
            return self.chan.voltage

        def calculate_battery_voltage(self):
            adc_voltage = self.measure_adc_voltage()
            battery_voltage = adc_voltage * self.voltage_divider_ratio
            return battery_voltage

        def calculate_percentage_charge(self):
            battery_voltage = self.calculate_battery_voltage()
            percentage_charge = ((battery_voltage - self.battery_voltage_min) / (self.battery_voltage_max - self.battery_voltage_min)) * 100
            return max(0, min(100, percentage_charge))
            
    class Comunication():
        def __init__(self):
            self.server_ip = self.obtener_ip_wlan0()
            self.server_port = 12345
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)

        def obtener_ip_wlan0():
            try:
                # Creamos un socket para obtener información de red
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Utilizamos el método getsockname() para obtener la dirección IP de la interfaz activa (WLAN0)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                
                return ip
            except Exception as e:
                return str(e)
        
        def wait_for_connection(self):
            print("Esperando conexiones...")
            client_socket, client_address = self.server_socket.accept()
            self.client_socket=client_socket
            print(f"Conexión establecida desde {client_address}")
            return client_socket

        def send_gps_data(self, gps_data):
            self.client_socket.sendall(gps_data.encode())
       
        def close(self):
            self.server_socket.close()
            self.client_socket.close() ## no se si iria


munay=Pi_Munay()
bateria=munay.Bateria()
informe=munay.Informe()
informe.init()
tiempo=informe.lista_tiempo()
comunicacion=munay.Comunication()
gps=munay.Gps()

# ABRIMOS EL DASHBOARD
# ACA
# ACA
# ACA

switch_activo = False
swich_anterior=False

def medicionesloop():
    while True:
        hora_actual = datetime.datetime.now()
        hora= str(hora_actual.hour) + ':' + str(hora_actual.minute)
        if hora_actual.hour == 23 and hora_actual.minute == 58:
            informe.crear_grafico() # aca luego de que todo fue creado deberia ponerse todas las listas en 0 denuevo
            informe.init()
        elif hora_actual.minute % 5 == 0:
            for indice, valor in enumerate(tiempo):
                if valor == hora:
                    adc_voltage = bateria.measure_adc_voltage()
                    battery_voltage = bateria.calculate_battery_voltage()
                    informe.volaje_grafico(battery_voltage, indice)
                    break
            time.sleep(300)


def actualizar_tablero():
    global switch_activo
    while switch_activo:
        pass
    time.sleep(1)
    

def pi_comuniacion():
    global switch_activo
    while switch_activo:
        comunicacion.__init__()
        gps.__init__()
        comunicacion.send_gps_data(comunicacion.wait_for_connection, gps.posición)
        comunicacion.close()
        gps.cerrar()
        time.sleep(1)


hilo_curva = threading.Thread(target=medicionesloop)
hilo_actualizartab=threading.Thread(target=actualizar_tablero)
hilo_comunicacion = threading.Thread(target=pi_comuniacion)


def actualizar_boton():
    global switch_activo
    while True:
        '''
        if GPIO.input(pin_boton) == GPIO.HIGH:
            switch_activo = True
        else:
            switch_activo = False'''
        if switch_activo != swich_anterior:
            if switch_activo==True:
                hilo_actualizartab.start()
                hilo_comunicacion.start()
            if switch_activo==False:
                hilo_actualizartab.join()
                hilo_comunicacion.join()
                pass
        time.sleep(2)


hilo_boton = threading.Thread(target=actualizar_boton)


# Inicia ambos hilos
hilo_curva.start() # loop inifito
hilo_boton.start()