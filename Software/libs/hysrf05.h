#ifndef HY_SRF05_H
#define HY_SRF05_H

#include <stdint.h>

// Estructura de configuración del sensor HY-SRF05
typedef struct {
    int trigger_pin;  // Pin GPIO para el trigger
    int echo_pin;     // Pin GPIO para el echo
} HY_SRF05;

// Función para inicializar el sensor
void HY_SRF05_init(HY_SRF05 *sensor);

// Función para medir distancia
float HY_SRF05_measure_distance(HY_SRF05 *sensor);

#endif
