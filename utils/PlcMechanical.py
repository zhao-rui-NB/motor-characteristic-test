from .ModbusTcpWorker import ModbusTcpWorker


class PlcMechanical:
    
    def __init__(self, ip, port):
        self.worker = ModbusTcpWorker(ip, port)
        
    def get_mechanical_data(self):
        result = self.worker.read_holding_registers(0x0000, 4)
        
        speed = self.worker.registers_to_float(result[0:2])
        torque = self.worker.registers_to_float(result[2:4])
        
        return {'speed': speed, 'torque': torque}
    
    def set_break(self, value):
        '''Set break value 0-4000'''
        return self.worker.write_register(20, value)
        


if __name__ == '__main__':
    plc = PlcMechanical('192.168.0.101', 502)
    
    print(plc.get_mechanical_data())
    
    
    print(plc.set_break(2000))
    
    plc.worker.client.close()    