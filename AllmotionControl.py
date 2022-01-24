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
    ports = ['COM%s' % (i) for i in range(255,-1,-1)]

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
    raise Exception("AllMotion Not Found")

def read_encoder(ser, motor):
    if motor not in [1,2,3,4]:
        raise Exception('Motor number invalid')
    cmd_string = f'/1aM{motor}R\r\n'
    send_command_then_wait_for_ready(ser, bytes(cmd_string, 'utf-8'))   # switch to selected motor
    ser.write(b'/1?8\r\n')  # query encoder
    resp = str(read_response(ser))
    # print(resp)
    start_idx = resp.index('/0`') + 3
    end_idx = resp.index('x03') - 1
    return int(resp[start_idx : end_idx])

def encoder_CV_Test(ser):
    res = []
    for i in range(10):
        send_command_then_wait_for_ready(ser, b'/1aM1aE1000V10000L20Z116800R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1aE1000V1000L10Z116800R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1z0R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1V59900L30A100000R\r\n')
        res.append(read_encoder(ser, 1))
        print(res)
    
    return res

def back_and_forth(ser):
    for i in range(10):
        send_command_then_wait_for_ready(ser, b'/1aM1V10000L20Z116800R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1V1000L10Z116800R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1V59000L50A110000R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1V59900L50A0R\r\n')
        print(i)
        
ser = find_AllMotion()

back_and_forth(ser)

ser.close()  
