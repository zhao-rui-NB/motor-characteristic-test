from .ScpiSerialPortWorker import ScpiSerialPortWorker

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
            print('result:', result)    
            
            if not callback:
                return
            success, response = result

            items = self._split_response(response) # if none, return None
            # print(f"items: {items}")

            if items is None and type_list:
                items = self._cvt_response_type(items, type_list)
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
        '''
            LAMBDA : 功率因數
            PHI : 功率因數角
            FU : 電壓頻率
            FI : 電流頻率
        '''
        # default process read pattern is 2  
        # process the result
        # # keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency', 'kW_a', 'kW_b', 'kW_c', 'kW_tot', 'kvar_a', 'kvar_b', 'kvar_c', 'kvar_tot', 'kVA_a', 'kVA_b', 'kVA_c', 'kVA_tot', 'PF']
        # keys = [
        #     'V1', 'I1', 'P1', 'S1', 'Q1', 'LAMBDA1', 'PHI1', 'FU1', 'FI1',
        #     'V2', 'I2', 'P2', 'S2', 'Q2', 'LAMBDA2', 'PHI2', 'FU2', 'FI2',
        #     'V3', 'I3', 'P3', 'S3', 'Q3', 'LAMBDA3', 'PHI3', 'FU3', 'FI3',
        #     'V_SIGMA', 'I_SIGMA', 'P_SIGMA', 'S_SIGMA', 'Q_SIGMA', 'LAMBDA_SIGMA', 'PHI_SIGMA', 'FU_SIGMA', 'FI_SIGMA'
        # ]
        
        key1 = ['V1', 'I1', 'P1', 'S1', 'Q1', 'LAMBDA1', 'PHI1', 'FU1', 'FI1']
        key2 = ['V2', 'I2', 'P2', 'S2', 'Q2', 'LAMBDA2', 'PHI2', 'FU2', 'FI2']
        key3 = ['V3', 'I3', 'P3', 'S3', 'Q3', 'LAMBDA3', 'PHI3', 'FU3', 'FI3']
        key_sigma = ['V_SIGMA', 'I_SIGMA', 'P_SIGMA', 'S_SIGMA', 'Q_SIGMA', 'LAMBDA_SIGMA', 'PHI_SIGMA', 'FU_SIGMA', 'FI_SIGMA']
        
        def process_resault(result):
            # all resault to float
            result = [float(x) for x in result]
            if result:
                data = {}
                for i, k in enumerate(key1):
                    data[k] = result[i]
                for i, k in enumerate(key2):
                    data[k] = result[i + 10]
                for i, k in enumerate(key3):
                    data[k] = result[i + 20]
                for i, k in enumerate(key_sigma):
                    data[k] = result[i + 30]
            callback(data)

        self._generic_command("NUMeric:NORMal:VALue?", callback=process_resault)
        
        
if __name__ == "__main__":
    import time
    import json

    wt330 = PowerMeterWT330("COM1")
    
    def print_callback(result):
        # if is dict type, print it in json format
        if isinstance(result, dict):
            print(json.dumps(result, indent=4))
        else:
            print(f"Received: {result}")
    
    print('\nget_serial_number')
    wt330.get_serial_number(print_callback)
    time.sleep(0.1)
    
    # print('\nget_numeric_format')
    # wt330.get_numeric_format(print_callback)
    # time.sleep(0.1)
    

    # print('\nset_numeric_format')
    # wt330.set_numeric_format("ASC", print_callback)
    # time.sleep(0.1)
    

    # print('\nget_numeric_format')
    # wt330.get_numeric_format(print_callback)
    # time.sleep(0.1)
    
    print('\nset_preset_read_pattern')    
    wt330.set_preset_read_pattern(2, print_callback)
    time.sleep(0.1)

    print('\nread_data')
    wt330.read_data(print_callback)
    time.sleep(5)
    
    

                                   
                           
                           
                            
    
