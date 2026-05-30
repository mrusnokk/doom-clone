import sys
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

debug_code = '''void Engine::playSound(short* data, int samples) {
    std::cout << "playSound called! data: " << data << ", samples: " << samples << std::endl;'''

code = code.replace('void Engine::playSound(short* data, int samples) {', debug_code)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
