import re
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix enemy.png fallback removal
code = re.sub(r'\s*if \(\!loadTex\("enemy\.png", enemyTexture\)\) \{.*?\n    \}\n', '\n', code, flags=re.DOTALL)

# Fix deadTimer and damageTimer in processInput
code = code.replace('sprite.deadTimer = 0;', '')
code = code.replace('sprite.damageTimer = 0;', '')

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
