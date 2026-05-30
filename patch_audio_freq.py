import re

# 1. Update Sprite.hpp to store sample rate and channels
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'r', encoding='utf-8') as f:
    code = f.read()

if 'int soundPainRate = 44100;' not in code:
    code = code.replace('int soundAttackSamples = 0;', '''int soundAttackSamples = 0;
    int soundPainRate = 44100;
    int soundDeathRate = 44100;
    int soundAttackRate = 44100;''')
    with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'w', encoding='utf-8') as f:
        f.write(code)

# 2. Update engine.hpp
with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'r', encoding='utf-8') as f:
    code = f.read()
code = code.replace('void playSound(short* data, int samples);', 'void playSound(short* data, int samples, int sampleRate = 44100);')
with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'w', encoding='utf-8') as f:
    f.write(code)

# 3. Update engine.cpp
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# fix playSound signature and usage
code = code.replace('void Engine::playSound(short* data, int samples) {', 'void Engine::playSound(short* data, int samples, int sampleRate) {')
code = code.replace('spec.freq = 44100;', 'spec.freq = sampleRate;')

# fix loadEnemyDef logic to store sampleRate
code = re.sub(r'def\.soundPainSamples = samples \* channels;', 'def.soundPainSamples = samples * channels;\n            def.soundPainRate = sample_rate;', code)
code = re.sub(r'def\.soundDeathSamples = samples \* channels;', 'def.soundDeathSamples = samples * channels;\n            def.soundDeathRate = sample_rate;', code)
code = re.sub(r'def\.soundAttackSamples = samples \* channels;', 'def.soundAttackSamples = samples * channels;\n            def.soundAttackRate = sample_rate;', code)

# fix play calls
code = re.sub(r'playSound\(enemyTypes\[([^\]]+)\]\.soundPain, enemyTypes\[\1\]\.soundPainSamples\);', r'playSound(enemyTypes[\1].soundPain, enemyTypes[\1].soundPainSamples, enemyTypes[\1].soundPainRate);', code)
code = re.sub(r'playSound\(enemyTypes\[([^\]]+)\]\.soundDeath, enemyTypes\[\1\]\.soundDeathSamples\);', r'playSound(enemyTypes[\1].soundDeath, enemyTypes[\1].soundDeathSamples, enemyTypes[\1].soundDeathRate);', code)
code = re.sub(r'playSound\(enemyTypes\[([^\]]+)\]\.soundAttack, enemyTypes\[\1\]\.soundAttackSamples\);', r'playSound(enemyTypes[\1].soundAttack, enemyTypes[\1].soundAttackSamples, enemyTypes[\1].soundAttackRate);', code)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
