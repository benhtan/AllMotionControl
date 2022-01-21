#Allmotion Python Serial port example
#Verified on Win 10  With CP2101 USB UART Bridge Running On COM5
#Verified on Anaconda Spyder 2.7

# may need to do do pip install pyserial at command prompt

import serial
import time

#ser.close()  

def serial_ports():
    ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# See which com port shows up and change "COM5" in code below to that com port
if __name__ == '__main__':
    print(serial_ports()) 
   
    ser = serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# ser has to be serial.Serial object. command is b'/1 command string'
def send_command_then_read_resp(ser, command):
    ser.write(command)
    return ser.read_until(expected=b'\r\n',size=8)

# ser has to be serial.Serial object
def waitForReady(ser):
    while True:
        ser.write(b'/1Q\r\n')
        if b'/0`' in ser.read_until(expected=b'\r\n',size=8):
            break

# find AllMotion in list of COM ports
def find_AllMotion():
    ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port=port, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
            s.write(b'/1&\r\n') # query board version
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# ser.write(b'/1aM1aE1000V5000L10Z116800R\r\n')   # Home
# waitForReady(ser)
# ser.write(b'/1aM1V59900L30A100000R\r\n')   # Go forward
# waitForReady(ser)
# ser.write(b'/1aM1aE1000V5000L10Z116800R\r\n')   # Home
# waitForReady(ser)
ser.close()  