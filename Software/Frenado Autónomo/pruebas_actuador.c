#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <pthread.h>
#include <unistd.h>
#include <pigpio.h>
#include "libs/hysrf05.h"  

#define URL "http://localhost:5000/get_braking_profile"

#define NUM_SENSORS 3

// Función de escritura para almacenar la respuesta de cURL
size_t write_callback(void *ptr, size_t size, size_t nmemb, char *data) {
    strcat(data, (char *)ptr);
    return size * nmemb;
}

// Función para obtener el perfil de frenado
char *get_braking_profile() {
    CURL *curl;
    CURLcode res;
    static char response[100] = "";  // Almacena la respuesta del servidor

    curl = curl_easy_init();
    if(curl) {
        // Configura cURL para hacer una solicitud GET
        curl_easy_setopt(curl, CURLOPT_URL, URL);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, response);

        // Realiza la solicitud
        res = curl_easy_perform(curl);

        // Verifica si ocurrió un error
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }
        // Libera recursos de cURL
        curl_easy_cleanup(curl);
    }

    return response;  // Devuelve la respuesta como una cadena
}

// Definir los sensores
Sensor sensors[NUM_SENSORS] = {
    {14, 15}, // Pines sensor 1
    {18, 23}, // Pines sensor 2 
    {24, 25}, // Pines sensor 3
};

// Pines del motor
#define MOTOR_PIN_1 8  // GPIO para controlar el motor

// Define la distancia límite (5 metros)
#define MAX_DISTANCE 450

// Variables compartidas
double min_distance = 9999;  // Almacena la distancia mínima medida
pthread_mutex_t distance_mutex;  // Mutex para proteger el acceso a la variable compartida

// Variable para el estado del freno
int motor_active = 0;  // 0 = reposo, 1 = frenando

// Función para controlar el motor
void* control_motor(void* arg) {
    while (1) {
        pthread_mutex_lock(&distance_mutex); //bloquear acceso a variable de distancia mínima
        double current_distance = min_distance;
        pthread_mutex_unlock(&distance_mutex); //desbloquear acceso 

        printf("Distancia actual: %.2f cm, Estado del motor: %d\n", current_distance, motor_active);

        if (current_distance < MAX_DISTANCE) {
            // Si el objeto está dentro del rango y el motor está inactivo
            printf("Activando el motor. Distancia: %.2f cm\n", current_distance);
            gpioWrite(MOTOR_PIN_1, PI_HIGH); // Encender el motor
            motor_active = 1; // Cambia estado a "frenando"
        } else if (current_distance >= MAX_DISTANCE && motor_active == 1) {
            // Si el objeto está fuera del rango y el freno está activado, detener el motor
            printf("Desactivando el motor. Distancia: %.2f cm\n", current_distance);
            gpioWrite(MOTOR_PIN_1, PI_LOW); // Detener el motor
            motor_active = 0; // Cambia estado a "reposo"
        }

        usleep(100000); // Pequeño retardo para evitar sobrecarga de CPU (100ms)
    }
    return NULL;
}

// Función de cada hilo de medición
void *measure_distance(void *arg) {
    int sensor_index = *(int *)arg;
    free(arg);

    while (1) {
        double distance = sensor_get_distance(&sensors[sensor_index]);
        printf("Sensor %d: distancia medida = %.2f cm\n", sensor_index + 1, distance);


        //bloquear mutex y modificar distancia minima
        pthread_mutex_lock(&distance_mutex);
        if (distance < min_distance || min_distance == 9999) {
            min_distance = distance;
            printf("Nueva distancia mínima: %.2f cm\n", min_distance);
        }
        pthread_mutex_unlock(&distance_mutex);

        usleep(500000);
    }

    return NULL;
}

// Función para reiniciar la distancia mínima cada 5 segundos
void* reset_min_distance(void* arg) {
    while (1) {
        sleep(5);  // Espera 5 segundos
        pthread_mutex_lock(&distance_mutex);
        min_distance = 9999;
        pthread_mutex_unlock(&distance_mutex);
        printf("Reiniciando distancia mínima\n");
    }
    return NULL;
}


int main() {
    char *profile = get_braking_profile();
    
    // Procesa la respuesta y usa el perfil de frenado
    printf("Perfil de frenado actual: %s\n", profile);

    if (gpioInitialise() < 0) {
            printf("¡Error al iniciar pigpio!\n");
            return 1;
        }

        // Inicializar los sensores
        for (int i = 0; i < NUM_SENSORS; i++) {
        int *sensor_index = malloc(sizeof(int));
        *sensor_index = i;
        if (pthread_create(&sensor_threads[i], NULL, measure_distance, sensor_index) != 0) {
            printf("Error al crear el hilo de medición para el sensor %d\n", i + 1);
            return 1;
            }
        }

                // Inicializar el mutex
        pthread_mutex_init(&distance_mutex, NULL);

        // Declarar los hilos
        pthread_t sensor_threads[NUM_SENSORS];
        pthread_t motor_thread;
        pthread_t reset_thread;

        // Inicializar el pin del motor
        gpioSetMode(MOTOR_PIN_1, PI_OUTPUT);

        if (gpioGetMode(MOTOR_PIN_1) != PI_OUTPUT) {
            printf("Error al configurar el pin del motor (GPIO %d) como salida\n", MOTOR_PIN_1);
            return 1;
        }

    // añadir lógica para usar el perfil en el código de frenado
    if (strstr(profile, "dry")) {

        // Crear hilos de medición para cada sensor
        for (int i = 0; i < NUM_SENSORS; i++) {
            int *sensor_index = malloc(sizeof(int));
            *sensor_index = i;
            if (pthread_create(&sensor_threads[i], NULL, measure_distance, sensor_index) != 0) {
                printf("Error al crear el hilo de medición para el sensor %d\n", i + 1);
                return 1;
            }
        }

        // Crear el hilo para controlar el motor
        if (pthread_create(&motor_thread, NULL, control_motor, NULL) != 0) {
            printf("Error al crear el hilo de control del motor\n");
            return 1;
        }

        // Crear el hilo para reiniciar la distancia mínima
        if (pthread_create(&reset_thread, NULL, reset_min_distance, NULL) != 0) {
            printf("Error al crear el hilo de reinicio de distancia mínima\n");
            return 1;
        }

        // Esperar a que los hilos terminen (aunque no lo harán, ya que corren indefinidamente)
        for (int i = 0; i < NUM_SENSORS; i++) {
            pthread_join(sensor_threads[i], NULL);
        }
        pthread_join(motor_thread, NULL);
        pthread_join(reset_thread, NULL);

        gpioTerminate();  // Finalizar pigpio
        pthread_mutex_destroy(&distance_mutex);  // Destruir el mutex

        return 0;


    } else if (strstr(profile, "rain")) {
        printf("Modo de frenado en condiciones de lluvia.\n");
        // Código para modo lluvia, actualmente es igual al seco, debe cambiarse cuando se puedan hacer pruebas
        // Crear hilos de medición para cada sensor
        for (int i = 0; i < NUM_SENSORS; i++) {
            int *sensor_index = malloc(sizeof(int));
            *sensor_index = i;
            if (pthread_create(&sensor_threads[i], NULL, measure_distance, sensor_index) != 0) {
                printf("Error al crear el hilo de medición para el sensor %d\n", i + 1);
                return 1;
            }
        }

        // Crear el hilo para controlar el motor
        if (pthread_create(&motor_thread, NULL, control_motor, NULL) != 0) {
            printf("Error al crear el hilo de control del motor\n");
            return 1;
        }

        // Crear el hilo para reiniciar la distancia mínima
        if (pthread_create(&reset_thread, NULL, reset_min_distance, NULL) != 0) {
            printf("Error al crear el hilo de reinicio de distancia mínima\n");
            return 1;
        }

        // Esperar a que los hilos terminen (aunque no lo harán, ya que corren indefinidamente)
        for (int i = 0; i < NUM_SENSORS; i++) {
            pthread_join(sensor_threads[i], NULL);
        }
        pthread_join(motor_thread, NULL);
        pthread_join(reset_thread, NULL);

        gpioTerminate();  // Finalizar pigpio
        pthread_mutex_destroy(&distance_mutex);  // Destruir el mutex

        return 0;
    } else if (strstr(profile, "snow")) {
        printf("Modo de frenado en condiciones de nieve.\n");
        // Código para modo nieve, actualmente es igual al seco, debe cambiarse cuando se puedan hacer pruebas 
        // Crear hilos de medición para cada sensor
        for (int i = 0; i < NUM_SENSORS; i++) {
            int *sensor_index = malloc(sizeof(int));
            *sensor_index = i;
            if (pthread_create(&sensor_threads[i], NULL, measure_distance, sensor_index) != 0) {
                printf("Error al crear el hilo de medición para el sensor %d\n", i + 1);
                return 1;
            }
        }

        // Crear el hilo para controlar el motor
        if (pthread_create(&motor_thread, NULL, control_motor, NULL) != 0) {
            printf("Error al crear el hilo de control del motor\n");
            return 1;
        }

        // Crear el hilo para reiniciar la distancia mínima
        if (pthread_create(&reset_thread, NULL, reset_min_distance, NULL) != 0) {
            printf("Error al crear el hilo de reinicio de distancia mínima\n");
            return 1;
        }

        // Esperar a que los hilos terminen (aunque no lo harán, ya que corren indefinidamente)
        for (int i = 0; i < NUM_SENSORS; i++) {
            pthread_join(sensor_threads[i], NULL);
        }
        pthread_join(motor_thread, NULL);
        pthread_join(reset_thread, NULL);

        gpioTerminate();  // Finalizar pigpio
        pthread_mutex_destroy(&distance_mutex);  // Destruir el mutex

        return 0;
    } else {
        printf("Modo de frenado desconocido.\n");
    }

    
    gpioTerminate();  // Finalizar pigpio
    pthread_mutex_destroy(&distance_mutex);  // Destruir el mutex

    return 0;
}
