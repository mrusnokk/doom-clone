import json
import sys

transcript_path = r'C:\Users\micha\.gemini\antigravity\brain\20c17694-b83f-4a90-92a0-446ec4416a12\.system_generated\logs\transcript.jsonl'

# files we want to reconstruct
files = {
    'E:/Michael/skola/cpp/projektFinal/src/engine.cpp': '',
    'E:/Michael/skola/cpp/projektFinal/include/Engine.hpp': '',
    'E:/Michael/skola/cpp/projektFinal/include/Sprite.hpp': ''
}

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line)
                if 'tool_calls' in entry:
                    for call in entry['tool_calls']:
                        if call['name'] == 'write_to_file' or call['name'] == 'replace_file_content':
                            pass # We don't have the full file from replace, only diffs. 
            except:
                pass
except Exception as e:
    print(e)
