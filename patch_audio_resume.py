import sys
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('audioDevice = SDL_OpenAudioDevice(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, nullptr);\n    if (audioDevice) {', 'audioDevice = SDL_OpenAudioDevice(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, nullptr);\n    if (audioDevice) {\n        SDL_ResumeAudioDevice(audioDevice);')

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
