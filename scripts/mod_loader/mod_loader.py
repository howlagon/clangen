import builtins
import glob
import ujson
import os

from .mod import Mod, mod_from_config

mods: dict[str, Mod] = {}
modified_files: dict[str, list[str]] = {}

old_import = builtins.__import__

def handle_mod_import(name, *args, **kwargs):
    # handles importing a script from a mod
    # if the import is coming from the base script, import the mod with highest priority
    # otherwise, import the mod with the next highest priority after the mod that the import is coming from
    # dont ask how i got to this idea or got the code to work. its kinda black magic to me
    if name not in modified_files:
        return old_import(name, *args, **kwargs)
    if mods[modified_files[name][-1]].mod_key in args[0]["__name__"]:
        return old_import(name, *args, **kwargs)
    
    mods_sorted = sorted([mods[mod] for mod in modified_files[name] if mods[mod].enabled], key=lambda mod: mod.priority, reverse=True)
    for mod in mods_sorted:
        if mod.mod_key in args[0]["__name__"]:
            name = mods_sorted[mods_sorted.index(mod) + 1].modified_scripts[name]
            break
    return old_import(name, *args, **kwargs)

def new_import(name, *args, **kwargs):
    if len(args) == 0:
        return old_import(name, *args, **kwargs)
    if 'mods.' in args[0]['__name__']:
        return handle_mod_import(name, *args, **kwargs)
    if (name not in modified_files) or (not mods[modified_files[name][0]].enabled):
        return old_import(name, *args, **kwargs)

    print(f"Importing {name} from {modified_files[name][0]}")
    return old_import(mods[modified_files[name][0]].modified_scripts[name], *args, **kwargs)

builtins.__import__ = new_import

if not os.path.exists('mods'):
    os.makedirs('mods')

def load_mods():
    for mod_path in glob.glob('mods/*'):
        if not os.path.isdir(mod_path):
            continue
        if not os.path.exists(f"{mod_path}/config.json"):
            print(f"Mod {mod_path} is missing a config.json file!")
            continue
        with open(f"{mod_path}/config.json", 'r') as fp:
            config = ujson.load(fp)
            required_params = ['name', 'version', 'author']
            missing_params = [param for param in required_params if param not in config]
            if missing_params:
                print(f"Mod {mod_path} is missing the following parameter(s) in config.json: {missing_params}")
                continue
        
        mod_class = mod_from_config(config)
        mods[config['name']] = mod_class

        mod_key = mod_path.replace('/', '.').replace('\\', '.') # e.g. mods.howl_test_mod
        for file in glob.glob(f"{mod_path}/scripts/**/*.py", recursive=True):
            file = mod_class.add_modified_script(mod_key, file)
            file_key = file.replace(f'{mod_key}.', '') # e.g. scripts.screens.StartScreen

        if modified_files.get(file_key) is not None:
            for index, mod_name in enumerate(modified_files[file_key]):
                if mods[mod_name].priority < mod_class.priority:
                    modified_files[file_key].insert(index, mod_class.name)
                    break
            else:
                modified_files[file_key].append(mod_class.name)
        else:
            modified_files[file_key] = [mod_class.name]
        
        mod_class.mod_key = mod_key


load_mods()
print('Loaded mods:', ''.join([f"\n  - {mod.name} v{mod.version} by {mod.author}" for mod in mods.values()]))