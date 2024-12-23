import socket
import threading
import queue
import time
import serial

'''
    this program not tested yet

'''

class ScpiSerialPortWorker:
    def __init__(self, comport, baudrate, timeout=0.5):
        self.serial = serial.Serial(
            port=comport,
            baudrate=baudrate,
            timeout=timeout
        )
        
        self.task_queue = queue.Queue()
        self.running = False
        self.worker_thread = None
        
        self.connected = threading.Event()
        self.connected.clear()

    def start(self):
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_task, daemon=True)
            self.worker_thread.start()
            self._connect()

    def stop(self):
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
        if self.serial:
            self.serial.close()
        print(f"[SerialPortWorker] Disconnected from {self.serial.port}")

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

    def _process_task(self): # worker thread, process task in queue
        while self.running:
            try:
                function, args, callback = self.task_queue.get(timeout=0.1)
                # check connection status
                if not self.connected.is_set():
                    self._connect()
                    
                result = function(*args)
                if callback:
                    callback(result)
            except queue.Empty:
                continue

    def _add_task(self, function, args, callback):
        if self.get_task_count() > 10:
            print(f"[SerialPortWorker] too heavy load, task queue size: {self.get_task_count()}")
        self.task_queue.put((function, args, callback))
        

    def _send_command(self, command, auto_read=True, read_response=False):
        if not self.connected.is_set():
            return False, None
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
        
    def get_task_count(self):
        return self.task_queue.qsize()
    
    def send_command_threaded(self, command, auto_read=True, read_response=False, callback=None):
        self._add_task(self._send_command, (command, auto_read, read_response), callback)

    def get_connection_status(self):
        return self.connected.is_set()

    def wait_connect(self):
        self.connected.wait()
        return True
    
    
if __name__ == "__main__":
    comport = "COM3"
    baudrate = 9600
    worker = ScpiSerialPortWorker(comport, baudrate)
    worker.start()
    
    
    
    
    def callback(resault):
        succ, response = resault
        if succ:
            print('Command sent')
            if response:
                print(f">>Received response: {response.decode()}")
        else:
            print('Failed to send command')
    
    try:
        while True:
            cmd = input()
            if cmd.lower() == "exit":
                break
            worker.send_command_threaded(cmd, callback=callback)
    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down...")
    finally:
        print("Exiting...")
        worker.stop()
        print("Done")
        