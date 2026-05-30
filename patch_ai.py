import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

ai_replacement = '''        // --- AI NEPŘÁTEL A PROJEKTILY ---
        std::vector<Sprite> newProjectiles;
        for (auto& sprite : sprites) {
            if (sprite.isProjectile) {
                if (sprite.state == 1) {
                    sprite.lifeTime -= deltaTime;
                    if (sprite.lifeTime <= 0) {
                        sprite.state = 0;
                    } else {
                        double moveSpeed = 8.0 * deltaTime;
                        sprite.x += sprite.dx * moveSpeed;
                        sprite.y += sprite.dy * moveSpeed;
                        
                        double pDist = std::sqrt((player.x - sprite.x)*(player.x - sprite.x) + (player.y - sprite.y)*(player.y - sprite.y));
                        if (pDist < 0.5) {
                            sprite.state = 0;
                            player.hp -= 15;
                            playerDamageTimer = 0.2;
                            playSound(playerPainData, playerPainSamples, playerPainRate, playerPainChannels);
                        }
                    }
                }
                continue;
            }

            if (sprite.state == 0) {
                sprite.deadTimer -= deltaTime;
                if (sprite.deadTimer <= 0) {
                    sprite.state = 1;
                    sprite.hp = 100;
                    sprite.x = sprite.spawnX;
                    sprite.y = sprite.spawnY;
                }
                continue;
            }

            if (sprite.damageTimer > 0) sprite.damageTimer -= deltaTime;
            if (sprite.attackCooldown > 0) sprite.attackCooldown -= deltaTime;

            double dx = player.x - sprite.x;
            double dy = player.y - sprite.y;
            double dist = std::sqrt(dx*dx + dy*dy);

            if (dist < 8.0 && dist > 0.6) {
                // Nepřítel pronásleduje hráče
                double speed = 1.5 * deltaTime;
                double moveX = (dx / dist) * speed;
                double moveY = (dy / dist) * speed;
                
                double sBufferX = (moveX > 0) ? 0.2 : -0.2;
                double sBufferY = (moveY > 0) ? 0.2 : -0.2;

                // Kolize pro nepřítele, aby nelezl přes zdi
                if (isWalkable(int(sprite.x + moveX + sBufferX), int(sprite.y))) {
                    sprite.x += moveX;
                }
                if (isWalkable(int(sprite.x), int(sprite.y + moveY + sBufferY))) {
                    sprite.y += moveY;
                }
                
                // Střelba projektilů
                if (sprite.attackCooldown <= 0 && (rand() % 100) < 2) {
                    sprite.attackCooldown = 2.0; // 2 sec cooldown
                    if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                        playSound(enemyTypes[sprite.type].soundAttack, enemyTypes[sprite.type].soundAttackSamples, enemyTypes[sprite.type].soundAttackRate, enemyTypes[sprite.type].soundAttackChannels);
                    }
                    Sprite proj;
                    proj.x = sprite.x;
                    proj.y = sprite.y;
                    proj.isProjectile = true;
                    proj.type = sprite.type;
                    proj.hp = 1;
                    proj.state = 1;
                    proj.dx = dx / dist;
                    proj.dy = dy / dist;
                    proj.lifeTime = 5.0;
                    newProjectiles.push_back(proj);
                }
            } else if (dist <= 0.6) {
                // Nepřítel útočí na blízko
                if (sprite.attackCooldown <= 0) {
                    sprite.attackCooldown = 1.5;
                    player.hp -= 5;
                    playerDamageTimer = 0.2;
                    playSound(playerPainData, playerPainSamples, playerPainRate, playerPainChannels);
                    if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                        playSound(enemyTypes[sprite.type].soundAttack, enemyTypes[sprite.type].soundAttackSamples, enemyTypes[sprite.type].soundAttackRate, enemyTypes[sprite.type].soundAttackChannels);
                    }
                }
            }
        }
        for (const auto& np : newProjectiles) {
            sprites.push_back(np);
        }
'''

# We will replace everything from "// --- AI NEPŘÁTEL ---" to the end of the AI loop.
pattern = r'// --- AI NEPŘÁTEL ---.*?if \(\(rand\(\) % 100\) < 5\) \{ \n.*?player\.hp -= 5;\n.*?playerDamageTimer = 0\.2;\n.*?playSound\(playerPainData, playerPainSamples, playerPainRate, playerPainChannels\);\n\s*\}\n\s*\}\n\s*\}'
code = re.sub(pattern, ai_replacement, code, flags=re.DOTALL)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
