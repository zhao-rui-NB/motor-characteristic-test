# %%
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np
# 手動用 pillow 繪製 Y 軸有 多種刻度標線的 曲線圖

# 每個 軸的滿刻度值
y_full_scales = [0.1,0.5,200,1000, 5000]
x_full_scales = [5000, 2000]


width = 1200
hight = 900

top_margin_ratio = 0.1
bottom_margin_ratio = 0.15
left_margin_ratio = 0.2
right_margin_ratio = 0.1

x_grid_count = 5
y_grid_count = 5

y_scale_count = 5
x_scale_count = 2
scale_box_width = 40
scale_box_height = 40


# scale_num_font = ImageFont.truetype("msjh.ttc", 24)
scale_num_font = ImageFont.truetype("font/SarasaMonoTC-Regular.ttf", 24)



plot_area_x_start = int(width * left_margin_ratio)
plot_area_x_end = int(width * (1 - right_margin_ratio))
plot_area_y_start = int(hight * top_margin_ratio)
plot_area_y_end = int(hight * (1 - bottom_margin_ratio))

plot_area_width = plot_area_x_end - plot_area_x_start
plot_area_height = plot_area_y_end - plot_area_y_start

x_scale_boxes = []
y_scale_boxes = []
for i in range(y_scale_count):
    xs = plot_area_x_start - scale_box_height * (i+1)
    ys = plot_area_y_start 
    xe = plot_area_x_start - scale_box_height * i
    ye = plot_area_y_end
    y_scale_boxes.append((xs, ys, xe, ye))
    
for i in range(x_scale_count):
    xs = plot_area_x_start
    ys = plot_area_y_end + scale_box_height * i
    xe = plot_area_x_end
    ye = plot_area_y_end + scale_box_height * (i + 1)
    x_scale_boxes.append((xs, ys, xe, ye))


def auto_calc_full_scale(max_value):
    """
    自动计算合适的刻度上限
    
    参数:
        max_value (float): 数据中的最大值
        
    返回:
        float: 合适的刻度上限 (1, 2或5的10的幂次方倍数)
    """
    if max_value <= 0:
        return 1.0  # 处理非正数情况
    
    # 特殊情况处理：非常小的数
    if max_value < 1e-100:
        return 1.0
        
    try:
        exponent = math.floor(math.log10(max_value))
        scale = 10 ** exponent
        base = [1, 2, 5, 10]  # 扩展基础选项
        
        # 找出第一个大于max_value的基准值
        for b in base:
            candidate = b * scale
            if max_value <= candidate * (1 + 1e-10):  # 添加容差避免浮点误差
                return candidate
                
        # 如果没有找到合适的基准值，跳到下一个数量级
        return 10 * scale
    except (ValueError, OverflowError):
        return max_value * 1.1  # 异常情况简单线性扩展

def format_number(num, max_digits=4):
    if abs(num - int(num)) < 1e-8:
        return str(int(num))
    else:
        return f"{num:.{max_digits}g}"

def draw_rotated_text_centered(base_img, box, text, font, angle=90, fill='black'):
    xs, ys, xe, ye = box
    center_x = (xs + xe) // 2
    center_y = (ys + ye) // 2

    # 建立暫時文字圖層（足夠大以防裁切）
    temp_img = Image.new('RGBA', (500, 200), (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp_img)

    # 取得文字大小
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # 計算畫在 temp_img 上的位置（先置中）
    text_x = (temp_img.width - text_width) // 2
    text_y = (temp_img.height - text_height) // 2
    temp_draw.text((text_x, text_y), text, font=font, fill=fill)

    # 旋轉文字圖層
    rotated = temp_img.rotate(angle, expand=1)

    # 計算貼回原圖的位置
    paste_x = center_x - rotated.width // 2
    paste_y = center_y - rotated.height // 2

    # 貼上透明圖層
    base_img.paste(rotated, (paste_x, paste_y), rotated)



# %%
image = Image.new('RGB', (width, hight), 'white')
draw = ImageDraw.Draw(image)

# 畫外框
draw.rectangle([plot_area_x_start, plot_area_y_start, plot_area_x_end, plot_area_y_end], outline="black", width=2)

# 畫 Y 軸格線（水平線）
for i in range(1, y_grid_count):
    y = plot_area_y_start + i * plot_area_height / y_grid_count
    draw.line([(plot_area_x_start, y), (plot_area_x_end, y)], fill='lightgray', width=1)

# 畫 X 軸格線（垂直線）
for i in range(1, x_grid_count):
    x = plot_area_x_start + i * plot_area_width / x_grid_count
    draw.line([(x, plot_area_y_start), (x, plot_area_y_end)], fill='lightgray', width=1)
    
# 畫刻度框
for i in x_scale_boxes:
    print(f'x_scale_boxes: {i}')
    draw.rectangle(i, outline="blue", width=3)
    
for i in y_scale_boxes:
    print(f'y_scale_boxes: {i}')
    draw.rectangle(i, outline="red", width=3)



y_tick_labels = []
for i, axis_scale in enumerate(y_full_scales):
    ticks = []
    scale_step = axis_scale / y_grid_count
    for j in range(y_grid_count):
        num = axis_scale - j * scale_step
        num_str = format_number(num)
        ticks.append(num_str)
    y_tick_labels.append(ticks)       
print (f'y_tick_labels: {y_tick_labels}')

x_tick_labels = []
for i, axis_scale in enumerate(x_full_scales):
    ticks = []
    scale_step = axis_scale / x_grid_count
    for j in range(x_grid_count):
        num = axis_scale - j * scale_step
        num_str = format_number(num)
        ticks.append(num_str)
    x_tick_labels.append(ticks)
print (f'x_tick_labels: {x_tick_labels}')


# 繪製 Y 軸刻度數字
for i, box in enumerate(y_scale_boxes):
    xs, ys, xe, ye = box
    for j in range(y_grid_count):
        x_center = int((xs + xe) // 2)
        y_center = int(ys + j* (ye - ys) / y_grid_count)

        num_str = y_tick_labels[i][j]
        draw_rotated_text_centered(image, [x_center,y_center]*2 , num_str, scale_num_font, angle=90, fill='black')
        
# 繪製 X 軸刻度數字
for i, box in enumerate(x_scale_boxes):
    xs, ys, xe, ye = box
    for j in range(x_grid_count):
        x_center = int(xe - j * (xe - xs) / x_grid_count)
        y_center = int((ys + ye) // 2)

        num_str = x_tick_labels[i][j]
        draw_rotated_text_centered(image, [x_center,y_center]*2 , num_str, scale_num_font, angle=0, fill='black')


y_scales_label = ['電流 (A )', '轉距 (Nm)', '效率 (% )', '入力 (W )', '出力 (W )']
x_scales_label = ['轉速(rpm)', '轉差率(%)']

# 繪製 Y 軸標籤
for i, box in enumerate(y_scale_boxes):
    xs, ys, xe, ye = box
    center_x = (xs + xe) // 2
    center_y = ye
    label = y_scales_label[i]
    draw_rotated_text_centered(image, [center_x,center_y]*2 , label, scale_num_font, angle=90, fill='black')
# 繪製 X 軸標籤
for i, box in enumerate(x_scale_boxes):
    xs, ys, xe, ye = box
    center_x = xs
    center_y = (ys + ye) // 2
    label = x_scales_label[i]
    # draw_rotated_text_centered(image, [center_x,center_y]*2 , label, scale_num_font, angle=0, fill='black')
    bbox = scale_num_font.getbbox(label)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    # 計算文字位置，使其y居中
    text_y = center_y - text_height // 2
    text_x = center_x
    
    draw.text((text_x,text_y), label, fill='black', font=scale_num_font)


def draw_curve(x_axis_index, y_axis_index, data):
    """
    绘制曲线
    :param x_axis_index: X轴索引
    :param y_axis_index: Y轴索引
    :param data: 数据列表，格式为 [(x1, y1), (x2, y2), ...]
    """
    if not data:
        return
    
    x_scale = x_full_scales[x_axis_index]
    y_scale = y_full_scales[y_axis_index]
    
    for i in range(len(data) - 1):
        x1, y1 = data[i]
        x2, y2 = data[i + 1]
        
        # 将数据转换为像素坐标
        x1_pixel = plot_area_x_start + (x1 / x_scale) * plot_area_width
        y1_pixel = plot_area_y_end - (y1 / y_scale) * plot_area_height
        x2_pixel = plot_area_x_start + (x2 / x_scale) * plot_area_width
        y2_pixel = plot_area_y_end - (y2 / y_scale) * plot_area_height
        
        draw.line([(x1_pixel, y1_pixel), (x2_pixel, y2_pixel)], fill='blue', width=2)
        
        
# 示例数据
# 生成並繪製幾組測試資料曲線
import random
# y_full_scales = [0.1,0.5,200,1000, 5000]
# sin wave data
curve1 = [(i, 0.05 * (math.sin(i / 500) + 1)) for i in range(0,5001,200)]

print(f'curve1: {curve1}')

draw_curve(0, 0, curve1)  # 電流
# draw_curve(0, 1, curve2)  # 效率
# draw_curve(0, 2, curve3)  # 出力
# draw_curve(0, 3, curve4)  # 轉距

# put label on the curve


image.show()




