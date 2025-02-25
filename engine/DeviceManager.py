import configparser
from typing import Union
from threading import Thread
import time

from utils.PowerMeterSPM3 import PowerMeterSPM3
from utils.PowerMeterWT330 import PowerMeterWT330
from utils.ModbusWorker import ModbusWorker
from utils.PowerSupplyASP7100 import PowerSupplyASP7100
from utils.PowerSupplyASR6450 import PowerSupplyASR6450
from utils.SegmentDisplay import SegmentDisplay
from utils.TorqueSensorDYN200 import TorqueSensorDYN200
from utils.PlcMechanical import PlcMechanical
from utils.PlcElectric import PlcElectric

class DeviceManager:
    
    def __init__(self):
        # hardware devices

        self.config = None
        
        self.serial_port_workers: dict[str, ModbusWorker] = {}

        self.power_supply: Union[PowerSupplyASP7100, PowerSupplyASR6450] = None
        self.power_meter: Union[PowerMeterSPM3, PowerMeterWT330] = None
        self.plc_mechanical: PlcMechanical = None
        self.plc_electric: PlcElectric = None
        self.torque_sensor: TorqueSensorDYN200 = None
        self.segment_display_dict: dict[int, SegmentDisplay] = {}
        
    def load_devices_from_ini(self, ini_file:str):
        if self.config is not None:
            print(f'[DeviceManager] Config already loaded, reload ini file: {ini_file}')
            self.release_resources()
                    
        
        self.config = configparser.ConfigParser()
        self.config.read(ini_file)
        
        # load power supply (PowerSupplyASP7100, PowerSupplyASR6450)
        if 'PowerSupplyASR6450' in self.config:
            ps_cfg = self.config['PowerSupplyASR6450']
            ip = ps_cfg.get('ip')
            port = ps_cfg.getint('port')
            self.power_supply = PowerSupplyASR6450(ip, port)
            print(f'[DeviceManager] Power Supply init, ip: {ip}, port: {port}')
            
        # load power meter (PowerMeterSPM3, PowerMeterWT330)
        if 'PowerMeterWT330' in self.config:
            pm_config = self.config['PowerMeterWT330']
            com_port = pm_config.get('com_port')
            baudrate = pm_config.getint('baudrate')
            self.power_meter = PowerMeterWT330(com_port, baudrate)
        
        if 'PlcMechanical' in self.config:
            plc_config = self.config['PlcMechanical']
            ip = plc_config.get('ip')
            port = plc_config.getint('port')
            self.plc_mechanical = PlcMechanical(ip, port)
            
        if 'PlcElectrical' in self.config:
            plc_config = self.config['PlcElectrical']
            ip = plc_config.get('ip')
            port = plc_config.getint('port')
            self.plc_electric = PlcElectric(ip, port)

    def _add_modbus_worker(self, com_port:str, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5):
        ''' if the com_port exists, will not create a new worker, all parameters will be same as the first worker '''
        com_port = com_port.upper()
        if com_port not in self.serial_port_workers:
            self.serial_port_workers[com_port] = ModbusWorker(com_port, baudrate, parity, stopbits, bytesize, timeout)
            print(f'[DeviceManager] Modbus Worker added, com_port: {com_port}')
        else:
            print(f'[DeviceManager] Warning: Modbus Worker already exists, com_port: {com_port}')
            
    
    # release resources
    def release_resources(self):
        self.config = None
        
        if self.power_supply is not None:
            self.power_supply.worker.stop()
            self.power_supply = None
        
        if self.power_meter is not None:
            self.power_meter.worker.stop()
            self.power_meter = None

        if self.plc_mechanical is not None:
            self.plc_mechanical.worker.stop()
            self.plc_mechanical = None
        
        if self.plc_electric is not None:
            self.plc_electric.worker.stop()
            self.plc_electric = None
            
        # for port in list(self.serial_port_workers.keys()):
        #     self.serial_port_workers[port].stop()
        # self.serial_port_workers.clear()
    
            
if __name__=="__main__":
    device_manger = DeviceManager()

    
    def print_power_meter_data(data):
        print(f'Power Meter Data: {data}')

    def print_power_supply_data(data):
        print(f'Power Supply Data: {data}')
    
    
    device_manger.load_devices_from_ini('device.ini')
    time.sleep(1)
    
    print('power_supply', device_manger.power_supply.get_idn())
    print('power_meter', device_manger.power_meter.get_serial_number())

    print('plc_mechanical', device_manger.plc_mechanical)
    print('plc_electric', device_manger.plc_electric)
    
    
    
    
    
    # print('power_supply', device_manger.power_supply)
    # print('power_meter', device_manger.power_meter)
    # print('torque_sensor', device_manger.torque_sensor)
    # print('segment_display_dict', device_manger.segment_display_dict)


    # release 
    device_manger.release_resources()
            
    
    
    
        
    
    