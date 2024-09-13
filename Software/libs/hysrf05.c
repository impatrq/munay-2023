#include "hysrf05.h"
#include <wiringPi.h>
#include <unistd.h>
#include <sys/time.h>

// Función para inicializar el sensor
void HY_SRF05_init(HY_SRF05 *sensor) {
    // Configurar pines de GPIO
    pinMode(sensor->trigger_pin, OUTPUT);
    pinMode(sensor->echo_pin, INPUT);
    digitalWrite(sensor->trigger_pin, LOW);
    usleep(10000);  // Esperar 10ms para estabilizar
}

// Función para medir distancia en cm
float HY_SRF05_measure_distance(HY_SRF05 *sensor) {
    long start_time, end_time;
    float distance;

    // Generar pulso de trigger
    digitalWrite(sensor->trigger_pin, HIGH);
    usleep(10);
    digitalWrite(sensor->trigger_pin, LOW);

    // Esperar a que el pin de echo esté alto
    while (digitalRead(sensor->echo_pin) == LOW);
    start_time = micros();  // Tiempo inicial

    // Esperar a que el pin de echo esté bajo
    while (digitalRead(sensor->echo_pin) == HIGH);
    end_time = micros();  // Tiempo final

    // Calcular la distancia en cm
    distance = ((end_time - start_time) / 2.0) / 29.1;

    return distance;
}
