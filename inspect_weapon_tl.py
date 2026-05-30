import sys
from PIL import Image
import glob

files = sorted(glob.glob('E:/Michael/skola/cpp/projektFinal/build/assets/SPRITES/WEAPONS/DUA9*.png'))
for f in files:
    img = Image.open(f).convert('RGBA')
    print(f"{f.split('/')[-1]}: {img.load()[0, 0]}")
