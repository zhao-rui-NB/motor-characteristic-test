from PIL import Image, ImageDraw, ImageFont
import math
import random

class MultiScalePlotter:
    def __init__(self,
                 width=1200,
                 height=900,
                 x_grid_count=5,
                 y_grid_count=5,
                 font_path="font/SarasaMonoTC-Regular.ttf",
                 font_size=24):

        self.width = width
        self.height = height
        self.x_grid_count = x_grid_count
        self.y_grid_count = y_grid_count

        self.scale_box_width = 40
        self.scale_box_height = 40

        self.left_margin_ratio = 0.2
        self.right_margin_ratio = 0.1
        self.top_margin_ratio = 0.1
        self.bottom_margin_ratio = 0.15

        self.plot_area_x_start = int(self.width * self.left_margin_ratio)
        self.plot_area_x_end = int(self.width * (1 - self.right_margin_ratio))
        self.plot_area_y_start = int(self.height * self.top_margin_ratio)
        self.plot_area_y_end = int(self.height * (1 - self.bottom_margin_ratio))

        self.plot_area_width = self.plot_area_x_end - self.plot_area_x_start
        self.plot_area_height = self.plot_area_y_end - self.plot_area_y_start

        self.image = Image.new('RGB', (self.width, self.height), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(font_path, font_size)

        self.x_axis_names = []
        self.y_axis_names = []
        self.y_axis_colors = []
        
        self.x_axis_scales = []
        self.y_axis_scales = []

        self.x_tick_labels = []
        self.y_tick_labels = []

        self.x_scale_boxes = []
        self.y_scale_boxes = []
        
        # [y axis index][x axis index] = [(x,y), (), ...]
        self.curve_datas = []

    
    def _draw_rotated_text_centered(self, box, text, angle=90, color='black'):
        center_x, center_y = box[0], box[1]
        temp_img = Image.new('RGBA', (500, 200), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = self.font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (temp_img.width - text_width) // 2
        text_y = (temp_img.height - text_height) // 2
        temp_draw.text((text_x, text_y), text, font=self.font, fill=color)
        rotated = temp_img.rotate(angle, expand=1)
        paste_x = center_x - rotated.width // 2
        paste_y = center_y - rotated.height // 2
        self.image.paste(rotated, (paste_x, paste_y), rotated)

    def _format_number(self, num, max_digits=4):
        return str(int(num)) if abs(num - int(num)) < 1e-8 else f"{num:.{max_digits}g}"

    def _auto_calc_full_scale(self, max_value):
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

    def _draw_base(self):
        # 畫主框與格線
        self.draw.rectangle([self.plot_area_x_start, self.plot_area_y_start, self.plot_area_x_end, self.plot_area_y_end], outline="black", width=2)

        for i in range(1, self.y_grid_count):
            y = self.plot_area_y_start + i * self.plot_area_height / self.y_grid_count
            self.draw.line([(self.plot_area_x_start, y), (self.plot_area_x_end, y)], fill='lightgray', width=1)

        for i in range(1, self.x_grid_count):
            x = self.plot_area_x_start + i * self.plot_area_width / self.x_grid_count
            self.draw.line([(x, self.plot_area_y_start), (x, self.plot_area_y_end)], fill='lightgray', width=1)

    def _make_tick_labels(self):
        self.y_tick_labels = []
        for i, axis_scale in enumerate(self.y_axis_scales):
            ticks = []
            scale_step = axis_scale / self.y_grid_count
            for j in range(self.y_grid_count):
                num = axis_scale - j * scale_step
                num_str = self._format_number(num)
                ticks.append(num_str)
            self.y_tick_labels.append(ticks)       
        
        self.x_tick_labels = []
        for i, axis_scale in enumerate(self.x_axis_scales):
            ticks = []
            scale_step = axis_scale / self.x_grid_count
            for j in range(self.x_grid_count):
                num = axis_scale - j * scale_step
                num_str = self._format_number(num)
                ticks.append(num_str)
            self.x_tick_labels.append(ticks)
            
        # print(f'y_tick_labels: {self.y_tick_labels}')
        # print(f'x_tick_labels: {self.x_tick_labels}')
        
    def _draw_ticks(self):
        # 繪製 Y 軸刻度數字
        for i, labels in enumerate(self.y_tick_labels):
            xs, ys, xe, ye = self.get_scale_boxes(axis='y', index=i)
            for j, lb in enumerate(labels):
                x_center = int((xs + xe) // 2)
                y_center = int(ys + j* (ye - ys) / self.y_grid_count)

                num_str = lb
                color = self.y_axis_colors[i] if self.y_axis_colors else 'black'
                self._draw_rotated_text_centered([x_center,y_center]*2 , num_str, angle=90, color=color)
                
        # 繪製 X 軸刻度數字
        for i, labels in enumerate(self.x_tick_labels):
            xs, ys, xe, ye = self.get_scale_boxes(axis='x', index=i)
            for j, lb in enumerate(labels):
                x_center = int(xe - j * (xe - xs) / self.x_grid_count)
                y_center = int((ys + ye) // 2)

                num_str = lb
                self._draw_rotated_text_centered([x_center,y_center]*2 , num_str, angle=0, color='black')

    def _draw_axis_name(self):
        for i, name in enumerate(self.y_axis_names):
            xs, ys, xe, ye = self.get_scale_boxes(axis='y', index=i)
            center_x = (xs + xe) // 2
            center_y = ye
            label = name
            color = self.y_axis_colors[i] if self.y_axis_colors else 'black'
            self._draw_rotated_text_centered([center_x,center_y]*2, label, angle=90, color=color)
            
        for i, name in enumerate(self.x_axis_names):
            xs, ys, xe, ye = self.get_scale_boxes(axis='x', index=i)
            center_x = xs
            center_y = (ys + ye) // 2
            label = name
            bbox = self.font.getbbox(label)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            # 計算文字位置，使其y居中, x軸文字在左側
            text_y = center_y - text_height // 2
            text_x = center_x
            self.draw.text((text_x, text_y), label, fill='black', font=self.font)

    def _draw_curve(self, x_axis_index, y_axis_index, data, color='blue', width=2):
        if not self.x_axis_scales or not self.y_axis_scales:
            raise ValueError("Please set x_axis_scales and y_axis_scales before drawing curves.")
        
        x_scale = self.x_axis_scales[x_axis_index]
        y_scale = self.y_axis_scales[y_axis_index]
        
        for i in range(len(data) - 1):
            x1, y1 = data[i]
            x2, y2 = data[i + 1]
            x1_pixel = self.plot_area_x_start + (x1 / x_scale) * self.plot_area_width
            y1_pixel = self.plot_area_y_end - (y1 / y_scale) * self.plot_area_height
            x2_pixel = self.plot_area_x_start + (x2 / x_scale) * self.plot_area_width
            y2_pixel = self.plot_area_y_end - (y2 / y_scale) * self.plot_area_height
            self.draw.line([(x1_pixel, y1_pixel), (x2_pixel, y2_pixel)], fill=color, width=width)

    def _auto_calculate_all_scales(self):
        # calc y axis scales
        for y_index in range(len(self.y_axis_names)):
            all_values = []
            for x_index in range(len(self.x_axis_names)):
                if self.curve_datas[y_index][x_index] is not None:
                    all_values.extend([y for x, y in self.curve_datas[y_index][x_index]])
            if all_values:
                max_value = max(all_values)
                self.y_axis_scales[y_index] = self._auto_calc_full_scale(max_value)
        
        # calc x axis scales
        for x_index in range(len(self.x_axis_names)):
            all_values = []
            for y_index in range(len(self.y_axis_names)):
                if self.curve_datas[y_index][x_index] is not None:
                    all_values.extend([x for x, y in self.curve_datas[y_index][x_index]])
            if all_values:
                max_value = max(all_values)
                self.x_axis_scales[x_index] = self._auto_calc_full_scale(max_value)
                
                

    def get_scale_boxes(self, axis='x', index=0):
        if axis == 'x':
            xs = self.plot_area_x_start
            xe = self.plot_area_x_end
            ys = self.plot_area_y_end + self.scale_box_height * index
            ye = self.plot_area_y_end + self.scale_box_height * (index + 1)
            return (xs, ys, xe, ye)
        elif axis == 'y':
            xs = self.plot_area_x_start - self.scale_box_height * (index+1)
            xe = self.plot_area_x_start - self.scale_box_height * index
            ys = self.plot_area_y_start
            ye = self.plot_area_y_end
            return (xs, ys, xe, ye)
        else:
            raise ValueError("Axis must be 'x' or 'y'")

    def set_x_axis(self, names):
        self.x_axis_names = names
        self.x_axis_scales = [1]*len(names)  # 默认每个轴的比例为1
        # updata the curves data 2D structure
        self.curve_datas = [[None for _ in range(len(self.x_axis_names))] for _ in range(len(self.y_axis_names))]
    
    def set_y_axis(self, name, colors=None):
        self.y_axis_names = name
        self.y_axis_scales = [1]*len(name)
        # updata the curves data 2D structure
        self.curve_datas = [[None for _ in range(len(self.x_axis_names))] for _ in range(len(self.y_axis_names))]
    
        if colors is not None:
            if len(colors) != len(name):
                raise ValueError("Colors list length must match the number of y axes.")
            self.y_axis_colors = colors
    
    def set_curve_data(self, x_axis_index, y_axis_index, data):
        if not (0 <= x_axis_index < len(self.x_axis_names)) or not (0 <= y_axis_index < len(self.y_axis_names)):
            raise IndexError("x_axis_index or y_axis_index out of range.")
        
        if self.curve_datas[y_axis_index][x_axis_index] is None:
            self.curve_datas[y_axis_index][x_axis_index] = []
        
        self.curve_datas[y_axis_index][x_axis_index].extend(data)
    
    def polt(self):
        self._auto_calculate_all_scales()
        self._draw_base()
        self._make_tick_labels()
        self._draw_ticks()
        self._draw_axis_name()
        for y_index, y_name in enumerate(self.y_axis_names):
            for x_index, x_name in enumerate(self.x_axis_names):
                if self.curve_datas[y_index][x_index] is not None:
                    color = self.y_axis_colors[y_index] if self.y_axis_colors else 'black'
                    self._draw_curve(x_index, y_index, self.curve_datas[y_index][x_index], color=color, width=5)
    
    def show(self):
        self.image.show()

    def save(self, path):
        self.image.save(path)



if __name__ == '__main__':

    # test 1

    def test1():
        plotter = MultiScalePlotter(x_grid_count=5 , y_grid_count=5)
        plotter.set_x_axis(['轉速(rpm)', '轉差率(%)'])
        plotter.set_y_axis(['電流 (A )', '轉距 (Nm)', '效率 (% )', '入力 (W )', '出力 (W )'])
        plotter.set_curve_data(0, 0, [(i, random.uniform(0, 100)) for i in range(0, 450)])
        plotter.polt()
        plotter.show()
        # plotter.save('multi_scale_plot.png')
    
    # test 2 from csv
    import csv
    file_path = 'test_file\CSV\cvt\loadsort.csv'
    # read the csv file
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers_en = next(reader)
        headers_ch = next(reader)
        print(f"headers_en: {headers_en}")
        print(f"headers_ch: {headers_ch}")
        
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

    plotter.x_tick_labels[1] = ['0.0', '0.2', '0.4', '-0.6', '0.8'] 
    plotter._draw_ticks()
    plotter._draw_axis_name()
    for y_index, y_name in enumerate(plotter.y_axis_names):
        for x_index, x_name in enumerate(plotter.x_axis_names):
            if plotter.curve_datas[y_index][x_index] is not None:
                color = plotter.y_axis_colors[y_index] if plotter.y_axis_colors else 'black'
                plotter._draw_curve(x_index, y_index, plotter.curve_datas[y_index][x_index], color=color, width=5)

    plotter.show()
    
    
    
    