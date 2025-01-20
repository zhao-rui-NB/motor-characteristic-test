from .ScpiSerialPortWorker import ScpiSerialPortWorker

'''
this program not tested yet

   2025_0118: change to sync, not test

'''

class PowerMeterWT330:
    def __init__(self, comport, baudrate=9600):
        self.worker = ScpiSerialPortWorker(comport, baudrate)
        self.worker.start()
        
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
    
    def _generic_command(self, cmd, type_list=None):
        success, reponse = self.worker.send_command(cmd)

        if not success:
            print(f"[PowerMeterWT330] Command failed: {cmd}")
            
        items = self._split_response(reponse) # if none, return None
        
        # if no need to convert type, return directly
        if type_list is None:
            return items
        
        # convert type, is failed, return None for each item
        items = self._cvt_response_type(items, type_list)
        if items is None:
            return [None for _ in type_list]
        return items
    
        
    #### power meter api
    
    # serial number
    def get_serial_number(self):
        return self._generic_command("*IDN?")
        
    # reset
    def reset(self):
        return self._generic_command("*RST")
        
    # clear status
    def clear_status(self):
        return self._generic_command("*CLS")
    
    # [:INPut]:WIRing
    def set_input_wiring(self, wiring):
        # (P1W2|P1W3|P3W3|P3W4|V3A3)
        '''
            P1W2 = Single-phase, two-wire system [1P2W] 
            P1W3 = Single-phase, three-wire system [1P3W] 
            P3W3 = Three-phase, three-wire system [3P3W] 
            P3W4 = Three-phase, four-wire system [3P4W] 
            V3A3 = Three-phase, three-wire system with a three-voltage, three-current method [3V3A]
        '''
        return self._generic_command(f"INPut:WIRing {wiring}")
            
    # NUMeric:FORMat
    def set_numeric_format(self, format):
        ''' 
            format: can only be ASC or FLO
            - ASC: ASCII
            - FLO: float
        '''
        return self._generic_command(f"NUMeric:FORMat {format}")
    
    def get_numeric_format(self):
        return self._generic_command("NUMeric:FORMat?")    # todo str type list 
        
        
    # Preset Patterns for Numeric Data Items
    # :NUMeric[:NORMal]:PRESet, 
    def set_preset_read_pattern(self, pattern_id):
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
        return self._generic_command(f"NUMeric:NORMal:PRESet {pattern_id}")
    
    # read the numeric data
    # :NUMeric[:NORMal]:VALue?
    def read_data(self):
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
        
        result = self._generic_command("NUMeric:NORMal:VALue?")
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
            return data
        else:
            data = {}
            for i, k in enumerate(key1):
                data[k] = None
            for i, k in enumerate(key2):
                data[k] = None
            for i, k in enumerate(key3):
                data[k] = None
            for i, k in enumerate(key_sigma):
                data[k] = None

            return data
    
    # :NUMeric[:NORMal]:NUMber
    def set_list_number(self, number):
        return self._generic_command(f"NUMeric:NORMal:NUMber {number}")
    

    # [:INPut]:VOLTage:RANGe
    def set_voltage_range(self, range):
        '''
            <Voltage> = 15, 30, 60, 150, 300, 600(V)
        '''

        return self._generic_command(f"INPut:VOLTage:RANGe {range}")


if __name__ == "__main__":
    import time
    import json

    wt330 = PowerMeterWT330("COM1")

    # wt330.reset()
    # time.sleep(5)

    print('\nget_serial_number', wt330.get_serial_number())
    
    
    wt330.set_numeric_format("ASC")
    time.sleep(1)   
    wt330.set_preset_read_pattern(2) 
    time.sleep(1)
    wt330.set_list_number(40)

    
    # wring 
    wt330.set_input_wiring("P3W3")
    time.sleep(1)

    

    print('\nread_data' , wt330.read_data())
    
    

                                   
                           
                           
                            
    
