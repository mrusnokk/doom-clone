import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'playerDamageTimer = 0.2;',
    'playerDamageTimer = 0.2;\\n                    playSound(playerPainData, playerPainSamples, playerPainRate, playerPainChannels);'
)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
