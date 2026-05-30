import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

debug_code = '''
    if (def.painFrames.empty() && !def.idleFrames.empty()) def.painFrames.push_back(def.idleFrames[0]);
    if (def.deathFrames.empty() && !def.idleFrames.empty()) def.deathFrames.push_back(def.idleFrames.back());
    
    std::cout << "Loaded Enemy from " << directoryPath 
              << ": Idle=" << def.idleFrames.size() 
              << ", Pain=" << def.painFrames.size() 
              << ", Death=" << def.deathFrames.size() << std::endl;
'''

code = code.replace('''    if (def.painFrames.empty() && !def.idleFrames.empty()) def.painFrames.push_back(def.idleFrames[0]);
    if (def.deathFrames.empty() && !def.idleFrames.empty()) def.deathFrames.push_back(def.idleFrames.back());''', debug_code)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
