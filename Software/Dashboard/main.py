from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import time
speed=0

app = Flask(__name__)

try:
    # Intentar importar módulos específicos que dependen del ADC
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

    # Intentar crear el objeto I2C bus y ADC
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)

    # Crear un canal de entrada analógica en el ADC
    chan = AnalogIn(ads, ADS.P0)

    # Definir la función int0 después de haber importado el módulo
    def int0(channel):
        global up_times, index, m2
        m1 = time.time()
        up_times[index] = (m1 - m2) * 1E6
        index = (index + 1) % 3
        m2 = m1
except ImportError:
    print("Error: No se pudo importar el módulo del ADC. El ADC no estará disponible.")
    chan = None  # Configurar chan como None si el ADC no está disponible
    encoder_reading_pin = None  # Configurar encoder_reading_pin como None si el ADC no está disponible
except Exception as e:
    print(f"Error initializing ADC: {e}")
    chan = None  # Configurar chan como None si la inicialización falla
    encoder_reading_pin = None  # Configurar encoder_reading_pin como None si la inicialización falla

# Configuración de GPIO si encoder_reading_pin está definido
if encoder_reading_pin is not None:
    GPIO.setmode(GPIO.BCM)

    # Variables para el medidor de velocidad
    encoder_reading_pin = 17
    up_times = [0, 0, 0]
    index = 0
    m2 = time.time()
    speed = 0

    GPIO.setup(encoder_reading_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(encoder_reading_pin, GPIO.BOTH, callback=int0)


# Función para calcular el porcentaje de carga de la batería
def calculate_percentage_charge(adc_voltage):
    if adc_voltage is None:
        return 0  # Default to 0% if ADC is not initialized

    # Define las variables de la batería
    voltage_divider_ratio = 15
    battery_voltage_min = 0.0 * 12  # 2.4V per cell for a 12-cell battery
    battery_voltage_max = 4.0 * 12  # 4.2V per cell for a 12-cell battery

    # Calcula el voltaje de la batería y el porcentaje de carga
    battery_voltage = adc_voltage * voltage_divider_ratio

    if battery_voltage < battery_voltage_min or battery_voltage > battery_voltage_max:
        return 0  # Default to 0% if voltage is out of range

    percentage_charge = ((battery_voltage - battery_voltage_min) / (battery_voltage_max - battery_voltage_min)) * 100

    if percentage_charge < 0:
        percentage_charge = 0
    elif percentage_charge > 100:
        percentage_charge = 100

    return percentage_charge

# Variable global para el perfil de frenado
braking_profile = "dry"  # Valor predeterminado

# Ruta para cambiar el perfil de frenado
@app.route('/set_braking_profile')
def set_braking_profile():
    global braking_profile
    profile = request.args.get('profile')
    
    if profile in ["dry", "rain", "snow"]:
        braking_profile = profile
        return f"Perfil de frenado cambiado a: {braking_profile}"
    else:
        return "Perfil no válido", 400

# Ruta para obtener el perfil de frenado actual (opcional)
@app.route('/get_braking_profile')
def get_braking_profile():
    return jsonify(profile=braking_profile)


# Endpoint para obtener el porcentaje de batería
@app.route("/get_battery_percentage", methods=["GET"])
def get_battery_percentage():
    # Leer el voltaje del ADC
    if chan is None:
        adc_voltage = 0  # Default to 0 if ADC is not initialized
    else:
        adc_voltage = chan.voltage

    # Calcular el porcentaje de carga
    percentage_charge = calculate_percentage_charge(adc_voltage)

    # Devolver el porcentaje en formato JSON
    return jsonify({"percentage": percentage_charge})

# Endpoint para obtener la velocidad actual
@app.route("/get_motor_speed", methods=["GET"])
def get_motor_speed():
    global speed
    return jsonify({"speedd": speed})

# Renderizar la plantilla con los valores del porcentaje y la velocidad
@app.route("/")
def index():
    return render_template("index.html", percentage=0, speedd=0)

if __name__ == "__main__":
    app.run()
