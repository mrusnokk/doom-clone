import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'if (sprite.state == 0) continue;',
    'if (sprite.state <= 0) continue;'
)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
