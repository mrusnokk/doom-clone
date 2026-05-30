import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add includes
if '<filesystem>' not in code:
    code = code.replace('#include <cmath>', '#include <cmath>\n#include <filesystem>\n#include <algorithm>')

# 2. Add playSound definition
if 'void Engine::playSound' not in code:
    code += '''
void Engine::playSound(short* data, int samples, int sampleRate, int channels) {
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
}
'''

# 3. Add loadEnemyDef definition
if 'void Engine::loadEnemyDef' not in code:
    code += '''
void Engine::loadEnemyDef(const std::string& directoryPath, EnemyDef& def) {
    if (!std::filesystem::exists(directoryPath)) return;
    auto loadDynTexLocal = [](const std::string& path, std::vector<uint32_t>& tex, int& w, int& h) {
        int channels;
        unsigned char* data = stbi_load(path.c_str(), &w, &h, &channels, 4);
        if (data) {
            tex.resize(w * h);
            for (int i = 0; i < w * h; i++) {
                uint8_t r = data[i * 4 + 0], g = data[i * 4 + 1], b = data[i * 4 + 2], a = data[i * 4 + 3];
                if (r == 0 && g == 255 && b == 255) a = 0;
                tex[i] = (a << 24) | (r << 16) | (g << 8) | b;
            }
            stbi_image_free(data);
        }
    };
    std::vector<std::string> files;
    for (const auto& entry : std::filesystem::directory_iterator(directoryPath)) {
        if (entry.path().extension() == ".png") files.push_back(entry.path().string());
    }
    std::sort(files.begin(), files.end());
    for (const auto& file : files) {
        std::string filename = std::filesystem::path(file).filename().string();
        if (filename.find('1') != std::string::npos || filename.find('0') != std::string::npos) {
            SpriteFrame sf;
            loadDynTexLocal(file, sf.pixels, sf.w, sf.h);
            if (!sf.pixels.empty()) {
                char frameLetter = 'A';
                for(size_t i=0; i<filename.length(); i++) {
                    if(filename[i]=='1'||filename[i]=='0') { if(i>0) frameLetter=filename[i-1]; break; }
                }
                if (frameLetter >= 'A' && frameLetter <= 'G') def.idleFrames.push_back(sf);
                else if (frameLetter == 'H') def.painFrames.push_back(sf);
                else if (frameLetter >= 'I' && frameLetter <= 'M') def.deathFrames.push_back(sf);
            }
        }
    }
    if (def.idleFrames.empty()) return;
    if (def.painFrames.empty()) def.painFrames.push_back(def.idleFrames[0]);
    if (def.deathFrames.empty()) def.deathFrames.push_back(def.idleFrames[0]);
    
    std::string folderName = std::filesystem::path(directoryPath).filename().string();
    std::string painP, deathP, attackP;
    if (folderName == "Agaures") { painP="assets/SOUNDS/AGURPAIN.ogg"; deathP="assets/SOUNDS/AGURDTH1.ogg"; attackP="assets/SOUNDS/AGURHITS.ogg"; }
    else if (folderName == "Cacobite") { painP="assets/SOUNDS/CACOBPAI.ogg"; deathP="assets/SOUNDS/CACOBDTH.ogg"; attackP="assets/SOUNDS/BABYBITE.ogg"; }
    else if (folderName == "Arachnobaron") { painP="assets/SOUNDS/DSABRDTH.ogg"; deathP="assets/SOUNDS/DSABRDTH.ogg"; attackP="assets/SOUNDS/AGURSWNG.ogg"; }

    auto lSnd = [](const std::string& p, short*& d, int& s, int& r, int& c) {
        if (!p.empty() && std::filesystem::exists(p)) {
            short* dec = nullptr;
            int smp = stb_vorbis_decode_filename(p.c_str(), &c, &r, &dec);
            if (smp > 0) { d = dec; s = smp * c; }
        }
    };
    lSnd(painP, def.soundPain, def.soundPainSamples, def.soundPainRate, def.soundPainChannels);
    lSnd(deathP, def.soundDeath, def.soundDeathSamples, def.soundDeathRate, def.soundDeathChannels);
    lSnd(attackP, def.soundAttack, def.soundAttackSamples, def.soundAttackRate, def.soundAttackChannels);
}
'''

# 4. Engine::Engine constructor audio fix & enemy loading
engine_init = '''    audioDevice = SDL_OpenAudioDevice(SDL_AUDIO_DEVICE_DEFAULT_PLAYBACK, nullptr);
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
            if (weaponAudioStream) SDL_BindAudioStream(audioDevice, weaponAudioStream);
        }
    }'''
code = re.sub(r'\s*audioDevice = SDL_OpenAudioDevice.*?if \(weaponAudioStream\) \{\s*SDL_BindAudioStream\(audioDevice, weaponAudioStream\);\s*\}\s*\}\s*\}', '\n' + engine_init, code, flags=re.DOTALL)

enemy_init = '''    EnemyDef type0; loadEnemyDef("assets/SPRITES/ENEMIES/Agaures", type0); type0.maxHp = 100; if (!type0.idleFrames.empty()) enemyTypes.push_back(type0);
    EnemyDef type1; loadEnemyDef("assets/SPRITES/ENEMIES/Cacobite", type1); type1.maxHp = 200; if (!type1.idleFrames.empty()) enemyTypes.push_back(type1);
    EnemyDef type2; loadEnemyDef("assets/SPRITES/ENEMIES/Arachnobaron", type2); type2.maxHp = 300; if (!type2.idleFrames.empty()) enemyTypes.push_back(type2);
    
    sprites = {
        {8.5, 8.5, 0, 100, 1, 0.0, 8.5, 8.5, 0.0, 0.0, 0, 0.0},
        {10.5, 9.5, 0, 100, 1, 0.0, 10.5, 9.5, 0.0, 0.0, 0, 0.0},
        {13.5, 3.5, 0, 100, 1, 0.0, 13.5, 3.5, 0.0, 0.0, 0, 0.0},
        {22.5, 15.5, 1, 200, 1, 0.0, 22.5, 15.5, 0.0, 0.0, 0, 0.0},
        {20.5, 20.5, 1, 200, 1, 0.0, 20.5, 20.5, 0.0, 0.0, 0, 0.0},
        {5.5, 25.5, 0, 100, 1, 0.0, 5.5, 25.5, 0.0, 0.0, 0, 0.0},
        {15.5, 28.5, 1, 200, 1, 0.0, 15.5, 28.5, 0.0, 0.0, 0, 0.0},
        {28.5, 4.5, 2, 300, 1, 0.0, 28.5, 4.5, 0.0, 0.0, 0, 0.0}
    };'''
code = re.sub(r'\s*sprites = \{.*?\};\s*', '\n' + enemy_init + '\n', code, flags=re.DOTALL)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)

