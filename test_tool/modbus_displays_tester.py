from utils.SegmentDisplay import SegmentDisplay
from utils.ModbusWorker import ModbusWorker

import time


if __name__=='__main__':
    
    start_address = 0x69
    display_cnt = 16
    sleep_time = 0.5

    num_list = [i*i for i in range(20)]
    
        
    modbus_worker = ModbusWorker(port='COM70')
    displays = [SegmentDisplay(modbus_worker, slave_address=start_address+i) for i in range(display_cnt)]
    
    def set_zero():
        for i in range(display_cnt):
            displays[i].set_number(0)
    
    # show self modbus address on display
    for i in range(display_cnt):
        displays[i].set_number(displays[i].slave)
    time.sleep(sleep_time)
    
    set_zero()
    time.sleep(sleep_time)
    
    # count number from 0 to 999
    for num in num_list:
        for i in range(display_cnt):
            displays[i].set_number(num)
        time.sleep(sleep_time)

    # 
    for i in range(display_cnt):
        set_zero()
        displays[i].set_number(100*i)
        time.sleep(sleep_time*2)