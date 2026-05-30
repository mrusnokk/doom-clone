import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

debug_print = '''
    FILE* f_debug_enemy = fopen("debug_audio_enemy.txt", "a");
    if (f_debug_enemy) {
        fprintf(f_debug_enemy, "Enemy %s sounds loaded: Pain=%d, Death=%d, Attack=%d\\n", folderName.c_str(), def.soundPain != nullptr, def.soundDeath != nullptr, def.soundAttack != nullptr);
        fclose(f_debug_enemy);
    }
'''
if 'debug_audio_enemy.txt' not in code:
    code = code.replace('// Write debug to file', '// Write debug to file' + debug_print)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
