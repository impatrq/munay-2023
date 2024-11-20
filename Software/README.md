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

### Pasos
#### 1. Servidor web 
  1. Clonar el repositorio en tu Raspberry Pi.
  1. Navegar hasta donde clonaste el repositorio
     ```bash
     cd /rutadondeclonaste/munay
     ``` 
  2. Iniciar el entorno virtual
     ```bash
     source venv/bin/activate
     ``` 
  3. Inicializar el dashboard
     ```bash
     cd Software/Dashboard && python main.py
     ```  
4. Accede a la interfaz en tu navegador desde http://localhost:5000

#### 2. Control del frenado autónomo.

1. 