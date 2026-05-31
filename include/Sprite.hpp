#pragma once
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
    int scoreValue = 100;
    
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
    
    // Projectile fields
    bool isProjectile = false;
    double dx = 0.0;
    double dy = 0.0;
    double lifeTime = 0.0;
};
