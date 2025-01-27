import time 
from threading import Thread

from engine.DeviceManager import DeviceManager

class DataCollector:
    
    def __init__(self, device_manager: DeviceManager):
        self.device_manager = device_manager
        
        self.update_interval = 1 # in seconds
    
        self.plc_mechanical_thread = None
        self.power_meter_thread = None
        
        self.plc_mechanical_running = False
        self.power_meter_running = False
    
        self.plc_mechanical_data = None
        self.power_meter_data = None
        
    def get_plc_mechanical_data(self):
        return self.plc_mechanical_data
    
    def get_power_meter_data(self):
        return self.power_meter_data
    
    def _plc_mechanical_thread(self):
        while self.plc_mechanical_running:
            try:
                data = self.device_manager.plc_mechanical.get_mechanical_data()
                self.plc_mechanical_data = data
                # print(f"[DataCollector _plc_mechanical_thread] data: {data}")
            except Exception as e:
                print(f"[DataCollector _plc_mechanical_thread] Error: {e}")
                self.plc_mechanical_data = None
            time.sleep(self.update_interval)

    def _power_meter_thread(self):
        while self.power_meter_running:
            try:
                data = self.device_manager.power_meter.read_data()
                self.power_meter_data = data
                # print(f"[DataCollector _power_meter_thread] data: {data}")
            except Exception as e:
                print(f"[DataCollector _power_meter_thread] Error: {e}")
                self.power_meter_data = None
            time.sleep(self.update_interval)
    
    def start(self):
        if self.plc_mechanical_thread is not None or self.power_meter_thread is not None:
            print('[DataCollector] already running')
            return
        
        self.plc_mechanical_running = True
        self.power_meter_running = True
        
        self.plc_mechanical_thread = Thread(target=self._plc_mechanical_thread, daemon=True)
        self.power_meter_thread = Thread(target=self._power_meter_thread, daemon=True)
        
        self.plc_mechanical_thread.start()
        self.power_meter_thread.start()

        
    def stop(self):
        self.plc_mechanical_running = False
        self.power_meter_running = False
        
        if self.plc_mechanical_thread is not None:
            self.plc_mechanical_thread.join()
        if self.power_meter_thread is not None:
            self.power_meter_thread.join()

        self.plc_mechanical_thread = None
        self.power_meter_thread = None
        
        # clear data        
        self.plc_mechanical_data = None
        self.power_meter_data = None
        

if __name__=="__main__":

    device_manager = DeviceManager()
    device_manager.load_devices_from_ini('device.ini')
    
    data_collector = DataCollector(device_manager)
    data_collector.start()
    
    
    
    while True:
        time.sleep(1)
    
    