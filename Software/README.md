# Software

Este repositorio contiene el código y los recursos necesarios para el funcionamiento del sistema de **frenado autónomo** y su dashboard.

## Estructura del Proyecto

### 1. `Dashboard`
Esta carpeta contiene el código para la interfaz de usuario (Dashboard):
- **`assets/ y static/`**: Archivos de estilo CSS y código JavaScript para la interfaz web.
- **`templates/`**: Archivo HTML con la estructura de la página principal del dashboard
- **`main.py`**: Script principal del servidor backend que conecta el hardware con el dashboard.

### 2. `Frenado Autónomo/`
Archivos del sistema de frenado autónomo escritos en C y contienen el funcionamiento principal de este sistema.
- **`libs/`**: Contienen las librerías que usamos para la inicialización de sensores y medición de distancia. 
- **`frenado_autónomo.c`**: Implementación principal del sistema.


## Instalación y Configuración

### Prerrequisitos
- Tener instalados `gcc` para compilar el código en C.
- Instalar las dependencias correspondientes en cada caso:
 ```bash
   cd Dashboard && pip install -r requirements.txt
   ``` 
 ```bash
   cd Frenado Autónomo && pip install -r requirements.txt
   ``` 

### Pasos
1. Clonar el repositorio en tu Raspberry Pi o máquina de desarrollo.
2. 