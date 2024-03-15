"""Automatically creates mod folder (if it doesn't exist) and then loads all mods from ./mods/*.zip"""

import glob
import os
import ujson
import zipfile
from scripts.file_loader import _FileHandler as FileHandler

if not os.path.exists("mods"):
    os.makedirs("mods")

mod_count = 0
mods = []
for mod in glob.glob("mods/*.zip"):
    mod = mod.replace("\\", "/")
    path = mod.strip("mods/").rstrip('.zip')
    zip = zipfile.ZipFile(mod)
    if not path + "/mod.json" in zip.namelist():
        raise FileNotFoundError(f"Mod {mod} is missing mod.json")
    zip_data = {name: zip.read(name) for name in zip.namelist() if not name.endswith("/") and not name.endswith("mod.json")}
    mod_data: dict = ujson.loads(zip.read(path + "/mod.json"))
    if not all([mod_data.get(key) for key in ["name", "version", "description", "author"]]):
        raise ValueError(f"Mod {mod} is missing adequate data in mod.json. Required fields: name, author, description, version")

    mods.append(mod_data)
    mod_count += 1

    merge = mod_data.get("merge", False) # in a perfect world, this would be called "merge?"
    for file in zip_data:
        if file.endswith("mod.json"): continue
        is_merged = merge and file.replace(f"{path}/", "") in mod_data.get("merge", [])
        FileHandler.change_binding_in_memory(file.replace(f"{path}/", ""), zip_data[file], is_merged)