import sys
with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('        if (!frameTex.empty()) {', '        if (!frameTex.empty()) {\n            std::cout << "Loaded weapon frame: " << filename << std::endl;')

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
