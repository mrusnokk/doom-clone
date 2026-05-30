import re

# 1. Update Sprite.hpp to add attackCooldown
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'r', encoding='utf-8') as f:
    code = f.read()

if 'double attackCooldown = 0.0;' not in code:
    code = code.replace('double spawnY = 0;', 'double spawnY = 0;\n    double attackCooldown = 0.0;')
    with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'w', encoding='utf-8') as f:
        f.write(code)

# 2. Update engine.cpp to use attackCooldown
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

attack_logic = '''                if (sprite.attackCooldown > 0.0) {
                    sprite.attackCooldown -= deltaTime;
                }
                
                double dist = std::sqrt((player.x - sprite.x) * (player.x - sprite.x) + (player.y - sprite.y) * (player.y - sprite.y));
                if (dist <= 0.6 && sprite.attackCooldown <= 0.0) {
                    player.hp -= 10;
                    sprite.attackCooldown = 1.0; // útok jednou za sekundu
                }'''

code = re.sub(r'\s*double dist = std::sqrt.*?player\.hp -= 2;\s*\}', '\n' + attack_logic, code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
