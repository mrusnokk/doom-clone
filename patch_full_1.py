import re

# SPRITE.HPP
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'r', encoding='utf-8') as f:
    code = f.read()

sprite_hpp_content = '''#pragma once
#include <vector>
#include <cstdint>

struct SpriteFrame {
    std::vector<uint32_t> pixels;
    int w;
    int h;
};

struct EnemyDef {
    std::vector<SpriteFrame> idleFrames;
    std::vector<SpriteFrame> painFrames;
    std::vector<SpriteFrame> deathFrames;
    int maxHp = 100;
    short* soundPain = nullptr;
    int soundPainSamples = 0;
    int soundPainRate = 44100;
    int soundPainChannels = 1;
    short* soundDeath = nullptr;
    int soundDeathSamples = 0;
    int soundDeathRate = 44100;
    int soundDeathChannels = 1;
    short* soundAttack = nullptr;
    int soundAttackSamples = 0;
    int soundAttackRate = 44100;
    int soundAttackChannels = 1;
};

struct Sprite {
    double x, y;
    int texture;
    int type = 0; // index into enemyTypes
    int hp = 100;
    int state = 1; // 1 = alive(idle), 2 = pain, 0 = dead
    double damageTimer = 0.0;
    double deadTimer = 0.0;
    double spawnX = 0;
    double spawnY = 0;
    double animTimer = 0.0;
    int frameIndex = 0;
    double attackCooldown = 0.0;
};
'''
with open('E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp', 'w', encoding='utf-8') as f:
    f.write(sprite_hpp_content)

# ENGINE.HPP
with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'r', encoding='utf-8') as f:
    code = f.read()

if 'std::vector<EnemyDef> enemyTypes;' not in code:
    code = code.replace('std::vector<SpriteFrame> weaponFrames;', 'std::vector<SpriteFrame> weaponFrames;\n    std::vector<EnemyDef> enemyTypes;\n    void loadEnemyDef(const std::string& directoryPath, EnemyDef& def);')

if 'void playSound(short* data, int samples, int sampleRate, int channels);' not in code:
    code = code.replace('void playSound(short* data, int samples);', 'void playSound(short* data, int samples, int sampleRate = 44100, int channels = 1);')

if 'int weaponAudioRate = 44100;' not in code:
    code = code.replace('int weaponAudioSamples = 0;', 'int weaponAudioSamples = 0;\n    int weaponAudioRate = 44100;\n    int weaponAudioChannels = 1;')

with open('E:/Michael/skola/cpp/projektFinal/include/engine.hpp', 'w', encoding='utf-8') as f:
    f.write(code)
