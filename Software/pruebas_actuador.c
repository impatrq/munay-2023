#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <pigpio.h>
#include "libs/hysrf05.h"  // Suponiendo que ya tienes esta librería para los sensores

// Definir los sensores
Sensor sensors[NUM_SENSORS] = {
    {14, 15}, // Pines sensor 1
    {18, 23}, // Pines sensor 2
    {24, 25}, // Pines sensor 3
    {8, 7},   // Pines sensor 4
    {12, 16}  // Pines sensor 5
};

// Pines del motor
#define MOTOR_PIN_1 17  // GPIO para controlar el motor

// Define la distancia límite (5 metros)
#define MAX_DISTANCE 500

// Variables compartidas
double min_distance = 9999;  // Almacena la distancia mínima medida
pthread_mutex_t distance_mutex;  // Mutex para proteger el acceso a la variable compartida

// Variable para el estado del freno
int motor_active = 0;  // 0 = reposo, 1 = frenando

// Función para accionar el freno
void activate_brake(double time_on) {
    gpioWrite(MOTOR_PIN_1, PI_HIGH);  // Activa el motor
    usleep(time_on * 1000000);        // Mantiene el motor activo por el tiempo calculado
    gpioWrite(MOTOR_PIN_1, PI_LOW);   // Detiene el motor
}

// Función para controlar el motor
void control_motor() {
    while (1) {
        pthread_mutex_lock(&distance_mutex);  // Bloquear acceso a min_distance
        double current_distance = min_distance;
        pthread_mutex_unlock(&distance_mutex);  // Desbloquear acceso

        if (current_distance < MAX_DISTANCE && motor_active == 0) {
            // Si el objeto está dentro del rango y el motor está inactivo
            double time_on = (MAX_DISTANCE - current_distance) / MAX_DISTANCE * 2;  // Tiempo de activación del freno
            activate_brake(time_on);  // Activa el freno
            motor_active = 1;  // Cambia el estado a "frenando"
        } else if (current_distance >= MAX_DISTANCE && motor_active == 1) {
            // Si el objeto está fuera del rango y el freno está activado, detener el motor
            gpioWrite(MOTOR_PIN_1, PI_LOW);  // Detener el motor
            motor_active = 0;  // Cambiar el estado a "reposo"
        }

        usleep(100000);  // Pequeño retardo para evitar sobrecarga de CPU (100ms)
    }
}

// Función de cada hilo de medición
void *measure_distance(void *arg) {
    int sensor_index = *(int *)arg;
    while (1) {
        double distance = sensor_get_distance(&sensors[sensor_index]);

        // Bloquear mutex y actualizar la distancia mínima
        pthread_mutex_lock(&distance_mutex);
        if (distance < min_distance) {
            min_distance = distance;
        }
        pthread_mutex_unlock(&distance_mutex);

        usleep(500000);  // Espera 500 ms antes de la siguiente medición
    }

    return NULL;
}

int main() {
    if (gpioInitialise() < 0) {
        printf("¡Error al iniciar pigpio!\n");
        return 1;
    }

    // Inicializar los sensores
    for (int i = 0; i < NUM_SENSORS; i++) {
        sensor_init(&sensors[i]);
    }

    // Inicializar el pin del motor
    gpioSetMode(MOTOR_PIN_1, PI_OUTPUT);

    // Inicializar el mutex
    pthread_mutex_init(&distance_mutex, NULL);

    // Crear hilos de medición para cada sensor
    pthread_t sensor_threads[NUM_SENSORS];
    int sensor_indexes[NUM_SENSORS];  // Almacena los índices de los sensores
    for (int i = 0; i < NUM_SENSORS; i++) {
        sensor_indexes[i] = i;
        if (pthread_create(&sensor_threads[i], NULL, measure_distance, &sensor_indexes[i]) != 0) {
            printf("Error al crear el hilo de medición para el sensor %d\n", i + 1);
            return 1;
        }
    }

    // Crear el hilo para controlar el motor
    pthread_t motor_thread;
    if (pthread_create(&motor_thread, NULL, control_motor, NULL) != 0) {
        printf("Error al crear el hilo de control del motor\n");
        return 1;
    }

    // Esperar a que los hilos terminen (aunque no lo harán, ya que corren indefinidamente)
    for (int i = 0; i < NUM_SENSORS; i++) {
        pthread_join(sensor_threads[i], NULL);
    }
    pthread_join(motor_thread, NULL);

    gpioTerminate();  // Finalizar pigpio
    pthread_mutex_destroy(&distance_mutex);  // Destruir el mutex

    return 0;
}
