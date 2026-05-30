import re

# 1. Update Sprite.hpp
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'r', encoding='utf-8') as f:
    sprite_code = f.read()

sound_fields = '''    int maxHp = 100;
    
    short* soundPain = nullptr;
    int soundPainSamples = 0;
    short* soundDeath = nullptr;
    int soundDeathSamples = 0;'''
sprite_code = sprite_code.replace('    int maxHp = 100;', sound_fields)
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'w', encoding='utf-8') as f:
    f.write(sprite_code)

# 2. Update Engine.hpp
with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'r', encoding='utf-8') as f:
    engine_code = f.read()

audio_streams = '''    SDL_AudioDeviceID audioDevice = 0;
    SDL_AudioStream* weaponAudioStream = nullptr;
    short* weaponAudioData = nullptr;
    int weaponAudioSamples = 0;
    
    SDL_AudioStream* activeStreams[8] = {nullptr};
    int currentAudioStream = 0;
    void playSound(short* data, int samples);'''
engine_code = re.sub(r'\s*SDL_AudioDeviceID audioDevice = 0;.*?int weaponAudioSamples = 0;', '\n' + audio_streams, engine_code, flags=re.DOTALL)
with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'w', encoding='utf-8') as f:
    f.write(engine_code)

