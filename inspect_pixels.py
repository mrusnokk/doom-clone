import sys
from PIL import Image

img = Image.open('E:/Michael/skola/cpp/projektFinal/build/assets/SPRITES/ENEMIES/Agaures/AGURA1C1.png').convert('RGBA')
pixels = img.load()
width, height = img.size
opaque = 0
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if a > 0:
            opaque += 1

print(f'Opaque pixels: {opaque} / {width * height}')
