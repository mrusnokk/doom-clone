import sys
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    for line in f:
        if 'for (char c =' in line or 'weaponFrames.push_back' in line or 'assets/' in line and 'DUA9' in line:
            print(line.strip())
