import socket

def send_scpi_command(ip, port, command, timeout=4):
    try:
        # 創建一個 TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)

            print(sock)
            sock.connect((ip, port))
            print(sock)

            for cmd in command:
                print('-------------------')
                if cmd[-1] != '\n':
                    cmd += '\n'
                sock.send(cmd.encode())
                print('send:', cmd)

                try:
                    if '?' in cmd:
                        response = sock.recv(1024)
                        print('response:',response)
                except socket.error as e:
                    print(f'Socket 錯誤: {e}')

            sock.close()
            # return response.decode()
    except socket.error as e:
        print(f'Socket 錯誤: {e}')
        return None

# 示例用法
ip_address = '192.168.50.169'  # 儀器的 IP 地址
port_number = 2268           # 儀器的端口號

# scpi_command = '*IDN?\n' # ok*idn?
# scpi_command = '*TST?\n'
# scpi_command = '*CLS\n' # ok
# scpi_command = '*RST?\n' 

commands = [
    '*CLS\n',
    '*IDN?\n',
    # ':SYSTem:REBoot\n',
    ':meas:volt?;curr?\n',

        
    ':OUTPut 0',
    

    # ':STATus:OPERation:CONDition?',

    # ':MEASure:SCALar:FREQuency?'

    # 'VOLT:RANG?',

    # 'VOLTage 75',
    # 'FREQ 60',
    # 'CURRent:LIMit:RMS 3.5',


    'VOLTage?',
    'FREQ?',
    'CURRent:LIMit:RMS?',

    'OUTPut?',

    
    # ':INITiate:NAME\n',
    # ':INITiate\n',
    
    # ':OUTPut:PON?\n',
    # ':OUTPut:PON 1\n',
    # ':OUTPut:STATe?\n',

    # ':OUTPut:PON 0\n',
    # 'MEASure:SCALar:FREQuency?\n',
    # ':OUTPut[:STATe]:TRIGgered?\n',

]

response = send_scpi_command(ip_address, port_number, commands)
