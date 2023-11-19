import serial

arduino_port = 'COM3'
baud_rate = 115200

ser = serial.Serial(arduino_port, baud_rate, timeout=1)
breaking_case = False
while not breaking_case:
    received = False
    while not received:
        try:
            ser_out = ser.readline().decode().strip().split(',')
            if not len(ser_out) == 2:
                continue
            received = True
            ser_out = [float(i) for i in ser_out]
            print(f"left: {ser_out[0]}, right: {ser_out[1]}")
        except KeyboardInterrupt:
            ser.close()
            breaking_case = True
            exit()
        except Exception as e:  
            continue

print("Jes")