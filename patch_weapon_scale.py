import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

weapon_render = '''            // Vykreslení zbraně
            if (!weaponFrames.empty() && weaponFrameIndex < weaponFrames.size()) {
                const SpriteFrame& wf = weaponFrames[weaponFrameIndex];
                int scale = 4; // Zvětšení zbraně
                int scaledW = wf.w * scale;
                int scaledH = wf.h * scale;
                
                int startX = screenWidth / 2 - scaledW / 2;
                int startY = screenHeight - scaledH;
                
                for(int y = 0; y < scaledH; y++) {
                    for(int x = 0; x < scaledW; x++) {
                        int screenX = startX + x;
                        int screenY = startY + y;
                        if(screenX >= 0 && screenX < screenWidth && screenY >= 0 && screenY < screenHeight) {
                            int srcX = x / scale;
                            int srcY = y / scale;
                            uint32_t color = wf.pixels[srcY * wf.w + srcX];
                            if ((color & 0xFF000000) != 0) {
                                framebuffer[screenY * screenWidth + screenX] = color;
                            }
                        }
                    }
                }
            }'''

code = re.sub(r'\s*// Vykreslení zbraně.*?\}\s*\}\s*\}\s*\}', '\n' + weapon_render, code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
