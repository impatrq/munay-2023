import torch
import cv2
import numpy as np

# Leemos el modelo
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')

# Realizo Videocaptura
cap = cv2.VideoCapture(0)

# Empezamos
while True:
    # Realizamos lectura de frames
    ret, frame = cap.read(0)

    # Correccion de color
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detect = model(frame)
    info = detect.pandas().xyxy[0]  # im1 predictions
    ave='bird'
    cv2.imshow('Detector de Carros', np.squeeze(detect.render()))

    if isinstance(detect, torch.Tensor):
        print("El objeto results es un tensor y no es iterable")
    else:
        if ave in detect.pandas().xyxy[0]['name'].tolist():
            print("El string contiene la palabra")


    t = cv2.waitKey(5)
    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()