#将目标文件夹下的所有dds图标转化为webp格式
from PIL import Image
import os

input_dir = 'C:/projects/ESOCN/public/esoui/art/icon/class/gamepad'
output_dir = 'C:/projects/ESOCN/public/esoui/art/icon/class/gamepad'

for filename in os.listdir(input_dir):
    if filename.endswith('.dds'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.dds', '.webp'))
        
        with Image.open(input_path) as img:
            img.save(output_path, 'WEBP')