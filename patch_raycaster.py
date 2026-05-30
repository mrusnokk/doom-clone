import re

with open('src/raycaster.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'if (sprites[spriteIdx].isProjectile && sprites[spriteIdx].state == 0) continue;',
    'if (sprites[spriteIdx].state == -1) continue;\n        if (sprites[spriteIdx].isProjectile && sprites[spriteIdx].state == 0) continue;'
)

with open('src/raycaster.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
