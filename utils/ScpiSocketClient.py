import socket
import time
import threading


class SocketClient:
    def __init__(self, host, port, timeout=1, reconnect_interval=1, max_reconnect_attempts=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.reconnect_interval = reconnect_interval
        self.max_reconnect_attempts = max_reconnect_attempts
        
        self.socket = None
        self.running = False
        
        self.thread = None
        self.lock = threading.Lock()
        self.connected = threading.Event()
        
        self.connected.clear()
        
    def _run(self):
        while self.running:
            if not self.connected.is_set():
                print("[SocketClient] Connecting...")
                self._connect()
            time.sleep(self.reconnect_interval)
    
    def _connect(self):
        with self.lock:
            try:
                if self.socket:
                    self.socket.close()
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(self.timeout)
                self.socket.connect((self.host, self.port))
                self.connected.set()
                print("[SocketClient] Connected to server")
            except socket.error as e:
                self.connected.clear()
                print(f"[SocketClient] Connection failed: {e}")


    def send_command(self, command:str,auto_read=True,read_response=False):
        if not self.connected.is_set():
            return False, None
        with self.lock:
            if command[-1] != '\n':
                command += '\n'
            try:
                # print(f"[SocketClient] Sending command: {command.encode()}")
                self.socket.sendall(command.encode())
                response = None
                if auto_read and '?' in command or read_response:
                    response = self.socket.recv(1024)
                return True, response
                
            except socket.error as e:
                self.connected.clear()
                print(f"[SocketClient] Send/Receive error: {e}")
            except Exception as e:
                self.connected.clear()
                print(f"[SocketClient] Unexpected error: {e}")
            return False, None


    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        if self.socket:
            self.socket.close()
        self.connected.clear()
        print("[SocketClient] Client stopped")
        
    def get_connection_status(self):
        '''Check if the client is connected to the server'''
        '''get correct status after sending command'''
        return self.connected.is_set()
    
    def wait_connect(self):
        '''Wait until the client is connected to the server'''
        self.connected.wait()
        return True

    # # stop the client when del
    # def __del__(self):
    #     self.stop()



if __name__ == "__main__":
    client = SocketClient("127.0.0.1", 2268)
    client.start()
    
    try:
        while True:
            cmd = input()
            if cmd.lower() == "exit":
                break
            succ, response = client.send_command(cmd)
            if succ:
                print('Command sent')
            else:
                print('Failed to send command')
                
            if response:
                print(f">>Received response: {response.decode()}")
    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down...")
    finally:
        print("Exiting...")
        client.stop()
        print("Done")