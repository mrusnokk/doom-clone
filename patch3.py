with open('E:/Michael/skola/cpp/projektFinal/src/raycaster.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('sprites[spriteIdx].damageTimer > 0', 'sprites[spriteIdx].state == 2')

with open('E:/Michael/skola/cpp/projektFinal/src/raycaster.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
