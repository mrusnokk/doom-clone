import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

debug_audio = '''
void Engine::playSound(short* data, int samples, int sampleRate, int channels) {
    FILE* dbg = fopen("debug_audio.txt", "a");
    if (dbg) {
        fprintf(dbg, "playSound called: data=%p, samples=%d, rate=%d, channels=%d\\n", (void*)data, samples, sampleRate, channels);
        fclose(dbg);
    }
    if (!audioDevice || !data || samples <= 0) return;
    if (activeStreams[currentAudioStream]) {
        SDL_DestroyAudioStream(activeStreams[currentAudioStream]);
    }
    SDL_AudioSpec spec;
    spec.format = SDL_AUDIO_S16LE;
    spec.channels = channels;
    spec.freq = sampleRate;
    activeStreams[currentAudioStream] = SDL_CreateAudioStream(&spec, nullptr);
    if (activeStreams[currentAudioStream]) {
        SDL_BindAudioStream(audioDevice, activeStreams[currentAudioStream]);
        SDL_PutAudioStreamData(activeStreams[currentAudioStream], data, samples * sizeof(short));
        SDL_FlushAudioStream(activeStreams[currentAudioStream]);
        if (dbg = fopen("debug_audio.txt", "a")) {
            fprintf(dbg, "Successfully created and flushed stream %d\\n", currentAudioStream);
            fclose(dbg);
        }
    } else {
        if (dbg = fopen("debug_audio.txt", "a")) {
            fprintf(dbg, "Failed to create stream: %s\\n", SDL_GetError());
            fclose(dbg);
        }
    }
    currentAudioStream = (currentAudioStream + 1) % 8;
}
'''
code = re.sub(r'void Engine::playSound\(short\* data, int samples, int sampleRate, int channels\) \{.*?currentAudioStream = \(currentAudioStream \+ 1\) % 8;\s*\}', debug_audio, code, flags=re.DOTALL)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
