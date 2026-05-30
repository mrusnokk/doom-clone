import re
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('"assets/SPRITES/WEAPONS/DUA9/DUA9"', '"SPRITES/WEAPONS/DUA9"')
code = code.replace('"assets/SOUNDS/DSDBLOAD.ogg"', '"SOUNDS/AUT9FIRC.ogg"')

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
