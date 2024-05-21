import PIL
import cv2
from PIL import Image, ImageTk
from tkinter import *
import tkinter as tk
import requests
import socket
import random

class APP_MUNAY():
    def __init__(self) -> None:
        pass

    class MunayInterfaz():
        def __init__(self) -> None:
            # Creamos la ventana principal
            self.pantalla = Tk()
            # Obtener las dimensiones de la pantalla
            ancho_pantalla = self.pantalla.winfo_screenwidth()
            alto_pantalla = self.pantalla.winfo_screenheight()
            self.width =  self.pantalla.winfo_screenwidth()
            self.height = self.pantalla.winfo_screenheight()
            # Establecer las dimensiones de la ventana a pantalla completa
            self.pantalla.geometry(f"{ancho_pantalla}x{alto_pantalla}")
            self.pantalla.attributes("-fullscreen", True)
            self.pantalla.title('Interfaz gráfica')
            self.pantalla.iconbitmap('munaylogo-04.ico') # Icono de la pantalla
            self.cosaa=cv2.cvtColor
            self.cosa2=cv2.COLOR_BGR2RGB
            self.unlabel=Label(self.pantalla)
            self.unlabel.place(width=self.width, height=self.height)
            self.pantalla.columnconfigure(0, weight=1)
            self.pantalla.columnconfigure(1, weight=1)
            self.pantalla.rowconfigure(0, weight=1)
            
            
            self.pantallaa(0)

        def generar_color_aleatorio(self):
            # Genera valores RGB aleatorios entre 0 y 255
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
            # Convierte los valores RGB en un formato hexadecimal
            color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
            
            return color_hex
        def pantallaa(self, *args):
            # Creo captura de camara
            self.captures = []
            self.camera_labels = []
            self.pantalla.protocol("WM_DELETE_WINDOW", self.finalizar)
            print (args)
            for i, camera_index in enumerate(args):
                self.captures.append(cv2.VideoCapture(camera_index))
                # Creo label
                self.camera_labels.append(Label(self.pantalla))
            # Aca pueden haber dos opciones
            # Primera opción: Dependiendo de la cantidad de camaras (que idealmnte siempre serían cuatro) ubica los labels
                if len(args) < 3:
                    self.camera_labels[i].place(width=self.width / len(args), height=self.height)
                    self.camera_labels[i].grid(row=0, column=i, sticky='nsew')
                elif len(args) >= 3:
                    self.pantalla.rowconfigure(1, weight=1)
                    if i == 0 or i ==1:
                        self.camera_labels[i].place(width=self.width / 2, height=self.height/2)
                        self.camera_labels[i].grid(row=0, column=i, sticky='nsew')
                    elif i == 2:
                        self.camera_labels[i].place(width=self.width / 2, height=self.height/2)
                        self.camera_labels[i].grid(row=1, column=0, sticky='nsew')
                    elif i ==3:
                        self.camera_labels[i].place(width=self.width / 2, height=self.height/2)
                        self.camera_labels[i].grid(row=1, column=1, sticky='nsew')
            
            ### MENU
            self.img_boton = PhotoImage(file='.\munaylogo-04.png')
            self.img_boton = self.img_boton.subsample(35, 35)
            self.boton = Button(self.pantalla, image=self.img_boton, borderwidth=0, command=self.menuu)
            self.boton.config(cursor="pirate")
            self.boton.place(anchor="ne", x=self.width-25, y=15)
            ## IMAGENES DEL MENU
            # Icono camara
            self.imagen_video = PhotoImage(file='.\camaramunay.png')
            self.imagen_video = self.imagen_video.subsample(12, 12)
            # Icono de filtro
            self.imagen_filtro = PhotoImage(file='./filtromunay.png')
            self.imagen_filtro = self.imagen_filtro.subsample(12, 12)
            # Icono WIFI
            self.imagen_wifi = PhotoImage(file='./wifi-1.png')
            self.imagen_wifi = self.imagen_wifi.subsample(12, 12)
            # Icono configuración
            self.imagen_config = PhotoImage(file='./configuraciones.png')
            self.imagen_config = self.imagen_config.subsample(12, 12)

            # CONFIGURAMOS EL MENU (LUEGO DESAPARECE)
            colorazul = '#011127'
            self.menu=Label(self.pantalla, bg=colorazul)
            self.menu.config(width=180, height=700)
            self.menu.place(x=self.width-100, y=0)
            # Botón logo munay azul
            self.boton2 = Button(self.menu, image=self.img_boton, borderwidth=0, command=self.quitar, bg=colorazul)
            self.boton2.place(anchor="ne", x=83, y=15)
            # Botón uno
            self.botonc = Button(self.menu, image=self.imagen_video, borderwidth=0, bg=colorazul,command=lambda: self.camaratres(1,1))
            self.botonc.place(anchor="e", x=75, y=150)
            # Botón dos
            self.botonb = Button(self.menu, image=self.imagen_wifi, borderwidth=0, bg=colorazul)
            self.botonb.place(anchor="e", x=75, y=220)
            # Botón tres
            self.botona = Button(self.menu, image=self.imagen_config, borderwidth=0, bg=colorazul, command=print('holaa'))
            self.botona.place(anchor="e", x=75, y=290)
            # Botón cuatro
            self.botond = Button(self.menu, image=self.imagen_video, borderwidth=0, bg=colorazul)
            self.botond.place(anchor="e", x=75, y=360)
            # Botón cinco
            self.botonfiltro = Button(self.menu, image=self.imagen_config, borderwidth=0, bg=colorazul)
            self.botonfiltro.place(anchor="ne", x=75, y=410)
            self.menu.place_forget()

            # CONFIGURAMOS LA CONF
            colorazuloscuro="#000915"
            config_height=50
            config_width=25
            self.opciones = Label(self.pantalla, bg=colorazuloscuro)
            self.opciones.config(height=config_height, width= config_width)
            self.opciones.place(x=self.width-280, y=0) 
            self.opc_div=[]
            for i in range(7):
                self.opc_div.append(Label(self.opciones, bg=self.generar_color_aleatorio()))
                self.opc_div[i].grid(row=i, column=0)
                self.opc_div[i].config(width=config_width, height=int(config_height/7))
                self.opc_div[i].grid_forget()
            self.opciones.place_forget()

            self.is_alerta='no'
            self.is_config='no'
                # Segunda opción: Directamente crea los labels (sabiendo que si por alguna razon no entran las 4 camaras el programa no funcionara)
            '''
            self.camera_labels[0].place(width=self.width/2, height=self.height/2)
            self.camera_labels[0].grid(row=0, column=0, sticky='nsew')
            self.camera_labels[1].place(width=self.width/2, height=self.height/2)
            self.camera_labels[1].grid(row=0, column=1, sticky='nsew')
            self.camera_labels[2].place(width=self.width/2, height=self.height/2)
            self.camera_labels[2].grid(row=1, column=0, sticky='nsew')
            self.camera_labels[3].place(width=self.width/2, height=self.height/2)
            self.camera_labels[3].grid(row=1, column=1, sticky='nsew')'''
        
        def detalles(self, n, tipo):
            for i in range(n):
                self.opc_div[i].grid(row=i, column=0)
            if tipo == 'camaras':
                self.primercam= Button(self.opc_div[0])
                self.segundacam= Button(self.opc_div[1])
                self.tercercam= Button(self.opc_div[2])
                self.cuatrocam= Button(self.opc_div[3])
                self.configcam= input(self.opc_div[4])

        def pantallaconfig(self, *args):
            self.camera_labels=[]
            for i, cam in enumerate(args):
                self.camera_labels.append(Label(self.unlabel))
                if len(args) < 3:
                        if i==0:
                            self.camera_labels[i].config(width=self.width, height=self.height)
                        self.camera_labels[i].place(width=self.width / len(args), height=self.height)
                        self.camera_labels[i].grid(row=0, column=i, sticky='nsew')
                elif len(args) >= 3:
                    if i == 0 or i ==1:
                        self.camera_labels[i].place(width=self.width / 2, height=self.height/2)
                        self.camera_labels[i].grid(row=0, column=i, sticky='nsew')
                    elif i == 2:
                        self.camera_labels[i].place(width=self.width / 2, height=self.height/2)
                        self.camera_labels[i].grid(row=1, column=0, sticky='nsew')
                    elif i ==3:
                        self.camera_labels[i].place(width=self.width / 2, height=self.height/2)
                        self.camera_labels[i].grid(row=1, column=1, sticky='nsew')
            print('terminamos')
            print(self.camera_labels)


        def update_camera(self, n = 1,c=0):
            ret = self.update_captures()

            if ret:
                for i in range(n):
                    imagen = PIL.Image.fromarray(self.cosaa(self.frames[i+c], self.cosa2))
                    imagen = imagen.resize((self.camera_labels[i].winfo_width(), self.camera_labels[i].winfo_height()))
                    imagen_tk = ImageTk.PhotoImage(imagen)
                    self.camera_labels[i].config(image=imagen_tk)
                    self.camera_labels[i].image = imagen_tk
            else:
                self.camera_labels[i].config(bg="blue")  ## C se pone una imagen que diga algo como "mno hay imagen de video"
            # Llamo la funcion nuevamente cada 10 ms
            self.pantalla.after(10, lambda: self.update_camera(n,c))


        def update_captures(self):
            self.frames = []
            # Capturo un cuadro de la camara
            for i, capture in enumerate(self.captures):
                ret, frame = capture.read()
                self.frames.append(frame)
                detected=None
                detect=None
                #if capture == 3:
                #    detect= Modelfod(self.frame)
                #elif capture==0 // capture==1 // capture ==2:
                #     detect = Modelave(self.frame)
                #     if bla es real:
                #         detcected = Modeldondeave(self.frame)
                #      
                # 
                # if detect:
                #       cvs.imwrite('detectado.png)
                #       self.alerta(detect.obj)

            return ret

        def finalizar(self):
                for capture in self.captures:
                    self.pantalla.quit()
                    capture.release()


        def loop(self) -> None:
            self.pantalla.mainloop()

        

        def menuu(self):
            self.menu.place(x=self.width-100, y=0)
            

        def configuracion (self):
            self.is_config='si'
            self.opciones.place(x=self.width-280, y=0)

        

        def quitar(self):
            self.menu.place_forget()

            if self.is_config=='si':
                self.opciones.place_forget()
                self.is_config=='no'
            if self.is_alerta=='si':
                self.frame_noti.place_forget()
                self.is_alerta='no'
        

        def camaratres(self,n,c=0):
                self.n=n
                print(self.camera_labels)
                for i in [0,1,2,3]:
                    self.camera_labels[i].place_forget()
                    self.camera_labels[i].grid_forget()
                self.pantallaconfig(1) #segun la cantidad de argumentos, la cantidad dde labels
                self.update_camera(n,c) # n= numero de camaras a visualizar y c= camara que quiero ver(opcional)


        def alerta(self, clase):
            self.is_alerta='si'
            self.frame_noti = Frame(self.pantalla, bg='red')
            self.frame_noti.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            self.imagen_detectada = PhotoImage(file='./detectado.png')
            self.imagen_detectada = self.imagen_detectada.subsample(9, 9)
            
            labelimg_noti = Label(self.frame_noti, image=self.imagen_detectada)
            labelimg_noti.pack()
            
            labeltxt_noti = Label(self.frame_noti, font='Arial 12', anchor=tk.E)
            labeltxt_noti.pack(fill="both", expand=True)
            
            frame_izquierda = Frame(labeltxt_noti, bg="lightgray")
            frame_derecha = Frame(labeltxt_noti, bg="lightgray")
            
            labeltxt_noti.columnconfigure(0, weight=1)
            labeltxt_noti.columnconfigure(1, weight=1)
            frame_izquierda.grid(row=0, column=0, sticky="nsew")
            frame_derecha.grid(row=0, column=1, sticky="nsew")
            
            btn_env = Button(frame_izquierda, text="No tener en cuenta", bg='lightgray')
            btn_env.pack(pady=10, padx=20, fill="both")
            
            btn_trash = Button(frame_derecha, text="Notificar", bg='white')
            btn_trash.pack(pady=10, padx=20, fill="both")
            self.enviar_telegram(clase)

        def datareception_pi(self):
            # Configuración del socket
            server_hostname = 'pimunay'  # Nombre de hostname de tu Raspberry Pi
            server_port = 49152

            # Resuelve el hostname a una dirección IP
            try:
                server_ip = socket.gethostbyname(server_hostname)

                # Crear un socket TCP
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))

                # Recibir los datos de GPS
                gps_data = client_socket.recv(1024).decode()
                msj_telegram=(f"Da{gps_data}")

                # Cerrar el socket del cliente
                client_socket.close()
            except socket.gaierror:
                msj_telegram=(f"No se pudo resolver el hostname {server_hostname}. Asegúrate de que el nombre de hostname sea correcto.")
            except ConnectionRefusedError:
                msj_telegram=(f"No se pudo conectar al servidor en {server_hostname}:{server_port}. Asegúrate de que el servidor esté en ejecución.")
            return msj_telegram


        def enviar_telegram (self, clase):
            self.frame_noti.place_forget()
            self.is_alerta='no'
            gps = self.datareception_pi()
            # requests.post("https://api.telegram.org/bot/sendMessage")
            # Token de acceso de tu bot de Telegram
            TOKEN = '6076619401:AAFRAWcuw1ePT7IN58DRtZxR9BtuJLsaVe8'
            # ID del chat donde quieres enviar el mensaje (puede ser tu ID de usuario o el ID de un grupo)
            CHAT_ID = -1001283738236
            # Mensaje que quieres enviar
            MESSAGE = f'Hemos detectado un {clase}, en {gps}'
            # URL de la API de Telegram para enviar mensajes
            URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

            # Parámetros del mensaje
            params = {
                'chat_id': CHAT_ID,
                'text': MESSAGE
            }

            # Envía el mensaje a través de la API de Telegram
            response = requests.post(URL, params=params)

            # Comprueba si el mensaje se envió correctamente
            if response.status_code == 200:
                # aca podria hacer algo que se le muestre a la persona 
                print('Mensaje enviado correctamente.')
            else:
                print(f'Error al enviar el mensaje. Código de estado HTTP: {response.status_code}')


# Creo interfaz
munay=APP_MUNAY()



app=munay.MunayInterfaz()
app.update_camera()
# Abro interfaz
app.loop()
