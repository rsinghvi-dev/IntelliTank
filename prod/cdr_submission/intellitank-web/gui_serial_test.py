import PySimpleGUI as sg
import serial
import time
import requests

data = {}

ser = serial.Serial('/dev/ttyUSB1',
                    baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)# Update with your serial port and baud rate

def update_values():
    try:
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
            dissolved_oxygen_class = "red"
        else:
            dissolved_oxygen_class = "white"
        return [[temperature, ph, turbidity, tds, dissolved_oxygen], \
            [temperature_class, ph_class, turbidity_class, tds_class, dissolved_oxygen_class]]
    except Exception as e:
        print(f"Error reading sensor data: {e}")
        return None
    
# Function to handle the "FEED" button press
def on_feed_button_pressed():
    print("Feed button pressed on the client")
    response = requests.post('http://localhost:5000/feeder')
    if response.status_code == 200 and response.json().get('result') == 'success':
        print("Feed request was successful")
    else:
        print("Feed request failed")

#Function to handle the "BUBBLE" button press
def on_bubble_press():
    print("Bubbler button pressed on the client")
    response = requests.post('http://localhost:5000/bubbler')
    if response.status_code == 200 and response.json().get('result') == 'success':
        print("Bubbler request was successful")
    else:
        print("Bubbler request failed")

def get_feeder_storage(mm):
    if mm > 40 and mm < 60:
        return "MED"
    elif mm >= 60 and mm <= 95:
        return "LOW"
    elif mm <= 40:
        return "FULL"
    else:
        return "OPEN"

def get_value_class(value, min_value, max_value):
    if value < min_value:
        # print(f'{value} is below range ({min_value} - {max_value})')
        return 'red'
    elif value > max_value:
        # print(f'{value} is above range ({min_value} - {max_value})')
        return 'red'
    else:
        # print(f'{value} is within range ({min_value} - {max_value})')
        return 'white'

# Hardcoded values for sensor data
temperature = 0.0
ph = 0.0
tds = 0
turbidity = 0.0
dissolved_oxygen = 0

# col_layout = [
#     []
# ]
# Define the layout
layout = [
    [sg.Text(f'Temperature: {temperature:.1f} °C', key='TEMP', font=('Helvetica', 26), size=(100, 1), text_color='white', background_color='black')],
    [sg.Text(f'pH: {ph:.1f}', key='PH', font=('Helvetica', 26), size=(100, 1), text_color='white', background_color='black')],
    [sg.Text(f'TDS: {tds} ppm', key='TDS', font=('Helvetica', 26), size=(100, 1), text_color='white', background_color='black')],
    [sg.Text(f'Turbidity: {turbidity:.1f} NTU', key='TURBIDITY', font=('Helvetica', 26), size=(100, 1), text_color='white', background_color='black')],
    [sg.Text(f'Feeder Measurement: {dissolved_oxygen}', key='DO', font=('Helvetica', 26), size=(100, 1), text_color='white', background_color='black')],
    [sg.Button('FEED', key='FEED', button_color=('white', 'red'), font=('Helvetica', 24), size=(20, 3), pad=(200, 100))],
    [sg.Button('BUBBLER', key='BUBBLER', button_color=('white', 'red'), size=(10,4), pad=(200, 100))],
]

# Create the window
window = sg.Window('Sensor App', layout, background_color='black', size=(700, 500), finalize=True)
window.Maximize()

# Event loop
while True:
    event, values = window.read(timeout=2000)

    if event == sg.WIN_CLOSED:
        break
    elif event == 'FEED':
        on_feed_button_pressed()
    elif event == "BUBBLER":
        on_bubble_press()
    elif event == sg.TIMEOUT_EVENT:
    # Convert the data to 
        data = update_values()
        if data:
            window['TEMP'].update(f'Temperature: {data[0][0]:.1f} °C', text_color = data[1][0])
            window['PH'].update(f'pH: {data[0][1]:.1f}', text_color = data[1][1])
            window['TDS'].update(f'TDS: {data[0][3]} ppm', text_color = data[1][3])
            window['TURBIDITY'].update(f'Turbidity: {data[0][2]:.1f} NTU', text_color = data[1][2])
            window['DO'].update(f'Feeder Measurement: {data[0][4]}', text_color = data[1][4])

# Close the window
window.close()
