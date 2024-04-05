"""Automatically creates mod folder (if it doesn't exist) and then loads all mods from ./mods/*.zip"""

import glob
import os
import ujson
import zipfile
from scripts.file_loader import _FileHandler as FileHandler

if not os.path.exists("mods"):
    os.makedirs("mods")

mod_count = 0
mods: dict = {}
enabled_mods = []

def load_all_mods():
    global mods, mod_count, enabled_mods
    for mod in glob.glob("mods/*.zip"):
        mod = mod.replace("\\", "/") # path replacement for windows
        path = mod.strip("mods/").rstrip('.zip')

        zip = zipfile.ZipFile(mod)
        if not path + "/mod.json" in zip.namelist():
            raise FileNotFoundError(f"Mod {mod} is missing mod.json")

        zip_data = {name: zip.read(name) for name in zip.namelist() if not name.endswith("/") and not name.endswith("mod.json")}
        mod_data: dict = ujson.loads(zip.read(path + "/mod.json"))
        if not all([mod_data.get(key) for key in ["name", "version", "description", "author"]]):
            raise ValueError(f"Mod {mod} is missing adequate data in mod.json. Required fields: name, author, description, version")

        mods[mod_data["name"]] = {
            "version": mod_data["version"],
            "description": mod_data["description"],
            "author": mod_data["author"],
            "merge": mod_data.get("merge", []),
            "changed_files": {}
        }
        mod_count += 1
        enabled_mods.append(mod_data["name"])

        for file in zip_data:
            if file.endswith("mod.json"): continue
            mods[mod_data["name"]]["changed_files"][file] = zip_data[file]

def load_bindings():
    FileHandler.clear_memory()
    # also clear the cache, just to be safe
    from scripts.game_structure.image_cache import clear_cache
    clear_cache()
    global mods
    for mod in mods:
        if not mod in enabled_mods: continue
        path = next(iter(mods[mod]["changed_files"].keys())).split("/")[0] # janky as hell but it works. i <3 bodged code
        for file in mods[mod]["changed_files"]:
            FileHandler.change_binding_in_memory(file.replace(f"{path}/", ""), mods[mod]["changed_files"][file], mod_name=mod, extend=file in mods[mod].get("merge", []))

def search_for_mod(mod: str) -> str:
    found = []
    for mod in mods:
        if mod.lower() in [m.lower() for m in mods.keys()]:
            found.append(mod)
    if len(found) == 1:
        return found[0]
    elif len(found) > 1:
        return False
    return None

def enable_mod(mod: str):
    """Enables a mod by name. Returns True if successful, False if the mod was not found, or None if multiple mods were found."""
    global enabled_mods
    mod = search_for_mod(mod)
    if mod is None:
        return None
    if not mod:
        return False
    if mod in enabled_mods:
        return "already enabled"
    enabled_mods.append(mod)
    return True

def disable_mod(mod: str):
    """Disables a mod by name. Returns True if successful, False if the mod was not found, or None if multiple mods were found. If the mod is already disabled, returns 3."""
    global enabled_mods
    mod = search_for_mod(mod)
    if mod is None:
        return None
    if not mod:
        return False
    if not mod in enabled_mods:
        return "already disabled"
    enabled_mods.remove(mod)
    return True

def main():
    load_all_mods()
    load_bindings()
    print(f"Loaded {mod_count} mod{'s' if mod_count != 1 else ''}.")

main()