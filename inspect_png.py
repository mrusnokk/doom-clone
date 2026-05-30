import sys
import struct

with open('E:/Michael/skola/cpp/projektFinal/build/assets/SPRITES/ENEMIES/Agaures/AGURA1C1.png', 'rb') as f:
    f.read(8) # png magic
    chunk_header = f.read(8)
    length, chunk_type = struct.unpack('>I4s', chunk_header)
    data = f.read(length)
    w, h, bit, color, comp, filter, interlace = struct.unpack('>IIBBBBB', data)
    print(f'Width: {w}, Height: {h}, BitDepth: {bit}, ColorType: {color}')
