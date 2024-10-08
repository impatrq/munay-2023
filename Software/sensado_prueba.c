#include <pigpio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdio.h>
#include "libs/hysrf05.h"

#define NUM_SENSORS 3

Sensor sensors[NUM_SENSORS] = {
    {14, 15},
    {18, 23},
    {24, 25}
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

        printf("El sensor %d es el más cercano con %.2f cm\n\n", closest_sensor + 1, min_distance);
        sleep(1);
    }
    return NULL;
}

int main(void) {
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
    gpioTerminate();

    return 0;
}
