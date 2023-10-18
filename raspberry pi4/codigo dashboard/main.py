from flask import Flask, jsonify, render_template
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

app = Flask(_name_)

# Create the I2C bus and ADC object
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Create an analog input channel on the ADC
chan = AnalogIn(ads, ADS.P0)

# Define the voltage divider ratio
voltage_divider_ratio = 15

# Define the battery capacity in Ah
battery_capacity = 100

# Define the battery voltage range
battery_voltage_min = 0.0 * 12  # 2.4V per cell for a 12-cell battery
battery_voltage_max = 4.0 * 12  # 4.2V per cell for a 12-cell battery

def calculate_percentage_charge(adc_voltage):
    # Calculate the battery voltage
    battery_voltage = adc_voltage * voltage_divider_ratio

    # Check if the battery voltage is within the expected range
    if battery_voltage < battery_voltage_min or battery_voltage > battery_voltage_max:
        return 0  # Default to 0% if voltage is out of range

    # Calculate the percentage of charge
    percentage_charge = ((battery_voltage - battery_voltage_min) / (battery_voltage_max - battery_voltage_min)) * 100

    # Check if the percentage of charge is within the expected range
    if percentage_charge < 0:
        percentage_charge = 0
    elif percentage_charge > 100:
        percentage_charge = 100

    return percentage_charge


@app.route("/")
def index():
    # Render the template with the percentage value
    return render_template("index.html", percentage=0)

if _name_ == "_main_":
    app.run()


@app.route("/get_battery_percentage")
def get_battery_percentage():
    # Read the voltage from the ADC
    adc_voltage = chan.voltage

    # Calculate the percentage of charge
    percentage_charge = calculate_percentage_charge(adc_voltage)

    # Return the percentage in JSON format
    return jsonify({"percentage": percentage_charge})