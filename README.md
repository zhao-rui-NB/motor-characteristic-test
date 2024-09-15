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


