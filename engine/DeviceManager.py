from threading import Thread
import time

from utils.PowerMeterSPM3 import PowerMeterSPM3
from utils.ModbusWorker import ModbusWorker
from utils.PowerSupplyASP7100 import PowerSupplyASP7100
from utils.SegmentDisplay import SegmentDisplay
from utils.TorqueSensorDYN200 import TorqueSensor

class DeviceManager:
    
    def __init__(self):
        # hardware devices

        self.serial_port_workers = {}

        self.power_supply: PowerSupplyASP7100 = None
        self.power_meter: PowerMeterSPM3 = None 
        self.torque_sensor: TorqueSensor = None
        self.segment_display_dict: dict[int, SegmentDisplay] = {}
        
    

    def init_power_supply(self, ip, port):
        if not ip or not port:
            print(f'[DeviceManager] Warning: Power Supply ip or port is empty')
            return False
        self.power_supply = PowerSupplyASP7100(ip, port)
        print(f'[DeviceManager] Power Supply init, ip: {ip}, port: {port}')
        return self.power_supply.worker.connected.is_set()

    def init_power_meter(self,com_port:str, slave_address, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5):
        if not com_port:
            print(f'[DeviceManager] Warning: Power Meter com_port is empty')
            return False
        
        com_port =  com_port.upper()
        
        if com_port not in self.serial_port_workers: # first make worker device will set parameters for the worker 
            self.serial_port_workers[com_port] = ModbusWorker(com_port, baudrate, parity, stopbits, bytesize, timeout)
        
        self.power_meter = PowerMeterSPM3(self.serial_port_workers[com_port], slave_address)

        print(f'[DeviceManager] Power Meter init, com_port: {com_port}, slave_address: {slave_address}')        
        return self.power_meter.worker.client.is_socket_open()
    
    def init_torque_sensor(self, com_port:str, slave_address, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5):
        if not com_port:
            print(f'[DeviceManager] Warning: Torque Sensor com_port is empty')
            return False
        
        com_port =  com_port.upper()
        
        if com_port not in self.serial_port_workers: # first make worker device will set parameters for the worker 
            self.serial_port_workers[com_port] = ModbusWorker(com_port, baudrate, parity, stopbits, bytesize, timeout)
        
        self.torque_sensor = TorqueSensor(self.serial_port_workers[com_port], slave_address)

        print(f'[DeviceManager] Torque Sensor init, com_port: {com_port}, slave_address: {slave_address}')
        return self.torque_sensor.worker.client.is_socket_open()
    
    
    
    def init_segment_displays(self, com_port:str, addresses:list, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5):
        '''
        if the com_port exists, all the parameters for the modbus worker will be set by the first device.
        addresses: list of addresses for the segment display
        '''
        com_port = com_port.upper()
        
        if com_port not in self.serial_port_workers:
            self.serial_port_workers[com_port] = ModbusWorker(com_port, baudrate, parity, stopbits, bytesize, timeout)
            
        for address in addresses:
            if address not in self.segment_display_dict:
                self.segment_display_dict[address] = SegmentDisplay(self.serial_port_workers[com_port], address)             
                print(f'[DeviceManager] Segment Display init, com_port: {com_port}, address: {address}')
            else:
                print(f'[DeviceManager] Warning: Segment Display already exists, com_port: {com_port}, address: {address}')
               
        
    
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
    
    
    