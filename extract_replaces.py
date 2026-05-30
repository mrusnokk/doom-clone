import json
import sys

with open(r'C:\Users\micha\.gemini\antigravity\brain\20c17694-b83f-4a90-92a0-446ec4416a12\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    if call['name'] == 'replace_file_content':
                        args = call['args']
                        if 'Sprite.hpp' in args.get('TargetFile', ''):
                            print("Sprite.hpp modified:")
                            print(args.get('ReplacementContent'))
                        if 'engine.cpp' in args.get('TargetFile', ''):
                            print("engine.cpp modified:")
                            print(args.get('ReplacementContent'))
        except:
            pass
