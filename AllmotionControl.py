#Allmotion Python Serial port example
#Verified on Win 10  With CP2101 USB UART Bridge Running On COM5
#Verified on Anaconda Spyder 2.7

# may need to do do pip install pyserial at command prompt

import serial
import time
import random

# read response
def read_response(ser):
    return ser.read_until(expected=b'\r\n')

# ser has to be serial.Serial object. command is b'/1 command string'
def send_command_then_wait_for_ready(ser, command):
    ser.write(command)
    time.sleep(.1)
    resp = read_response(ser)
    # print(resp)
    waitForReady(ser)

# ser has to be serial.Serial object
def waitForReady(ser):
    resp = ''
    while True:
        ser.write(b'/1Q\r\n')
        resp = read_response(ser)
        # print(resp)
        if b'/0`' in resp:
            break
    return resp

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

def set_default_speed_accel(ser):
    send_command_then_wait_for_ready(ser, b'/1aM1V40000L20R\r\n')
    send_command_then_wait_for_ready(ser, b'/1aM1aaL500R\r\n')
    send_command_then_wait_for_ready(ser, b'/1aM1aL5R\r\n')
    
    send_command_then_wait_for_ready(ser, b'/1aM2V40000L10R\r\n')
    send_command_then_wait_for_ready(ser, b'/1aM2aL5aaL500R\r\n')
    
def enable_limit_mode(ser):
    send_command_then_wait_for_ready(ser, b'/1aM1n2\r\n')
    send_command_then_wait_for_ready(ser, b'/1aM2n2\r\n')

def home_Z(ser):
    send_command_then_wait_for_ready(ser, b'/1aM2n0\r\n')
    send_command_then_wait_for_ready(ser, b'/1aM2V20000L10Z134400R\r\n')    # home fast
    send_command_then_wait_for_ready(ser, b'/1aM2V5000L10Z5000R\r\n')    # home slow
    set_default_speed_accel(ser)
    
def home_X(ser):
    send_command_then_wait_for_ready(ser, b'/1aM1n0\r\n')
    send_command_then_wait_for_ready(ser, b'/1aM1V10000L20Z116800R\r\n')    # home fast
    send_command_then_wait_for_ready(ser, b'/1aM1V1000L20Z1200R\r\n')     # home slow
    set_default_speed_accel(ser)
    
def Z_down(ser):
    send_command_then_wait_for_ready(ser, b'/1aM2A109606R\r\n')

def Z_up(ser):
    send_command_then_wait_for_ready(ser, b'/1aM2A0R\r\n')
    
def go_to_X(ser, coord):
    cmd_string = f'/1aM1A{coord}R\r\n'
    send_command_then_wait_for_ready(ser, bytes(cmd_string, 'utf-8'))

def encoder_CV_Test(ser):
    res = []
    for i in range(10):
        home_X(ser)
        send_command_then_wait_for_ready(ser, b'/1aM1z0R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1V3500A100000R\r\n')
        res.append(read_encoder(ser, 1))
        print(res)
        
        send_command_then_wait_for_ready(ser, b'/1aM1V59900A0R\r\n')
    
    return res

def back_and_forth_X(ser):
    for i in range(10):
        home_X(ser)
        # enable_limit_mode(ser)
        send_command_then_wait_for_ready(ser, b'/1aM1A100000R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM1A0R\r\n')
        print(i)
        
def back_and_forth_Z(ser):
    for i in range(10):
        home_Z(ser)
        send_command_then_wait_for_ready(ser, b'/1aM2A100000R\r\n')
        send_command_then_wait_for_ready(ser, b'/1aM2A0R\r\n')
        print(i)

def go_to_all_WP_loc(ser):
    for i in range(10):
        home_Z(ser)
        home_X(ser)
        
        # send_command_then_wait_for_ready(ser, b'/1aM1A18975R\r\n')     # col 12
        go_to_X(ser, 18975)
        Z_down(ser)
        Z_up(ser)
        home_Z(ser)
        
        for j in range(11):
            send_command_then_wait_for_ready(ser, b'/1aM1P5669R\r\n')  # go to next column
            Z_down(ser)
            Z_up(ser)
            home_Z(ser)
        
        send_command_then_wait_for_ready(ser, b'/1aM1A0R\r\n')         # go to 0 (wash station)
        print(i)
        
def go_to_random_WP_loc(ser):
    for i in range(10):
        home_Z(ser)
        home_X(ser)
        
        well_loc = [18976, 24645, 30314, 35983, 41653, 47322, 52991, 58661, 64330, 69999, 75668, 81338]
        
        for j in range(12):
            random.shuffle(well_loc)    # randomize order
            go_to_X(ser, well_loc[i])   # go to well
            Z_down(ser)
            time.sleep(.5)
            Z_up(ser)
            home_Z(ser)
        
        send_command_then_wait_for_ready(ser, b'/1aM1A0R\r\n')         # go to 0 (wash station)
        print(i)
 
ser = find_AllMotion()

# encoder_CV_Test(ser)
# go_to_all_WP_loc(ser)
# back_and_forth_X(ser)
go_to_random_WP_loc(ser)

ser.close()  
