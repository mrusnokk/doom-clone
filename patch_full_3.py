import re
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# Add attack cooldown
if 'sprite.attackCooldown -= deltaTime;' not in code:
    code = re.sub(r'sprite\.deadTimer -= deltaTime;\s*\}', 'sprite.deadTimer -= deltaTime;\n                }\n                if (sprite.attackCooldown > 0) sprite.attackCooldown -= deltaTime;', code)

# Play attack sound
play_attack = '''if (dist <= 0.6 && sprite.attackCooldown <= 0.0 && sprite.state == 1) {
                    player.hp -= 10;
                    sprite.attackCooldown = 1.0;
                    if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                        playSound(enemyTypes[sprite.type].soundAttack, enemyTypes[sprite.type].soundAttackSamples, enemyTypes[sprite.type].soundAttackRate, enemyTypes[sprite.type].soundAttackChannels);
                    }
                }'''
code = re.sub(r'if \(dist <= 0\.6\)\s*\{\s*player\.hp -= 10;\s*\}', play_attack, code)

# Play pain and death sounds
play_pain_death = '''sprite.hp -= 34; // Zásah
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
                    sprite.state = 2; // Pain
                    sprite.animTimer = 0;
                    sprite.frameIndex = 0;
                    sprite.damageTimer = 0.2;
                    if (sprite.type >= 0 && sprite.type < enemyTypes.size()) {
                        playSound(enemyTypes[sprite.type].soundPain, enemyTypes[sprite.type].soundPainSamples, enemyTypes[sprite.type].soundPainRate, enemyTypes[sprite.type].soundPainChannels);
                    }
                }'''
code = re.sub(r'sprite\.hp -= 34; // Zásah\s*if \(sprite\.hp <= 0 && sprite\.state != 0\) \{\s*sprite\.state = 0; // Smrt\s*sprite\.animTimer = 0;\s*sprite\.frameIndex = 0;\s*sprite\.deadTimer = 5\.0; // 5 sekund do respawnu\s*player\.score \+= 100;\s*\}\s*else if \(sprite\.hp > 0 && sprite\.state == 1\) \{\s*sprite\.state = 2; // Pain state\s*sprite\.animTimer = 0;\s*sprite\.frameIndex = 0;\s*sprite\.damageTimer = 0\.2; // 200 ms pro pain state\s*\}', play_pain_death, code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
