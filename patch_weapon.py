import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# Změna zbraně z AUT9 na DUA9
code = code.replace('"SPRITES/AUT9"', '"assets/SPRITES/WEAPONS/DUA9/DUA9"')
code = code.replace('"SOUNDS/AUT9FIRC.ogg"', '"assets/SOUNDS/DSDBLOAD.ogg"') # DSDBLOAD je klasický doom super shotgun zvuk

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
