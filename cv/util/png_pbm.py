'''
Credits to:
https://stackoverflow.com/questions/71246299/image-conversion-from-png-to-pbm-solely-1s-and-0s-using-pil
'''

from pathlib import Path
from PIL import Image

# flip 1 and 0 to comply with cat.pbm/teapot.pbm 
bits = '1', '0'                 # orig: '0', '1'
path = Path('./in/seahorse.png')

img = Image.open(path).convert('1') 
width, height = img.size

data = [bits[bool(val)] for val in img.getdata()]
data = [data[offset: offset+width] for offset in range(0, width*height, width)]

with open(f'{path.stem}.pbm', 'w') as file:
    file.write('P1\n')
    file.write(f'# Conversion of {path} to PBM format\n')
    file.write(f'{width} {height}\n')
    for row in data:
        file.write(' '.join(row) + '\n')
