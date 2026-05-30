import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix the case sensitivity in loadEnemyDef
fix_png = '''if (entry.path().extension() == ".png" || entry.path().extension() == ".PNG") files.push_back(entry.path().string());'''
code = code.replace('if (entry.path().extension() == ".png") files.push_back(entry.path().string());', fix_png)

# 2. Add loading of projectiles in Engine::Engine
load_projectiles = '''
    auto loadProj = [&](const std::string& prefix, std::vector<SpriteFrame>& frames) {
        for (int i = 0; i < 26; ++i) {
            char suffix = 'A' + i;
            std::string path1 = "assets/SPRITES/PROJECTILES/" + prefix + suffix + "0.png";
            std::string path2 = "assets/SPRITES/PROJECTILES/" + prefix + suffix + "0.PNG";
            std::string path = std::filesystem::exists(path1) ? path1 : (std::filesystem::exists(path2) ? path2 : "");
            if (!path.empty()) {
                SpriteFrame frame;
                int channels;
                unsigned char* data = stbi_load(path.c_str(), &frame.w, &frame.h, &channels, 4);
                if (data) {
                    frame.pixels.assign((uint32_t*)data, (uint32_t*)data + (frame.w * frame.h));
                    stbi_image_free(data);
                    frames.push_back(frame);
                }
            } else {
                break; // Stop loading if frame doesn't exist
            }
        }
    };
    std::vector<SpriteFrame> p0, p1, p2;
    loadProj("AGAS", p0); // Agaures projectile
    loadProj("BCAB", p1); // Cacobite projectile
    loadProj("BLVB", p2); // Arachnobaron projectile
    projectileTypes.push_back(p0);
    projectileTypes.push_back(p1);
    projectileTypes.push_back(p2);
'''
code = code.replace('EnemyDef type0; loadEnemyDef("assets/SPRITES/ENEMIES/Agaures", type0);', load_projectiles + '\n    EnemyDef type0; loadEnemyDef("assets/SPRITES/ENEMIES/Agaures", type0);')

# 3. Add projectile handling logic to processInput
# Find the end of processInput, which is before oid Engine::drawMenu()
proj_logic = '''
    // --- Zpracování projektilů ---
    for (auto it = sprites.begin(); it != sprites.end(); ) {
        if (it->isProjectile) {
            it->lifeTime -= deltaTime;
            it->animTimer += deltaTime;
            if (it->animTimer > 0.1) {
                it->animTimer = 0;
                it->frameIndex++;
                if (it->type >= 0 && it->type < projectileTypes.size() && !projectileTypes[it->type].empty()) {
                    it->frameIndex %= projectileTypes[it->type].size();
                } else {
                    it->frameIndex = 0;
                }
            }
            
            // Pohyb projektilu
            double speed = 15.0 * deltaTime;
            double moveX = it->dx * speed;
            double moveY = it->dy * speed;
            
            it->x += moveX;
            it->y += moveY;
            
            bool destroy = false;
            if (it->lifeTime <= 0) destroy = true;
            else if (worldMap[int(it->x)][int(it->y)] > 0) destroy = true; // Zásah zdi
            else {
                // Zásah hráče
                double distToPlayer = std::sqrt((player.x - it->x)*(player.x - it->x) + (player.y - it->y)*(player.y - it->y));
                if (distToPlayer < 0.5) {
                    player.hp -= 15; // Poškození hráči
                    destroy = true;
                }
            }
            
            if (destroy) {
                it = sprites.erase(it);
            } else {
                ++it;
            }
        } else {
            ++it;
        }
    }
'''
code = re.sub(r'// Pohyb dopedu.*?(if \(isShooting\))', proj_logic + '\n    // Pohyb dopedu\n    \g<1>', code, flags=re.DOTALL)

# 4. Update the shooting logic inside enemy AI in processInput to spawn projectiles
enemy_shoot = '''} else if (dist <= 8.0 && sprite.attackCooldown <= 0.0) {
                sprite.attackCooldown = 1.5; // Cooldown pro střelbu
                if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                    playSound(enemyTypes[sprite.type].soundAttack, enemyTypes[sprite.type].soundAttackSamples, enemyTypes[sprite.type].soundAttackRate, enemyTypes[sprite.type].soundAttackChannels);
                }
                // Vystřelit projektil
                Sprite proj;
                proj.isProjectile = true;
                proj.x = sprite.x;
                proj.y = sprite.y;
                proj.type = sprite.type; // Použijeme stejný index pro projectileTypes (0=AGAS, 1=BCAB, 2=BLVB)
                proj.lifeTime = 5.0; // Max 5 sekund života
                proj.dx = dx / dist;
                proj.dy = dy / dist;
                sprites.push_back(proj); // Pozor, iterátor ve for cyklu přes sprites se zneplatní!
                break; // Přerušíme cyklus for přes sprites, aby nedošlo k chybě (zbytek nepřátel se updatuje další frame)
            }'''
code = re.sub(r'\} else if \(dist <= 0\.6 && sprite\.attackCooldown <= 0\.0\) \{.*?player\.hp -= 10;.*?sprite\.attackCooldown = 1\.0;.*?playSound\(.*?\);.*?\}', enemy_shoot, code, flags=re.DOTALL)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)

