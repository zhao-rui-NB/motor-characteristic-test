# %%
from datetime import datetime
import matplotlib.pyplot as plt
import os 
import csv
# set plot font
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

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
        
        # motor information dictionary
        self.information_dict = {}
        
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
    
    def update_motor_information(self, key, value):
        self.information_dict[key] = value
        
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
        
    def add_result_load_test(self, raw_data, is_single_phase_high_current=False):
        res = {
            'timestamp': self.make_time_stamp(),
            'is_single_phase_high_current': is_single_phase_high_current,
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

        if self.is_single_phase():
            self.result_dc_resistance = sum(resistance) / len(resistance)
        else:
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
        # print(raw_data)

        speeds = [ d['mechanical']['speed'] for d in raw_data ] 
        torques = [ d['mechanical']['torque'] for d in raw_data ]
        power_output = [ speed*torque / 9.5493 for speed, torque in zip(speeds, torques) ]


        if self.is_single_phase():
            if not self.data_load[-1].get('is_single_phase_high_current', False):
                current = [ d['power_meter']['I1'] for d in raw_data ]
                power_input = [ d['power_meter']['P1'] for d in raw_data ]
                power_factor = [ d['power_meter']['LAMBDA1'] for d in raw_data ]
            else:
                current = [ d['power_meter']['I2'] for d in raw_data ]
                power_input = [ d['power_meter']['P2'] for d in raw_data ]
                power_factor = [ d['power_meter']['LAMBDA2'] for d in raw_data ]
        else:
            current = [ d['power_meter']['I_SIGMA'] for d in raw_data ]
            power_input = [ d['power_meter']['P_SIGMA'] for d in raw_data ]
            power_factor = [ d['power_meter']['LAMBDA_SIGMA'] for d in raw_data ]
        # fix div by zero
        # efficiency = [ po / pi * 100 for po, pi in zip(power_output, power_input) ]
        efficiency = []
        for po, pi in zip(power_output, power_input):
            if pi == 0:
                efficiency.append(0)
            else:
                efficiency.append(po / pi)
        
        # remove speed < 500 data , find the speed < 500 index
        # speeds is sorted reversed
        print('speeds', speeds)

        speed_500_index = -1
        for i, s in enumerate(speeds):
            if s < 500:
                speed_500_index = i
                break
        speeds = speeds[:speed_500_index]
        torques = torques[:speed_500_index]
        current = current[:speed_500_index]
        power_input = power_input[:speed_500_index]
        power_output = power_output[:speed_500_index]
        power_factor = power_factor[:speed_500_index]
        efficiency = efficiency[:speed_500_index]


        self.result_load_test = {
            'speeds': speeds,
            'torques': torques,
            'current': current,
            'power_input': power_input,
            'power_output': power_output,
            'power_factor': power_factor,
            'efficiency': efficiency,
            
        }

        # # for print 
        # for key, value in self.result_load_test.items():
        #     print(key, value)        
    def polt_load_test(self, axs: list[plt.Axes]=None, show=False):
        print('plot_load_test')
        print('axs', axs)   
        if axs is None:
            fig, axs = plt.subplots(2, 2, figsize=(12, 8))
            axs = [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]]

        # data key: speeds, torques, current, power_input, power_output, power_factor, efficiency    
        data = self.result_load_test
        
        # polt 4 figures
        # 1 speed vs torque
        # 2 speed vs power_input and power_output
        # 3 speed vs current
        # 4 speed vs efficiency and power factor
        speeds = data['speeds']
        torques = data['torques']
        current = data['current']
        power_input = data['power_input']
        power_output = data['power_output']
        power_factor = data['power_factor']
        efficiency = data['efficiency']

        # clear the plot
        axs[0].clear()
        axs[1].clear()
        axs[2].clear()
        axs[3].clear()

        # 1 speed vs torque
        axs[0].plot(speeds, torques, 'ro-')
        axs[0].set_title('Speed vs Torque')
        axs[0].set_xlabel('Speed (RPM)')
        axs[0].set_ylabel('Torque (Nm)')

        # 2 speed vs power_input and power_output
        axs[1].plot(speeds, power_input, 'ro-', label='Input Power')
        axs[1].plot(speeds, power_output, 'bo-', label='Output Power')
        axs[1].set_title('Speed vs Power')
        axs[1].set_xlabel('Speed (RPM)')
        axs[1].set_ylabel('Power (W)')
        axs[1].legend()

        # 3 speed vs current
        axs[2].plot(speeds, current, 'ro-')
        axs[2].set_title('Speed vs Current')
        axs[2].set_xlabel('Speed (RPM)')
        axs[2].set_ylabel('Current (A)')

        # 4 speed vs efficiency and power factor
        axs[3].plot(speeds, efficiency, 'ro-', label='Efficiency')
        axs[3].plot(speeds, power_factor, 'bo-', label='Power Factor')
        axs[3].set_title('Speed vs Efficiency and Power Factor')
        axs[3].set_xlabel('Speed (RPM)')
        axs[3].set_ylabel('Efficiency / Power Factor')
        axs[3].legend()

        # call draw
        axs[0].figure.tight_layout()
        axs[0].figure.canvas.draw()
        axs[1].figure.tight_layout()
        axs[1].figure.canvas.draw()
        axs[2].figure.tight_layout()
        axs[2].figure.canvas.draw()
        axs[3].figure.tight_layout()
        axs[3].figure.canvas.draw()


        if show:
            plt.tight_layout()
            plt.show()
              
    def analyze_separate_excitation(self):
        if not self.data_separate_excitation:
            print('No data for Separate Excitation')
            return

        print(f"Analyzing Separate Excitation from {self.data_separate_excitation[-1]['timestamp']}")
        raw_data = self.data_separate_excitation[-1]['raw_data']

        voltage = []
        current = []
        power = []

        if self.is_single_phase():
            voltage.extend([ d['power_meter']['V1'] for d in raw_data ])
            current.extend([ d['power_meter']['I1'] for d in raw_data ])
            power.extend([ d['power_meter']['P1'] for d in raw_data ])
        else:
            voltage.extend([ d['power_meter']['V_SIGMA'] for d in raw_data ])
            current.extend([ d['power_meter']['I_SIGMA'] for d in raw_data ])
            power.extend([ d['power_meter']['P_SIGMA'] for d in raw_data ])

        self.result_separate_excitation = {
            'voltage': voltage,
            'current': current,
            'power': power,
        }
    
    def plot_separate_excitation(self, ax:plt.Axes=None, show=True):
        if ax is None:
            fig, ax = plt.subplots()
        
        data = self.result_separate_excitation
        current = data['current']
        voltage = data['voltage']
        voltage_sq = [ v**2 for v in voltage ]
        # current = data['current']
        power = data['power']
        # power - 3* I^2 * self.result_dc_resistance 
        for i, p in enumerate(power):
            power[i] = p - 3 * self.result_dc_resistance * current[i]**2
            
        
        




        # voltage sort is reversed
        # find 80% and 100% voltage point inedex
        voltage_80_index = -1
        voltage_100_index = 0
        for i, v in enumerate(voltage):
            if v < self.rated_voltage * 0.8:
                voltage_80_index = i
                break
        for i, v in enumerate(voltage):
            if v < self.rated_voltage * 0.9:
                voltage_100_index = i
                break

        # print('voltage_80_index', voltage_80_index, voltage[voltage_80_index], power[voltage_80_index])
        # print('voltage_100_index', voltage_100_index, voltage[voltage_100_index], power[voltage_100_index])

        # draw voltage^2 vs power

        # clear the plot
        ax.clear()

        ax.plot(voltage_sq, power, 'ro-', label='原始資料')
        ax.set_title('Separate Excitation')
        ax.set_xlabel('Voltage^2 (V^2)')
        ax.set_ylabel('Power (W)')

        line_x = [voltage[voltage_80_index]**2, voltage[voltage_100_index]**2]
        line_y = [power[voltage_80_index], power[voltage_100_index]]
        ax.plot(line_x, line_y, 'b-')

        m = (line_y[1] - line_y[0]) / (line_x[1] - line_x[0])
        b = line_y[0] - m * line_x[0]

        # print('m', m, 'b', b)

        # line1_x = [0, line_x[0]]
        # line1_y = [b, line_y[0]]
        # ax.plot(line1_x, line1_y, 'g-')

        line2_x = voltage_sq
        line2_y = [ m * x + b for x in line2_x ]

        ax.plot(line2_x, line2_y, 'y-', label='線性回歸')

        # 飽和損失 power - line2_y
        line3_x = voltage_sq
        line3_y = [ p - l for p, l in zip(power, line2_y) ]

        ax.plot(line3_x, line3_y, 'go-', label='飽和損失')

        # polt y =0
        ax.axhline(y=0, color='k', linestyle='--')

        # name the line, legend
        # ax.legend(['Data', 'Linear Fit', 'Saturation Loss'])

        ax.legend()



        

        if show:
            plt.show()

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

            'information_dict': self.information_dict,
            
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
        self.information_dict = data['information_dict']
        
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
    
    def _raw_data_to_csv(self, data_log):
        raw_data = data_log['raw_data']
        
        header = [] 
        write_data = []

        for frame in raw_data: # 10 frames
            new_data_row = []
            for device in frame.keys(): # {'power_meter': {key: value}, 'mechanical': {key: value}} 
                for key, value in frame[device].items():
                    if key not in header:
                        header.append(key)
                    new_data_row.append(value)
            write_data.append(new_data_row)
        # print('header', header)
        # print('write_data', write_data)
        return header, write_data
    
    def save_to_csv_files(self, save_dir, file_name_prefix=None):
        os.makedirs(save_dir, exist_ok=True)
        if file_name_prefix is None:
            file_name_prefix = self.make_time_stamp()


        # test raw data export list
        raw_data_export_list = [
            ('dc_resistance', self.data_dc_resistance),
            ('open_circuit', self.data_open_circuit),
            ('locked_rotor', self.data_locked_rotor),
            ('load_test', self.data_load),
            ('separate_excitation', self.data_separate_excitation),
            ('frequency_drift', self.frequency_drift),
        ]

        for test_name, data_log in raw_data_export_list:
            if not data_log or len(data_log) == 0:
                continue
            header, write_data = self._raw_data_to_csv(data_log[-1])
            with open(f'{save_dir}/{file_name_prefix}_{test_name}.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\n')    
                writer.writerow(header)
                for row in write_data:
                    writer.writerow(row)

        # export motor information
        with open(f'{save_dir}/{file_name_prefix}_motor_information.csv', 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')    
            writer.writerow(['key', 'value'])
            for key, value in self.information_dict.items():
                writer.writerow([key, value])
        
        
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
    # file_path = 'test_file/2025_0201_merged.motor.json'
    # file_path = 'test_file/QA123_20250203_151517.motor.json'
    file_path ='test_file\QA123_20250203_170449.motor.json'
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        motor.from_dict(data)

    motor.save_to_csv_files('./rm_test_csv', 'ttttttt')

    # print(json.dumps(motor.to_dict(), indent=4))
    # motor.analyze_dc_resistance()
    # motor.analyze_open_circuit()    
    # motor.analyze_locked_rotor()
    
    # motor.analyze_load_test()
    # motor.polt_load_test(show=True)

    # motor.analyze_separate_excitation()
    # motor.plot_separate_excitation(show=True)
    
    
    
    