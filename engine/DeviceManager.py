from threading import Thread
import time

from utils.PowerMeterSPM3 import PowerMeterSPM3
from utils.ModbusWorker import ModbusWorker
from utils.PowerSupplyASP7100 import PowerSupplyASP7100

class DeviceManager:
    
    def __init__(self):
        # hardware devices

        self.serial_port_workers = {}

        self.power_supply: PowerSupplyASP7100 = None
        self.power_meter: PowerMeterSPM3 = None 
    

    def init_power_supply(self, ip, port):
        self.power_supply = PowerSupplyASP7100(ip, port)
        return self.power_supply.worker.connected.is_set()

    def init_power_meter(self,com_port:str, slave_address, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5):
        com_port =  com_port.upper()
        
        if com_port not in self.serial_port_workers: # first make worker device will set parameters for the worker 
            self.serial_port_workers[com_port] = ModbusWorker(com_port, baudrate, parity, stopbits, bytesize, timeout)
        
        self.power_meter = PowerMeterSPM3(self.serial_port_workers[com_port], slave_address)
        # return check if the device is connected
        
        return self.power_meter.worker.client.is_socket_open()
    
    # release resources
    def release_resources(self):
        self.power_supply.worker.stop()
        self.power_supply = None
        
        self.power_meter = None
            
        for port in list(self.serial_port_workers.keys()):
            self.serial_port_workers[port].stop()
        self.serial_port_workers.clear()
    
            
if __name__=="__main__":
    device = DeviceManager()

    
    def print_power_meter_data(data):
        print(f'Power Meter Data: {data}')

    def print_power_supply_data(data):
        print(f'Power Supply Data: {data}')
    
    print()
    print("Device start...")    
    r_power = device.init_power_supply("127.0.0.1", 2268)
    r_meter = device.init_power_meter("COM3", 0x0F)
    print(f'Power Supply connected: {r_power}')
    print(f'Power Meter connected: {r_meter}')
    
    print()
    print("Device stop...")
    device.release_resources()
    
    
    
    print()    
    print("Device start...")
    device.init_power_meter("COM3", 0x0F)
    device.init_power_supply("127.0.0.1", 2268)
    
    device.power_meter.read_vcfp(print_power_meter_data)
    device.power_supply.get_voltage(print_power_supply_data)
    
    
    device.release_resources()
    
    # time.sleep(1)
    
    
    