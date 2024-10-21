
from .ModbusWorker import ModbusWorker

from typing import Union

class SegmentDisplay:
    def __init__(self, modbus_worker: ModbusWorker, slave_address=1):
        self.modbus = modbus_worker
        self.slave = slave_address

    def set_number(self, number: Union[int, float]): # > 0
        # display_digits = 4  # 显示的数字位数
        int_value = 0  # 整数值
        decimal_places = 0  # 小数点位数
        
        if number < 0 or number > 9999:
            print('[SegmentDisplay] Number must be between 0 and 9999')
            return 

        if isinstance(number, int):
            int_value = number
            decimal_places = 0
            
        elif isinstance(number, float):
            if int(number) >= 10**3:
                int_value = int(number)
                decimal_places = 0
            elif int(number) >= 10**2:
                int_value = int(number * 10)
                decimal_places = 1
            elif int(number) >= 10**1:
                int_value = int(number * 100)
                decimal_places = 2
            else:
                int_value = int(number * 1000)
                decimal_places = 3
        
        register6 = ((decimal_places << 8) & 0x0F00) | ((int_value >> 16) & 0xFF)
        register7 = int_value & 0xFFFF 
        
        self.modbus.write_registers_threaded(0x6, [register6, register7], self.slave, self._write_callback)
        
    def set_brightness(self, level: int):
        """
        设置显示亮度
        :param level: 亮度级别 (0-7)
        """
        level = max(0, min(level, 7))  # 确保level在0-7之间
        self.modbus.write_register_threaded(14, level, self.slave, self._write_callback)

    def set_blink(self, blink_pattern: int):
        """
        设置闪烁模式
        :param blink_pattern: 6位二进制数，每位对应一个数码管的闪烁状态
        """
        blink_pattern = blink_pattern & 0x3F  # 确保只有低6位有效
        self.modbus.write_register_threaded(8, blink_pattern, self.slave, self._write_callback)

    def _write_callback(self, result):
        return 
        if result:
            print("Write operation successful")
        else:
            print("Write operation failed")

# 使用示例
if __name__ == "__main__":
    import time 
    
    modbus_worker = ModbusWorker(port='COM70')  # 请根据实际情况修改端口
    display = SegmentDisplay(modbus_worker, slave_address=0x69)

    # 显示数字
    # display.set_number(67.89)

    # # 设置亮度
    # display.set_brightness(2)

    # # 设置闪烁 (例如，让前三个数码管闪烁)
    # display.set_blink(0b0111)


    # test set_number float 
    for i in range(10,1000):
        display.set_number(i/10)
        import time
        time.sleep(0.2)

    # test_list = [0.005, 1.1, 22.22, 333.3, 4444.4, 55555, 55555.0]
    # for i in test_list:
    #     display.set_number(i)
    #     time.sleep(1)

    # for i in range(8):
    #     display.set_brightness(i)
    #     display.set_number(i+8000)
    #     time.sleep(1)

    # # 确保所有任务完成
    while not modbus_worker.task_queue.empty():
        pass

    modbus_worker.stop()