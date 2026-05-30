import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# Implement playSound
play_sound_impl = '''
void Engine::playSound(short* data, int samples) {
    if (!audioDevice || !data || samples <= 0) return;
    if (activeStreams[currentAudioStream]) {
        SDL_DestroyAudioStream(activeStreams[currentAudioStream]);
    }
    SDL_AudioSpec spec;
    spec.format = SDL_AUDIO_S16LE;
    spec.channels = 1;
    spec.freq = 44100;
    activeStreams[currentAudioStream] = SDL_CreateAudioStream(&spec, nullptr);
    if (activeStreams[currentAudioStream]) {
        SDL_BindAudioStream(audioDevice, activeStreams[currentAudioStream]);
        SDL_PutAudioStreamData(activeStreams[currentAudioStream], data, samples * sizeof(short));
    }
    currentAudioStream = (currentAudioStream + 1) % 8;
}
'''
if 'void Engine::playSound' not in code:
    code = code.replace('Engine::~Engine()', play_sound_impl + '\nEngine::~Engine()')

# Destroy active streams in destructor
destructor_destroy = '''
    for (int i = 0; i < 8; i++) {
        if (activeStreams[i]) SDL_DestroyAudioStream(activeStreams[i]);
    }
'''
code = code.replace('    if (weaponAudioStream) {', destructor_destroy + '\    if (weaponAudioStream) {')

# Play Pain Sound
pain_sound = '''                    closestSprite->hp -= 34; // 3 rány na 100 HP
                    closestSprite->state = 2; // Pain stav
                    closestSprite->frameIndex = 0;
                    closestSprite->animTimer = 0.0;
                    if (closestSprite->type >= 0 && closestSprite->type < enemyTypes.size()) {
                        playSound(enemyTypes[closestSprite->type].soundPain, enemyTypes[closestSprite->type].soundPainSamples);
                    }
                    if (closestSprite->hp <= 0) {
                        closestSprite->state = 0; // Mrtvý
                        closestSprite->frameIndex = 0;
                        closestSprite->animTimer = 0.0;
                        if (closestSprite->type >= 0 && closestSprite->type < enemyTypes.size()) {
                            playSound(enemyTypes[closestSprite->type].soundDeath, enemyTypes[closestSprite->type].soundDeathSamples);
                        }
                    }'''
code = re.sub(r'closestSprite->hp -= 34;.*?closestSprite->animTimer = 0\.0;\s*\}\s*\}', pain_sound + '\n                }', code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
