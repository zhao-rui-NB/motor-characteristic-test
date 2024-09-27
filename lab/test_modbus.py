from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException

# 設置串口參數
PORT = 'COM3'  # 根據您的系統修改串口
SLAVE_ADDRESS = 0x0F      # Modbus從機地址

# 創建Modbus RTU客戶端
client = ModbusSerialClient(
    port=PORT,
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

# 讀取功能碼04（讀取輸入寄存器）
def read_input_registers(address, count):
    try:
        # 連接到Modbus設備
        client.connect()
        
        # 讀取輸入寄存器
        result = client.read_input_registers(address=address, count=count, slave=SLAVE_ADDRESS)
        print('result', result)
        
        
        if not result.isError():
            return result.registers
        else:
            print(f"讀取錯誤: {result}")
            return None
    except ModbusException as e:
        print(f"Modbus異常: {e}")
        return None
    finally:
        # 確保關閉連接
        client.close()

# 主程序
if __name__ == "__main__":
    register_address = 0x1000    # 起始寄存器地址
    
    print('register_address' , register_address)
    
    number_of_registers = 2 # 要讀取的寄存器數量
    
    result = read_input_registers(register_address, number_of_registers)
    if result:
        print(f"讀取的值: {result}")
        
        
    # 4byte to float
    import struct
    print(struct.unpack('f', struct.pack('HH', result[0], result[1]))[0])
    