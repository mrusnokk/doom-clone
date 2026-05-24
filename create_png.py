import sys
from PIL import Image

def generate_textures():
    # 1. Wall Texture (Bricks)
    img_wall = Image.new('RGB', (64, 64), color='darkred')
    pixels = img_wall.load()
    for y in range(64):
        for x in range(64):
            if x % 32 == 0 or y % 16 == 0:
                pixels[x, y] = (150, 0, 0)
            elif x % 32 == 16 and y % 32 >= 16:
                pixels[x, y] = (150, 0, 0)
    img_wall.save('wall.png')

    # 2. Floor Texture (Tiles)
    img_floor = Image.new('RGB', (64, 64), color='gray')
    pixels = img_floor.load()
    for y in range(64):
        for x in range(64):
            if (x // 16 + y // 16) % 2 == 0:
                pixels[x, y] = (100, 100, 100)
            else:
                pixels[x, y] = (150, 150, 150)
    img_floor.save('floor.png')

    # 3. Ceiling Texture (Sky/Clouds)
    img_ceil = Image.new('RGB', (64, 64), color='skyblue')
    pixels = img_ceil.load()
    for y in range(64):
        for x in range(64):
            if (x * y) % 50 < 20:
                pixels[x, y] = (180, 220, 255)
    img_ceil.save('ceil.png')

    # 4. Enemy Sprite (Green Slime)
    img_enemy = Image.new('RGBA', (64, 64), color=(0,0,0,0))
    pixels = img_enemy.load()
    for y in range(64):
        for x in range(64):
            dx = x - 32
            dy = y - 32
            if dx*dx + dy*dy < 25*25:
                if dy < 0 and abs(dx) > 10 and abs(dx) < 20:
                    pixels[x, y] = (255, 0, 0, 255) # Oči
                else:
                    pixels[x, y] = (0, 200, 50, 255) # Tělo
    img_enemy.save('enemy.png')

generate_textures()
