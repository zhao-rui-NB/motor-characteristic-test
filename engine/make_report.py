import os
import csv
import shutil
import time
from openpyxl import load_workbook

from engine.Motor import Motor
from engine.MultiScalePlotter import MultiScalePlotter


def make_report_a(motor: Motor, input_dir, output_path: str):
    template_path = 'report_template\電動機特性計算表a_20250702.xlsx'
    
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy(template_path, output_path)
    
    wb = load_workbook(output_path)  # 載入 Excel
    ws = wb.active                   # 使用第一個工作表
    
    ws['C4'] = motor.information_dict.get("試驗日期", "試驗日期")
    ws['I4'] = motor.information_dict.get("印表日期", "印表日期")
    ws['C5'] = motor.information_dict.get("電腦編號", "電腦編號")
    ws['F5'] = motor.information_dict.get("序號" , "序號")
    ws['I5'] = motor.information_dict.get("型式" , "型式")
    ws['C6'] = motor.information_dict.get("工作單號" , "工作單號")
    ws['F6'] = motor.information_dict.get("製造號碼" , "製造號碼")
    ws['I6'] = motor.information_dict.get("廠牌" , "廠牌")
    
    ws['C7'] = motor.rated_voltage
    ws['F7'] = motor.rated_current
    ws['H7'] = motor.horsepower
    ws['K7'] = motor.no_load_current
    
    ws['C8'] = motor.power_phases
    ws['F8'] = motor.frequency
    ws['H8'] = motor.poles
    ws['K8'] = motor.information_dict.get("溫升" , "溫升")
    
    ws['C9'] = motor.speed
    ws['K9'] = motor.information_dict.get("絕緣種類" , "絕緣種類")
    
    ws['C10'] = motor.information_dict.get("定子規格" , "定子規格")
    ws['C11'] = motor.information_dict.get("轉子規格" , "轉子規格")
    
    ws['C12'] = motor.information_dict.get("本線" , "本線")
    ws['H12'] = motor.information_dict.get("啟動線" , "啟動線")

    ws['C13'] = motor.information_dict.get("備註" , "備註")
    
    
    # ####################### data table #######################
    load_report_csv = os.path.join(input_dir, 'load_report.csv')
    if not os.path.exists(load_report_csv):
        print(f"[make_report_a] Load report CSV file not found: {load_report_csv}")
    
    with open(load_report_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers_en = next(reader)
        headers_ch = next(reader)
        # print(f"headers_en: {headers_en}")
        # print(f"headers_ch: {headers_ch}")
        
        # each row last is the V header
        v_header = []
        csv_data = []
        for row in reader:
            v_header.append(row[-1].strip())
            csv_data.append(list(map(float, row[:-1])))
            
        # print("v_header:", v_header)
        # print("csv_data:", csv_data) 

    # b18
    table_start_row = 18
    table_start_col = 2 
    
    excel_h_header = ['voltage','current', 'pf', 'speed', 'slip', 'torque', 'power', 'pout', 'eff' ]
    excel_v_header = ['no_load', '25%', '50%', '75%', '100%', '125%', '150%', 'po_max', 'start', 'tq_max']
    
    # try to match the header_en with the csv data
    for c, hd1 in enumerate(headers_en):
        for r, hd2 in enumerate(v_header):
            # find hd1 in excel_h_header
            if hd1 in excel_h_header and hd2 in excel_v_header:
                # find the index of hd1 in excel_h_header
                h_index = excel_h_header.index(hd1)
                v_index = excel_v_header.index(hd2)
                
                cell = ws.cell(row=table_start_row + v_index, column=table_start_col + h_index)
                cell.value = csv_data[r][c]
    
    # save the workbook
    wb.save(output_path)
    wb.close()
    print(f"[make_report_a] Report saved to {output_path}")
    
    
    
def make_report_b(motor: Motor, input_dir, output_path: str):
    template_path = 'report_template\電動機特性計算表b_20250702.xlsx'
    
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy(template_path, output_path)
    
    wb = load_workbook(output_path)  # 載入 Excel
    ws = wb.active                   # 使用第一個工作表
    
    ws['C4'] = motor.information_dict.get("試驗日期", "試驗日期")
    ws['I4'] = motor.information_dict.get("印表日期", "印表日期")
    ws['C5'] = motor.information_dict.get("電腦編號", "電腦編號")
    ws['F5'] = motor.information_dict.get("序號" , "序號")
    ws['I5'] = motor.information_dict.get("型式" , "型式")
    ws['C6'] = motor.information_dict.get("工作單號" , "工作單號")
    ws['F6'] = motor.information_dict.get("製造號碼" , "製造號碼")
    ws['I6'] = motor.information_dict.get("廠牌" , "廠牌")
    
    ws['C7'] = motor.rated_voltage
    ws['F7'] = motor.rated_current
    ws['H7'] = motor.horsepower
    ws['K7'] = motor.no_load_current
    
    ws['C8'] = motor.power_phases
    ws['F8'] = motor.frequency
    ws['H8'] = motor.poles
    ws['K8'] = motor.information_dict.get("溫升" , "溫升")
    
    ws['C9'] = motor.speed
    ws['K9'] = motor.information_dict.get("絕緣種類" , "絕緣種類")
    
    ws['C10'] = motor.information_dict.get("定子規格" , "定子規格")
    ws['C11'] = motor.information_dict.get("轉子規格" , "轉子規格")
    
    ws['C12'] = motor.information_dict.get("本線" , "本線")
    ws['H12'] = motor.information_dict.get("啟動線" , "啟動線")

    ws['C13'] = motor.information_dict.get("備註" , "備註")


    img_save_path = f'./.output/{time.time()}.png'
    os.makedirs(os.path.dirname(img_save_path), exist_ok=True)
    
    cvt_csv_loadsort = f'{input_dir}/loadsort.csv'
    polt_motor_characteristic_fig(motor, cvt_csv_loadsort, img_save_path)
    
    if os.path.exists(img_save_path):
        from openpyxl.drawing.image import Image
        img = Image(img_save_path)
        resize_ratio = 0.53
        img.width = int(img.width * resize_ratio)
        img.height = int(img.height * resize_ratio)
        img.anchor = 'A16'
        
        ws.add_image(img)
    else:
        print(f"[make_report_b] Image file not found: {img_save_path}")

    # save the workbook
    wb.save(output_path)
    wb.close()
    print(f"[make_report_b] Report saved to {output_path}")

def make_report_cns(motor: Motor, input_dir, output_path: str):
    template_path = 'report_template\電動機特性計算表_cns_20250701.xlsx'
    
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy(template_path, output_path)
    
    wb = load_workbook(output_path)  # 載入 Excel
    ws = wb.active                   # 使用第一個工作表
    
    ws['C4'] = "輸出功率"
    ws['E4'] = motor.horsepower
    ws['H4'] = motor.frequency
    
    ws['C5'] = motor.poles
    ws['H5'] = motor.speed
    ws['C6'] = motor.rated_voltage
    ws['H6'] = "周圍溫度"

    # save the workbook
    wb.save(output_path)
    wb.close()
    print(f"[make_report_cns] Report saved to {output_path}")


def polt_motor_characteristic_fig(motor: Motor, input_dir, output_path: str):
    """
    Generate a motor characteristic plot and save it to the specified output 
    inupt directory : need a csv file, loadsort.csv
    """
    with open(input_dir, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers_en = next(reader)
        headers_ch = next(reader)
        # print(f"headers_en: {headers_en}")
        # print(f"headers_ch: {headers_ch}")
        
        csv_data = []
        for row in reader:
            csv_data.append(list(map(float, row)))
            
    plotter = MultiScalePlotter(x_grid_count=5 , y_grid_count=5)
    y_colors = ['red', 'orange', 'green', 'blue', 'purple']
    
    curve_colors = [
        (214, 39, 40),    # 紅
        (255, 127, 14),   # 橘
        (204, 153, 0),    # 暗金黃（黃但不亮）
        (44, 160, 44),    # 綠
        (31, 119, 180)    # 藍
    ]
    y_colors = curve_colors
    plotter.set_x_axis(['轉速(rpm)', '轉差率(%)'])
    # plotter.set_x_axis(['轉速(rpm)'])
    plotter.set_y_axis(['電流 (A )', '轉距 (Nm)', '效率 (% )', '入力 (W )', '出力 (W )'], colors=y_colors)
    
    speed = [row[headers_en.index('speed')] for row in csv_data]
    current = [row[headers_en.index('current')] for row in csv_data]
    torque = [row[headers_en.index('torque')] for row in csv_data]
    eff = [row[headers_en.index('eff')] for row in csv_data]
    power = [row[headers_en.index('power')] for row in csv_data]
    pout = [row[headers_en.index('pout')] for row in csv_data]
    
    plotter.set_curve_data(0, 0, list(zip(speed, current)))
    plotter.set_curve_data(0, 1, list(zip(speed, torque)))
    plotter.set_curve_data(0, 2, list(zip(speed, eff)))
    plotter.set_curve_data(0, 3, list(zip(speed, power)))
    plotter.set_curve_data(0, 4, list(zip(speed, pout)))
    
    # plotter.polt()

    plotter._auto_calculate_all_scales()
    plotter._draw_base()
    plotter._make_tick_labels()

    # plotter.x_tick_labels[1] = ['0.0', '0.2', '0.4', '-0.6', '0.8'] 
    
    # calc the 轉差率
    # (同步轉速 - 轉速) / 同步轉速
    for i in range(len(plotter.x_tick_labels[0])):
        spd = float(plotter.x_tick_labels[0][i])
        if spd != 0:
            slip = (motor.speed - spd) / motor.speed
            plotter.x_tick_labels[1][i] = f"{slip:.2f}"
    
    plotter._draw_ticks()
    plotter._draw_axis_name()
    for y_index, y_name in enumerate(plotter.y_axis_names):
        for x_index, x_name in enumerate(plotter.x_axis_names):
            if plotter.curve_datas[y_index][x_index] is not None:
                color = plotter.y_axis_colors[y_index] if plotter.y_axis_colors else 'black'
                plotter._draw_curve(x_index, y_index, plotter.curve_datas[y_index][x_index], color=color, width=5)

    plotter.save(output_path)
    print(f"[polt_motor_characteristic_fig] Plot saved to {output_path}")


if __name__ == '__main__':
    import json
    file_path = 'test_file\project_file\T123_20250207_223915_hand_merge_cns.motor.json'
    with open(file_path, 'r', encoding='UTF8') as f:
        data = json.load(f)
    
    # Example usage
    motor = Motor()
    motor.from_dict(data)   
    
    input_dir = 'test_file/CSV/cvt'
    output_path = 'test_file/gen/電動機特性計算表a.xlsx'
    make_report_a(motor, input_dir, output_path)
    
    output_path = 'test_file/gen/電動機特性計算表b.xlsx'
    make_report_b(motor, input_dir, output_path)
    
    output_path = 'test_file/gen/電動機特性計算表cns.xlsx'
    make_report_cns(motor, None, output_path)
    
    