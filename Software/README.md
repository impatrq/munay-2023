# Software

Este repositorio contiene el código y los recursos necesarios para el funcionamiento del sistema de **frenado autónomo** y su dashboard.

## Estructura del Proyecto

### 1. `Dashboard`
Esta carpeta contiene el código para la interfaz de usuario (Dashboard):
- **`assets/ y static/`**: Archivos de estilo CSS y código JavaScript para la interfaz web.
- **`templates/`**: Archivo HTML con la estructura de la página principal del dashboard.
- **`main.py`**: Script principal del servidor backend que conecta el hardware con el dashboard.

### 2. `Frenado Autónomo/`
Archivos del sistema de frenado autónomo escritos en C y que contienen el funcionamiento principal de este sistema.
- **`libs/`**: Contienen las librerías locales que usamos para la inicialización de sensores y medición de distancia. 
- **`frenado_autónomo.c`**: Implementación principal del sistema.


## Instalación y Configuración

### Prerrequisitos
- Tener instalados `gcc` en tu Raspberry Pi para compilar el código en C.
- Instalar las dependencias necesarias para el código en C.
```bash
   sudo apt update
   sudo apt install -y libcurl4-openssl-dev libpigpio-dev libcjson-dev build-essential
```
- Clonar el repositorio en tu Raspberry Pi.
  ```bash
   git clone https://github.com/impatrq/munay.git
   ``` 

### Pasos
#### 1. Servidor web 
  1. Navegar hasta donde clonaste el repositorio.
     ```bash
     cd /rutadondeclonaste/munay
     ``` 
  2. Iniciar el entorno virtual.
     ```bash
     source venv/bin/activate
     ``` 
  3. Inicializar el dashboard.
     ```bash
     cd Software/Dashboard && python main.py
     ```  
4. Accede a la interfaz en tu navegador desde: http://localhost:5000

#### 2. Control del frenado autónomo.

1. Navegar hasta el directorio "Frenado Autónomo"
   ```bash
   cd /rutadondeclonaste/munay/Software/Frenado\ Autónomo/
   ``` 
2. Compilar el código. 
   ```bash
   gcc -o FrenadoAutonomo frenado_autonomo.c "libs/hysrf05.c" -I/usr/include/aarch64-linux-gnu -L/usr/include/aarch64-linux-gnu -lpigpio -lpthread -lcurl -lcjson
   ``` 
3. Ejecutar el archivo compilado.
   ```bash
   sudo ./FrenadoAutonomo
   ``` 
    3.1. Puede generarse un error con la librería "pigpio" al ejecutar este programa en Raspberry Pi OS, ya que tiene su propia versión de esta librería. Puede solucionarse con el siguiente comando:
    ```bash
   sudo killall pigpiod
   ``` 
