#!/usr/bin/env python3
import json
import os
import re

categories = {}
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.txt'):
            cat = file.replace('.txt', '').replace(' ', '').title()
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f if line.strip() and len(line.strip()) > 5]
                categories[cat] = lines[:1000]  # Cap for perf; remove for full
                print(f"{cat}: {len(lines)} items")
            except Exception as e:
                print(f"Error parsing {file}: {e}")

js = "const items = " + json.dumps(categories, indent=2) + ";"
with open('itemsgenerated.js', 'w') as f:
    f.write(js)
print("Generated itemsgenerated.js")
