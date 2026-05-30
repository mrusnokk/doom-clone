import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

load_sounds = '''
    if (def.painFrames.empty() && !def.idleFrames.empty()) def.painFrames.push_back(def.idleFrames[0]);
    if (def.deathFrames.empty() && !def.idleFrames.empty()) def.deathFrames.push_back(def.idleFrames.back());
    
    // Load sounds if they exist
    std::string folderName = std::filesystem::path(directoryPath).filename().string();
    std::string painSoundPath, deathSoundPath;
    if (folderName == "Agaures") {
        painSoundPath = "assets/SOUNDS/AGURPAIN.ogg";
        deathSoundPath = "assets/SOUNDS/AGURDTH1.ogg";
    } else if (folderName == "Cacobite") {
        painSoundPath = "assets/SOUNDS/CACOBPAI.ogg";
        deathSoundPath = "assets/SOUNDS/CACOBDTH.ogg";
    } else if (folderName == "Arachnobaron") {
        painSoundPath = "assets/SOUNDS/DSABRDTH.ogg"; // reuse death sound for pain
        deathSoundPath = "assets/SOUNDS/DSABRDTH.ogg";
    }
    
    if (!painSoundPath.empty()) {
        int channels, sample_rate;
        short* decoded = nullptr;
        int samples = stb_vorbis_decode_filename(painSoundPath.c_str(), &channels, &sample_rate, &decoded);
        if (samples > 0) {
            def.soundPain = decoded;
            def.soundPainSamples = samples * channels;
        }
    }
    if (!deathSoundPath.empty()) {
        int channels, sample_rate;
        short* decoded = nullptr;
        int samples = stb_vorbis_decode_filename(deathSoundPath.c_str(), &channels, &sample_rate, &decoded);
        if (samples > 0) {
            def.soundDeath = decoded;
            def.soundDeathSamples = samples * channels;
        }
    }
'''
code = re.sub(r'\s*if \(def\.painFrames\.empty\(\).*?push_back\(def\.idleFrames\.back\(\)\);\s*', '\n' + load_sounds + '\n', code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
