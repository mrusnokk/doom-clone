import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Projectile Hitscan protection
code = code.replace(
    'if (sprite.state == 0) continue;',
    'if (sprite.state == 0) continue;\n                    if (sprite.isProjectile) continue;'
)

# 2. Projectile Wall Collision
proj_collision_old = '''                        double moveSpeed = 8.0 * deltaTime;
                        sprite.x += sprite.dx * moveSpeed;
                        sprite.y += sprite.dy * moveSpeed;'''
proj_collision_new = '''                        double moveSpeed = 8.0 * deltaTime;
                        if (!isWalkable(int(sprite.x + sprite.dx * moveSpeed), int(sprite.y + sprite.dy * moveSpeed))) {
                            sprite.state = 0;
                            continue;
                        }
                        sprite.x += sprite.dx * moveSpeed;
                        sprite.y += sprite.dy * moveSpeed;'''
code = code.replace(proj_collision_old, proj_collision_new)

# 3. Sprite Animation update
anim_old = '''        // --- AI NEPŘÁTEL A PROJEKTILY ---
        std::vector<Sprite> newProjectiles;
        for (auto& sprite : sprites) {
            if (sprite.isProjectile) {'''

anim_new = '''        // --- AI NEPŘÁTEL A PROJEKTILY ---
        std::vector<Sprite> newProjectiles;
        for (auto& sprite : sprites) {
            // Animace sprite
            sprite.animTimer += deltaTime;
            if (sprite.animTimer >= 0.15) {
                sprite.animTimer -= 0.15;
                int maxFrames = 1;
                if (sprite.isProjectile) {
                    if (sprite.type >= 0 && sprite.type < projectileTypes.size()) maxFrames = projectileTypes[sprite.type].size();
                } else if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                    if (sprite.state == 0) maxFrames = enemyTypes[sprite.type].deathFrames.size();
                    else if (sprite.state == 1) maxFrames = enemyTypes[sprite.type].idleFrames.size();
                    else if (sprite.state == 2) maxFrames = enemyTypes[sprite.type].painFrames.size();
                }
                if (maxFrames <= 0) maxFrames = 1;
                
                sprite.frameIndex++;
                if (sprite.state == 0) {
                    if (sprite.frameIndex >= maxFrames) sprite.frameIndex = maxFrames - 1;
                } else if (sprite.state == 2) {
                    if (sprite.frameIndex >= maxFrames) {
                        sprite.state = 1;
                        sprite.frameIndex = 0;
                    }
                } else {
                    sprite.frameIndex %= maxFrames;
                }
            }

            if (sprite.isProjectile) {'''
code = code.replace(anim_old, anim_new)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
