#include <stdio.h>
#include <pthread.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "hysrf05.h"
#include <wiringPi.h>

// Configuración de pines para múltiples sensores
#define SENSOR_1_TRIGGER_PIN 5
#define SENSOR_1_ECHO_PIN 18

#define SENSOR_2_TRIGGER_PIN 6
#define SENSOR_2_ECHO_PIN 19

#define SENSOR_3_TRIGGER_PIN 12
#define SENSOR_3_ECHO_PIN 20

#define SENSOR_4_TRIGGER_PIN 13
#define SENSOR_4_ECHO_PIN 21

#define SENSOR_5_TRIGGER_PIN 16
#define SENSOR_5_ECHO_PIN 22


// Función de tarea para medir la distancia de un sensor
void task_measure_distance(void *pvParameters) {
    HY_SRF05 *sensor = (HY_SRF05 *)pvParameters;

    HY_SRF05_init(sensor);

    while (1) {
        float distance = HY_SRF05_measure_distance(sensor);
        printf("Distancia medida en el sensor con trigger pin %d: %.2f cm\n", sensor->trigger_pin, distance);
        vTaskDelay(pdMS_TO_TICKS(100));  // Esperar 100 ms antes de la próxima medición
    }
}

int main() {
    // Inicializar wiringPi
    wiringPiSetupGpio();

    // Crear instancias de los sensores
    HY_SRF05 sensor1 = {SENSOR_1_TRIGGER_PIN, SENSOR_1_ECHO_PIN};
    HY_SRF05 sensor2 = {SENSOR_2_TRIGGER_PIN, SENSOR_2_ECHO_PIN};
    HY_SRF05 sensor3 = {SENSOR_3_TRIGGER_PIN, SENSOR_3_ECHO_PIN};
    HY_SRF05 sensor4 = {SENSOR_4_TRIGGER_PIN, SENSOR_4_ECHO_PIN};
    HY_SRF05 sensor5 = {SENSOR_5_TRIGGER_PIN, SENSOR_5_ECHO_PIN};

    // Crear tareas para cada sensor
    xTaskCreate(task_measure_distance, "MeasureDistanceSensor1", 2048, &sensor1, 1, NULL);
    xTaskCreate(task_measure_distance, "MeasureDistanceSensor2", 2048, &sensor2, 1, NULL);
    xTaskCreate(task_measure_distance, "MeasureDistanceSensor3", 2048, &sensor3, 1, NULL);
    xTaskCreate(task_measure_distance, "MeasureDistanceSensor4", 2048, &sensor4, 1, NULL);
    xTaskCreate(task_measure_distance, "MeasureDistanceSensor5", 2048, &sensor5, 1, NULL);

    // Iniciar el scheduler de FreeRTOS
    vTaskStartScheduler();

    // Este punto no se alcanzará nunca
    while (1);
    return 0;
}
