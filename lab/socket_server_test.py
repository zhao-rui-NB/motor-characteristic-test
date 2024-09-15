import socket
import select
import sys
import time
import random

class SimPowerSupply:
    def __init__(self):
        self.voltage = 10
        self.current = 10
        self.frequency = 60
        self.output = False
        
        self.voltage_lim = (20, 90)
        
        self.voltage_range = 155 # 155,310,600        
        
        self.meas_voltage = 0
        self.meas_current = 0
        self.meas_power = 0
        
        self.update_meas()
    
    def update_meas(self):
        """更新測量值"""
        self.meas_voltage = self.voltage * (0.95 + 0.1 * random.random())
        self.meas_current = self.current * (0.95 + 0.1 * random.random())
        self.meas_power = self.meas_voltage * self.meas_current

    def scpi_command(self, command):
        """解析 SCPI 指令"""       
        '''
        *IDN	
        *CLS	
        MEAS:CURR	
        MEAS:VOLT
        MEAS:POW:APP
        MEAS:POW
        SOUR:READ
        SOUR:VOLT
        SOUR:FREQ
        SOUR:CURR:LIM:RMS
        SOUR:VOLT:RANG
        OUTPut
        SYSTem:REBoot
        
        '''

        if command == "*IDN?":
            return "GWINSTEK,APS-7100,GEQ120257,01.10.20151016\n"
        elif command == "*CLS":
            return None
        elif command == "MEAS:CURR?":
            # return f"{self.current:.3f}"
            # test num time 
            return f'{time.time():.3f}'
            
        elif command == "MEAS:VOLT?":
            return f"{self.voltage:.3f}"
        elif command == "MEAS:POW:APP?":
            return f"{self.voltage * self.current:.3f}"
        elif command == "MEAS:POW?":
            return f"{self.voltage * self.current:.3f}"
        elif command == "SOUR:READ?":
            return f"{self.meas_voltage:.3f},{self.meas_current:.3f},{self.frequency:.3f},{self.meas_power:.3f},{self.meas_power:.3f},{self.current*3:.3f}"

        
        elif command == "SOUR:VOLT?":
            return f"{self.voltage:.3f}"
        elif command == "SOUR:FREQ?":
            return f"{self.frequency:.3f}"
        elif command == "SOUR:CURR:LIM:RMS?":
            return f"{self.current:.3f}"
        elif command == "SOUR:VOLT:RANG?":
            return f'{self.voltage_range[0]:.3f},{self.voltage_range[1]:.3f}'
        elif command == "OUTPut?":
            return "1" if self.output else "0"
        
   
        
        
        elif command.startswith("SOUR:VOLT "):
            self.voltage = float(command.split(" ")[1])
            self.update_meas()
            return None
        # elif command.startswith("SOUR:CURR "):
        #     self.current = float(command.split(" ")[1])
        #     self.update_meas()
        #     return None
        elif command.startswith("SOUR:FREQ "):
            self.frequency = float(command.split(" ")[1])
            self.update_meas()
            return None
        elif command.startswith("OUTPut "):
            self.output = command.split(" ")[1] == "1"
            self.update_meas()
            return None

        elif command.startswith("SOUR:CURR:LIM:RMS "):
            val = command.split(" ")[1]
            self.current = float(val)
            self.update_meas()
        
        elif command.startswith("SOUR:VOLT:LIM:RMS "):
            val = command.split(" ")[1]
            v = val.split(",")
            self.voltage_range[0] = float(v[0])
            self.voltage_range[1] = float(v[1])
            return None
        
        elif command.startswith("SOUR:VOLT:RANG "):
            val = command.split(" ")[1]
            v = val.split(",")
            self.voltage_range[0] = float(v[0])
            self.voltage_range[1] = float(v[1])
            return None
        
            
        

    def print_power_now_state(self):
        print('-' * 50)
        print("Power Supply State:")
        print(f"{'Voltage':18}{'Current':18}{'Power':18}")
        print(f'{self.voltage:<18.3f}{self.current:<18.3f}{self.voltage * self.current:<18.3f}')
        print(f"{'Meas Voltage':18}{'Meas Current':18}{'Meas Power':18}")
        print(f'{self.meas_voltage:<18.3f}{self.meas_current:<18.3f}{self.meas_power:<18.3f}')        
        print(f'{"OUTPUT state":18}' )
        print(f'{self.output:<18}')
        print('-' * 50)
        
        





















class SocketServer:
    def __init__(self, host='127.0.0.1', port=2268):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.power_supply = SimPowerSupply()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        
        while True:
            print("Waiting for a connection...")
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection established with {client_address}")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode().strip()
                print(f"Received from client: {message}")
                
                power_resp = self.power_supply.scpi_command(message)
                self.power_supply.print_power_now_state()

                if power_resp:
                    print(f"Power supply response: {power_resp}")
                    client_socket.send(power_resp.encode())
                else:
                    print("No response from power supply")
            except socket.error as e:
                print(f"Client connection error: {e}")
                break
        
        print("Client disconnected")
        client_socket.close()


def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 2268))
    s.listen(5)
    s.settimeout(1.0)  # 設置 1 秒超時
    print("Server started on 127.0.0.1:2268")

    power_supply = SimPowerSupply()
    running = True

    while running:
        try:
            conn, client_addr = s.accept()
            print("Client connected:", client_addr)
            conn.settimeout(3)  # 設置客戶端連接的超時

            while running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode().strip()
                    print("Received from client:", message)

                    power_resp = power_supply.scpi_command(message)
                    power_supply.print_power_now_state()

                    if power_resp:
                        print("Power supply response:", power_resp)
                        conn.send(power_resp.encode())
                    else:
                        print("No response from power supply")
                        # conn.send(b"NO_RESPONSE")

                except socket.timeout:
                    # 超時，繼續循環以檢查 running 標誌
                    continue
                except Exception as e:
                    print("Error handling client:", e)
                    break

            conn.close()
            print("Client disconnected:", client_addr)

        except socket.timeout:
            # 超時，繼續主循環
            continue
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Shutting down...")
            running = False
        except Exception as e:
            print("Server error:", e)
            running = False

    s.close()
    print("Server shut down")


def run_server_select():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 2268))
    s.listen(5)
    s.settimeout(1.0)  # 設置 1 秒超時
    print("Server started on")
    
    power_supply = SimPowerSupply()
    running = True
    
    inputs = [s]
    outputs = []
    
    while running:
        readable, writable, exceptional = select.select(inputs, [], [])
        
        for r in readable:
            if r is s:
                conn, client_addr = r.accept()
                print("Client connected:", client_addr)
                conn.setblocking(0)
                inputs.append(conn)
                outputs.append(conn)
            else:
                data = r.recv(1024)
                if data:
                    message = data.decode().strip()
                    print("Received from client:", message)
                    
                    try :
                        power_resp = power_supply.scpi_command(message)
                        power_supply.print_power_now_state()
                    except ValueError as e:
                        print("Error handling client:", e)
                        power_resp = None

                    
                    if power_resp:
                        print("Power supply response:", power_resp)
                        r.send(power_resp.encode())
                    else:
                        print("No response from power supply")
                else:
                    print("Client disconnected:", r.getpeername())
                    inputs.remove(r)
                    outputs.remove(r)
                    r.close()
        
        

if __name__ == "__main__":
    # server = SocketServer()
    # try:
    #     server.start()
    # except KeyboardInterrupt:
    #     print("Keyboard interrupt received. Shutting down...")
    # finally:
    #     print("Server has been shut down.")
    #     server.server_socket.close()
    

    # run_server()
    
    try:
        run_server_select()
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down...")

    