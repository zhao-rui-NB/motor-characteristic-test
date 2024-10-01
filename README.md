# motor-characteristic-test

## 軟體功能

### 主頁
```
高雄科技大學電機系
馬達特性測試系統

單相馬達
三相馬達
exit結束
```

### 單相
```
單相馬達測試
1.無載測試
2.堵轉測試
3.鐵損分離測試
4.頻率變動測試
5.馬達參數輸入
6.測試結果查詢
7.載入馬達參數
8.綜合測試
9.測試結果列印
10.回上頁
```

### 3相
```
三相馬達測試
1.無載測試
2.堵轉測試
3.鐵損分離測試
4.頻率變動測試
5.馬達參數輸入
6.測試結果查詢
7.載入馬達參數
8.綜合測試
9.測試結果列印
10.回上頁
```


### 參數表格
```
試驗日期
印表日期

額定電壓
額定電流
馬力
空載電流

相數
頻率
極數
迴轉數
```





## 交流可調電源 aps 7100
* SCPI commands 樹狀節點組成
* `:`開始代表root node
* 節點`:`連接
* 命令`;`連接
* 多command若沒`:`開頭,延續使用第一指令node

PROGRAMMING MANUAL: [PDF](https://www.gwinstek.com/en-global/products/downloadSeriesDownNew/8395/562)

### command 

| 命令 | 用途 |
|------|------|
| `*IDN` | 識別設備 |
| `*CLS` | 清除狀態 |
| `MEAS:CURR` | 測量電流 |
| `MEAS:VOLT` | 測量電壓 |
| `MEAS:POW:APP` | 測量視在功率 |
| `MEAS:POW` | 測量實際功率 |
| `SOUR:READ` | 讀取源設置 |
| `SOUR:VOLT` | 設置/查詢輸出電壓 |
| `SOUR:FREQ` | 設置/查詢輸出頻率 |
| `SOUR:CURR:LIM:RMS` | 設置/查詢 RMS 電流限制 |
| `SOUR:VOLT:RANG` | 設置/查詢電壓範圍 # 155,310,600 |
| `OUTPut` | 控制/查詢輸出開關狀態 |
| `SYSTem:REBoot` | 重啟系統 |

#### output
```
OUTPut 0
OUTPut 1
```

#### f a v 
```
'VOLTage 75',
'FREQ 60',
'CURRent:LIMit:RMS 3.5'
```

#### read 
```
send: *IDN?
response: b'GWINSTEK,APS-7100,GEQ120257,01.10.20151016\n'
-------------------
send: :meas:volt?;curr?
response: b'+75.0000;+0.0000\n'
-------------------
send: :OUTPut 1
-------------------
send: VOLTage?
response: b'+75.0000\n'
-------------------
send: FREQ?
response: b'+60.0000\n'
-------------------
send: CURRent:LIMit:RMS?
response: b'+3.5000\n'
-------------------
send: OUTPut?
response: b'+0\n'
```

## spm3 可調電源

User guide: [PDF](https://www.cleswitch.com.tw/uploads/files/1666929988.pdf)

```
Modbus RTU
IEEE 754 Format
03 Read Holding RegistersRead the content of read/write location   
04 Read Input Registers Read the contents of read only location16 Pre-set Multiple Registers Set the contents of read/write location
```

### modbus reg 
#### vcf

|---|---|
|---|---|
|Vln_a |  0x1000-0x1001|
|Vln_b |  0x1002-0x1003|
|Vln_c |  0x1004-0x1005|
|Vln_avg |  0x1006-0x1007|
|Vll_ab |  0x1008-0x1009|
|Vll_bc |  0x100a-0x100b|
|Vll_ca |  0x100c-0x100d|
|Vll_avg |  0x100e-0x100f|
|I_a |  0x1010-0x1011|
|I_b |  0x1012-0x1013|
|I_c |  0x1014-0x1015|
|I_avg |  0x1016-0x1017|
|Frequency |  0x1018-0x1019|


#### power resault 
| Parameter | Hex Address   | Unit |
|-----------|---------------|------|
| kW_a      | 0x101A-0x101B | kW   |
| kW_b      | 0x101C-0x101D | kW   |
| kW_c      | 0x101E-0x101F | kW   |
| kW_tot    | 0x1020-0x1021 | kW   |
| kvar_a    | 0x1022-0x1023 | kvar |
| kvar_b    | 0x1024-0x1025 | kvar |
| kvar_c    | 0x1026-0x1027 | kvar |
| kvar_tot  | 0x1028-0x1029 | kvar |
| kVA_a     | 0x102A-0x102B | kVA  |
| kVA_b     | 0x102C-0x102D | kVA  |
| kVA_c     | 0x102E-0x102F | kVA  |
| kVA_tot   | 0x1030-0x1031 | kVA  |
| PF        | 0x1032-0x1033 | -    |







## 中盛数码管显示屏

# 中盛数码管显示屏寄存器功能列表

| 地址 | 功能描述 | 备注 |
|------|----------|------|
| 0-5  | 控制各位数码管显示内容 | 每个寄存器对应一位数码管,存储ASCII码值 |
| 6    | 数据格式 | 高字节高4位: 0正/1负; 低4位: 小数点位置; 低字节: 数据最高8位 |
| 7    | 显示数据 | 与寄存器6配合使用,存储数据的中间8位和最低8位 |
| 8    | 闪烁控制 | 每位对应一个数码管,1闪烁0不闪烁,掉电不保存 |
| 9    | 显示内容保存 | 0不保存,1保存所有数码管显示内容,掉电保存 |
| 10   | 模块485总线地址 | 范围1~254,0是广播地址,掉电保存 |
| 11   | 波特率设置 | 0:4800, 1:9600, 2:14400, 3:19200, 4:38400, 5:56000, 6:57600, 7:115200, 掉电保存 |
| 12   | 停止位设置 | 0:1位, 1:1.5位, 2:2位, 掉电保存 |
| 13   | 校验位设置 | 0:无校验, 1:奇校验, 2:偶校验, 掉电保存 |
| 14   | 亮度调节 | 范围0~7,0最暗7最亮,掉电保存 |
| 15   | 上电初始显示模式设置 | 0:显示"0", 1:显示485地址, 2:显示保存的数据, 掉电保存 |

注意:
1. 寄存器6和7需要配合使用来显示数值。
2. 大多数设置参数在掉电后会保存,但闪烁控制(寄存器8)不会。
3. 通信参数的更改(如波特率、停止位、校验位)在掉电保存后生效。


寄存器6和7 (32位总长)

[31:28] | [27:24] | [23:16]  | [15:8]   | [7:0]
--------|---------|----------|----------|---------
  符号   | 小数点  | 数据高位 | 数据中位 | 数据低位


