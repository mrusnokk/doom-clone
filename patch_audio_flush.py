import re

# 1. Update Sprite.hpp to store channels
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'r', encoding='utf-8') as f:
    code = f.read()

if 'int soundPainChannels = 1;' not in code:
    code = code.replace('int soundAttackRate = 44100;', '''int soundAttackRate = 44100;
    int soundPainChannels = 1;
    int soundDeathChannels = 1;
    int soundAttackChannels = 1;''')
    with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'w', encoding='utf-8') as f:
        f.write(code)

# 2. Update engine.hpp
with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'r', encoding='utf-8') as f:
    code = f.read()
if 'int weaponAudioChannels = 1;' not in code:
    code = code.replace('int weaponAudioRate = 44100;', 'int weaponAudioRate = 44100;\n    int weaponAudioChannels = 1;')
    code = code.replace('void playSound(short* data, int samples, int sampleRate = 44100);', 'void playSound(short* data, int samples, int sampleRate, int channels);')
    with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'w', encoding='utf-8') as f:
        f.write(code)

# 3. Update engine.cpp
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('void Engine::playSound(short* data, int samples, int sampleRate) {', 'void Engine::playSound(short* data, int samples, int sampleRate, int channels) {')
code = code.replace('spec.channels = 1;', 'spec.channels = channels;')

# Fix weapon data loading
code = re.sub(r'weaponAudioRate = sample_rate;', 'weaponAudioRate = sample_rate;\n            weaponAudioChannels = channels;', code)

# Fix loadEnemyDef logic to store channels
code = re.sub(r'def\.soundPainRate = sample_rate;', 'def.soundPainRate = sample_rate;\n            def.soundPainChannels = channels;', code)
code = re.sub(r'def\.soundDeathRate = sample_rate;', 'def.soundDeathRate = sample_rate;\n            def.soundDeathChannels = channels;', code)
code = re.sub(r'def\.soundAttackRate = sample_rate;', 'def.soundAttackRate = sample_rate;\n            def.soundAttackChannels = channels;', code)

# fix play calls
code = re.sub(r'playSound\(enemyTypes\[([^\]]+)\]\.soundPain, enemyTypes\[\1\]\.soundPainSamples, enemyTypes\[\1\]\.soundPainRate\);', r'playSound(enemyTypes[\1].soundPain, enemyTypes[\1].soundPainSamples, enemyTypes[\1].soundPainRate, enemyTypes[\1].soundPainChannels);', code)
code = re.sub(r'playSound\(enemyTypes\[([^\]]+)\]\.soundDeath, enemyTypes\[\1\]\.soundDeathSamples, enemyTypes\[\1\]\.soundDeathRate\);', r'playSound(enemyTypes[\1].soundDeath, enemyTypes[\1].soundDeathSamples, enemyTypes[\1].soundDeathRate, enemyTypes[\1].soundDeathChannels);', code)
code = re.sub(r'playSound\(enemyTypes\[([^\]]+)\]\.soundAttack, enemyTypes\[\1\]\.soundAttackSamples, enemyTypes\[\1\]\.soundAttackRate\);', r'playSound(enemyTypes[\1].soundAttack, enemyTypes[\1].soundAttackSamples, enemyTypes[\1].soundAttackRate, enemyTypes[\1].soundAttackChannels);', code)

# Add SDL_FlushAudioStream
code = re.sub(r'SDL_PutAudioStreamData\(weaponAudioStream, weaponAudioData, weaponAudioSamples \* sizeof\(short\)\);', r'SDL_PutAudioStreamData(weaponAudioStream, weaponAudioData, weaponAudioSamples * sizeof(short));\n                                SDL_FlushAudioStream(weaponAudioStream);', code)
code = re.sub(r'SDL_PutAudioStreamData\(activeStreams\[currentAudioStream\], data, samples \* sizeof\(short\)\);', r'SDL_PutAudioStreamData(activeStreams[currentAudioStream], data, samples * sizeof(short));\n        SDL_FlushAudioStream(activeStreams[currentAudioStream]);', code)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
