#Allmotion Python Serial port example
#Verified on Win 10  With CP2101 USB UART Bridge Running On COM5
#Verified on Anaconda Spyder 2.7

# may need to do do pip install pyserial at command prompt

import serial
import time

# read response
def read_response(ser):
    return ser.read_until(expected=b'\r\n')

# ser has to be serial.Serial object. command is b'/1 command string'
def send_command_then_wait_for_ready(ser, command):
    ser.write(command)
    waitForReady(ser)

# ser has to be serial.Serial object
def waitForReady(ser):
    while True:
        ser.write(b'/1Q\r\n')
        resp = read_response(ser)
        # print(resp)
        if b'/0`' in resp:
            break

# find AllMotion in list of COM ports
def find_AllMotion():
    ports = ['COM%s' % (i + 1) for i in range(0,256)]

    for port in ports:
        try:
            print(f'Checking {port}')
            ser = serial.Serial(port=port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, write_timeout=0.5, timeout=0.5)
            ser.write(b'/1&\r\n') # query board version
            resp = read_response(ser)
            if b'EZController AllMotion' in resp:
                print(f'Found AllMotion: {port}')
                return ser
            else:
                ser.close()
        except (OSError, serial.SerialException):
            pass
    return None


# send_command_then_wait_for_ready(ser, b'/1aM1aE1000V5000L10Z116800R\r\n')
# send_command_then_wait_for_ready(ser, b'/1aM1V59900L30A100000R\r\n')
# send_command_then_wait_for_ready(ser, b'/1aM1aE1000V5000L10Z116800R\r\n')
ser = find_AllMotion()
send_command_then_wait_for_ready(ser, b'/1aM1aE1000V5000L10Z116800R\r\n')
send_command_then_wait_for_ready(ser, b'/1aM1aE1000V5000L10Z116800R\r\n')
send_command_then_wait_for_ready(ser, b'/1aM1V59900L30A100000R\r\n')
ser.close()  