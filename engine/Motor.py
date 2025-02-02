# %%
from datetime import datetime
import matplotlib.pyplot as plt

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
        
        # motor information
        self.manufacturer = None
        self.model = None
        self.serial_number = None
        self.note = None
        
        
        
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
    
    def update_motor_parameter(self, para_name, value):
        int_type_para = ['power_phases', 'poles']
        float_type_para = ['rated_voltage', 'speed', 'rated_current', 'frequency', 'horsepower', 'no_load_current']
        other_para = ['manufacturer', 'model', 'serial_number', 'note'] # other parameters
        if para_name in int_type_para:
            try:
                setattr(self, para_name, int(value))
                return True
            except ValueError:# set 
                setattr(self, para_name, None)
                print(f"[Motor] Invalid update motor parameter: {para_name} with value: {value}")
        elif para_name in float_type_para:
            try:
                setattr(self, para_name, float(value))
                return True
            except ValueError:
                setattr(self, para_name, None)
                print(f"[Motor] Invalid update motor parameter: {para_name} with value: {value}")
        elif para_name in other_para:
            setattr(self, para_name, value)
            return True
        else:
            print(f"[Motor] Invalid motor parameter: {para_name}")
        return False


    # add test results
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
    
    
    # analysis functions
    def analyze_dc_resistance(self):
        if not self.data_dc_resistance:
            print('No data for DC Resistance')
            return
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
        self.result_dc_resistance = round(self.result_dc_resistance, 4)
        print(f"DC Resistance: {self.result_dc_resistance}")

    def analyze_open_circuit(self):
        if not self.data_open_circuit:
            print('No data for Open Circuit')
            return
        print(f"Analyzing Open Circuit from {self.data_open_circuit[-1]['timestamp']}")
        raw_data = self.data_open_circuit[-1]['raw_data']
        
        voltage = []
        current = []
        input_power = []
        power_factor = []
        
        if self.is_single_phase():
            voltage = [ d['power_meter']['V1'] for d in raw_data ]
            current = [ d['power_meter']['I1'] for d in raw_data ]
            input_power = [ d['power_meter']['P1'] for d in raw_data ]
            power_factor = [ d['power_meter']['LAMBDA1'] for d in raw_data ]
        else:
            voltage.extend([ d['power_meter']['V_SIGMA'] for d in raw_data ])
            current.extend([ d['power_meter']['I_SIGMA'] for d in raw_data ])
            input_power.extend([ d['power_meter']['P_SIGMA'] for d in raw_data ])
            power_factor.extend([ d['power_meter']['LAMBDA_SIGMA'] for d in raw_data ])
        
        print('voltage', voltage)
        print('current', current)
        print('input_power', input_power)
        print('power_factor', power_factor)
        
        
        voltage = sum(voltage) / len(voltage)
        current = sum(current) / len(current)
        input_power = sum(input_power) / len(input_power)
        power_factor = sum(power_factor) / len(power_factor)
        
        # round 4 decimal
        voltage = round(voltage, 4)
        current = round(current, 4)
        input_power = round(input_power, 4)
        power_factor = round(power_factor, 4)
        
        self.result_open_circuit = {
            'voltage': voltage,
            'current': current,
            'power': input_power,
            'power_factor': power_factor,
        }
        
        print(f"Open Circuit: {self.result_open_circuit}")

        
    def analyze_locked_rotor(self):
        if not self.data_locked_rotor:
            print('No data for Locked Rotor')
            return
        print(f"Analyzing Locked Rotor from {self.data_locked_rotor[-1]['timestamp']}")
        raw_data = self.data_locked_rotor[-1]['raw_data']

        voltage = []
        current = []
        input_power = []
        power_factor = []
        
        if self.is_single_phase():
            voltage = [ d['power_meter']['V1'] for d in raw_data ]
            current = [ d['power_meter']['I1'] for d in raw_data ]
            input_power = [ d['power_meter']['P1'] for d in raw_data ]
            power_factor = [ d['power_meter']['LAMBDA1'] for d in raw_data ]
        else:
            voltage.extend([ d['power_meter']['V_SIGMA'] for d in raw_data ])
            current.extend([ d['power_meter']['I_SIGMA'] for d in raw_data ])
            input_power.extend([ d['power_meter']['P_SIGMA'] for d in raw_data ])
            power_factor.extend([ d['power_meter']['LAMBDA_SIGMA'] for d in raw_data ])
            
        print('voltage', voltage)
        print('current', current)
        print('power', input_power)
        print('power_factor', power_factor)
        
        voltage = sum(voltage) / len(voltage)
        current = sum(current) / len(current)
        input_power = sum(input_power) / len(input_power)
        power_factor = sum(power_factor) / len(power_factor)

        voltage = round(voltage, 4)
        current = round(current, 4)
        input_power = round(input_power, 4)
        power_factor = round(power_factor, 4)
        
        self.result_locked_rotor = {
            'voltage': voltage,
            'current': current,
            'power': input_power,
            'power_factor': power_factor,
        }
        
        print(f"Locked Rotor: {self.result_locked_rotor}")
        
    
    def analyze_load_test(self):
        if not self.data_load:
            print('No data for Load Test')
            return
        
        print(f"Analyzing Load Test from {self.data_load[-1]['timestamp']}")
        raw_data = self.data_load[-1]['raw_data']
        if not raw_data:
            print('No data for Load Test')
            return
        print(raw_data)

        speeds = [ d['mechanical']['speed'] for d in raw_data ] 
        torques = [ d['mechanical']['torque'] for d in raw_data ]
        self.result_load_test = {
            'speeds': speeds,
            'torques': torques,
        }
        
    def polt_load_test(self, ax:plt.Axes=None, show=True):
        if ax is None:
            fig, ax = plt.subplots()
            
        data = self.result_load_test
        speeds = data['speeds']
        torques = data['torques']

        # clear the plot
        ax.clear()
        
        ax.plot(speeds, torques, 'ro-')
        ax.set_title('Load Test')
        ax.set_xlabel('Speed (rpm)')
        ax.set_ylabel('Torque (Nm)')
        
        if show:
            plt.show()
              
    
    def analyze_separate_excitation(self):
        pass

    def analyze_frequency_drift(self):
        pass
    
        
    
    
    def to_dict(self):
        return {
            # key motor parameters
            'rated_voltage': self.rated_voltage,
            'power_phases': self.power_phases,
            'speed': self.speed,
            'rated_current': self.rated_current,
            'frequency': self.frequency,
            'horsepower': self.horsepower,
            'poles': self.poles,
            'no_load_current': self.no_load_current,
            # motor information
            'manufacturer': self.manufacturer,
            'model': self.model,
            'serial_number': self.serial_number,
            'note': self.note,
            
            'test_results': {
                'result_dc_resistance': self.result_dc_resistance,
                'result_open_circuit': self.result_open_circuit,
                'result_locked_rotor': self.result_locked_rotor,
                'result_load_test': self.result_load_test,
                'result_separate_excitation': self.result_separate_excitation,
                'result_frequency_drift': self.result_frequency_drift,
            },
            
            'test_data_log': {
                'data_dc_resistance': self.data_dc_resistance,
                'data_open_circuit': self.data_open_circuit,
                'data_locked_rotor': self.data_locked_rotor,
                'data_load': self.data_load,
                'data_separate_excitation': self.data_separate_excitation,
                'frequency_drift': self.frequency_drift,
            },
        }
        
    def from_dict(self, data):
        # key motor parameters
        self.rated_voltage = data['rated_voltage']
        self.power_phases = data['power_phases']
        self.speed = data['speed']
        self.rated_current = data['rated_current']
        self.frequency = data['frequency']
        self.horsepower = data['horsepower']
        self.poles = data['poles']
        self.no_load_current = data['no_load_current']
        # motor information
        self.manufacturer = data['manufacturer']
        self.model = data['model']
        self.serial_number = data['serial_number']
        self.note = data['note']
        
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
    motor = Motor()
    
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

    
    
    # motor = Motor()
    ## load data
    # with open('test_file/motor_2025.json', 'r') as f:
    # with open('test_file/motor_20250120_160710.json', 'r') as f:
    #     data = json.load(f)
    #     motor.from_dict(data)
    

    ## save data 
    # timestamp = motor.make_time_stamp()
    # with open(f'test_file/motor_20250120_160710_ana.json', 'w') as f:
    #     json.dump(motor.to_dict(), f, indent=4)



    # print(json.dumps(motor.to_dict(), indent=4))    
    # motor.analyze_dc_resistance()
    
    
    # %%
    file_path = 'test_file/2025_0201_merged.motor.json'
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        motor.from_dict(data)
        
    # print(json.dumps(motor.to_dict(), indent=4))
    # motor.analyze_dc_resistance()
    # motor.analyze_open_circuit()    
    # motor.analyze_locked_rotor()
    
    motor.analyze_load_test()
    motor.load_test_plot()  
    
    
    
    