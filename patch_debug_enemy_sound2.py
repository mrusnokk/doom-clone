import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('if (f) {', 'FILE* f_debug_enemy = fopen("debug_audio_enemy.txt", "a");\n    if (f_debug_enemy) {\n        fprintf(f_debug_enemy, "Enemy %s sounds loaded: Pain=%d, Death=%d, Attack=%d\\n", folderName.c_str(), def.soundPain != nullptr, def.soundDeath != nullptr, def.soundAttack != nullptr);\n        fclose(f_debug_enemy);\n    }')
code = code.replace('        fprintf(f,', '')

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
