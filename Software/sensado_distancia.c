#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <pigpio.h>
#include "libs/hysrf05.h"

Sensor sensors[NUM_SENSORS] = {
    {14, 15},//Completa con los pines a los que se conecte el sensor 1
    {18, 23},//Completa con los pines a los que se conecte el sensor 2
    {24, 25},//Completa con los pines a los que se conecte el sensor 3
    {8, 7},//Completar con los pines a los que se conecte el sensor 4
    {12, 16} //Completa con los pines a los que se conecte el sensor 5
};


void *measure_distances(void *arg) {
    while (1) {
        double min_distance = 9999;
        int closest_sensor = -1;

        for (int i = 0; i < NUM_SENSORS; i++) {
            double distance = sensor_get_distance(&sensors[i]);
            printf("Sensor %d mide: %.2f cm\n", i + 1, distance);

            if (distance < min_distance) {
                min_distance = distance;
                closest_sensor = i;
            }
        }
        sleep(1);
    }
    return NULL;
}

int main() {
    
    if (gpioInitialise() < 0) {
        printf("¡Error al iniciar pigpio!\n");
        return 1;
    }

    for (int i = 0; i < NUM_SENSORS; i++) {
        sensor_init(&sensors[i]);
    }

    pthread_t distance_thread;
    if (pthread_create(&distance_thread, NULL, measure_distances, NULL) != 0) {
        printf("Error al crear el hilo de medición\n");
        return 1;
    }

    pthread_join(distance_thread, NULL);
    /*agregar variable en la que se guarde el valor mas bajo medido, despues agregar un actuador que 
    varía la cantidad de freno en funcion de qué tan cerca esté el objeto */
    gpioTerminate();

    return 0;
}
