import sys
from PIL import Image

img = Image.open('E:/Michael/skola/cpp/projektFinal/build/assets/SPRITES/WEAPONS/DUA9A0.png').convert('RGBA')
pixels = img.load()
width, height = img.size
opaque = 0
cyan = 0
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if a > 0:
            opaque += 1
        if r == 0 and g == 255 and b == 255:
            cyan += 1

print(f'Width: {width}, Height: {height}')
print(f'Opaque pixels: {opaque} / {width * height}')
print(f'Cyan pixels: {cyan}')
