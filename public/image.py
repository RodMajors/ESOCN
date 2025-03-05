from PIL import Image
import os

input_dir = 'E:/projects/ESOCN/public/esoui/art/icons'
output_dir = 'E:/projects/ESOCN/public/esoui/art/outputs'

for filename in os.listdir(input_dir):
    if filename.endswith('.png'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace('.png', '.webp'))
        
        with Image.open(input_path) as img:
            img.save(output_path, 'WEBP')