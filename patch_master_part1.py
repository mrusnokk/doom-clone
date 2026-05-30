import re

# 1. Sprite.hpp
with open('include/Sprite.hpp', 'r', encoding='utf-8') as f:
    code = f.read()
code = '''#pragma once
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
    int type = 0;
    int hp = 100;
    int state = 1; // 1=idle, 2=pain, 0=death
    double damageTimer = 0.0;
    double spawnX = 0;
    double spawnY = 0;
    double deadTimer = 0.0;
    double animTimer = 0.0;
    int frameIndex = 0;
    double attackCooldown = 0.0;
};
'''
with open('include/Sprite.hpp', 'w', encoding='utf-8') as f:
    f.write(code)

# 2. Engine.hpp
with open('include/Engine.hpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r'\s*struct SpriteFrame \{.*?\};\s*', '\n', code, flags=re.DOTALL)
if 'std::vector<EnemyDef> enemyTypes;' not in code:
    code = code.replace('std::vector<SpriteFrame> weaponFrames;', 'std::vector<SpriteFrame> weaponFrames;\n    std::vector<EnemyDef> enemyTypes;\n    void loadEnemyDef(const std::string& directoryPath, EnemyDef& def);')

if 'void playSound(short* data, int samples);' in code:
    code = code.replace('void playSound(short* data, int samples);', 'void playSound(short* data, int samples, int sampleRate = 44100, int channels = 1);')

if 'int weaponAudioRate = 44100;' not in code:
    code = code.replace('int weaponAudioSamples = 0;', 'int weaponAudioSamples = 0;\n    int weaponAudioRate = 44100;\n    int weaponAudioChannels = 1;')

# add audio streams array
if 'SDL_AudioStream* activeStreams[8];' not in code:
    code = code.replace('SDL_AudioStream* weaponAudioStream = nullptr;', 'SDL_AudioStream* weaponAudioStream = nullptr;\n    SDL_AudioStream* activeStreams[8] = {nullptr};\n    int currentAudioStream = 0;\n    void playSound(short* data, int samples, int sampleRate = 44100, int channels = 1);')

with open('include/Engine.hpp', 'w', encoding='utf-8') as f:
    f.write(code)

# 3. Raycaster.hpp
with open('include/Raycaster.hpp', 'r', encoding='utf-8') as f:
    code = f.read()
if 'const std::vector<EnemyDef>& enemyTypes' not in code:
    code = code.replace('void renderSprites(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player, std::vector<Sprite>& sprites, const std::vector<double>& zBuffer);', 'void renderSprites(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player, std::vector<Sprite>& sprites, const std::vector<double>& zBuffer, const std::vector<EnemyDef>& enemyTypes);')
with open('include/Raycaster.hpp', 'w', encoding='utf-8') as f:
    f.write(code)

# 4. Raycaster.cpp
with open('src/raycaster.cpp', 'r', encoding='utf-8') as f:
    code = f.read()
if 'const std::vector<EnemyDef>& enemyTypes' not in code:
    code = code.replace('void Raycaster::renderSprites(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player, std::vector<Sprite>& sprites, const std::vector<double>& zBuffer) {', 'void Raycaster::renderSprites(std::vector<uint32_t>& framebuffer, int screenWidth, int screenHeight, const Player& player, std::vector<Sprite>& sprites, const std::vector<double>& zBuffer, const std::vector<EnemyDef>& enemyTypes) {')
    
    render_code = '''
        const std::vector<SpriteFrame>* animFrames = nullptr;
        int type = sprite.type;
        if (type < 0 || type >= enemyTypes.size()) type = 0;
        
        if (enemyTypes.size() > type) {
            if (sprite.state == 1) animFrames = &enemyTypes[type].idleFrames;
            else if (sprite.state == 2) animFrames = &enemyTypes[type].painFrames;
            else animFrames = &enemyTypes[type].deathFrames;
        }
        
        if (animFrames && !animFrames->empty()) {
            int frameIdx = sprite.frameIndex;
            if (frameIdx < 0 || frameIdx >= animFrames->size()) frameIdx = 0;
            const auto& sf = (*animFrames)[frameIdx];
            texWidth = sf.w;
            texHeight = sf.h;
            texturePtr = sf.pixels.data();
        } else {
            texturePtr = enemyTexture;
        }
'''
    code = re.sub(r'const uint32_t\* texturePtr = enemyTexture;', render_code, code)
    
with open('src/raycaster.cpp', 'w', encoding='utf-8') as f:
    f.write(code)

