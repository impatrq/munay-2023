#include <pigpio.h>
#include <stdio.h>
#include <unistd.h>
#include "hysrf05.h"

// Inicializa los pines GPIO para el sensor
void sensor_init(Sensor *sensor) {
    gpioSetMode(sensor->trigger, PI_OUTPUT);
    gpioSetMode(sensor->echo, PI_INPUT);
    gpioWrite(sensor->trigger, PI_LOW);  // Establece el pin trigger en bajo inicialmente
}

// Función para calcular la distancia medida por el sensor
double sensor_get_distance(Sensor *sensor) {
    // Enviar un pulso de 10 microsegundos
    gpioWrite(sensor->trigger, PI_HIGH);
    gpioDelay(10);  // Espera de 10 microsegundos
    gpioWrite(sensor->trigger, PI_LOW);

    // Espera hasta que el pin de eco se ponga en alto
    while (gpioRead(sensor->echo) == PI_LOW);

    // Registra el tiempo de inicio (en microsegundos)
    uint32_t start_time = gpioTick();

    // Espera hasta que el eco se ponga en bajo (termina el pulso)
    while (gpioRead(sensor->echo) == PI_HIGH);

    // Registra el tiempo de finalización
    uint32_t stop_time = gpioTick();

    // Calcula el tiempo de viaje del pulso
    uint32_t travel_time = stop_time - start_time;

    // Velocidad del sonido: 34300 cm/s, es decir, 0.034 cm/µs
    double distance = (travel_time * 0.034) / 2;

    return distance;
}

