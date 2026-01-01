#!/usr/bin/env python3
import json
import os
import re
import zipfile  # Fallback
from rarfile import RarFile  # pip install rarfile unrar

# RAR from Releases or root (Actions downloads)
rar_path = 'OuterWorld2ItemIDs.rar'
password = 'RAR_PASSWORD'

def extract_rar():
    if not os.path.exists(rar_path):
        # Download from latest release
        import requests
        resp = requests.get(f'https://api.github.com/repos/{os.getenv("GITHUB_REPOSITORY")}/releases/latest')
        assets = resp.json()['assets']
        rar_url = next(a['browser_download_url'] for a in assets if 'rar' in a['name'].lower())
        with open(rar_path, 'wb') as f:
            f.write(requests.get(rar_url).content)
    
    with RarFile(rar_path) as rf:
        rf.setpassword(password)
        rf.extractall('extracted/')

categories = {}
for root, dirs, files in os.walk('extracted/'):
    for file in files:
        if file.endswith('.txt'):
            cat = file.replace('.txt', '').replace('_', ' ').title()
            with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip() and 'ArkansasContentBlueprints' in line]
            categories[cat] = lines

# Output JS
js = "const items = " + json.dumps(categories, indent=4) + ";"
with open('items_generated.js', 'w') as f:
    f.write(js)

print("Extracted & parsed RAR → items_generated.js")
