from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
import time
from engine.Motor import Motor
from engine.TestRunner import TestRunner


# 測試模擬用 delay Qthread
class Qthread_test_delay(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor, delay:int):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
        self.delay = delay
    def run(self):
        print(f"Qthread_test_delay start delay: {self.delay}")
        for i in range(self.delay):
            time.sleep(1)
            print(f"{i+1} ", end="")
        print(f"Qthread_test_delay finish")
        self.signal_finish.emit(True)        


class Qthread_run_dc_resistance_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        try:
            succ = self.test_runner.run_dc_resistance_test(self.motor)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_dc_resistance_cold_test] error: {e}")
            self.signal_finish.emit(False)
            
class Qthread_run_open_circuit_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        try:
            succ = self.test_runner.run_open_circuit_test(self.motor)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_open_circuit_test] error: {e}")
            self.signal_finish.emit(False)
        
class Qthread_run_lock_rotor_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        # try:
        succ = self.test_runner.run_lock_rotor_test(self.motor)
        self.signal_finish.emit(succ)
        # except Exception as e:
        #     print(f"[Qthread_run_lock_rotor_test] error: {e}")
        #     self.signal_finish.emit(False)
        
class Qthread_run_load_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        try:
            succ = self.test_runner.run_load_test(self.motor)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_load_test] error: {e}")
            self.signal_finish.emit(False)
        
class Qthread_run_separate_excitation_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        try:
            succ = self.test_runner.run_separate_excitation_test(self.motor)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_separate_excitation_test] error: {e}")
            self.signal_finish.emit(False)

class Qthread_run_frequency_drift_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        try:
            succ = self.test_runner.run_frequency_drift_test(self.motor)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_frequency_drift_test] error: {e}")
            self.signal_finish.emit(False)
            
            
class Qthread_run_CNS14400_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor, step_time:int, enable_150:bool):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
        self.step_time = step_time
        self.enable_150 = enable_150
    def run(self):
        try:
            succ = self.test_runner.run_CNS14400_test(self.motor, step_time=self.step_time, enable_150=self.enable_150)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_CNS14400_test] error: {e}")
            self.signal_finish.emit(False)

class Qthread_run_three_phase_starting_torque_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        try:
            succ = self.test_runner.run_three_phase_starting_torque_test(self.motor)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_three_phase_starting_torque_test] error: {e}")
            self.signal_finish.emit(False)


class Qthread_run_single_phase_starting_torque_test(QThread):
    signal_finish = pyqtSignal(bool)
    def __init__(self, test_runner:TestRunner, motor:Motor):
        super().__init__()
        self.test_runner = test_runner
        self.motor = motor
    def run(self):
        try:
            succ = self.test_runner.run_singel_phase_starting_torque_test(self.motor)
            self.signal_finish.emit(succ)
        except Exception as e:
            print(f"[Qthread_run_single_phase_starting_torque_test] error: {e}")
            self.signal_finish.emit(False)
    

            


        
