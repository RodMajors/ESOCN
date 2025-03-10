from PIL import Image
import os

input_dir = 'E:/projects/ESOCN/public/LuiExtended/media/icons/abilities'
output_dir = 'E:/projects/ESOCN/public/LuiExtended/media/icons/output'

for filename in os.listdir(input_dir):
    if filename.endswith('.dds'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.dds', '.webp'))
        
        with Image.open(input_path) as img:
            img.save(output_path, 'WEBP')