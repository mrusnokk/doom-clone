import re

with open('src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix loading death frames based on folder name
fix_load_frames = '''
                if (folderName == "Agaures") {
                    if (frameLetter >= 'A' && frameLetter <= 'D') def.idleFrames.push_back(sf);
                    else if (frameLetter >= 'H' && frameLetter <= 'H') def.painFrames.push_back(sf);
                    else if (frameLetter >= 'I' && frameLetter <= 'O') def.deathFrames.push_back(sf);
                } else if (folderName == "Cacobite") {
                    if (frameLetter >= 'A' && frameLetter <= 'E') def.idleFrames.push_back(sf);
                    else if (frameLetter == 'F') def.painFrames.push_back(sf);
                    else if (frameLetter >= 'G' && frameLetter <= 'L') def.deathFrames.push_back(sf);
                } else if (folderName == "Arachnobaron") {
                    if (frameLetter >= 'A' && frameLetter <= 'F') def.idleFrames.push_back(sf);
                    else if (frameLetter >= 'G' && frameLetter <= 'H') def.painFrames.push_back(sf);
                    else if (frameLetter >= 'J' && frameLetter <= 'O') def.deathFrames.push_back(sf);
                } else {
                    if (frameLetter >= 'A' && frameLetter <= 'E') def.idleFrames.push_back(sf);
                    else if (frameLetter == 'H') def.painFrames.push_back(sf);
                    else if (frameLetter >= 'I' && frameLetter <= 'O') def.deathFrames.push_back(sf);
                }
'''
code = re.sub(r'if \(frameLetter >= \'A\' && frameLetter <= \'G\'\) def\.idleFrames\.push_back\(sf\);.*?else if \(frameLetter >= \'I\' && frameLetter <= \'M\'\) def\.deathFrames\.push_back\(sf\);', fix_load_frames, code, flags=re.DOTALL)

with open('src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
