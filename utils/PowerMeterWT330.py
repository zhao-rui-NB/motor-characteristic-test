
from ScpiSerialPortWorker import ScpiSerialPortWorker

'''
this program not tested yet

'''

class PowerMeterWT330:
    def __init__(self, comport, baudrate=9600):
        self.worker = ScpiSerialPortWorker(comport, baudrate)
        self.worker.start()
        # self.lock = threading.Lock()
        
    def _split_response(self, response, to_1d=True):
        if response is None:
            return None
        
        if isinstance(response, bytes):
            response = response.decode()
        response = response.strip() 
        
        response = response.split(";")
        response = [x.split(",") for x in response]

        response_1d = []
        for x in response:
            response_1d.extend(x)
        
        return response_1d if to_1d else response
    
    def _cvt_response_type(self, response_list, type_list):
        if response_list is None or type_list is None:
            return None
        if len(response_list) != len(type_list):
            return None
        
        for i in range(len(response_list)):
            try:
                response_list[i] = type_list[i](response_list[i])
            except ValueError:
                return None
        return response_list
    
    def _generic_command(self, cmd, callback, type_list=None):
        def internal_callback(result):
            if not callback:
                return
            success, response = result
            items = self._split_response(response) # if none, return None
            items = self._cvt_response_type(items, type_list)

            if items is None and type_list:
                callback([None for _ in type_list])
            else:
                callback(items)
            
        self.worker.send_command_threaded(cmd, callback=internal_callback)
        
    #### power meter api
    
    # serial number
    def get_serial_number(self, callback):
        self._generic_command("*IDN?", callback)
        
    # reset
    def reset(self, callback):
        self._generic_command("*RST", callback)
        
    # clear status
    def clear_status(self, callback):
        self._generic_command("*CLS", callback)
    
    '''
    NUMeric Group, (meter real time data)
    
    '''    
    
    # NUMeric:FORMat
    def set_numeric_format(self, format, callback):
        ''' 
            format: can only be ASC or FLO
            - ASC: ASCII
            - FLO: float
        '''
        self._generic_command(f"NUMeric:FORMat {format}", callback)
    
    def get_numeric_format(self, callback):
        self._generic_command("NUMeric:FORMat?", callback)    # todo str type list 
        
        
    # Preset Patterns for Numeric Data Items
    # :NUMeric[:NORMal]:PRESet, 
    def set_preset_read_pattern(self, pattern_id, callback):
        '''
            Pattern 1
                ITEM<x>     Function    Element
                1           U           1
                2           I           1
                3           P           1
                4 to 6      U to P      2
                7 to 9      U to P      3
                10 to 12    U to P      SIGMA
                13 to 255   NONE        -
                
            Pattern 2
                ITEM<x>     Function    Element
                1           U           1
                2           I           1
                3           P           1
                4           S           1
                5           Q           1
                6           LAMBda      1
                7           PHI         1
                8           FU          1
                9           FI          1
                10          NONE        -
                11 to 19    U to FI     2
                20          NONE        -
                21 to 29    U to FI     3
                30          NONE        -
                31 to 39    U to FI     SIGMA
                40          NONE        -
                41 to 255   NONE        -


        '''
        self._generic_command(f"NUMeric:NORMal:PRESet {pattern_id}", callback)
    
    # read the numeric data
    # :NUMeric[:NORMal]:VALue?
    def read_data(self, callback):
        self._generic_command("NUMeric:NORMal:VALue?", callback) # todo : type_list=[float]
        
        
if __name__ == "__main__":
    import time

    wt330 = PowerMeterWT330("COM3")
    
    def print_callback(result):
        print(f"Received: {result}")
        
    wt330.get_serial_number(print_callback)
    time.sleep(0.1)
    
    
    wt330.get_numeric_format(print_callback)
    time.sleep(0.1)
    
    wt330.set_numeric_format("ASC", print_callback)
    time.sleep(0.1)
    
    wt330.get_numeric_format(print_callback)
    time.sleep(0.1)
    
    
    wt330.set_preset_read_pattern(1, print_callback)
    time.sleep(0.1)

    wt330.read_data(print_callback)
    time.sleep(0.1)
    
    

                                   
                           
                           
                            
    
