#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "ultrasonic.h" // Include your custom library

#define NUM_SENSORS 5  // Adjust based on how many sensors you're using

// Define your sensors
Sensor sensors[NUM_SENSORS] = {
    {0, 2},  // Sensor 1 (GPIO 17, 27)
    {3, 4},  // Sensor 2 (GPIO 22, 23)
    {5, 6},  // Sensor 3 (GPIO 24, 25)
    {21, 22}, // Sensor 4 (GPIO 9, 10)
    {23, 24}  // Sensor 5 (GPIO 11, 8)
};

// Function for each sensor thread
void *sensor_thread(void *arg) {
    Sensor *sensor = (Sensor *)arg;
    while (1) {
        double dist = sensor_get_distance(sensor);
        printf("Sensor on Trigger %d detects distance: %.2f cm\n", sensor->trigger, dist);
        sleep(1);  // Wait 1 second before next reading
    }
    return NULL;
}

int main(void) {
    // Initialize WiringPi
    if (wiringPiSetup() == -1) {
        printf("WiringPi setup failed!\n");
        return 1;
    }

    // Initialize all sensors
    for (int i = 0; i < NUM_SENSORS; i++) {
        sensor_init(&sensors[i]);
    }

    // Create threads for each sensor
    pthread_t threads[NUM_SENSORS];
    for (int i = 0; i < NUM_SENSORS; i++) {
        if (pthread_create(&threads[i], NULL, sensor_thread, (void *)&sensors[i]) != 0) {
            printf("Error creating thread for sensor %d\n", i + 1);
            return 1;
        }
    }

    // Wait for all threads to finish
    for (int i = 0; i < NUM_SENSORS; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}
