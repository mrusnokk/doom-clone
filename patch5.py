import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

debug_code = '''
    if (def.painFrames.empty() && !def.idleFrames.empty()) def.painFrames.push_back(def.idleFrames[0]);
    if (def.deathFrames.empty() && !def.idleFrames.empty()) def.deathFrames.push_back(def.idleFrames.back());
    
    // Write debug to file
    FILE* f = fopen("debug.txt", "a");
    if (f) {
        fprintf(f, "Loaded Enemy from %s: Idle=%d, Pain=%d, Death=%d\\n", directoryPath.c_str(), (int)def.idleFrames.size(), (int)def.painFrames.size(), (int)def.deathFrames.size());
        fclose(f);
    }
'''

code = re.sub(r'    if \(def\.painFrames\.empty\(\).*?push_back\(def\.idleFrames\.back\(\)\);\s*std::cout.*?std::endl;', debug_code, code, flags=re.DOTALL)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
