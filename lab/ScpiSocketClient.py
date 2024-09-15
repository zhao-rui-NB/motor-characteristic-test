import socket
import threading
import time
import queue


class SocketClient:
    def __init__(self, host, port, timeout=1, reconnect_interval=3):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.reconnect_interval = reconnect_interval
        self.socket = None
        self.command_queue = queue.Queue()
        self.failed_commands = None
        self.running = False
        self.connected_event = threading.Event()

    def _run(self):
        while self.running:
            if not self.connected_event.is_set():
                print("[SocketClient] Reconnecting...")
                self._reconnect()
            try:
                if self.failed_commands:
                    print("[SocketClient] Retrying failed command...")
                    command, read_response, callback = self.failed_commands
                    self.failed_commands = None
                else:
                    command, read_response, callback = self.command_queue.get(timeout=0.5)
                if command == '':
                    continue
                self.socket.sendall(command.encode())
                if read_response:
                    response = self.socket.recv(1024)
                    if callback:
                        callback(response)
            except queue.Empty:
                continue
            except socket.timeout:
                continue
            except socket.error as e:
                self.failed_commands = (command, read_response, callback)
                print(f"[SocketClient] Send/Receive error: {e}")
                self.connected_event.clear()

    def _connect(self):
        try:
            if self.socket:
                self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected_event.set()
            print("[SocketClient] Connected to server")
            
        except socket.error as e:
            print(f"[SocketClient] Connection failed: {e}")
            self.socket = None
        except Exception as e:
            print(f"[SocketClient] Unexpected error during connection: {e}")
            self.socket = None
    
    def _reconnect(self):
        self.connected_event.clear()
        while self.running:
            if self.socket:
                self.socket.close()
                self.socket = None
            self._connect()
            if self.connected_event.is_set():
                return
            time.sleep(self.reconnect_interval)
                
    def start(self):
        if self.running:
            return
        self._connect()
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        
    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        if self.socket:
            self.socket.close()
        print("[SocketClient] Client stopped")
    
    def send_command(self, command, response, callback=None):
        self.command_queue.put((command, response, callback))
        

if __name__ == "__main__":
    client = SocketClient("127.0.0.1", 2268)
    
    def callback(response):
        print(f">>Received response: {response.decode()}")
        
    client.start()
    
    try:
        while True:
            time.sleep(0.5)
            cmd = input()
            if cmd.lower() == "exit":
                break
            client.send_command(cmd, True, callback=callback)
    except KeyboardInterrupt:
        print("Interrupted by user. Shutting down...")
    finally:
        print("Exiting...")
        client.stop()
        print("Done")