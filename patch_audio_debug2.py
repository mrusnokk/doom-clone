import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# fix the newline in strings
code = re.sub(r'failed: %s\n",', r'failed: %s\\n",', code)
code = re.sub(r'success\n"\)', r'success\\n")', code)
code = re.sub(r'success: %u\n",', r'success: %u\\n",', code)

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
