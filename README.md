# motor-characteristic-test


## main

高雄科技大學電機系
馬達特性測試系統

單相馬達
三相馬達
exit結束

# 1

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

## 3

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


## aps 7100
### output
:OUTPut 0
:OUTPut 1

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


