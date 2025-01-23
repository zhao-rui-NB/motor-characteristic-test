from engine.DeviceManager import DeviceManager
from engine.DataSender import DataSender
from engine.Motor import Motor
import time
device_manager = DeviceManager()
device_manager.load_devices_from_ini('device.ini')

data_sender = DataSender(device_manager)
data_sender.start_plc_electric_data_sender(interval=1)
print("Data sender started.")



try:
    while True:
        time.sleep(1)                       
        data = device_manager.power_meter.read_data()
        device_manager.plc_electric.send_power_meter_data(data)
        print("Data sent.")
        print(data)
except KeyboardInterrupt:
    data_sender.stop_plc_electric_data_sender()
    data_sender.device_manager.release_resources()
    print("Data sender stopped.")