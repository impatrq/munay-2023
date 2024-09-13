#include "libs/hysrf05.h"
#include <wiringPi.h>
#include <stdio.h>
#include <pthread.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// Configuración de pines del sensor
#define SENSOR_TRIGGER_PIN 5
#define SENSOR_ECHO_PIN 18

// Función de tarea para medir la distancia
void task_measure_distance(void *pvParameters) {
    HY_SRF05 sensor = {SENSOR_TRIGGER_PIN, SENSOR_ECHO_PIN};
    HY_SRF05_init(&sensor);

    while (1) {
        float distance = HY_SRF05_measure_distance(&sensor);
        printf("Distancia medida: %.2f cm\n", distance);
        vTaskDelay(pdMS_TO_TICKS(100));  // Esperar 100 ms antes de la próxima medición
    }
}

int main() {
    // Inicializar wiringPi
    wiringPiSetupGpio();

    // Crear la tarea de FreeRTOS
    xTaskCreate(task_measure_distance, "MeasureDistanceTask", 2048, NULL, 1, NULL);

    // Iniciar el scheduler de FreeRTOS
    vTaskStartScheduler();

    // Este punto no se alcanzará nunca
    while (1);
    return 0;
}