import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import os
import cv2
import numpy as np

# Verificar si TensorFlow detecta la GPU
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    print("GPUs disponibles:", physical_devices)
    try:
        tf.config.experimental.set_virtual_device_configuration(
            physical_devices[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=7168)])  # Asigna 7168 MB de VRAM
    except RuntimeError as e:
        print(e)
else:
    print("No se detectaron GPUs")

# Función para parsear cada línea del archivo de lista
def parse_line(line):
    items = line.strip().split()
    if len(items) < 2:
        print(f"Line format incorrect: {line}")
        return None, None, None
    image_path = items[0]
    label_path = items[1]
    labels = [int(x) for x in items[2:]] if len(items) > 2 else []
    return image_path, label_path, labels

# Generador de datos para cargar imágenes en lotes
def data_generator(list_file, dataset_dir, batch_size, img_width=800, img_height=288):
    while True:
        with open(list_file, 'r') as file:
            lines = file.readlines()
            for start in range(0, len(lines), batch_size):
                batch_images = []
                batch_labels = []
                end = min(start + batch_size, len(lines))
                for i in range(start, end):
                    line = lines[i]
                    image_path, label_path, line_labels = parse_line(line)
                    if image_path is None or label_path is None:
                        continue
                    full_image_path = os.path.join(dataset_dir, image_path[1:])
                    full_label_path = os.path.join(dataset_dir, label_path[1:])
                    
                    if not os.path.isfile(full_image_path):
                        print(f"File not found: {full_image_path}")
                        continue
                    if not os.path.isfile(full_label_path):
                        print(f"File not found: {full_label_path}")
                        continue
                    
                    image = cv2.imread(full_image_path)
                    if image is None:
                        print(f"Failed to load image: {full_image_path}")
                        continue
                    
                    image = cv2.resize(image, (img_width, img_height))
                    batch_images.append(image)
                    batch_labels.append(line_labels)
                
                yield np.array(batch_images), np.array(batch_labels)

# Función para cargar los datos de prueba
def load_test_data(list_file, dataset_dir, img_width=800, img_height=288):
    images = []
    labels = []
    image_paths = []
    with open(list_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            image_path, label_path, line_labels = parse_line(line)
            if image_path is None or label_path is None:
                continue
            full_image_path = os.path.join(dataset_dir, image_path[1:])
            full_label_path = os.path.join(dataset_dir, label_path[1:])
            
            if not os.path.isfile(full_image_path):
                print(f"File not found: {full_image_path}")
                continue
            if not os.path.isfile(full_label_path):
                print(f"File not found: {full_label_path}")
                continue
            
            image = cv2.imread(full_image_path)
            if image is None:
                print(f"Failed to load image: {full_image_path}")
                continue
            
            image = cv2.resize(image, (img_width, img_height))
            images.append(image)
            image_paths.append(full_image_path)
            
            labels.append(line_labels)
    
    return np.array(images), np.array(labels), image_paths

# Función para crear el modelo de red neuronal
def create_model(input_shape):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),  # Primera capa convolucional
        MaxPooling2D((2, 2)),  # Primera capa de max pooling
        Conv2D(64, (3, 3), activation='relu'),  # Segunda capa convolucional
        MaxPooling2D((2, 2)),  # Segunda capa de max pooling
        Conv2D(128, (3, 3), activation='relu'),  # Tercera capa convolucional
        MaxPooling2D((2, 2)),  # Tercera capa de max pooling
        Flatten(),  # Aplanar los datos para la capa densa
        Dense(128, activation='relu'),  # Capa densa con 128 unidades
        Dense(4, activation='sigmoid')  # Capa de salida con 4 unidades y activación sigmoide
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    # Especifica los archivos de lista y el directorio de datos
    train_list = 'D:/Red Neuronal/list/train_gt.txt'  # Archivo con la lista de datos de entrenamiento
    test_list = 'D:/Red Neuronal/list/test.txt'       # Archivo con la lista de datos de prueba
    dataset_dir = 'D:/Red Neuronal/'  # Directorio base donde se encuentran los datos
    
    # Crear y entrenar el modelo
    input_shape = (288, 800, 3)  # Tamaño de la entrada para las imágenes
    model = create_model(input_shape)
    
    # Definir parámetros del generador
    batch_size = 32  # Tamaño del lote para el generador
    
    # Crear generadores de datos
    train_generator = data_generator(train_list, dataset_dir, batch_size)
    
    # Cargar los datos de prueba
    print("Loading test data...")
    x_test, y_test, test_image_paths = load_test_data(test_list, dataset_dir)
    print(f"Loaded {len(x_test)} test images.")
    
    print(f"Training the model with batch size {batch_size}...")
    steps_per_epoch = len(open(train_list).readlines()) // batch_size
    
    # Entrenar el modelo usando el generador
    model.fit(train_generator, steps_per_epoch=steps_per_epoch, epochs=10)

    # Evaluar el modelo con los datos de prueba
    print("Evaluating the model...")
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print(f"Test Accuracy: {test_acc}")

    # Guardar el modelo entrenado
    model.save('trained_RedNeuronal')
    print("Model saved successfully.")
