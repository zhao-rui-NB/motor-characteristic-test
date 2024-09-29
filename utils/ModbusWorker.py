from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

import struct
import threading
import queue
from queue import Queue

class ModbusWorker:

    def __init__(self, port, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=0.5):
        self.client: ModbusSerialClient = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )

        self.task_queue = Queue()
        self.running = False
        self.worker_thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_task, daemon=True)
            self.worker_thread.start()
            res = self.client.connect()
            if res:
                print(f"[ModbusWorker] connected to {self.client.comm_params.host}")
            else:
                print(f"[ModbusWorker] failed to connect to {self.client.comm_params.host}")

    def stop(self):
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
        self.client.close()
        print(f"[ModbusWorker] disconnected from {self.client.comm_params.host}")

    def _add_task(self, function , args, callback):
        if self.get_task_count() > 10:
            print(f"[ModbusWorker] too heavy load, task queue size: {self.get_task_count()}")
        self.task_queue.put((function, args, callback))

    def get_task_count(self):
        return self.task_queue.qsize()
    
    def _process_task(self):
        while self.running:
            try:
                function, args, callback = self.task_queue.get(timeout=0.1)
                result = function(*args)
                if callback:
                    callback(result)
            except queue.Empty:
                continue

    def _read_input_registers(self,  address, count, slave):
        try:
            result = self.client.read_input_registers(address=address, count=count, slave=slave)
            if not result.isError():
                return result.registers
            else:
                print(f"[ModbusWorker] read input registers error: {result}")
        except ModbusException as e:
            print(f"[ModbusWorker] Modbus exception: {e}")

    def _read_holding_registers(self, address, count, slave):
        try:
            result = self.client.read_holding_registers(address=address, count=count, slave=slave)
            if not result.isError():
                return result.registers
            else:
                print(f"[ModbusWorker] read holding registers error: {result}")
        except ModbusException as e:
            print(f"[ModbusWorker] Modbus exception: {e}")

    def _write_register(self, address, value, slave):
        try:
            result = self.client.write_register(address=address, value=value, slave=slave)
            if not result.isError():
                return True
            else:
                print(f"[ModbusWorker] write register error: {result}")
        except ModbusException as e:
            print(f"[ModbusWorker] Modbus exception: {e}")

    def read_input_registers_threaded(self, address, count, slave, callback):
        self._add_task(self._read_input_registers, (address, count, slave), callback)
        
    def read_holding_registers_threaded(self, address, count, slave, callback):
        self._add_task(self._read_holding_registers, (address, count, slave), callback)
        
    def write_register_threaded(self, address, value, slave, callback):
        self._add_task(self._write_register, (address, value, slave), callback)
    


    @staticmethod
    def registers_to_float(registers):
        if len(registers) == 2:
            return struct.unpack('f', struct.pack('HH', registers[0], registers[1]))[0]

    @staticmethod
    def registers_to_long(registers):
        if len(registers) == 2:
            return struct.unpack('i', struct.pack('HH', registers[0], registers[1]))[0]

    @staticmethod
    def float_to_registers(value):
        data = struct.pack('f', value)
        return struct.unpack('HH', data)
    
    @staticmethod
    def long_to_registers(value):
        data = struct.pack('i', value)
        return struct.unpack('HH', data)



if __name__ == "__main__":
    counter = 0 
    def vcf_callback(result):
        global counter
        counter += 1
        print(f'\n\ncounter: {counter}')
        
        if result:
            keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency']
            res_dict = {k: ModbusWorker.registers_to_float(result[i*2:i*2+2]) for i, k in enumerate(keys)}
            print({k: f'{v:.2f}' for k, v in res_dict.items()})
            # print(f'{{k: ModbusWorker.registers_to_float(result[i*2:i*2+2]) for i, k in enumerate(keys)}}')
            
    
    def read_vcf(worker:ModbusWorker): # datasheet p28 #5 
        # # start address 0x1000 4byte float
        # keys = ['Vln_a', 'Vln_b', 'Vln_c', 'Vln_avg', 'Vll_ab', 'Vll_bc', 'Vll_ca', 'Vll_avg', 'I_a', 'I_b', 'I_c', 'I_avg', 'Frequency']
        # data = self.modbus.read_input_registers(0x1000,len(keys)*2)
        # # cvt to float store data into dict
        # return {k: self.modbus.registers_to_float(data[i*2:i*2+2]) for i, k in enumerate(keys)} 

        worker.read_input_registers_threaded(0x1000, 26, 0x0F, vcf_callback)

    
    modbus = ModbusWorker(port='COM3')
    modbus.start()
    # modbus.read_input_registers_threaded(0x1000, 24, 0x0F, print)
    import time
    for i in range(100):
        read_vcf(modbus)
        # time.sleep(1)

    while not modbus.task_queue.empty():
        pass
    
    modbus.stop()
    
    print('done')
