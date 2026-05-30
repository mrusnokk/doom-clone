import re

with open('src/raycaster.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

render_code = '''
        int texWidth = TEX_WIDTH;
        int texHeight = TEX_HEIGHT;
        const uint32_t* texturePtr = enemyTexture;
        
        int type = sprites[spriteIdx].type;
        const std::vector<SpriteFrame>* animFrames = nullptr;
        if (type >= 0 && type < enemyTypes.size()) {
            if (sprites[spriteIdx].state == 1) animFrames = &enemyTypes[type].idleFrames;
            else if (sprites[spriteIdx].state == 2) animFrames = &enemyTypes[type].painFrames;
            else animFrames = &enemyTypes[type].deathFrames;
        }
        
        if (animFrames && !animFrames->empty()) {
            int frameIdx = sprites[spriteIdx].frameIndex;
            if (frameIdx < 0 || frameIdx >= animFrames->size()) frameIdx = 0;
            const auto& sf = (*animFrames)[frameIdx];
            texWidth = sf.w;
            texHeight = sf.h;
            texturePtr = sf.pixels.data();
        }
        '''
code = re.sub(r'int texWidth = TEX_WIDTH;\s*int texHeight = TEX_HEIGHT;\s*const uint32_t\* texturePtr = enemyTexture;', render_code, code)
# Also change the condition to NOT skip dead sprites because we WANT to render dead sprites!
code = code.replace('if (sprites[spriteIdx].state == 0) continue; // Mrtvc nekreslme', '// Mrtvoly vykreslujeme d>le')

with open('src/raycaster.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
