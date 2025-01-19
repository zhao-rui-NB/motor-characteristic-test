import socket
import threading
import queue
import time
import serial


'''
   2025_0118: change to sync, not test

'''



class ScpiSerialPortWorker:
    def __init__(self, comport, baudrate, timeout=0.5):
        self.serial = serial.Serial(
            port=comport,
            baudrate=baudrate,
            timeout=timeout
        )
        
        self.connected = threading.Event()
        self.lock = threading.Lock()
        self.start()

    def _connect(self):
        try:
            if self.serial:
                self.serial.close()
            self.serial.open()
            
            self.connected.set()
            print(f"[SerialPortWorker] Connected to {self.serial.port}")
        except serial.SerialException as e:
            self.connected.clear()
            print(f"[SerialPortWorker] Connection failed: {e}")
    
    def start(self):
        if not self.connected.is_set():
            self._connect()
        else:
            print(f"[SerialPortWorker] Already connected to {self.serial.port}, please stop first")

    def stop(self):
        if self.serial:
            self.serial.close()
        print(f"[SerialPortWorker] Disconnected from {self.serial.port}")
        

    def send_command(self, command, auto_read=True, read_response=False):
        if not self.connected.is_set():
            return False, None
        with self.lock:
            try:
                if command[-1] != '\n':
                    command += '\n'
                self.serial.write(command.encode())
                response = None
                if auto_read and '?' in command or read_response:
                    response = self.serial.readline()
                return True, response
            except serial.SerialException as e:
                self.connected.clear()
                print(f"[SerialPortWorker] Error sending command: {e}")
                return False, None

    def get_connection_status(self):
        return self.connected.is_set()

    def wait_connect(self):
        self.connected.wait()
        return True
    
    
if __name__ == "__main__":
    comport = "COM1"
    baudrate = 9600
    worker = ScpiSerialPortWorker(comport, baudrate)
    
    try:
        while True:
            cmd = input()
            if cmd.lower() == "exit":
                break
            succ, response = worker.send_command(cmd)
            if succ:
                print('Command sent')
                if response:
                    print(f">>Received response: {response.decode()}")
            else:
                print('Failed to send command')
                
    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down...")
    finally:
        print("Exiting...")
        worker.stop()
        print("Done")
        