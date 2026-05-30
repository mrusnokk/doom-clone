import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Agaures death frames
code = code.replace(
    "if (folderName == \"Agaures\") {\n                          if (frameLetter >= 'A' && frameLetter <= 'D') def.idleFrames.push_back(sf);\n                          else if (frameLetter >= 'H' && frameLetter <= 'H') def.painFrames.push_back(sf);\n                          else if (frameLetter >= 'I' && frameLetter <= 'O') def.deathFrames.push_back(sf);",
    "if (folderName == \"Agaures\") {\n                          if (frameLetter >= 'A' && frameLetter <= 'D') def.idleFrames.push_back(sf);\n                          else if (frameLetter >= 'H' && frameLetter <= 'H') def.painFrames.push_back(sf);\n                          else if (frameLetter >= 'I' && frameLetter <= 'M') def.deathFrames.push_back(sf);"
)

# 2. Arachnobaron projectile from BLVB to BLTR
code = code.replace(
    'loadProj("BLVB", p2); // Arachnobaron projectile',
    'loadProj("BLTR", p2); // Arachnobaron projectile'
)

# 3. Enemy dead behavior
old_dead = '''            if (sprite.state == 0) {
                sprite.deadTimer -= deltaTime;
                if (sprite.deadTimer <= 0) {
                    sprite.state = 1;
                    sprite.hp = 100;
                    sprite.x = sprite.spawnX;
                    sprite.y = sprite.spawnY;
                }
                continue;
            }'''
new_dead = '''            if (sprite.state == 0) {
                sprite.deadTimer -= deltaTime;
                if (sprite.deadTimer <= 0) {
                    sprite.state = -1; // Completly disappear
                }
                continue;
            }
            if (sprite.state == -1) continue;'''
code = code.replace(old_dead, new_dead)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
