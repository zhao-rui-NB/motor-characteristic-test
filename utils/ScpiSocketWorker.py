import socket
import threading
import queue
import time

'''
   2025_0118: change to sync, not test

'''

class ScpiSocketWorker:
    def __init__(self, host, port, timeout=1):
        self.host = host
        self.port = port
        self.timeout = timeout
        
        self.socket = None
        
        self.lock = threading.Lock()
        self.connected = threading.Event()
        
        self.start()

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
    
    def start(self):
        if not self.connected.is_set():
            self._connect()
        else:
            print(f"[SocketWorker] Already connected to {self.host}:{self.port}, please stop first")
            
    def stop(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            
        print(f"[SocketWorker] Disconnected from {self.host}:{self.port}")

    def send_command(self, command, auto_read=True, read_response=False):
        if not self.connected.is_set():
            return False, None
        with self.lock:
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

    def get_connection_status(self):
        return self.connected.is_set()

    def wait_connect(self):
        self.connected.wait()
        return True
    
    
if __name__ == "__main__":
    # new code
    worker = ScpiSocketWorker("127.0.0.1", 2268)
    
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
        