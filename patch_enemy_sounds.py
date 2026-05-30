import re

# 1. Update Sprite.hpp to add soundAttack
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'r', encoding='utf-8') as f:
    code = f.read()

if 'short* soundAttack = nullptr;' not in code:
    code = code.replace('short* soundDeath = nullptr;', 'short* soundDeath = nullptr;\n    short* soundAttack = nullptr;\n    int soundAttackSamples = 0;')
    with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'w', encoding='utf-8') as f:
        f.write(code)

# 2. Update engine.cpp to load and play attack sound
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# Loading
load_attack = '''
    std::string attackSoundPath;
    if (folderName == "Agaures") {
        attackSoundPath = "assets/SOUNDS/AGURHITS.ogg";
    } else if (folderName == "Cacobite") {
        attackSoundPath = "assets/SOUNDS/BABYBITE.ogg";
    } else if (folderName == "Arachnobaron") {
        attackSoundPath = "assets/SOUNDS/AGURSWNG.ogg";
    }
    if (!attackSoundPath.empty()) {
        int channels, sample_rate;
        short* decoded = nullptr;
        int samples = stb_vorbis_decode_filename(attackSoundPath.c_str(), &channels, &sample_rate, &decoded);
        if (samples > 0) {
            def.soundAttack = decoded;
            def.soundAttackSamples = samples * channels;
        }
    }
'''
if 'def.soundAttack =' not in code:
    code = code.replace('    if (!painSoundPath.empty()) {', load_attack + '\n    if (!painSoundPath.empty()) {')

# Playing
play_attack = '''                if (dist <= 0.6 && sprite.attackCooldown <= 0.0) {
                    player.hp -= 10;
                    sprite.attackCooldown = 1.0; // útok jednou za sekundu
                    if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                        playSound(enemyTypes[sprite.type].soundAttack, enemyTypes[sprite.type].soundAttackSamples);
                    }
                }'''
code = re.sub(r'\s*if \(dist <= 0\.6 && sprite\.attackCooldown <= 0\.0\) \{.*?sprite\.attackCooldown = 1\.0; // útok jednou za sekundu\s*\}', '\n' + play_attack, code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
