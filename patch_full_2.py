import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix playSound signature and implementation
play_sound_impl = '''void Engine::playSound(short* data, int samples, int sampleRate, int channels) {
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
    }
    currentAudioStream = (currentAudioStream + 1) % 8;
}'''
code = re.sub(r'void Engine::playSound\(short\* data, int samples\) \{.*?\n\}', play_sound_impl, code, flags=re.DOTALL)

# Fix weapon audio loading and device unpausing
audio_init = '''    audioDevice = SDL_OpenAudioDevice(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, nullptr);
    if (audioDevice) {
        SDL_ResumeAudioDevice(audioDevice);
        int channels = 0, sample_rate = 0;
        short* decoded_data = nullptr;
        int samples = stb_vorbis_decode_filename("SOUNDS/AUT9FIRC.ogg", &channels, &sample_rate, &decoded_data);
        if (samples > 0 && decoded_data) {
            weaponAudioData = decoded_data;
            weaponAudioSamples = samples * channels;
            weaponAudioRate = sample_rate;
            weaponAudioChannels = channels;
            
            SDL_AudioSpec spec;
            spec.format = SDL_AUDIO_S16LE;
            spec.channels = channels;
            spec.freq = sample_rate;
            weaponAudioStream = SDL_CreateAudioStream(&spec, nullptr);
            if (weaponAudioStream) {
                SDL_BindAudioStream(audioDevice, weaponAudioStream);
            }
        }
    }'''
code = re.sub(r'\s*audioDevice = SDL_OpenAudioDevice.*?if \(weaponAudioStream\) \{\s*SDL_BindAudioStream\(audioDevice, weaponAudioStream\);\s*\}\s*\}\s*\}', '\n' + audio_init, code, flags=re.DOTALL)

# Add loadEnemyDef
load_enemy_def = '''void Engine::loadEnemyDef(const std::string& directoryPath, EnemyDef& def) {
    auto loadFrames = [&](const std::string& prefix, std::vector<SpriteFrame>& frames) {
        for (int i = 0; i < 26; ++i) {
            char suffix = 'A' + i;
            std::string path = directoryPath + "/" + prefix + suffix + "0.png";
            if (std::filesystem::exists(path)) {
                SpriteFrame frame;
                int channels;
                unsigned char* data = stbi_load(path.c_str(), &frame.w, &frame.h, &channels, 4);
                if (data) {
                    frame.pixels.assign((uint32_t*)data, (uint32_t*)data + (frame.w * frame.h));
                    stbi_image_free(data);
                    frames.push_back(frame);
                }
            }
        }
    };
    std::string folderName = std::filesystem::path(directoryPath).filename().string();
    loadFrames(folderName.substr(0, 4), def.idleFrames);
    loadFrames(folderName.substr(0, 4) + "A", def.painFrames); // hacky default
    loadFrames(folderName.substr(0, 4) + "H", def.deathFrames); // hacky default

    std::string painSoundPath, deathSoundPath, attackSoundPath;
    if (folderName == "Agaures") {
        painSoundPath = "assets/SOUNDS/AGURPAIN.ogg";
        deathSoundPath = "assets/SOUNDS/AGURDTH1.ogg";
        attackSoundPath = "assets/SOUNDS/AGURHITS.ogg";
    } else if (folderName == "Cacobite") {
        painSoundPath = "assets/SOUNDS/CACOBPAI.ogg";
        deathSoundPath = "assets/SOUNDS/CACOBDTH.ogg";
        attackSoundPath = "assets/SOUNDS/BABYBITE.ogg";
    } else if (folderName == "Arachnobaron") {
        painSoundPath = "assets/SOUNDS/DSABRDTH.ogg";
        deathSoundPath = "assets/SOUNDS/DSABRDTH.ogg";
        attackSoundPath = "assets/SOUNDS/AGURSWNG.ogg";
    }

    auto loadSnd = [](const std::string& path, short*& data, int& samps, int& rate, int& chs) {
        if (!path.empty() && std::filesystem::exists(path)) {
            short* decoded = nullptr;
            int samples = stb_vorbis_decode_filename(path.c_str(), &chs, &rate, &decoded);
            if (samples > 0) {
                data = decoded;
                samps = samples * chs;
            }
        }
    };
    loadSnd(painSoundPath, def.soundPain, def.soundPainSamples, def.soundPainRate, def.soundPainChannels);
    loadSnd(deathSoundPath, def.soundDeath, def.soundDeathSamples, def.soundDeathRate, def.soundDeathChannels);
    loadSnd(attackSoundPath, def.soundAttack, def.soundAttackSamples, def.soundAttackRate, def.soundAttackChannels);
}'''
if 'void Engine::loadEnemyDef' not in code:
    code += '\n' + load_enemy_def + '\n'

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
