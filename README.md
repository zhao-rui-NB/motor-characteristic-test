# motor-characteristic-test

## install
```

```

## run

ui
```
python -m gui.main
python main.py
```

## 打包
```
pyinstaller --onefile main.py
```

### 測試工具
模擬多 modbus数码管显示屏
```
python test_tool/SegmentDisplaySimulator.py
```

模擬 socket power supply
```
python test_tool/PowerSupplySimulator.py
```

```
& "C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" test_file/gen/電動機特性計算表b.xlsx
```

## 自動測試選項 測試項目功能說明表

# 馬達測試項目與動作說明表

| 測試名稱               | 方法名稱                             | 適用馬達 | 實際動作說明 |
|------------------------|--------------------------------------|----------|---------------|
| 直流電阻測試           | `run_dc_resistance_test`            | 單相、三相 | 使用低電壓直流注入各繞組，量測電壓與電流以計算電阻，測試時馬達靜止、軸不轉。測試冷、熱兩次以比對溫升情況。 |
| 空載測試               | `run_open_circuit_test`             | 三相     | 啟動馬達後逐漸升壓至額定，無負載運轉一段時間，量測空載電流與功率，判斷鐵損與空轉特性。 |
| 堵轉測試               | `run_lock_rotor_test`               | 三相     | 機械軸固定不轉（施加最大剎車力），從低壓開始慢慢升壓，直到馬達電流達到額定，觀察啟動初期的最大電流與力矩。 |
| 三相啟動轉矩測試       | `run_three_phase_starting_torque_test` | 三相 | 馬達起始靜止，逐步升壓，記錄啟動過程中電流、轉速、啟動扭力變化，觀察起動性能。 |
| 單相啟動轉矩測試       | `run_singel_phase_starting_torque_test` | 單相 | 同上，針對單相馬達操作，測試起動期間的扭力與電流表現。 |
| 負載測試               | `run_load_test`                     | 單相、三相 | 馬達帶動煞車系統，逐漸增加負載（剎車電流）直到達到馬達額定馬力或堵轉為止，觀察在不同負載下的效率與熱特性。 |
| 鐵損分離測試           | `run_separate_excitation_test`      | 三相     | 馬達無機械連結（脫離負載），從低電壓慢慢升壓至120%，觀察電流變化與鐵損行為，不施加負載扭矩。 |
| 頻率飄移測試           | `run_frequency_drift_test`          | 單相、三相 | 馬達在負載下運轉（達到額定馬力），逐步改變輸入頻率（±5%），觀察轉速、功率與效率變化，檢測異常響應。 |
| CNS14400 測試          | `run_CNS14400_test`                 | 單相、三相 | 馬達在多種負載比例（如 25%、50%、75%、100%）下長時間運轉，每段運轉後進行熱電阻測試以比對溫升特性，模擬實際使用壽命與負載情境。 |


# 報告

## 外部轉檔工具
必須要匯出: `load_report_x.csv`, `loadsort_x.csv`, `load_x.csv`, `cns14400_report.csv` 後續才能產生excel report
```
convert.exe D:/three_phase/T123/20250519_172601 3 123479abcdeftq
```

## 報表製作依賴關係
[範例CSV](test_file/CSV/2025_0730)

| 報表種類  | 依賴關係 |
|----------|----------|
| a        | load_report_x |
| b1       | loadsort_x, load_x |
| cns      | cns14400_report |