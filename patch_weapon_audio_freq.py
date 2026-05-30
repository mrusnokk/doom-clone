import re

# Update engine.hpp to add weaponAudioRate
with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'r', encoding='utf-8') as f:
    code = f.read()
if 'int weaponAudioRate = 44100;' not in code:
    code = code.replace('int weaponAudioSamples = 0;', 'int weaponAudioSamples = 0;\n    int weaponAudioRate = 44100;')
    with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'w', encoding='utf-8') as f:
        f.write(code)

# Update engine.cpp
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r'weaponAudioSamples = samples \* channels;', 'weaponAudioSamples = samples * channels;\n            weaponAudioRate = sample_rate;', code)

# fix the SDL_CreateAudioStream for weaponAudioStream
weapon_stream_fix = '''    SDL_AudioSpec spec;
    spec.format = SDL_AUDIO_S16LE;
    spec.channels = 1;
    spec.freq = weaponAudioRate;'''
code = re.sub(r'\s*SDL_AudioSpec spec;\s*spec\.format = SDL_AUDIO_S16LE;\s*spec\.channels = 1;\s*spec\.freq = 44100;\s*weaponAudioStream = SDL_CreateAudioStream', '\n' + weapon_stream_fix + '\n    weaponAudioStream = SDL_CreateAudioStream', code)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
