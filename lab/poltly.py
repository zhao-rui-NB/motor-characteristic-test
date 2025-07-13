from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 1. 创建画布
width, height = 1400, 900
img = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(img)

# 2. 加载字体（如果系统有Arial字体，否则使用默认字体）
try:
    font = ImageFont.truetype("arial.ttf", 12)
    font_large = ImageFont.truetype("arial.ttf", 24)
except:
    # 如果找不到字体，使用默认字体
    font = ImageFont.load_default()
    font_large = ImageFont.load_default()

# 3. 定义绘图区域
margin = {'left': 120, 'right': 100, 'top': 80, 'bottom': 100}
plot_width = width - margin['left'] - margin['right']
plot_height = height - margin['top'] - margin['bottom']

# 4. 定义四个Y轴的尺度转换函数
def create_scaler(min_val, max_val):
    """创建尺度转换函数"""
    def scaler(value):
        return margin['top'] + plot_height * (1 - (value - min_val) / (max_val - min_val))
    return scaler

# 四个尺度定义 (最小值, 最大值, 颜色)
scales = [
    {'min': 0, 'max': 100, 'color': 'blue', 'ticks': 5, 'format': '{:.0f}'},    # 线性尺度
    {'min': 1, 'max': 1000, 'color': 'green', 'ticks': 5, 'format': '{:.0f}'}, # 对数尺度
    {'min': -50, 'max': 50, 'color': 'red', 'ticks': 5, 'format': '{:.0f}'},   # 自定义尺度
    {'min': 0, 'max': 4, 'color': 'purple', 'ticks': 5, 'format': '{:.0f}'}    # 离散尺度
]

# 初始化尺度转换函数
for scale in scales:
    scale['scaler'] = create_scaler(scale['min'], scale['max'])

# 5. 生成示例数据
x_values = np.linspace(0, plot_width, 411)
data = [
    50 + 40 * np.sin(x_values/50),                   # 尺度1数据
    10 ** (1 + 2 * np.sin(x_values/70)),             # 尺度2数据
    40 * np.cos(x_values/30) - 10,                   # 尺度3数据
    np.floor(2 + 2 * np.sin(x_values/20))            # 尺度4数据
]

# 6. 绘制共享网格系统
def calculate_ticks(min_val, max_val, num_ticks):
    """计算均匀分布的刻度值"""
    step = (max_val - min_val) / (num_ticks - 1)
    return [min_val + i * step for i in range(num_ticks)]

# 使用尺度1作为网格基准
grid_ticks = calculate_ticks(scales[0]['min'], scales[0]['max'], 5)

# 绘制水平网格线
for tick in grid_ticks:
    y_pixel = scales[0]['scaler'](tick)
    draw.line([(margin['left'], y_pixel), (width - margin['right'], y_pixel)], 
             fill='lightgray', width=1)
    
    # 添加网格标签 (左侧)
    label = scales[0]['format'].format(tick)
    bbox = draw.textbbox((0, 0), label, font=font)
    draw.text((margin['left'] - 50, y_pixel - bbox[3]//2), 
             label, fill='black', font=font)

# 绘制垂直网格线 (每50像素)
for x in range(0, 411, 50):
    x_pixel = margin['left'] + (x/410) * plot_width
    draw.line([(x_pixel, margin['top']), (x_pixel, height - margin['bottom'])], 
             fill='lightgray', width=1)
    
    # 添加X轴标签
    label = str(x)
    bbox = draw.textbbox((0, 0), label, font=font)
    draw.text((x_pixel - bbox[2]//2, height - margin['bottom'] + 10), 
             label, fill='black', font=font)

# 7. 绘制坐标轴
# X轴
draw.line([(margin['left'], height - margin['bottom']), 
          (width - margin['right'], height - margin['bottom'])], fill='black', width=2)

# Y轴 (四个)
y_axis_positions = [margin['left'] + i*40 for i in range(4)]
for pos, scale in zip(y_axis_positions, scales):
    # 绘制轴线
    draw.line([(pos, margin['top']), (pos, height - margin['bottom'])], 
             fill=scale['color'], width=2)
    
    # 计算该尺度的刻度位置
    ticks = calculate_ticks(scale['min'], scale['max'], scale['ticks'])
    
    # 绘制刻度线
    for tick in ticks:
        y_pixel = scale['scaler'](tick)
        draw.line([(pos - 5, y_pixel), (pos, y_pixel)], 
                 fill=scale['color'], width=2)
        
        # 添加刻度标签 (右侧)
        label = scale['format'].format(tick)
        bbox = draw.textbbox((0, 0), label, font=font)
        draw.text((pos + 10, y_pixel - bbox[3]//2), 
                 label, fill=scale['color'], font=font)

# 8. 绘制数据曲线
for i, (scale, values) in enumerate(zip(scales, data)):
    points = []
    for x, y in zip(x_values, values):
        x_pixel = margin['left'] + (x/plot_width) * plot_width
        y_pixel = scale['scaler'](y)
        points.append((x_pixel, y_pixel))
    
    # 绘制曲线
    for j in range(len(points) - 1):
        draw.line([points[j], points[j+1]], fill=scale['color'], width=3)
    
    # 添加数据点标记 (每20个点)
    for j in range(0, len(points), 20):
        x, y = points[j]
        draw.ellipse([(x-4, y-4), (x+4, y+4)], 
                    fill=scale['color'], outline='white')

# 9. 添加图例和标题
draw.text((width//2 - 100, 30), "四尺度共享网格图表", 
          fill='black', font=font_large)

legend_items = [(f"尺度 {i+1}", scale['color']) for i, scale in enumerate(scales)]
for i, (text, color) in enumerate(legend_items):
    # 图例颜色块
    draw.rectangle([width - 180, 80 + i*40, width - 160, 100 + i*40], 
                  fill=color, outline='black')
    # 图例文本
    draw.text((width - 150, 80 + i*40), text, fill='black', font=font)

# 保存图像
img.save('multi_scale_grid_plot.png')
img.show()