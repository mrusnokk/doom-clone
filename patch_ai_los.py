import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

ai_logic_old = '''            double dx = player.x - sprite.x;
            double dy = player.y - sprite.y;
            double dist = std::sqrt(dx*dx + dy*dy);

            if (dist < 8.0 && dist > 0.6) {
                // Nepřítel pronásleduje hráče'''

ai_logic_new = '''            double dx = player.x - sprite.x;
            double dy = player.y - sprite.y;
            double dist = std::sqrt(dx*dx + dy*dy);

            // Line of sight check
            bool canSeePlayer = true;
            int steps = max(1, (int)(dist * 10));
            for(int i=0; i<=steps; i++) {
                double cx = sprite.x + dx * ((double)i / steps);
                double cy = sprite.y + dy * ((double)i / steps);
                if (!isWalkable((int)cx, (int)cy)) {
                    canSeePlayer = false;
                    break;
                }
            }

            if (canSeePlayer && dist < 8.0 && dist > 0.6) {
                // Nepřítel pronásleduje hráče'''
code = code.replace(ai_logic_old, ai_logic_new)

ai_attack_old = '''            } else if (dist <= 0.6) {
                // Nepřítel útočí na blízko'''
ai_attack_new = '''            } else if (canSeePlayer && dist <= 0.6) {
                // Nepřítel útočí na blízko'''
code = code.replace(ai_attack_old, ai_attack_new)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
