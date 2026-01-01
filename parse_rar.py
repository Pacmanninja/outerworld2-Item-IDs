#!/usr/bin/env python3
import json
import os
import re

# Parse extracted/ TXT files → JS array
categories = {}
for root, dirs, files in os.walk('extracted/'):
    for file in files:
        if file.endswith('.txt'):
            cat = file.replace('.txt', '').replace('_', ' ').title()
            filepath = os.path.join(root, file)
            print(f"Parsing {filepath}")
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = []
                    for line in f:
                        line = line.strip()
                        if line and 'ArkansasContentBlueprints' in line:
                            # Extract ID + Name
                            match = re.search(r'BlueprintGeneratedClass\s*\(\s*\'([^\']+)\'\s*,\s*\'([^\']+)\'\s*\)', line)
                            if match:
                                id_, name = match.groups()
                                lines.append({"id": id_, "name": name})
                    categories[cat] = lines
                    print(f"{cat}: {len(lines)} items")
            except Exception as e:
                print(f"Error parsing {file}: {e}")

# Output JS
js = "const items = " + json.dumps(categories, indent=2) + ";"
with open('itemsgenerated.js', 'w') as f:
    f.write(js)
print("✅ Generated itemsgenerated.js")
