# motor-characteristic-test

## 功能

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


## 表格
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

## 監視器
```
[01] 電壓_RS
[02] 電壓_ST
[03] 電壓_TR
[04] 平均電壓
[05] 電流_R
[06] 電流_S
[07] 電流_T
[08] 平均電流
[09] 功率_RS
[13] 功率_TS
[17] 輸入功率
[21] 轉速
[10] 乏功率_RS
[14] 乏功率_TS
[18] 輸入乏功率
[22] 轉矩
[11] 視在功率_RS
[15] 視在功率_TS
[19] 輸入視在功率
[23] 輸出功率
[12] 功率因數_RS
[16] 功率因數_TS
[20] 平均功率因數
[24] 效率

```



## 交流可調電源 aps 7100
* SCPI commands 樹狀節點組成
* `:`開始代表root node
* 節點`:`連接
* 命令`;`連接
* 多command若沒`:`開頭,延續使用第一指令node

PROGRAMMING MANUAL: [PDF](https://www.gwinstek.com/en-global/products/downloadSeriesDownNew/8395/562)
```
Setting the Voltage Range → from page 61
Setting the Voltage Limit → from page 62
Setting the Output Voltage → from page 63
Setting the Frequency Limit → page 65
Setting the Output Frequency → page 66
Setting the Peak Current Limit → from page 67
Setting the Current RMS Level → from page 69
Clearing the Alarm → from page 75
Turning the Output on/off → from page 79
```
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

### output
OUTPut 0
OUTPut 1

### f a v 
'VOLTage 75',
'FREQ 60',
'CURRent:LIMit:RMS 3.5'


### read 
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


# spm3 modbus reg 
## vcf (flaot)

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


## power resault 
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

## 
| Parameter | Hex address   |
|-----------|---------------|
| kWh       | 0x1034-0x1035 |
| kvarh     | 0x1036-0x1037 |
| kVAh      | 0x1038-0x1039 |


## vcf (flaot)
Vln_a
Vln_b
Vln_c
Vln_avg

Vll_ab 
Vll_bc
Vll_ca
Vll_avg

I_a
I_b
I_c
I_avg

Frequency
