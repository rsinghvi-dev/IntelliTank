import serial
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

ser = serial.Serial('/dev/ttyS0',
                    baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)# Update with your serial port and baud rate

@app.route('/')
def index():
    data = ser.readline().decode().strip().split(',')
    print(data)
    temperature = float(data[2])
    ph = float(data[1])
    turbidity = float(data[0])
    tds = float(data[3])
    dissolved_oxygen = float(data[4])
    temperature_class = get_value_class(temperature, 65, 75)
    ph_class = get_value_class(ph, 6.5, 7.5)
    turbidity_class = get_value_class(turbidity, 0, 2000)
    tds_class = get_value_class(tds, 0, 100)
    dissolved_oxygen_class = get_value_class(dissolved_oxygen, 5, 10)
    return render_template('index.html', temperature=temperature, ph=ph, turbidity=turbidity, tds=tds, dissolved_oxygen=dissolved_oxygen,
    	temperature_class=temperature_class, ph_class=ph_class, turbidity_class=turbidity_class, tds_class=tds_class, dissolved_oxygen_class=dissolved_oxygen_class, 
        my_data=data)

@app.route('/sensor-data')
def sensor_data():
    data = ser.readline().decode().strip().split(',')
    print(data)
    temperature = float(data[2])
    ph = float(data[1])
    turbidity = float(data[0])
    tds = float(data[3])
    dissolved_oxygen = float(data[4])
    temperature_class = get_value_class(temperature, 65, 75)
    ph_class = get_value_class(ph, 6.5, 7.5)
    turbidity_class = get_value_class(turbidity, 0, 2000)
    tds_class = get_value_class(tds, 0, 100)
    dissolved_oxygen_class = get_value_class(dissolved_oxygen, 5, 10)
    return jsonify(temperature=temperature, ph=ph, turbidity=turbidity, tds=tds, dissolved_oxygen=dissolved_oxygen,
    	temperature_class=temperature_class, ph_class=ph_class, turbidity_class=turbidity_class, tds_class=tds_class, dissolved_oxygen_class=dissolved_oxygen_class)


def get_value_class(value, min_value, max_value):
    if value < min_value:
        # print(f'{value} is below range ({min_value} - {max_value})')
        return 'low'
    elif value > max_value:
        # print(f'{value} is above range ({min_value} - {max_value})')
        return 'high'
    else:
        # print(f'{value} is within range ({min_value} - {max_value})')
        return 'normal'
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')