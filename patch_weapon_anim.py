import re

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'r', encoding='utf-8') as f:
    code = f.read()

# Změna z for (char c = 'A'; c <= 'Z'; c++) na for (char c = 'A'; c <= 'E'; c++)
code = code.replace("for (char c = 'A'; c <= 'Z'; c++) {", "for (char c = 'A'; c <= 'E'; c++) {")

with open('E:/Michael/skola/cpp/projektFinal/src/engine.cpp', 'w', encoding='utf-8') as f:
    f.write(code)
