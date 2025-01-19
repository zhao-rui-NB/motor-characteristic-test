import time 
from threading import Thread

from engine.DeviceManager import DeviceManager
'''

'''
class DataCollector:
    
    def __init__(self):
        self.running = False
        self.update_interval = 1 # in seconds
        self.collect_thread = None
        
        self.collect_functions = []
        
        self.is_callback_functions = {}
        self.new_data_flags = {}
        self.collected_data = {} # key is the collect function, value is the function return value
        
    def wait_all_new_data(self):
        # clear all new data flags
        for func in self.collect_functions:
            self.new_data_flags[func] = False
            
        # wait until all new data flags are true
        while not all(self.new_data_flags.values()):
            time.sleep(0.1)
            
    def get_collected_data(self, collect_function):
        return self.collected_data[collect_function]
        
    def _add_collect_function(self, collect_function, is_cb_func=False):
        self.collect_functions.append(collect_function)

        self.is_callback_functions[collect_function] = is_cb_func
        self.new_data_flags[collect_function] = False
        self.collected_data[collect_function] = None
    
    def _make_callback_function(self, collect_function):
        def cb_func(data):
            self.collected_data[collect_function] = data
            self.new_data_flags[collect_function] = True
        return cb_func
    
    
    def _run(self):
        while self.running:
            for func in self.collect_functions:
                is_callback = self.is_callback_functions[func]
                if is_callback:
                    func(self._make_callback_function(func))
                else:
                    self.collected_data[func] = func()
                    self.new_data_flags[func] = True
            time.sleep(self.update_interval)

    
    def start(self):
        if self.running:
            print('[DataCollector] already running, please stop first')
            return
        self.running = True
        
        self.collect_thread = Thread(target=self._run, daemon=True)
        self.collect_thread.start()
        
    def stop(self):
        self.running = False
        if self.collect_thread is not None:
            self.collect_thread.join()
            self.collect_thread = None
        

if __name__=="__main__":
    
    def test_get_voltage_cb(callback):
        def run():
            time.sleep(10)
            callback({'voltage': 10, 'time': time.time()})
        Thread(target=run).start()
        
                
    def test_get_current_cb(callback):
        def run():
            time.sleep(10)
            callback({'current': 5, 'time': time.time()})
        Thread(target=run).start()
        
        
    data_collector = DataCollector()
    
    try:
        data_collector._add_collect_function(test_get_voltage_cb, is_cb_func=True)
        data_collector._add_collect_function(test_get_current_cb, is_cb_func=True)
        
        data_collector.start()
        
        while True:
            data_collector.wait_all_new_data()
            print('voltage:', data_collector.get_collected_data(test_get_voltage_cb))
            print('current:', data_collector.get_collected_data(test_get_current_cb))
            time.sleep(2)
            
    except KeyboardInterrupt:
        pass

    data_collector.stop()
    print('done')
    # time.sleep(3)