


'''
send data to serial port in a thread 

'''

import time
import serial
from threading import Thread




def send_data_to_serial(ser:serial.Serial, data: str, interval: int):
    while True:
        for i in range(10):
            
            ser.write(data.encode())
        time.sleep(interval)
    


if __name__=="__main__":
    ser = serial.Serial(port='COM69', baudrate=115200, timeout=1)
    thread1 = Thread(target=send_data_to_serial, args=(ser, '0000 0000\n', 1), daemon=True) 
    thread2 = Thread(target=send_data_to_serial, args=(ser, '1111 1111\n', 1), daemon=True)
    
    thread1.start()
    thread2.start()
    
    
    time.sleep(10)
    
    ser.close()    
    
    


