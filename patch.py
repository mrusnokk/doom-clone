import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update sprites array
code = re.sub(r'sprites = \{.*?\};', '''sprites = {
        // x, y, type, hp, state, animTimer, frameIndex, spawnX, spawnY
        {8.5, 8.5, 0, 100, 1, 0.0, 0, 8.5, 8.5},
        {10.5, 9.5, 0, 100, 1, 0.0, 0, 10.5, 9.5},
        {13.5, 3.5, 0, 100, 1, 0.0, 0, 13.5, 3.5},
        {22.5, 15.5, 1, 200, 1, 0.0, 0, 22.5, 15.5},
        {20.5, 20.5, 1, 200, 1, 0.0, 0, 20.5, 20.5},
        {5.5, 25.5, 0, 100, 1, 0.0, 0, 5.5, 25.5},
        {15.5, 28.5, 1, 200, 1, 0.0, 0, 15.5, 28.5},
        {28.5, 4.5, 2, 300, 1, 0.0, 0, 28.5, 4.5}
    };''', code, flags=re.DOTALL)

# 2. Update texture loading
code = re.sub(r'// Načtení druhů nepřátel \(zatím 2 typy\).*?enemyTextures\.push_back\(sf\);\s*\}\s*\}', '''// Načtení nových animovaných druhů nepřátel
    EnemyDef type0;
    loadEnemyDef("assets/SPRITES/ENEMIES/Agaures", type0);
    type0.maxHp = 100;
    if (!type0.idleFrames.empty()) enemyTypes.push_back(type0);

    EnemyDef type1;
    loadEnemyDef("assets/SPRITES/ENEMIES/Cacobite", type1);
    type1.maxHp = 200;
    if (!type1.idleFrames.empty()) enemyTypes.push_back(type1);

    EnemyDef type2;
    loadEnemyDef("assets/SPRITES/ENEMIES/Arachnobaron", type2);
    type2.maxHp = 300;
    if (!type2.idleFrames.empty()) enemyTypes.push_back(type2);''', code, flags=re.DOTALL)

# 3. Update Hitscan logic
hitscan_old = '''                            if (transformY < 15.0) { // Dostřel
                                sprite.hp -= 35;
                                sprite.damageTimer = 0.2; 
                                if (sprite.hp <= 0) {
                                    sprite.state = 0; 
                                    sprite.deadTimer = 5.0; // 5 sekund do respawnu
                                }
                            }'''
hitscan_new = '''                            if (transformY < 15.0) { // Dostřel
                                sprite.hp -= 35;
                                sprite.state = 2; // Pain state
                                sprite.animTimer = 0;
                                sprite.frameIndex = 0;
                                if (sprite.hp <= 0) {
                                    sprite.state = 0; // Death state
                                    sprite.animTimer = 0;
                                    sprite.frameIndex = 0;
                                }
                            }'''
code = code.replace(hitscan_old, hitscan_new)

# 4. Update Animation Timer Logic
anim_old = '''            if (sprite.state == 0) {
                sprite.deadTimer -= deltaTime;
                if (sprite.deadTimer <= 0) {
                    sprite.state = 1;
                    sprite.hp = 100;
                    sprite.x = sprite.spawnX;
                    sprite.y = sprite.spawnY;
                }
                continue;
            }

            if (sprite.damageTimer > 0) sprite.damageTimer -= deltaTime;'''
anim_new = '''            sprite.animTimer += deltaTime;
            if (sprite.animTimer > 0.15) { // 150ms na snímek
                sprite.animTimer = 0.0;
                sprite.frameIndex++;
                
                int maxFrames = 1;
                if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                    if (sprite.state == 1) maxFrames = enemyTypes[sprite.type].idleFrames.size();
                    else if (sprite.state == 2) maxFrames = enemyTypes[sprite.type].painFrames.size();
                    else maxFrames = enemyTypes[sprite.type].deathFrames.size();
                }
                if (maxFrames == 0) maxFrames = 1;

                if (sprite.frameIndex >= maxFrames) {
                    if (sprite.state == 0) {
                        sprite.frameIndex = maxFrames - 1; // Mrtvý zůstane na posledním snímku smrti
                    } else if (sprite.state == 2) {
                        sprite.state = 1; // Konec pain stavu, zpět do idle
                        sprite.frameIndex = 0;
                    } else {
                        sprite.frameIndex = 0; // Smyčka idle animace
                    }
                }
            }

            if (sprite.state == 0) {
                // Mrtvý nepřítel už nic nedělá a nevstává
                continue;
            }'''
code = code.replace(anim_old, anim_new)

# 5. Update renderSprites call
code = code.replace('raycaster.renderSprites(framebuffer, screenWidth, screenHeight, player, sprites, zBuffer, enemyTextures);', 'raycaster.renderSprites(framebuffer, screenWidth, screenHeight, player, sprites, zBuffer, enemyTypes);')
code = code.replace('raycaster.renderSprites(framebuffer, screenWidth, screenHeight, player, sprites, zBuffer);', 'raycaster.renderSprites(framebuffer, screenWidth, screenHeight, player, sprites, zBuffer, enemyTypes);')

# 6. Append loadEnemyDef
load_func = '''
void Engine::loadEnemyDef(const std::string& directoryPath, EnemyDef& def) {
    if (!std::filesystem::exists(directoryPath)) return;
    
    auto loadDynTexLocal = [](const std::string& path, std::vector<uint32_t>& tex, int& w, int& h) {
        int channels;
        unsigned char* data = stbi_load(path.c_str(), &w, &h, &channels, 4);
        if (data) {
            tex.resize(w * h);
            bool autoTransparent = true;
            if (data[3] == 0) autoTransparent = false;
            for (int i = 0; i < w * h; i++) {
                uint8_t r = data[i * 4 + 0];
                uint8_t g = data[i * 4 + 1];
                uint8_t b = data[i * 4 + 2];
                uint8_t a = data[i * 4 + 3];
                if (autoTransparent && r == 0 && g == 255 && b == 255) {
                    a = 0;
                }
                tex[i] = (a << 24) | (r << 16) | (g << 8) | b;
            }
            stbi_image_free(data);
        }
    };

    std::vector<std::string> files;
    for (const auto& entry : std::filesystem::directory_iterator(directoryPath)) {
        if (entry.path().extension() == ".png") {
            files.push_back(entry.path().string());
        }
    }
    std::sort(files.begin(), files.end());

    for (const auto& file : files) {
        std::string filename = std::filesystem::path(file).filename().string();
        
        // Hledáme pouze čelní sprity (1 nebo 0)
        if (filename.find('1') != std::string::npos || filename.find('0') != std::string::npos) {
            SpriteFrame sf;
            loadDynTexLocal(file, sf.pixels, sf.w, sf.h);
            if (!sf.pixels.empty()) {
                char frameLetter = 'A';
                for(size_t i = 0; i < filename.length(); i++) {
                    if (filename[i] == '1' || filename[i] == '0') {
                        if (i > 0) frameLetter = filename[i-1];
                        break;
                    }
                }

                if (frameLetter >= 'A' && frameLetter <= 'G') {
                    def.idleFrames.push_back(sf);
                } else if (frameLetter == 'H') {
                    def.painFrames.push_back(sf);
                } else {
                    def.deathFrames.push_back(sf);
                }
            }
        }
    }
    
    if (def.painFrames.empty() && !def.idleFrames.empty()) def.painFrames.push_back(def.idleFrames[0]);
    if (def.deathFrames.empty() && !def.idleFrames.empty()) def.deathFrames.push_back(def.idleFrames.back());
}
'''
if 'void Engine::loadEnemyDef' not in code:
    code += load_func

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)

print("Done")
