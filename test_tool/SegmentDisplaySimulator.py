import sys
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from pymodbus.server import StartSerialServer, ServerStop
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock, ModbusSparseDataBlock
import threading

class ModbusServerQThread(QThread):

    def __init__(self, com_port, slave_addresses):
        super().__init__()
        self.com_port = com_port
        self.slave_addresses = slave_addresses
        # self.store= {address:ModbusSlaveContext() for address in slave_addresses}
        
        self.store = {}
        for address in slave_addresses:
            datablock = ModbusSequentialDataBlock(address=0, values=[0]*100)
            self.store[address] = ModbusSlaveContext(di=datablock, co=datablock, hr=datablock, ir=datablock)
            
            
        for address, context in self.store.items():
            context.setValues(3, 6, [0])  # 設置不同的初始值
            context.setValues(3, 7, [0])
            
        
        self.context = ModbusServerContext(slaves=self.store, single=False)
        

    def run(self):
        try:
            StartSerialServer(
                context=self.context,
                port=self.com_port,
                framer="rtu",
                baudrate=9600,
                stopbits=1,
                bytesize=8,
                parity='N'
            )
        except Exception as e:
            print(f'[ModbusServerThread] [com_port={self.com_port}] {str(e)}')
        
        print(f'[ModbusServerThread] [com_port={self.com_port}] server started')        

    def quit(self):
        ServerStop()
        print('[ModbusServerThread] server stopped')
        super().quit()
        

class ModbusServerThread(threading.Thread):
    def __init__(self, com_port, slave_addresses):
        super().__init__()
        self.com_port = com_port
        self.slave_addresses = slave_addresses
        self.store = {}
        
        # 初始化數據存儲
        for address in slave_addresses:
            datablock = ModbusSequentialDataBlock(address=0, values=[0]*100)
            self.store[address] = ModbusSlaveContext(di=datablock, co=datablock, hr=datablock, ir=datablock)
        
        for address, context in self.store.items():
            context.setValues(3, 6, [0])
            context.setValues(3, 7, [0])
        
        self.context = ModbusServerContext(slaves=self.store, single=False)
        self._running = False

    def run(self):
        if not self._running:
            try:
                self._running = True
                StartSerialServer(
                    context=self.context,
                    port=self.com_port,
                    framer="rtu",
                    baudrate=9600,
                    stopbits=1,
                    bytesize=8,
                    parity='N'
                )
            except Exception as e:
                print(f'[ModbusServerThread] [com_port={self.com_port}] {str(e)}')
            
            print(f'[ModbusServerThread] [com_port={self.com_port}] server started')
        else:
            print('[ModbusServerThread] server already running')
            
    def stop(self):
        self._running = False  # 停止運行的標誌
        ServerStop()
        print('[ModbusServerThread] server stopped')       
    

class SegmentDisplaySimulator(QWidget):
    def __init__(self, modbus_server: ModbusServerThread, slave_address: int):
        super().__init__()
        self.modbus_server = modbus_server
        self.slave_address = slave_address
        self.initUI()
        
        font = QFont()
        font.setPointSize(20)
        self.setFont(font)
        self.setGeometry(100, 100, 600, 400)
        
        
        # 啟動定時器以定期更新顯示
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)  # 每100ms更新一次

    def initUI(self):
        self.setWindowTitle('SegmentDisplay Modbus從站模擬器')
        self.main_layout = QVBoxLayout(self)

        self.top_layout = QHBoxLayout()

        self.info = QLabel(f'[Addr] {hex(self.slave_address)}')
        self.info.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.top_layout.addWidget(self.info)
        
        self.top_layout.addSpacing(10)
        
        self.name = QLineEdit()
        self.name.setPlaceholderText('名稱')
        self.top_layout.addWidget(self.name)
        
        self.main_layout.addLayout(self.top_layout)
        
        self.display = QLCDNumber(6)
        self.display.setSegmentStyle(QLCDNumber.SegmentStyle.Filled)
        self.main_layout.addWidget(self.display)




    def update_display(self):
        try:
            reg6 = self.modbus_server.store[self.slave_address].getValues(3, 6, 1)[0]  # 功能碼3表示保持寄存器
            reg7 = self.modbus_server.store[self.slave_address].getValues(3, 7, 1)[0] 

            decimal_places = (reg6 >> 8) & 0xFF
            number = ((reg6 & 0xFF) << 16) | reg7

            if decimal_places > 4:
                decimal_places = 4  # 最多4位小數

            display_number = number / (10 ** decimal_places)
            self.display.display(f'{display_number:.{decimal_places}f}')

        except Exception as e:
            print(f'[SegmentDisplaySimulator] slave_address={self.slave_address}] {str(e)}')
            
    # delete the simulator
    # def __del__
    
class MultiSegmentDisplayManager(QWidget):
    def __init__(self):
        super().__init__()
        
        self.server_thread = None
        self.simulators = []
        
        
        self.initUI()
        font = QFont()
        font.setPointSize(20)
        self.setFont(font)
        self.setGeometry(100, 100, 800, 600)

        
    def initUI(self):
        # one line at the top , setting comport and start address and nxm display(row x column)
        self.setWindowTitle('多重 SegmentDisplay Modbus 從站模擬器管理器')
        self.setGeometry(100, 100, 800, 600)
        
        self.main_layout = QVBoxLayout(self)
        
        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)
        
        
        lo = QVBoxLayout()
        lo.addWidget(QLabel('COM Port'))
        self.com_port = QLineEdit('COM69')
        self.com_port.setPlaceholderText('COMx')
        lo.addWidget(self.com_port)
        self.top_layout.addLayout(lo)
        
        lo = QVBoxLayout()
        lo.addWidget(QLabel('Start Address'))
        self.start_address = QLineEdit('0x69')
        self.start_address.setPlaceholderText('0x')
        lo.addWidget(self.start_address)
        self.top_layout.addLayout(lo)
        
        
        lo = QVBoxLayout()
        lo.addWidget(QLabel('Row'))        
        self.row = QLineEdit()
        self.row.setPlaceholderText('row')
        lo.addWidget(self.row)
        self.top_layout.addLayout(lo)
        
        lo = QVBoxLayout()
        lo.addWidget(QLabel('Column'))
        self.column = QLineEdit()
        self.column.setPlaceholderText('column')
        lo.addWidget(self.column)
        self.top_layout.addLayout(lo)
        
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start)
        self.top_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop)
        self.top_layout.addWidget(self.stop_button)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        
    def start(self):
        print('[MultiSegmentDisplayManager] start')
        com_port = self.com_port.text()
        start_address = int(self.start_address.text(), 16)
        row = int(self.row.text())
        column = int(self.column.text())
        
        address_list = [start_address + i for i in range(row*column)]
        
        self.server_thread = ModbusServerThread(com_port, address_list)
        self.server_thread.start()
        
        self.simulators = [SegmentDisplaySimulator(self.server_thread, address) for address in address_list]
        # make the simulators row x column
        for i in range(row):
            row_layout = QHBoxLayout()
            for j in range(column):
                row_layout.addWidget(self.simulators[i*column + j])
            self.scroll_layout.addLayout(row_layout)
            
        # dislable the start button and all the input
        self.start_button.setEnabled(False)
        self.com_port.setEnabled(False)
        self.start_address.setEnabled(False)
        self.row.setEnabled(False)
        self.column.setEnabled(False)
        
        
    def stop(self):
        print('[MultiSegmentDisplayManager] stopping')
        
        if self.server_thread:
            # self.server_thread.quit()
            # self.server_thread.wait()
            
            self.server_thread.stop()
            
            
            self.server_thread = None

        # 刪除所有模擬器
        for simulator in self.simulators:
            simulator.setParent(None)  # 從父控件中移除
            # simulator.deleteLater()  # 安排控件稍後刪除

        self.simulators.clear()  # 清空模擬器列表
        
        # enable the start button and all the input
        self.start_button.setEnabled(True)
        self.com_port.setEnabled(True)
        self.start_address.setEnabled(True)
        self.row.setEnabled(True)
        self.column.setEnabled(True)
        
        
        print('[MultiSegmentDisplayManager] stoped')
        


            
        
        

if __name__ == '__main__':
    
    #### test single segment display
    # app = QApplication(sys.argv)
    # server = ModbusServerThread('COM69', [0x69])
    # server.start()
    # display = SegmentDisplaySimulator(server, 0x69)
    # display.show()
    # app.exec()
    
    
    #### test multi segment display
    app = QApplication(sys.argv)
    manager = MultiSegmentDisplayManager()
    manager.show()
    app.exec()
