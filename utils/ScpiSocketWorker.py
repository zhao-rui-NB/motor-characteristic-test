import socket
import threading
import queue
import time

class ScpiSocketWorker:
    def __init__(self, host, port, timeout=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        
        self.socket = None
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
        if self.socket:
            self.socket.close()
        print(f"[SocketWorker] Disconnected from {self.host}:{self.port}")

    def _connect(self):
        try:
            if self.socket:
                self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected.set()
            print(f"[SocketWorker] Connected to {self.host}:{self.port}")
        except socket.error as e:
            self.connected.clear()
            print(f"[SocketWorker] Connection failed: {e}")

    def _process_task(self): # worker thread, process task in queue
        while self.running:
            try:
                # get task from queue
                function, args, callback = self.task_queue.get(timeout=0.1)
                
                # check connection status
                if not self.connected.is_set():
                    self._connect()
                    
                result = function(*args)
                if callback:
                    callback(result)
            except queue.Empty:
                continue
            # except Exception as e:
            #     print(f"[SocketWorker] Error processing task: {e}")

    def _add_task(self, function, args, callback):
        if self.get_task_count() > 10:
            print(f"[SocketWorker] Too heavy load, task queue size: {self.get_task_count()}")
        self.task_queue.put((function, args, callback))

    def _send_command(self, command, auto_read=True, read_response=False):
        if not self.connected.is_set():
            return False, None
        try:
            if command[-1] != '\n':
                command += '\n'
            self.socket.sendall(command.encode())
            response = None
            if auto_read and '?' in command or read_response:
                response = self.socket.recv(1024)
            return True, response
        except socket.error as e:
            self.connected.clear()
            print(f"[SocketWorker] Send/Receive error: {e}")
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
    # new code
    worker = ScpiSocketWorker("127.0.0.1", 2268)
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
        