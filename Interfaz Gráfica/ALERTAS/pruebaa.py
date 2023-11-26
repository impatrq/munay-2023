import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import torch

class CameraApp:
    def __init__(self, window):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5n')
        self.window = window
        self.window.title("Captura de cámara")
        
        # Crear un lienzo para mostrar la imagen capturada
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()
        
        # Inicializar la cámara
        self.cap = cv2.VideoCapture(0)
        
        # Llamar al método para mostrar la imagen inicial
        self.update_image()
        
    def update_image(self):
        key = cv2.waitKey(1)
        if key != -1:
            self.capture_image()
        # Capturar un fotograma de la cámara
        ret, frame = self.cap.read()
        
        if ret:
            detect = self.model(frame)
            info = detect.pandas().xyxy[0]
            # Convertir el fotograma de OpenCV a una imagen que se pueda mostrar en Tkinter
            image = cv2.cvtColor(np.squeeze(detect.render()), cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            
            # Actualizar la imagen en el lienzo
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image
        
        # Llamar al método nuevamente después de 15 milisegundos (aproximadamente 66 fps)
        self.window.after(15, self.update_image)
        
    def capture_image(self):
        # Capturar un fotograma de la cámara
        ret, frame = self.cap.read()
        
        if ret:
            # Guardar la imagen capturada en un archivo
            cv2.imwrite("captura.jpg", frame)
            print("Imagen capturada y guardada como captura.jpg")
            
if __name__ == '__main__':
    # Crear la ventana de la aplicación
    root = tk.Tk()
    app = CameraApp(root)
    
    # Iniciar el bucle principal de la aplicación
    root.mainloop()
