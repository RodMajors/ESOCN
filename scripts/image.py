from PIL import Image
import os

input_dir = 'E:/esoui/esoui/art/icons'
output_dir = 'E:/esoui/esoui/art/icon'

for filename in os.listdir(input_dir):
    if filename.endswith('.dds'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.dds', '.webp'))
        
        with Image.open(input_path) as img:
            img.save(output_path, 'WEBP')