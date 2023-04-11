import serial
import time
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests

app = Flask(__name__)
data = {}
wled_ip = "4.3.2.1"
ser = serial.Serial('/dev/ttyUSB1',
                    baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)# Update with your serial port and baud rate

@app.route('/')
def index():
    data = ser.readline().decode().strip().split(',')
    ser.flushInput()
    print(data)
    temperature = float(data[2])
    ph = float(data[1])
    turbidity = float(data[0])
    tds = float(data[3])
    dissolved_oxygen = get_feeder_storage(int(data[4]))
    # Get the class of the data
    temperature_class = get_value_class(temperature, 70, 80)
    ph_class = get_value_class(ph, 6.5, 8.5)
    turbidity_class = get_value_class(turbidity, 0, 500)
    tds_class = get_value_class(tds, 0, 250)
    if dissolved_oxygen == "LOW":
        dissolved_oxygen_class = "low"
    else:
        dissolved_oxygen_class = "normal"
    return render_template('index.html', temperature=temperature, ph=ph, turbidity=turbidity, tds=tds, dissolved_oxygen=dissolved_oxygen,
    	temperature_class=temperature_class, ph_class=ph_class, turbidity_class=turbidity_class, tds_class=tds_class, dissolved_oxygen_class=dissolved_oxygen_class)

@app.route('/sensor-data')
def sensor_data():
    data = ser.readline().decode().strip().split(',') # Read the serial port and split the data
    ser.flushInput() # Clear the serial port
    print(data)
    # Convert the data to floats
    temperature = float(data[2])
    ph = float(data[1])
    turbidity = float(data[0])
    tds = float(data[3])
    dissolved_oxygen = get_feeder_storage(int(data[4]))
    # Get the class of the data
    temperature_class = get_value_class(temperature, 70, 80)
    ph_class = get_value_class(ph, 6.5, 8.5)
    turbidity_class = get_value_class(turbidity, 0, 500)
    tds_class = get_value_class(tds, 0, 250)
    if dissolved_oxygen == "LOW":
        dissolved_oxygen_class = "low"
    else:
        dissolved_oxygen_class = "normal"
        
    # Return the data as JSON
    return jsonify(temperature=temperature, ph=ph, turbidity=turbidity, tds=tds, dissolved_oxygen=dissolved_oxygen,
    	temperature_class=temperature_class, ph_class=ph_class, turbidity_class=turbidity_class, tds_class=tds_class, dissolved_oxygen_class=dissolved_oxygen_class)

# @app.route('/sensor-data', methods=['POST', 'GET'])
# def sensor_data():
#     global data
#     if request.method == 'POST':
#         data = request.json
#         print('Received sensor data:', data)
#         print(type(data))
#         return jsonify(data)
#     else:
#         return jsonify(data)

@app.route('/feeder', methods=['POST'])
def feeder():
    # Send the string "F" in serial when the feeder button is clicked
    ser.write(b"F\n")
    print("Feed button pressed on the server")
    return jsonify({"result": "success"})

@app.route('/bubbler', methods=['POST'])
def bubbler():
    # Send the string "B" in serial when the bubbler button is clicked
    ser.write(b"B\n")
    print("Bubbler button pressed on the server")
    return jsonify({"result": "success"})

@app.route('/change_mode', methods=['POST'])
def change_mode():
    # Change the mode of the WLED strip
    mode = request.form['mode']
    url = f'http://{wled_ip}/win&FX={mode}'
    requests.get(url)
    return redirect(url_for('index'))

@app.route('/change_brightness', methods=['POST'])
def change_brightness():
    # Change the brightness of the WLED strip
    brightness = request.form['brightness']
    url = f'http://{wled_ip}/win&A={brightness}'
    requests.get(url)
    return redirect(url_for('index'))

@app.route('/change_speed', methods=['POST'])
def change_speed():
    # Change the speed of the WLED strip
    speed = request.form['speed']
    url = f'http://{wled_ip}/win&SX={speed}'
    requests.get(url)
    return redirect(url_for('index'))

@app.route('/change_intensity', methods=['POST'])
def change_intensity():
    # Change the intensity of the WLED strip
    intensity = request.form['intensity']
    url = f'http://{wled_ip}/win&IX={intensity}'
    requests.get(url)
    return redirect(url_for('index'))

@app.route('/change_color', methods=['POST'])
def change_color():
    # Change the color of the WLED strip
    print(request.form['color'])
    color = request.form['color'].lstrip("#")
    r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    url = f'http://{wled_ip}/win&R={r}&G={g}&B={b}'
    requests.get(url)
    return redirect(url_for('index'))

@app.route('/livestream')
def livestream():
    # Use the YouTube API to get the livestream ID

    # Render the template with the embedded livestream
    return render_template('livestream.html', livestream_id='RBxBVUzWIfM')

# @app.route('/led/<int:config>')
# def led(config):
#     # Send the string "LEDn" in serial when a led config button is clicked, where n is the config number
#     ser.write(f"LED{config}\n".encode('utf-8'))
#     return 'OK'

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
    
def get_feeder_storage(mm):
    if mm > 40 and mm < 60:
        return "MED"
    elif mm >= 60 and mm <= 95:
        return "LOW"
    elif mm <= 40:
        return "FULL"
    else:
        return "OPEN"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')