#ifndef ULTRASONIC_H
#define ULTRASONIC_H

// Estructura para los pines de cada sensor
typedef struct {
    int trigger;
    int echo;
} Sensor;

// Función para inicializar los pines GPIO del sensor
void sensor_init(Sensor *sensor);

// Función para calcular la distancia medida por el sensor
double sensor_get_distance(Sensor *sensor);

#endif // ULTRASONIC_H
