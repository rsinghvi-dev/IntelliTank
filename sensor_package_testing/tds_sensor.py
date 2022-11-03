from machine import ADC
import time

# import monotonic

v_ref = 5
scount = 30

adc = ADC(27)
analog_buffer = []
analog_buffer_temp = []
copy_index = 0
average_voltage = 0
tds_value = 0
temperature = 25
count = 0
        
while True:
    analog_sample_timepoint = time.time()
    if (time.time() - analog_sample_timepoint) > 0.04:
        analog_sample_timepoint = time.time()
        analog_buffer.insert(count, adc.read_u16())
        count+=1
        if count == scount:
#             analog_buffer = []
            count = 0
    print_timepoint = time.time()
    if (time.time() - print_timepoint) > 0.8:
        print_timepoint = time.time()
        for item in analog_buffer:
            analog_buffer_temp.append(item)
        average_voltage = analog_buffer_temp.sort()
        mid = len(average_voltage) // 2
        average_voltage = (average_voltage[mid] + average_voltage[~mid]) / 2
        compensation_coeff = 1.0 + 0.02*(temperature - 25.0)
        compensation_voltage = average_voltage/compensation_coeff
        tdsValue = (133.42*compensation_voltage*compensation_voltage - 255.86*compensation_voltage*compensation_voltage + 857.39*compensation_voltage)*0.5
        print("TDS Value: " + str(int(tdsValue)) + " ppm")
    