import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

sprites_new = '''    sprites = {
        // x, y, type, hp, state, animTimer, frameIndex, spawnX, spawnY
        // typ = 0 (Agaures)
        {5.5, 5.5, 0, 100, 1, 0.0, 0, 5.5, 5.5},
        {10.5, 6.5, 0, 100, 1, 0.0, 0, 10.5, 6.5},
        {15.5, 5.5, 0, 100, 1, 0.0, 0, 15.5, 5.5},
        // typ = 1 (Cacobite)
        {20.5, 6.5, 1, 200, 1, 0.0, 0, 20.5, 6.5},
        {25.5, 5.5, 1, 200, 1, 0.0, 0, 25.5, 5.5},
        {8.5, 10.5, 0, 100, 1, 0.0, 0, 8.5, 10.5},
        {14.5, 15.5, 1, 200, 1, 0.0, 0, 14.5, 15.5},
        // typ = 2 (Arachnobaron)
        {22.5, 18.5, 2, 300, 1, 0.0, 0, 22.5, 18.5}
    };'''

code = re.sub(r'\s*sprites = \{.*?\};\s*', '\n' + sprites_new + '\n', code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
