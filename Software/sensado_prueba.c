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




void setup() {
    // Inicializar wiringPi
    wiringPiSetupGpio();

    // Crear instancias de los sensores
    HY_SRF05 sensor1 = {SENSOR_1_TRIGGER_PIN, SENSOR_1_ECHO_PIN};
    HY_SRF05 sensor2 = {SENSOR_2_TRIGGER_PIN, SENSOR_2_ECHO_PIN};
    HY_SRF05 sensor3 = {SENSOR_3_TRIGGER_PIN, SENSOR_3_ECHO_PIN};

    // Crear tareas para cada sensor
    xTaskCreate(measure_distance1, "MeasureDistanceSensor1", 2048, &sensor1, 1, NULL);
    xTaskCreate(measure_distance2, "MeasureDistanceSensor2", 2048, &sensor2, 1, NULL);
    xTaskCreate(measure_distance3, "MeasureDistanceSensor3", 2048, &sensor3, 1, NULL);


    // Iniciar el scheduler de FreeRTOS
    vTaskStartScheduler();

    // Este punto no se alcanzará nunca
    while (1);
    return 0;
}
