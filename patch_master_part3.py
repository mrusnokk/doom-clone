import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# 5. Add AI, animation and sound playing to processInput
enemy_ai = '''            sprite.animTimer += deltaTime;
            if (sprite.animTimer > 0.15) {
                sprite.animTimer = 0.0;
                sprite.frameIndex++;
                int maxFrames = 1;
                if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                    if (sprite.state == 1) maxFrames = enemyTypes[sprite.type].idleFrames.size();
                    else if (sprite.state == 2) maxFrames = enemyTypes[sprite.type].painFrames.size();
                    else maxFrames = enemyTypes[sprite.type].deathFrames.size();
                }
                if (sprite.frameIndex >= maxFrames) {
                    if (sprite.state == 0) sprite.frameIndex = maxFrames - 1;
                    else if (sprite.state == 2) { sprite.state = 1; sprite.frameIndex = 0; }
                    else sprite.frameIndex = 0;
                }
            }

            if (sprite.state == 0) {
                sprite.deadTimer -= deltaTime;
                if (sprite.deadTimer <= 0) {
                    sprite.state = 1;
                    sprite.hp = (sprite.type >= 0 && sprite.type < enemyTypes.size()) ? enemyTypes[sprite.type].maxHp : 100;
                    sprite.x = sprite.spawnX;
                    sprite.y = sprite.spawnY;
                }
                continue; // Mrtvý se nehýbe
            }
            if (sprite.damageTimer > 0) sprite.damageTimer -= deltaTime;
            if (sprite.attackCooldown > 0) sprite.attackCooldown -= deltaTime;
            if (sprite.state == 2) continue; // Zraněný se nehýbe

            double dx = player.x - sprite.x;
            double dy = player.y - sprite.y;
            double dist = std::sqrt(dx*dx + dy*dy);

            if (dist < 8.0 && dist > 0.6) {
                double speed = 1.5 * deltaTime;
                double moveX = (dx / dist) * speed;
                double moveY = (dy / dist) * speed;
                double sBufferX = (moveX > 0) ? 0.2 : -0.2;
                double sBufferY = (moveY > 0) ? 0.2 : -0.2;
                if (worldMap[int(sprite.x + moveX + sBufferX)][int(sprite.y)] == 0) sprite.x += moveX;
                if (worldMap[int(sprite.x)][int(sprite.y + moveY + sBufferY)] == 0) sprite.y += moveY;
            } else if (dist <= 0.6 && sprite.attackCooldown <= 0.0) {
                player.hp -= 10;
                sprite.attackCooldown = 1.0;
                if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                    playSound(enemyTypes[sprite.type].soundAttack, enemyTypes[sprite.type].soundAttackSamples, enemyTypes[sprite.type].soundAttackRate, enemyTypes[sprite.type].soundAttackChannels);
                }
            }'''
code = re.sub(r'\s*double dx = player\.x - sprite\.x;.*?else if \(dist <= 0\.6\) \{\s*player\.hp -= 10;\s*\}', '\n' + enemy_ai, code, flags=re.DOTALL)

enemy_hit = '''sprite.hp -= 34; // Zásah
                if (sprite.hp <= 0 && sprite.state != 0) {
                    sprite.state = 0; // Smrt
                    sprite.animTimer = 0;
                    sprite.frameIndex = 0;
                    sprite.deadTimer = 5.0; // 5 sekund do respawnu
                    player.score += 100;
                    if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                        playSound(enemyTypes[sprite.type].soundDeath, enemyTypes[sprite.type].soundDeathSamples, enemyTypes[sprite.type].soundDeathRate, enemyTypes[sprite.type].soundDeathChannels);
                    }
                } else if (sprite.hp > 0 && sprite.state == 1) {
                    sprite.state = 2; // Pain state
                    sprite.animTimer = 0;
                    sprite.frameIndex = 0;
                    sprite.damageTimer = 0.2; // 200 ms pro pain state
                    if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                        playSound(enemyTypes[sprite.type].soundPain, enemyTypes[sprite.type].soundPainSamples, enemyTypes[sprite.type].soundPainRate, enemyTypes[sprite.type].soundPainChannels);
                    }
                }'''
code = re.sub(r'sprite\.hp -= 34; // Zásah\s*if \(sprite\.hp <= 0\) \{\s*sprite\.state = 0; // Smrt\s*sprite\.deadTimer = 5\.0; // 5 sekund do respawnu\s*player\.score \+= 100;\s*\}', enemy_hit, code, flags=re.DOTALL)

# 6. Update render() to pass enemyTypes
code = code.replace('raycaster.renderSprites(framebuffer, screenWidth, screenHeight, player, sprites, zBuffer);', 'raycaster.renderSprites(framebuffer, screenWidth, screenHeight, player, sprites, zBuffer, enemyTypes);')

# 7. Add weapon flush and anim constraint
code = code.replace('weaponFrameIndex = (weaponFrameIndex + 1) % weaponFrames.size();', 'weaponFrameIndex++;\n                            if (weaponFrameIndex > 4) weaponFrameIndex = 0; // omezení na A-E')
code = code.replace('SDL_PutAudioStreamData(weaponAudioStream, weaponAudioData, weaponAudioSamples * sizeof(short));', 'SDL_PutAudioStreamData(weaponAudioStream, weaponAudioData, weaponAudioSamples * sizeof(short));\n                    SDL_FlushAudioStream(weaponAudioStream);')

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)

