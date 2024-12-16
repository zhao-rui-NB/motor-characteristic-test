import time 
from threading import Thread
from engine.DeviceManager import DeviceManager
from engine.DataCollector import DataCollector



class TestRunner:
    
    def __init__(self,device_manager: DeviceManager, data_collector: DataCollector):
        self.device_manager = device_manager
        self.data_collector = data_collector

        self.test_running = False
        self.test_thread = None
        self.test_interval = 1
        self.test_address_config: dict[str,dict[str,dict]] = {}
        
        self.test_data = {}
        self.test_data_callback = None

    
    '''
        a.	ASR6450 輸出關掉
        b.	ASR6450選擇單/三相 (注意提醒更換接線)
        c.	設定ASR6450 [1P/2W]  或 [3P/4W]  外部接線開關
        d.	設定ASR6450 內部接線命令
        e.	設定ASR6450 電壓命令
        f.	設定ASR6450 最大電流命令(無載電流*120%)
        g.	設定ASR6450 頻率輸出命令
        h.	設定ASR6450 電壓輸出命令
        i.	讀取 WT333 電壓與頻率 (核對電壓輸出)
        j.	設定外部輸出開關 (啟動測試電壓輸出)
    
    '''
    
    
    # 開路試驗
    def _open_circuit_test_thread(self):
        self.test_data = {}
        
    
    def open_circuit_test(self, interval=1):
        self.test_running = True
        self.test_interval = interval
        self.test_thread = Thread(target=self._open_circuit_test_thread, daemon=True)
        self.test_thread.start()
        
        


        
        
            