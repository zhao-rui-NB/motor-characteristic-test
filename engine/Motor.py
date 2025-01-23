from datetime import datetime

class Motor:
    def __init__(self):
        
        # key motor parameters
        self.rated_voltage = None
        self.power_phases = None
        self.speed = None
        self.rated_current = None
        self.frequency = None
        self.horsepower = None
        self.poles = None
        self.no_load_current = None
        
        # test data log
        self.data_dc_resistance = []
        self.data_open_circuit = []
        self.data_locked_rotor = []
        self.data_load = []
        self.data_separate_excitation = []
        self.frequency_drift = []
        
        # test results
        self.result_dc_resistance = None
        self.result_open_circuit = None
        self.result_locked_rotor = None
        self.result_load_test = None
        self.result_separate_excitation = None
        self.result_frequency_drift = None
        
        
    def make_time_stamp(self):
        # UTC time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return timestamp
    
    def is_single_phase(self):
        return self.power_phases == 1
    
            
    def add_result_dc_resistance(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data,
        }
        self.data_dc_resistance.append(res)
    
    def add_result_open_circuit(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data,
        }
        self.data_open_circuit.append(res)
        
    def add_result_locked_rotor(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data, 
        }
        self.data_locked_rotor.append(res)
        
    def add_result_load_test(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data, 
        }
        self.data_load.append(res)
        
    def add_result_separate_excitation(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data, 
        }
        self.data_separate_excitation.append(res)

    def add_result_frequency_drift(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data, 
        }
        self.frequency_drift.append(res)
    
    def analyze_dc_resistance(self):
        print(f"Analyzing DC Resistance from {self.data_dc_resistance[-1]['timestamp']}") 
        raw_data = self.data_dc_resistance[-1]['raw_data']

        if self.is_single_phase():
            voltage = [ d['power_meter']['V1'] for d in raw_data ]
            current = [ d['power_meter']['I1'] for d in raw_data ]
        else:
            group_num = len(raw_data)//3

            print('group_num', group_num)

            voltage = []
            current = []
            voltage.extend([ d['power_meter']['V1'] for d in raw_data[:group_num] ])
            voltage.extend([ d['power_meter']['V1'] for d in raw_data[group_num:group_num*2] ])
            voltage.extend([ d['power_meter']['V3'] for d in raw_data[group_num*2:] ])

            current.extend([ d['power_meter']['I1'] for d in raw_data[:group_num] ])
            current.extend([ d['power_meter']['I1'] + d['power_meter']['I3'] for d in raw_data[group_num:group_num*2] ])
            current.extend([ d['power_meter']['I3'] for d in raw_data[group_num*2:] ])


        print('voltage', voltage)
        print('current', current)

        resistance = [ v / i for v, i in zip(voltage, current) ]

        self.result_dc_resistance = sum(resistance) / len(resistance) / 1.5
        print(f"DC Resistance: {self.result_dc_resistance}")


        
    
    def analyze_open_circuit(self):
        pass
    
    def analyze_locked_rotor(self):
        pass
    
    def analyze_load_test(self):
        pass
    
    def analyze_separate_excitation(self):
        pass

    def analyze_frequency_drift(self):
        pass
    
        
    
    
    def to_dict(self):
        return {
            'rated_voltage': self.rated_voltage,
            'power_phases': self.power_phases,
            'speed': self.speed,
            'rated_current': self.rated_current,
            'frequency': self.frequency,
            'horsepower': self.horsepower,
            'poles': self.poles,
            'no_load_current': self.no_load_current,
            'test_results': {
                'result_dc_resistance': self.result_dc_resistance,
                'result_open_circuit': self.result_open_circuit,
                'result_locked_rotor': self.result_locked_rotor,
                'result_load_test': self.result_load_test,
                'result_separate_excitation': self.result_separate_excitation,
            },
            
            'test_data_log': {
                'data_dc_resistance': self.data_dc_resistance,
                'data_open_circuit': self.data_open_circuit,
                'data_locked_rotor': self.data_locked_rotor,
                'data_load': self.data_load,
                'data_separate_excitation': self.data_separate_excitation,
            },
        }
        
    def from_dict(self, data):
        self.rated_voltage = data['rated_voltage']
        self.power_phases = data['power_phases']
        self.speed = data['speed']
        self.rated_current = data['rated_current']
        self.frequency = data['frequency']
        self.horsepower = data['horsepower']
        self.poles = data['poles']
        self.no_load_current = data['no_load_current']
        
        self.result_dc_resistance = data['test_results']['result_dc_resistance']
        self.result_open_circuit = data['test_results']['result_open_circuit']
        self.result_locked_rotor = data['test_results']['result_locked_rotor']
        self.result_load_test = data['test_results']['result_load_test']
        self.result_separate_excitation = data['test_results']['result_separate_excitation']
        self.result_frequency_drift = data['test_results']['result_frequency_drift']
        
        
        self.data_dc_resistance = data['test_data_log']['data_dc_resistance']
        self.data_open_circuit = data['test_data_log']['data_open_circuit']
        self.data_locked_rotor = data['test_data_log']['data_locked_rotor']
        self.data_load = data['test_data_log']['data_load']
        self.data_separate_excitation = data['test_data_log']['data_separate_excitation']
        self.frequency_drift = data['test_data_log']['frequency_drift']
        
        
    
        
        
        
if __name__ == '__main__':
    import json
    # motor = Motor()
    # print(json.dumps(motor.to_dict(), indent=4))
    # motor.rated_voltage = 220
    # motor.power_phases = 3
    # motor.speed = 1800
    # motor.rated_current = 10
    # motor.frequency = 60
    # motor.horsepower = 10
    # motor.poles = 4
    # motor.no_load_current = 5
    # print(json.dumps(motor.to_dict(), indent=4))
    
    # timestamp = motor.make_time_stamp()
    # with open(f'test_file/motor_{timestamp}.json', 'w') as f:
    #     json.dump(motor.to_dict(), f, indent=4)

    
    
    motor = Motor()
    # with open('test_file/motor_2025.json', 'r') as f:
    with open('test_file/motor_20250120_160710.json', 'r') as f:
        data = json.load(f)
        motor.from_dict(data)

    motor.analyze_dc_resistance()

    # print(json.dumps(motor.to_dict(), indent=4))    
    

    # save 
    timestamp = motor.make_time_stamp()
    with open(f'test_file/motor_20250120_160710_ana.json', 'w') as f:
        json.dump(motor.to_dict(), f, indent=4)