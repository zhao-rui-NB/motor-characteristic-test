# %%
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os 
import csv

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 改成支援中文的字體
plt.rcParams['axes.unicode_minus'] = False  # 避免負號顯示成方塊

class Motor:
    def __init__(self):
        # test para 
        self.v_test_dc = 10

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
        self.data_frequency_drift = []
        self.data_CNS14400 = []
        self.data_three_phase_starting_torque = []
        self.data_single_phase_starting_torque = []
        
        # test results
        self.result_dc_resistance = None
        self.result_open_circuit = None
        self.result_locked_rotor = None
        self.result_load_test = None
        self.result_separate_excitation = None
        self.result_frequency_drift = None
        self.result_CNS14400 = None
        self.result_three_phase_starting_torque = None
        self.result_single_phase_starting_torque = None
    
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
        self.data_frequency_drift.append(res)
    
    def add_result_CNS14400(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data, 
        }
        self.data_CNS14400.append(res)  

    def add_result_three_phase_starting_torque(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data, 
        }
        self.data_three_phase_starting_torque.append(res)

    def add_result_single_phase_starting_torque(self, raw_data):
        res = {
            'timestamp': self.make_time_stamp(),
            'raw_data' : raw_data, 
        }
        self.data_single_phase_starting_torque.append(res)

    # analysis functions
    def analyze_dc_resistance(self):
        data_dc_resistance = self.data_dc_resistance
        if not data_dc_resistance:
            print('No data for DC Resistance')
            return
        print(f"Analyzing DC Resistance {data_dc_resistance[-1]['timestamp']}")
            
        
        
        raw_data = data_dc_resistance[-1]['raw_data']

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
        # print('speeds', speeds)

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
    def plot_separate_excitation(self, ax:plt.Axes=None, show=False):
        if not self.result_dc_resistance:
            print('No data for Separate Excitation')
            return

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

        try:
            m = (line_y[1] - line_y[0]) / (line_x[1] - line_x[0])
        except ZeroDivisionError:
            m = 0
        b = line_y[0] - m * line_x[0]

        # print('m', m, 'b', b)

        line2_x = voltage_sq
        line2_y = [ m * x + b for x in line2_x ]

        ax.plot(line2_x, line2_y, 'y-', label='線性回歸')

        # 飽和損失 power - line2_y
        line3_x = voltage_sq
        line3_y = [ p - l for p, l in zip(power, line2_y) ]

        ax.plot(line3_x, line3_y, 'go-', label='飽和損失')

        # polt y =0
        ax.axhline(y=0, color='k', linestyle='--')
        ax.legend()
        # call draw
        ax.figure.tight_layout()
        ax.figure.canvas.draw()
        if show:
            plt.show()

    def analyze_frequency_drift(self):
        if not self.data_frequency_drift:
            print('No data for Frequency Drift')
            return
        
        print(f"Analyzing Frequency Drift from {self.data_frequency_drift[-1]['timestamp']}")
        raw_data = self.data_frequency_drift[-1]['raw_data']
        if not raw_data:
            print('No data for Frequency Drift')
            return

        speeds = [ d['mechanical']['speed'] for d in raw_data ] 
        torques = [ d['mechanical']['torque'] for d in raw_data ]
        power_output = [ speed*torque / 9.5493 for speed, torque in zip(speeds, torques) ]
        frequency = [ d['power_meter']['FU1'] for d in raw_data ]

        if self.is_single_phase():
                current = [ d['power_meter']['I1'] for d in raw_data ]
                power_input = [ d['power_meter']['P1'] for d in raw_data ]
                power_factor = [ d['power_meter']['LAMBDA1'] for d in raw_data ]
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

        self.result_frequency_drift = {
            'speeds': speeds,
            'torques': torques,
            'current': current,
            'power_input': power_input,
            'power_output': power_output,
            'power_factor': power_factor,
            'efficiency': efficiency,
            'frequency': frequency,
            
        }
    def plot_frequency_drift(self, ax:plt.Axes=None, show=False):
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        data = self.result_frequency_drift
        # draw frequency vs (torque, current, power_input, power_output, power_factor, efficiency)
        
        speeds = data['speeds']
        torques = data['torques']
        current = data['current']
        power_input = data['power_input']
        power_output = data['power_output']
        power_factor = data['power_factor']
        efficiency = data['efficiency']
        frequency = data['frequency']
        
        # clear the plot
        ax.clear()
        
        # print("@@@@ frequency:" , frequency)

        # ax1
        ax1 = ax
        ax1.cla()
        ax1.plot(frequency, torques, 'ro-', label='Torque (Nm)')
        ax1.set_ylabel('Torque (Nm)', color='r')
        ax1.tick_params(axis='y', colors='r')
        ax1.yaxis.set_label_position('left')
        ax1.yaxis.tick_left()
        
        # ax2
        ax2 = ax1.twinx()
        ax2.cla()
        ax2.spines['left'].set_position(('outward', 40))
        ax2.plot(frequency, current, 'bo-', label='Current (A)')
        ax2.set_ylabel('Current (A)', color='b')
        ax2.tick_params(axis='y', colors='b')
        ax2.yaxis.set_label_position('left')
        ax2.yaxis.tick_left()
        
        # ax3
        ax3 = ax1.twinx()
        ax3.cla()
        ax3.spines['left'].set_position(('outward', 80))
        ax3.plot(frequency, power_input, 'go-', label='Input Power (W)')
        ax3.plot(frequency, power_output, 'mo-', label='Output Power (W)')
        ax3.set_ylabel('Power (W)', color='g')
        ax3.tick_params(axis='y', colors='g')
        ax3.yaxis.set_label_position('left')
        ax3.yaxis.tick_left()
        
        # ax4
        ax4 = ax1.twinx()
        ax4.cla()
        ax4.spines['left'].set_position(('outward', 120))
        ax4.plot(frequency, power_factor, 'co-', label='Power Factor')
        ax4.set_ylabel('Power Factor', color='c')
        ax4.tick_params(axis='y', colors='c')
        ax4.yaxis.set_label_position('left')
        ax4.yaxis.tick_left()
        
        # ax5
        ax5 = ax1.twinx()
        ax5.cla()
        ax5.spines['left'].set_position(('outward', 160))
        ax5.plot(frequency, efficiency, 'yo-', label='Efficiency (%)')
        ax5.set_ylabel('Efficiency (%)', color='y')
        ax5.tick_params(axis='y', colors='y')
        ax5.yaxis.set_label_position('left')
        ax5.yaxis.tick_left()
        
        # set x label
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_title('Performance Curves vs Frequency', fontsize=16)
        
        # 合併圖例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines3, labels3 = ax3.get_legend_handles_labels()
        lines4, labels4 = ax4.get_legend_handles_labels()
        lines5, labels5 = ax5.get_legend_handles_labels()
        ax1.legend(lines1 + lines2 + lines3 + lines4 + lines5, labels1 + labels2 + labels3 + labels4 + labels5, loc='center left')
        
        # call draw
        ax1.figure.tight_layout()
        ax1.figure.canvas.draw()
        
        if show:
            plt.tight_layout()
            plt.show()
    
    def analyze_CNS14400(self):
        if not self.data_CNS14400:
            print('No data for CNS14400')
            return
        
        print(f"Analyzing CNS14400 from {self.data_CNS14400[-1]['timestamp']}")
        raw_data = self.data_CNS14400[-1]['raw_data']
        
        # print(raw_data)
        # print(raw_data[0])
        # print(raw_data[0]['power_meter'])
        
        group_num = len(raw_data)//6
        print('group_num', group_num)
        
        # group to calculate the average value
        # voltage
        # current
        # power_input
        # nr
        # speed 
        # torque 
        # power_output 
        # power_factor 
        # efficiency 
        
        speed = [ d['mechanical']['speed'] for d in raw_data ]
        torque = [ d['mechanical']['torque'] for d in raw_data ]
        power_output = [ speed*torque / 9.5493 for speed, torque in zip(speed, torque) ]
        # nr = [ d['power_meter']['NR1'] for d in raw_data ]
        
        if self.is_single_phase():
            voltage = [ d['power_meter']['V1'] for d in raw_data ]
            current = [ d['power_meter']['I1'] for d in raw_data ]
            power_input = [ d['power_meter']['P1'] for d in raw_data ]
            power_factor = [ d['power_meter']['LAMBDA1'] for d in raw_data ]
        
        else:
            voltage = [ d['power_meter']['V_SIGMA'] for d in raw_data ]
            current = [ d['power_meter']['I_SIGMA'] for d in raw_data ]
            power_input = [ d['power_meter']['P_SIGMA'] for d in raw_data ]
            power_factor = [ d['power_meter']['LAMBDA_SIGMA'] for d in raw_data ]
            
        efficiency = []
        for po, pi in zip(power_output, power_input):
            if pi == 0:
                efficiency.append(0)
            else:
                efficiency.append(po / pi)
                
        
        # calculate the average value of each group
        def group_average(data, group_num):
            group_data = []
            for i in range(0, len(data), group_num):
                group_data.append(sum(data[i:i+group_num]) / group_num)
            return group_data
        
        speed = group_average(speed, group_num)
        torque = group_average(torque, group_num)
        power_output = group_average(power_output, group_num)
        voltage = group_average(voltage, group_num)
        current = group_average(current, group_num)
        power_input = group_average(power_input, group_num)
        power_factor = group_average(power_factor, group_num)
        efficiency = group_average(efficiency, group_num)
        
        # t max
        t_max = max(torque)
        p_max = max(power_output)   
        
        self.result_CNS14400 = {
            'speed': speed,
            'torque': torque,
            'voltage': voltage,
            'current': current,
            'power_input': power_input,
            'power_output': power_output,
            'power_factor': power_factor,
            'efficiency': efficiency,
            't_max': t_max,
            'p_max': p_max,
        }

    def make_CNS14400_csv_str(self):
        ret_csv_str = ''
        
        header = ['Speed (rpm)', 'Torque (Nm)', 'Voltage (V)', 'Current (A)', 'Input Power (W)', 'Output Power (W)', 'Power Factor', 'Efficiency (%)']
        data = self.result_CNS14400
        
        ret_csv_str += ','.join(header) + '\n'
        
        for i in range(len(data['speed'])):
            ret_csv_str += f"{data['speed'][i]},{data['torque'][i]},{data['voltage'][i]},{data['current'][i]},{data['power_input'][i]},{data['power_output'][i]},{data['power_factor'][i]},{data['efficiency'][i]}\n"
            
        ret_csv_str  += f"Max Torque (Nm), {data['t_max']}\n"
        ret_csv_str  += f"Max Power (W), {data['p_max']}\n"
        
        return ret_csv_str 
        
    
    # # polt a combined figure that has 5 curves in one figure (current, torque, efficiency, input power, output power) vs speed
    def plot_load_test_combined_figure(self, ax:plt.Axes=None, show=False):
        # 平滑資料 , not use np 
        def smooth_data(data, window_size=6):
            # return data
            smoothed_data = []
            for i in range(len(data)):
                start = max(0, i - window_size)
                end = min(len(data), i + window_size)
                smoothed_data.append(sum(data[start:end]) / (end - start))
            return smoothed_data
        
        
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
        
        data = self.result_load_test
        speed = data['speeds']
        
        
        # 電流 (主軸)
        ax1 = ax
        ax1.clear()
        ax1.plot(speed, smooth_data(data['current']), 'r-', label='Current (A)')
        ax1.set_ylabel('Current (A)', color='r')
        ax1.tick_params(axis='y', colors='r')
        ax1.yaxis.set_label_position('left')
        ax1.yaxis.tick_left()

        # 轉矩 (左側第二軸)
        ax2 = ax1.twinx()
        ax2.clear()
        ax2.spines['left'].set_position(('outward', 40))
        ax2.plot(speed, smooth_data(data['torques']), 'b-', label='Torque (Nm)')
        ax2.set_ylabel('Torque (Nm)', color='b')
        ax2.tick_params(axis='y', colors='b')
        ax2.yaxis.set_label_position('left')
        ax2.yaxis.tick_left()

        # 效率 (左側第三軸)
        ax3 = ax1.twinx()
        ax3.clear()
        ax3.spines['left'].set_position(('outward', 80))
        ax3.plot(speed, smooth_data(data['efficiency']), 'g-', label='Efficiency (%)')
        ax3.set_ylabel('Efficiency (%)', color='g')
        ax3.tick_params(axis='y', colors='g')
        ax3.yaxis.set_label_position('left')
        ax3.yaxis.tick_left()
        
        # 輸入功率 (左側第四軸)
        ax4 = ax1.twinx()
        ax4.clear()
        ax4.spines['left'].set_position(('outward', 120))
        ax4.plot(speed, smooth_data(data['power_input']), 'c-', label='Input Power (W)')
        ax4.plot(speed, smooth_data(data['power_output']), 'm-', label='Output Power (W)')
        ax4.set_ylabel('Power (W)', color='c')
        ax4.tick_params(axis='y', colors='c')
        ax4.yaxis.set_label_position('left')
        ax4.yaxis.tick_left()
        
        # 統一x軸標籤和標題
        ax1.set_xlabel('Speed (rpm)')
        ax1.set_title('Performance Curves vs Speed', fontsize=16)

        # 合併圖例
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        lines3, labels3 = ax3.get_legend_handles_labels()
        lines4, labels4 = ax4.get_legend_handles_labels()
        # lines5, labels5 = ax5.get_legend_handles_labels()
        ax1.legend(lines1 + lines2 + lines3 + lines4, labels1 + labels2 + labels3 + labels4, loc='center left')   

        # call draw
        ax1.figure.tight_layout()
        ax1.figure.canvas.draw()
        
        if show:
            plt.tight_layout()
            plt.show()

    
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
                'result_CNS14400': self.result_CNS14400,
                'result_three_phase_starting_torque': self.result_three_phase_starting_torque,
                'result_single_phase_starting_torque': self.result_single_phase_starting_torque,
            },
            
            'test_data_log': {
                'data_dc_resistance': self.data_dc_resistance,
                'data_open_circuit': self.data_open_circuit,
                'data_locked_rotor': self.data_locked_rotor,
                'data_load': self.data_load,
                'data_separate_excitation': self.data_separate_excitation,
                'frequency_drift': self.data_frequency_drift,
                'CNS14400': self.data_CNS14400,
                'three_phase_starting_torque': self.data_three_phase_starting_torque,
                'single_phase_starting_torque': self.data_single_phase_starting_torque,
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
        self.result_CNS14400 = data['test_results']['result_CNS14400']
        self.result_three_phase_starting_torque = data.get('test_results', {}).get('result_three_phase_starting_torque', [])
        self.result_single_phase_starting_torque = data.get('test_results', {}).get('result_single_phase_starting_torque', [])

        self.data_dc_resistance = data['test_data_log']['data_dc_resistance']
        self.data_open_circuit = data['test_data_log']['data_open_circuit']
        self.data_locked_rotor = data['test_data_log']['data_locked_rotor']
        self.data_load = data['test_data_log']['data_load']
        self.data_separate_excitation = data['test_data_log']['data_separate_excitation']
        self.data_frequency_drift = data['test_data_log']['frequency_drift']
        self.data_CNS14400 = data['test_data_log']['CNS14400']
        self.data_three_phase_starting_torque = data.get('test_data_log', {}).get('three_phase_starting_torque', [])
        self.data_single_phase_starting_torque = data.get('test_data_log', {}).get('single_phase_starting_torque', [])

    def remove_test_result(self):
        # test data log
        self.data_dc_resistance = []
        self.data_open_circuit = []
        self.data_locked_rotor = []
        self.data_load = []
        self.data_separate_excitation = []
        self.data_frequency_drift = []
        self.data_CNS14400 = []
        self.data_three_phase_starting_torque = []
        self.data_single_phase_starting_torque = []
        
        # test results
        self.result_dc_resistance = None
        self.result_open_circuit = None
        self.result_locked_rotor = None
        self.result_load_test = None
        self.result_separate_excitation = None
        self.result_frequency_drift = None
        self.result_CNS14400 = None
        self.result_three_phase_starting_torque = None
        self.result_single_phase_starting_torque = None

    # def _fix_meter_I2(self, )
    def _raw_data_to_csv(self, data_log):
        # raw_data = data_log['raw_data']
        if "raw_data" not in data_log:
            raw_data = data_log
        else:
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
            ('frequency_drift', self.data_frequency_drift),
            # ('CNS14400', self.result_CNS14400),
            ('three_phase_starting_torque', self.data_three_phase_starting_torque),
            ('single_phase_starting_torque', self.data_single_phase_starting_torque),
        ]


        for test_name, data_log in raw_data_export_list:
            if not data_log or len(data_log) == 0:
                continue

            # if resistance in test name , power meter I2 = I1+I3
            if 'resistance' in test_name:
                for frame in data_log[-1]['raw_data']:
                    if 'power_meter' in frame:
                        frame['power_meter']['I2'] = frame['power_meter']['I1'] + frame['power_meter']['I3']

            header, write_data = self._raw_data_to_csv(data_log[-1])
            with open(f'{save_dir}/{test_name}.csv', 'w') as f:
                writer = csv.writer(f, lineterminator='\n')    
                writer.writerow(header)
                for row in write_data:
                    writer.writerow(row)

        # export CNS14400
        if self.data_CNS14400:
            print('export CNS14400')
            cns_data = self.data_CNS14400[-1]['raw_data']
            # print(cns_data)
            for test_name, data_logs in cns_data.items():
                if 'resistance' in test_name:
                    for frame in data_logs:
                        if 'power_meter' in frame:
                            frame['power_meter']['I2'] = frame['power_meter']['I1'] + frame['power_meter']['I3']
                header, write_data = self._raw_data_to_csv(data_logs)

                # if resistance in test name , power meter I2 = I1+I3

                with open(f'{save_dir}/CNS14400_{test_name}.csv', 'w', encoding='utf8') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerow(header)
                    for row in write_data:
                        writer.writerow(row)
        # export motor information
        with open(f'{save_dir}/motor_information.csv', 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')    
            writer.writerow(['key', 'value'])
            for key, value in self.information_dict.items():
                writer.writerow([key, value])

            # export motor parameters
            writer.writerow(['rated_voltage', self.rated_voltage])
            writer.writerow(['power_phases', self.power_phases])
            writer.writerow(['speed', self.speed])
            writer.writerow(['rated_current', self.rated_current])
            writer.writerow(['frequency', self.frequency])
            writer.writerow(['horsepower', self.horsepower])
            writer.writerow(['poles', self.poles])
            writer.writerow(['no_load_current', self.no_load_current])


        
    
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
    # file_path ='test_file\QA123_20250206_hand.motor.json'
    file_path ='model_20250207_183822.motor.json'
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
        # print(data['test_data_log']["CNS14400"])
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
    
    # motor.analyze_load_test()
    # motor.plot_load_test_combined_figure(show=True)
    
    # motor.analyze_frequency_drift()
    # motor.plot_frequency_drift(show=True)
    
    