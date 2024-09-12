import socket

def read_power_supply(ip_address, port):
    # 创建一个 socket 对象
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # 连接到电源供应器
        s.connect((ip_address, port))

        print(s)

        # 发送查询命令
        command = ':SYSTem:BEEPer:STATe?'
        s.sendall(command.encode())
        
        # # 接收电源供应器的响应
        # response = s.recv(300, )

        # client,addr = s.accept()
        
        # # 打印响应
        # print(f"响应: {response}")



# 示例用法
ip_address = '192.168.50.169'  # 替换为你的电源供应器的 IP 地址
port = 2268  # 替换为电源供应器的端口号
read_power_supply(ip_address, port)
