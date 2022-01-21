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

# ser.write(b'/1aM1V781L30Z18045R\r\n')
ser.write(b'/1Q\r\n')
time.sleep(0.5)
print(ser.read(size=5).decode("utf-8"))
ser.close()  