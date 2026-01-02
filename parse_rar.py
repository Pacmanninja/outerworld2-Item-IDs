#!/usr/bin/env python3
import json
import os
import re
from rarfile import RarFile
import requests  # For release download if needed

rarpath = "OuterWorld2ItemIDs.rar"
password = os.getenv('RAR_PASSWORD')
if not password:
    raise ValueError("RAR_PASSWORD env var missing!")

extracted = "extracted"
os.makedirs(extracted, exist_ok=True)

# Download from latest release if not in repo
if not os.path.exists(rarpath):
    repo = os.getenv('GITHUB_REPOSITORY', 'Pacmanninja/outerworld2-Item-IDs')
    headers = {'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'}
    r = requests.get(f'https://api.github.com/repos/{repo}/releases/latest', headers=headers)
    assets = r.json()['assets']
    rar_url = next(a['browser_download_url'] for a in assets if 'rar' in a['name'].lower())
    with open(rarpath, 'wb') as f:
        f.write(requests.get(rar_url, headers=headers).content)
    print(f"Downloaded {rarpath}")

with RarFile(rarpath) as rf:
    rf.setpassword(password)
    rf.extractall(extracted)

categories = {}
for root, dirs, files in os.walk(extracted):
    for file in files:
        if file.endswith('.txt'):
            cat = re.sub(r'[_-]', ' ', file.replace('.txt', '')).title()
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            items = []
            for line in lines:
                # Real prefix from files
                match = re.search(r'ArkansasContentBlueprints(.+)', line)
                if match:
                    id_ = match.group(1).strip()
                    if len(id_) > 5 and not id_.startswith('/'):  # Valid ID
                        items.append(id_)
            categories[cat] = items[:5000]  # Cap perf, remove for full ~250k
            print(f"{cat}: {len(items)} items")

js = f'const items = {json.dumps(categories, indent=2)};'
with open('itemsgenerated.js', 'w') as f:
    f.write(js)
print("Generated itemsgenerated.js")
