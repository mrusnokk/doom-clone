import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

fix_audio = '''        int samples = stb_vorbis_decode_filename("assets/SOUNDS/AUT9FIRC.ogg", &channels, &sample_rate, &decoded_data);
        if (samples <= 0) samples = stb_vorbis_decode_filename("SOUNDS/AUT9FIRC.ogg", &channels, &sample_rate, &decoded_data);
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
        samples = stb_vorbis_decode_filename("assets/SOUNDS/AGURPAIN.ogg", &channels, &sample_rate, &decoded_data);
        if (samples <= 0) samples = stb_vorbis_decode_filename("SOUNDS/AGURPAIN.ogg", &channels, &sample_rate, &decoded_data);
        if (samples > 0 && decoded_data) {
            playerPainData = decoded_data;
            playerPainSamples = samples * channels;
            playerPainRate = sample_rate;
            playerPainChannels = channels;
        }
'''
code = re.sub(r'int samples = stb_vorbis_decode_filename\("assets/SOUNDS/AUT9FIRC\.ogg".*?weaponAudioChannels = channels;\s*\}', fix_audio, code, flags=re.DOTALL)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
