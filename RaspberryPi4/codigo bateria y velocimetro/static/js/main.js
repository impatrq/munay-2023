initBattery();

function initBattery() {
    const batteryLiquid = document.querySelector('.battery__liquid'),
        batteryStatus = document.querySelector('.battery__status'),
        batteryPercentage = document.querySelector('.battery__percentage');

    updateBattery = (percentage) => {
        /* 1. We update the number level of the battery */
         let roundedPercentage = percentage.toFixed(0);
    batteryPercentage.innerHTML = roundedPercentage + " %";




        /* 2. We update the background level of the battery */
        batteryLiquid.style.height = `${parseInt(percentage)}%`;

        /* 3. We validate full battery, low battery and if it is charging or not */
        if (percentage == 100) { /* We validate if the battery is full */
            batteryStatus.innerHTML = `Full battery <i class="ri-battery-2-fill green-color"></i>`;
            batteryLiquid.style.height = '103%'; /* To hide the ellipse */
        } else if (percentage <= 20) { /* We validate if the battery is low */
            batteryStatus.innerHTML = `Low battery <i class="ri-plug-line animated-red"></i>`;
        } else if (percentage <= 40) { /* We validate if the battery is charging */
            batteryStatus.innerHTML = `Charging... <i class="ri-flashlight-line animated-green"></i>`;
        } else { /* If it's not loading, don't show anything. */
            batteryStatus.innerHTML = '';
        }

        /* 4. We change the colors of the battery and remove the other colors */
        if (percentage <= 20) {
            batteryLiquid.classList.add('gradient-color-red');
            batteryLiquid.classList.remove('gradient-color-orange', 'gradient-color-yellow', 'gradient-color-green');
        } else if (percentage <= 40) {
            batteryLiquid.classList.add('gradient-color-orange');
            batteryLiquid.classList.remove('gradient-color-red', 'gradient-color-yellow', 'gradient-color-green');
        } else if (percentage <= 80) {
            batteryLiquid.classList.add('gradient-color-yellow');
            batteryLiquid.classList.remove('gradient-color-red', 'gradient-color-orange', 'gradient-color-green');
        } else {
            batteryLiquid.classList.add('gradient-color-green');
            batteryLiquid.classList.remove('gradient-color-red', 'gradient-color-orange', 'gradient-color-yellow');
        }
    };

    function updateBatteryPercentage() {
        fetch("/get_battery_percentage")
            .then(response => response.json())
            .then(data => {
                updateBattery(data.percentage);
            })
            .catch(error => {
                console.error("Error fetching battery percentage:", error);
            });
    }

    updateBatteryPercentage(); /* Initial call */

    /* 5. Battery status events */
    setInterval(updateBatteryPercentage, 5000); /* Update every 5 seconds */
}

// Asumiendo que tienes un elemento en tu HTML con la clase 'pointer' para la aguja del velocímetro
const speedometerNeedle = document.querySelector('.gauge .pointer. hand');

function updateSpeed() {
    // Realiza una solicitud al servidor Flask para obtener la velocidad del motor
    fetch("/get_motor_speed")
        .then(response => response.json())
        .then(data => {
            // Actualiza el valor d¿e velocidad en tu interfaz de usuario
            const velocidad = data.speed;
            const max_velocidad = 40;

            // Actualiza la posición de la aguja del velocímetro
            const rotationAngle = data.speed * 9; // Ajusta según sea necesario
            document.querySelector(".gauge .pointer .hand").style.transform = `rotate(${deg}deg)`;
        })
}

// Llama a la función para actualizar la velocidad cada 1 segundo (ajusta según sea necesario)
setInterval(updateSpeed, 1000);
