from machine import ADC
from time import sleep, monotonic

v_ref = 5
scount = 30

adc = ADC(pin_no)
analog_buffer = []
analog_buffer_temp = []
copy_index = 0
average_voltage = 0
tds_value = 0
temperature = 25
        
while True:
    analog_sample_timepoint = monotonic()
    if (monotonic() - analog_sample_timepoint) > 0.04:
        analog_sample_timepoint = monotonic()
        count = 0
        analog_buffer.append(adc.read_u16())
        if count == scount:
            analog_buffer = []
            analog_buffer = 0
    print_timepoint = monotonic()
    if (monotonic() - print_timepoint) > 0.8:
        print_timepoint = monotonic()
        for i in range(scount):
            analog_buffer_temp[i] = analog_buffer[i]
        average_voltage = analog_buffer_temp.sort()
        mid = len(average_voltage) // 2
        average_voltage = (average_voltage[mid] + average_voltage[~mid]) / 2
        compensation_coeff = 1.0 + 0.02*(temperature - 25.0)
        compensation_voltage = average_voltage/compensation_coeff
        tdsValue = (133.42*compensation_voltage*compensation_voltage - 255.86*compensation_voltage*compensation_voltage + 857.39*compensation_voltage)*0.5
        print("TDS Value: " + str(int(tdsValue)) + " ppm")
    