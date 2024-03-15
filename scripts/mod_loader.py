"""Automatically loads all mods from ./mods/*, creates folder if it doesn't exist"""

import glob
import os
import ujson
from scripts.file_loader import _FileHandler as FileHandler

if not os.path.exists("mods"):
    os.makedirs("mods")

mod_count = 0
mods = []
for mod in glob.glob("mods/*"):
    if not os.path.exists(f"{mod}/mod.json"): continue
    mod_data: dict = ujson.load(open(f"{mod}/mod.json"))
    if not all([mod_data.get(key) for key in ["name", "version", "description", "author"]]):
        raise ValueError(f"Mod {mod} is missing adequate data in mod.json. Required fields: name, author, description, version")

    mods.append(mod_data)
    mod_count += 1

    merge = mod_data.get("merge", False) # in a perfect world, this would be called "merge?"
    # grab every single file in the mod folder, and change the binding of the old file to the modded version
    files = []
    for folder in ["sprites", "resources"]:
        files.extend(glob.glob(f"{mod}/{folder}/**/*", recursive=True))
    for file in files:
        if file.endswith("mod.json"): continue
        if os.path.isdir(file): continue

        orig_file = file.replace(mod, "").lstrip("\\").lstrip("/")
        is_merged = merge and orig_file.replace("\\", "/") in mod_data.get("merge", [])
        FileHandler.change_binding(orig_file, file, is_merged)